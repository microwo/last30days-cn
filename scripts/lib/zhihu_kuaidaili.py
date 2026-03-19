"""Zhihu search using Kuaidaili API for last30days-cn.

使用快代理知乎 API 进行搜索。

数据映射：
- voteup_count → 赞同数
- comment_count → 评论数
- created → 创建时间
"""

import asyncio
import sys
import requests
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone, timedelta

# Depth configurations: how many items to search
DEPTH_CONFIG = {
    "quick": 5,
    "default": 10,
    "deep": 20,
}

# Max words to keep from content
CONTENT_MAX_WORDS = 300

# API Configuration
API_BASE_URL = "https://api.kuaidaili.com"


def _log(msg: str):
    """Log to stderr."""
    sys.stderr.write(f"[Zhihu] {msg}\n")
    sys.stderr.flush()


def is_available() -> bool:
    """Check if Zhihu search is available (requires API key)."""
    import os
    return bool(os.getenv("ZHIHU_API_KEY"))


def _compute_relevance(query: str, title: str) -> float:
    """Compute relevance based on query and title match."""
    query_tokens = set(query.lower().split())
    title_tokens = set(title.lower().split())

    if not query_tokens:
        return 0.5

    overlap = len(query_tokens & title_tokens)
    ratio = overlap / len(query_tokens)
    return max(0.1, min(1.0, ratio))


def _get_api_key() -> Optional[str]:
    """Get API key from environment."""
    import os
    return os.getenv("ZHIHU_API_KEY")


async def search_zhihu_kuaidaili(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
) -> Dict[str, Any]:
    """Search Zhihu via Kuaidaili API.

    Args:
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: 'quick', 'default', or 'deep'

    Returns:
        Dict with 'items' list of Q&A metadata dicts.
    """
    api_key = _get_api_key()

    if not api_key:
        return {
            "items": [],
            "error": "ZHIHU_API_KEY environment variable not set. Get API key from https://www.kuaidaili.com/"
        }

    count = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["default"])

    _log(f"Searching Zhihu for '{topic}' (count={count}, API=Kuaidaili)")

    try:
        # 调用快代理知乎搜索 API
        # API 文档：https://www.kuaidaili.com/doc
        url = f"{API_BASE_URL}/zhihu/search"
        params = {
            "q": topic,
            "count": count,
            "sort": "time_desc",  # 按时间倒序
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # 同步请求（使用requests）
        response = requests.get(url, params=params, headers=headers, timeout=30)

        if response.status_code != 200:
            return {
                "items": [],
                "error": f"API error: HTTP {response.status_code} - {response.text[:100]}"
            }

        data = response.json()

        # 解析响应（假设返回格式）
        # 实际格式需要根据 API 文档调整
        items = []
        if "data" in data:
            for item in data["data"]:
                # 提取问题信息
                items.append({
                    "question_id": item.get("id", ""),
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "author_name": item.get("author", {}).get("name", ""),
                    "date": item.get("created", "")[:10],  # YYYY-MM-DD
                    "engagement": {
                        "views": item.get("view_count", 0),
                        "upvotes": item.get("voteup_count", 0),
                        "comments": item.get("comment_count", 0),
                    },
                    "relevance": _compute_relevance(topic, item.get("title", "")),
                    "why_relevant": f"Zhihu: {item.get('title', topic)[:60]}",
                    "content_snippet": item.get("excerpt", "")[:CONTENT_MAX_WORDS],
                })

        # 日期过滤
        from_date_dt = datetime.strptime(from_date, "%Y-%m-%d")
        recent = [i for i in items if i["date"] >= from_date]

        if len(recent) >= 3:
            items = recent
            _log(f"Found {len(items)} items within date range")
        else:
            _log(f"Found {len(items)} items ({len(recent)} within date range, keeping all)")

        # 按赞同数排序
        items.sort(key=lambda x: x["engagement"]["upvotes"], reverse=True)

        return {"items": items}

    except requests.exceptions.Timeout:
        return {
            "items": [],
            "error": "API request timed out (30s)"
        }
    except Exception as e:
        return {
            "items": [],
            "error": f"{type(e).__name__}: {e}"
        }


def search_and_transcribe(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
) -> Dict[str, Any]:
    """Full Zhihu search (synchronous wrapper).

    Args:
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: 'quick', 'default', or 'deep'

    Returns:
        Dict with 'items' list.
    """
    try:
        result = asyncio.run(search_zhihu_kuaidaili(topic, from_date, to_date, depth))
        return result
    except RuntimeError:
        import nest_asyncio
        nest_asyncio.apply()
        result = asyncio.run(search_zhihu_kuaidaili(topic, from_date, to_date, depth))
        return result


def parse_zhihu_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse Zhihu search response to normalized format.

    Returns:
        List of item dicts ready for normalization.
    """
    return response.get("items", [])
