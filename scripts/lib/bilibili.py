"""Bilibili search and transcript extraction via bilibili-api-python for last30days-cn.

Uses bilibili-api-python (https://github.com/Nemo2011/bilibili-api) for Bilibili search.
No API keys needed for basic search.

Bilibili data mapping:
- play → 播放量
- like → 点赞
- review → 评论数
- description → 视频描述
- pubdate → 发布时间
"""

import asyncio
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Set

try:
    from bilibili_api import search, video
except ImportError:
    search = None
    video = None

# Depth configurations: how many videos to search
DEPTH_CONFIG = {
    "quick": 10,
    "default": 20,
    "deep": 40,
}

# Max words to keep from description (as "transcript" replacement)
TRANSCRIPT_MAX_WORDS = 500

# Stopwords for relevance computation (common Chinese/English words)
STOPWORDS = frozenset({
    # Chinese stopwords
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
    '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
    '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '吗',
    '什么', '这个', '那个', '怎么', '为什么', '可以', '能', '让', '给',
    '这些', '那些', '它们', '你们', '我们', '他们', '大家', '只是',
    '还是', '或者', '虽然', '但是', '因为', '所以', '如果', '然后',
    # English stopwords
    'the', 'a', 'an', 'to', 'for', 'how', 'is', 'in', 'of', 'on',
    'and', 'with', 'from', 'by', 'at', 'this', 'that', 'it', 'my',
    'your', 'i', 'me', 'we', 'you', 'what', 'are', 'do', 'can',
    'its', 'be', 'or', 'not', 'no', 'so', 'if', 'but', 'about',
    'all', 'just', 'get', 'has', 'have', 'was', 'will',
})


# Synonym groups for relevance scoring (Chinese + English)
SYNONYMS = {
    # English tech terms
    'ai': {'人工智能', 'artificial', 'intelligence'},
    '人工智能': {'ai', 'artificial', 'intelligence'},
    'ml': {'机器学习', 'machine', 'learning'},
    '机器学习': {'ml', 'machine', 'learning'},
    'python': {'Python', 'py'},
    'java': {'Java'},
    'js': {'javascript', 'js'},
    'javascript': {'js'},
    'react': {'reactjs', 'React'},
    'vue': {'vuejs', 'Vue'},
    'typescript': {'ts', 'TypeScript'},
    'ts': {'typescript', 'TypeScript'},
    # Chinese tech terms
    '前端': {'frontend', 'web'},
    '后端': {'backend', 'server'},
    '数据库': {'database', 'db'},
    '算法': {'algorithm'},
    '编程': {'programming', 'coding'},
    '开发': {'development', 'dev'},
    '教程': {'tutorial', 'guide'},
    '实战': {'practice', 'hands-on'},
    '入门': {'beginner', 'introduction'},
    '进阶': {'advanced', 'intermediate'},
    # Other
    'b站': {'bilibili'},
    'bilibili': {'b站'},
}


def _tokenize(text: str) -> Set[str]:
    """Tokenize text, remove stopwords, expand with synonyms."""
    # Remove punctuation and lowercase
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = text.split()

    # Remove stopwords and single chars
    tokens = {w for w in words if w not in STOPWORDS and len(w) > 1}

    # Expand synonyms
    expanded = set(tokens)
    for t in tokens:
        if t in SYNONYMS:
            expanded.update(SYNONYMS[t])

    return expanded


def _compute_relevance(query: str, title: str) -> float:
    """Compute relevance as ratio of query tokens found in title."""
    q_tokens = _tokenize(query)
    t_tokens = _tokenize(title)

    if not q_tokens:
        return 0.5  # Neutral fallback

    overlap = len(q_tokens & t_tokens)
    ratio = overlap / len(q_tokens)
    return max(0.1, min(1.0, ratio))


def _log(msg: str):
    """Log to stderr."""
    sys.stderr.write(f"[Bilibili] {msg}\n")
    sys.stderr.flush()


def is_available() -> bool:
    """Check if bilibili-api is available."""
    return search is not None and video is not None


def _extract_core_subject(topic: str) -> str:
    """Extract core subject from verbose query for Bilibili search."""
    text = topic.lower().strip()

    # Strip multi-word prefixes
    prefixes = [
        # English
        'what are the best', 'what is the best', 'what are the latest',
        'what are people saying about', 'what do people think about',
        'how do i use', 'how to use', 'how to',
        'what are', 'what is', 'tips for', 'best practices for',
        # Chinese
        '最好的', '什么是最好的', '最新的', '大家都在说',
        '大家怎么看', '如何使用', '怎么使用', '什么是',
        '有什么', '什么是', '关于', '关于的',
    ]
    for p in prefixes:
        if text.startswith(p + ' '):
            text = text[len(p):].strip()

    # Strip individual noise words
    noise = {
        # English
        'best', 'top', 'good', 'great', 'awesome', 'killer',
        'latest', 'new', 'news', 'update', 'updates',
        'trending', 'hottest', 'popular', 'viral',
        'practices', 'features',
        'recommendations', 'advice',
        'prompt', 'prompts', 'prompting',
        'methods', 'strategies', 'approaches',
        # Chinese
        '最好的', '最牛', '最强', '最新', '热门', '爆款',
        '推荐', '建议', '教程', '攻略', '指南',
        '技巧', '方法', '策略', '方案',
    }
    words = text.split()
    filtered = [w for w in words if w not in noise]

    result = ' '.join(filtered) if filtered else text
    return result.rstrip('?!。')


def _convert_timestamp(timestamp: int) -> str:
    """Convert Unix timestamp to YYYY-MM-DD format."""
    if not timestamp:
        return None
    try:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y-%m-%d")
    except (ValueError, OSError):
        return None


async def search_bilibili_async(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
) -> Dict[str, Any]:
    """Search Bilibili via bilibili-api-python.

    Args:
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: 'quick', 'default', or 'deep'

    Returns:
        Dict with 'items' list of video metadata dicts.
    """
    if not is_available():
        return {"items": [], "error": "bilibili-api-python not installed"}

    count = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["default"])
    core_topic = _extract_core_subject(topic)

    _log(f"Searching Bilibili for '{core_topic}' (count={count})")

    try:
        # Perform search
        result = await search.search(core_topic, page=1)

        # Extract video results
        result_data = result.get('result', [])
        video_result = next((item for item in result_data if item.get('result_type') == 'video'), None)

        if not video_result or 'data' not in video_result:
            _log("No video results found")
            return {"items": []}

        videos = video_result['data'][:count]

        # Parse video data
        items = []
        for vid in videos:
            bvid = vid.get('bvid', '')
            play_count = vid.get('play', 0)
            like_count = vid.get('like', 0)
            review_count = vid.get('review', 0) or vid.get('video_review', 0)
            pubdate = vid.get('pubdate', 0)

            date_str = _convert_timestamp(pubdate)

            # Use description as "transcript" placeholder
            description = vid.get('description', '')
            transcript_snippet = _truncate_description(description)

            items.append({
                "bvid": bvid,
                "title": vid.get('title', ''),
                "url": f"https://www.bilibili.com/video/{bvid}",
                "uploader_name": vid.get('author', ''),
                "date": date_str,
                "engagement": {
                    "views": play_count,
                    "likes": like_count,
                    "comments": review_count,
                },
                "duration": vid.get('duration', ''),
                "relevance": _compute_relevance(core_topic, vid.get('title', '')),
                "why_relevant": f"Bilibili: {vid.get('title', core_topic)[:60]}",
                "transcript_snippet": transcript_snippet,
            })

        # Soft date filter: prefer recent items but fall back to all if too few
        recent = [i for i in items if i["date"] and i["date"] >= from_date]
        if len(recent) >= 3:
            items = recent
            _log(f"Found {len(items)} videos within date range")
        else:
            _log(f"Found {len(items)} videos ({len(recent)} within date range, keeping all)")

        # Sort by views descending (handle None values)
        items.sort(key=lambda x: (x["engagement"]["views"] or 0), reverse=True)

        return {"items": items}

    except Exception as e:
        _log(f"Search error: {type(e).__name__}: {e}")
        return {"items": [], "error": f"{type(e).__name__}: {e}"}


def _truncate_description(desc: str) -> str:
    """Truncate description to max words."""
    if not desc:
        return ""
    words = desc.split()
    if len(words) > TRANSCRIPT_MAX_WORDS:
        return ' '.join(words[:TRANSCRIPT_MAX_WORDS]) + '...'
    return desc


def search_and_transcribe(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
) -> Dict[str, Any]:
    """Full Bilibili search (synchronous wrapper).

    Args:
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: 'quick', 'default', or 'deep'

    Returns:
        Dict with 'items' list. Each item has a 'transcript_snippet' field (description).
    """
    # Run async function in event loop
    try:
        result = asyncio.run(search_bilibili_async(topic, from_date, to_date, depth))
        return result
    except RuntimeError:
        # If event loop is already running
        import nest_asyncio
        nest_asyncio.apply()
        result = asyncio.run(search_bilibili_async(topic, from_date, to_date, depth))
        return result


def parse_bilibili_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse Bilibili search response to normalized format.

    Returns:
        List of item dicts ready for normalization.
    """
    return response.get("items", [])
