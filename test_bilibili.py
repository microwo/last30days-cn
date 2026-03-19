#!/usr/bin/env python3
"""Test script for Bilibili search module."""

import sys
from pathlib import Path

# Add lib to path
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR / "scripts"))

from lib import bilibili
from datetime import datetime, timezone, timedelta

# Test parameters
TOPIC = "人工智能"
DEPTH = "quick"  # quick | default | deep

# Date range: last 30 days
to_date = datetime.now(timezone.utc)
from_date = to_date - timedelta(days=30)
from_date_str = from_date.strftime("%Y-%m-%d")
to_date_str = to_date.strftime("%Y-%m-%d")

print(f"Searching Bilibili for '{TOPIC}'...")
print(f"Date range: {from_date_str} to {to_date_str}")
print(f"Depth: {DEPTH}")
print("-" * 60)

# Search and transcribe
result = bilibili.search_and_transcribe(
    TOPIC,
    from_date_str,
    to_date_str,
    depth=DEPTH,
)

# Check for errors
if result.get("error"):
    print(f"Error: {result['error']}")
    sys.exit(1)

# Display results
items = result.get("items", [])
print(f"Found {len(items)} videos")
print("-" * 60)

for i, item in enumerate(items[:5], 1):
    print(f"\n{i}. {item['title']}")
    print(f"   URL: {item['url']}")
    print(f"   UP主: {item['uploader_name']}")
    print(f"   日期: {item['date']}")
    print(f"   播放: {item['engagement']['views']:,} | 点赞: {item['engagement']['likes']:,} | 评论: {item['engagement']['comments']:,}")
    if item.get('transcript_snippet'):
        print(f"   字幕: {item['transcript_snippet'][:100]}...")
    print(f"   相关度: {item['relevance']:.2f}")

print("\n" + "-" * 60)
print(f"Total videos: {len(items)}")
