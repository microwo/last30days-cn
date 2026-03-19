"""Zhihu search module for last30days-cn.

支持多种后端：快代理API、官方API、自定义爬虫。

数据映射：
- voteup_count → 赞同数
- comment_count → 评论数
- created → 创建时间
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
    sys.stderr.write(f"[Zhihu] {msg}\n")
    sys.stderr.flush()


def is_available() -> bool:
    """Check if Zhihu search is available (requires API key or backend)."""
    import os
    return bool(os.getenv("ZHIHU_API_KEY") or os.getenv("ZHIHU_BACKEND"))


def _compute_relevance(query: str, title: str) -> float:
    """Compute relevance based on query and title match."""
    query_tokens = set(query.lower().split())
    title_tokens = set(title.lower().split())

    if not query_tokens:
        return 0.5

    overlap = len(query_tokens & title_tokens)
    ratio = overlap / len(query_tokens)
    return max(0.1, min(1.0, ratio))


async def search_zhihu_async(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
) -> Dict[str, Any]:
    """Search Zhihu via configured backend.

    Args:
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: 'quick', 'default', or 'deep'

    Returns:
        Dict with 'items' list of Q&A metadata dicts.
    """
    import os

    backend = os.getenv("ZHIHU_BACKEND", "kuaidaili")

    _log(f"Using Zhihu backend: {backend}")

    if backend == "kuaidaili":
        # 使用快代理API
        try:
            from . import zhihu_kuaidaili
            return await zhihu_kuaidaili.search_zhihu_kuaidaili(
                topic, from_date, to_date, depth
            )
        except ImportError:
            return {
                "items": [],
                "error": "Kuaidaili backend requires zhihu_kuaidaili.py and requests library"
            }
    elif backend == "official":
        # 使用官方API（待实现）
        return {
            "items": [],
            "error": "Official Zhihu API not yet implemented (requires enterprise account)"
        }
    elif backend == "custom":
        # 使用自定义爬虫（待实现）
        return {
            "items": [],
            "error": "Custom crawler not yet implemented"
        }
    else:
        return {
            "items": [],
            "error": f"Unknown backend: {backend}. Supported: kuaidaili, official, custom"
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
        result = asyncio.run(search_zhihu_async(topic, from_date, to_date, depth))
        return result
    except RuntimeError:
        import nest_asyncio
        nest_asyncio.apply()
        result = asyncio.run(search_zhihu_async(topic, from_date, to_date, depth))
        return result


def parse_zhihu_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse Zhihu search response to normalized format.

    Returns:
        List of item dicts ready for normalization.
    """
    return response.get("items", [])
