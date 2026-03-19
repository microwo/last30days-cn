"""Xiaohongshu (小红书) search placeholder for last30days-cn.

小红书搜索需要第三方 API（如快代理小红书 API）或自行实现爬虫。

当前状态：框架已实现，等待 API 集成

数据映射：
- liked_count → 点赞数
- collected_count → 收藏数
- comment_count → 评论数
"""

import sys
from typing import Any, Dict, List, Optional

# Depth configurations: how many items to search
DEPTH_CONFIG = {
    "quick": 5,
    "default": 10,
    "deep": 20,
}

# Max words to keep from content
CONTENT_MAX_WORDS = 300


def _log(msg: str):
    """Log to stderr."""
    sys.stderr.write(f"[Xiaohongshu] {msg}\n")
    sys.stderr.flush()


def is_available() -> bool:
    """Check if Xiaohongshu search is available (requires API key)."""
    # TODO: Check if API key is configured
    return False


def _compute_relevance(query: str, title: str) -> float:
    """Compute relevance based on query and title match."""
    query_tokens = set(query.lower().split())
    title_tokens = set(title.lower().split())

    if not query_tokens:
        return 0.5

    overlap = len(query_tokens & title_tokens)
    ratio = overlap / len(query_tokens)
    return max(0.1, min(1.0, ratio))


async def search_xiaohongshu_async(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
) -> Dict[str, Any]:
    """Search Xiaohongshu via API (placeholder).

    Args:
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: 'quick', 'default', or 'deep'

    Returns:
        Dict with 'items' list of note metadata dicts.
    """
    _log(f"Xiaohongshu search requires API key (not yet implemented)")
    _log(f"Topic: '{topic}', Date range: {from_date} to {to_date}")

    # TODO: Implement actual API call when API key is available
    # Example implementation:
    # 1. Use 快代理小红书 API: https://www.kuaidaili.com/
    # 2. Or use custom crawler with authentication

    return {
        "items": [],
        "error": "Xiaohongshu search requires API key (not yet implemented)"
    }


def search_and_transcribe(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
) -> Dict[str, Any]:
    """Full Xiaohongshu search (synchronous wrapper).

    Args:
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: 'quick', 'default', or 'deep'

    Returns:
        Dict with 'items' list.
    """
    import asyncio
    try:
        result = asyncio.run(search_xiaohongshu_async(topic, from_date, to_date, depth))
        return result
    except RuntimeError:
        import nest_asyncio
        nest_asyncio.apply()
        result = asyncio.run(search_xiaohongshu_async(topic, from_date, to_date, depth))
        return result


def parse_xiaohongshu_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse Xiaohongshu search response to normalized format.

    Returns:
        List of item dicts ready for normalization.
    """
    return response.get("items", [])
