#!/usr/bin/env python3
"""Test script for Zhihu and Xiaohongshu search modules."""

import sys
from pathlib import Path

# Add lib to path
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR / "scripts"))

from lib import zhihu, xiaohongshu
from datetime import datetime, timezone, timedelta

# Test parameters
TOPIC = "人工智能"
DEPTH = "quick"  # quick | default | deep

# Date range: last 30 days
to_date = datetime.now(timezone.utc)
from_date = to_date - timedelta(days=30)
from_date_str = from_date.strftime("%Y-%m-%d")
to_date_str = to_date.strftime("%Y-%m-%d")

print(f"Testing Zhihu and Xiaohongshu search for '{TOPIC}'...")
print(f"Date range: {from_date_str} to {to_date_str}")
print(f"Depth: {DEPTH}")
print("=" * 60)

# Test Zhihu
print("\n【Zhihu 测试】")
zhihu_result = zhihu.search_and_transcribe(
    TOPIC,
    from_date_str,
    to_date_str,
    depth=DEPTH,
)

zhihu_items = zhihu.parse_zhihu_response(zhihu_result)
print(f"Zhihu: {len(zhihu_items)} items")

if zhihu_result.get("error"):
    print(f"Error: {zhihu_result['error']}")

# Test Xiaohongshu
print("\n【Xiaohongshu 测试】")
xhs_result = xiaohongshu.search_and_transcribe(
    TOPIC,
    from_date_str,
    to_date_str,
    depth=DEPTH,
)

xhs_items = xiaohongshu.parse_xiaohongshu_response(xhs_result)
print(f"Xiaohongshu: {len(xhs_items)} items")

if xhs_result.get("error"):
    print(f"Error: {xhs_result['error']}")

print("\n" + "=" * 60)
print("注意：知乎和小红书搜索需要 API 密钥，当前为占位符实现")
print("要使用这些平台，需要配置相应的 API 服务（如快代理）")
