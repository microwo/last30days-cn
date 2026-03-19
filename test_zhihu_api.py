#!/usr/bin/env python3
"""Test script for Zhihu API integration.

使用说明：
1. 设置环境变量 ZHIHU_API_KEY
2. 运行此脚本测试 API 连接
"""

import sys
import os
from pathlib import Path

# Add lib to path
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR / "scripts"))

from lib import zhihu
from datetime import datetime, timezone, timedelta

# Test parameters
TOPIC = "人工智能"
DEPTH = "quick"  # quick | default | deep

# Date range: last 30 days
to_date = datetime.now(timezone.utc)
from_date = to_date - timedelta(days=30)
from_date_str = from_date.strftime("%Y-%m-%d")
to_date_str = to_date.strftime("%Y-%m-%d")

print("=" * 60)
print("知乎 API 集成测试")
print("=" * 60)

# 检查 API Key
api_key = os.getenv("ZHIHU_API_KEY")
if api_key:
    print(f"\n✅ API Key 已配置: {api_key[:20]}...（前20位）")
else:
    print("\n❌ API Key 未配置")
    print("\n设置方法：")
    print("  export ZHIHU_API_KEY='your_api_key_here'")
    print("\n或创建 .env 文件：")
    print("  ZHIHU_API_KEY=your_api_key_here")
    print("\n获取 API Key：")
    print("  访问 https://www.kuaidaili.com/")
    print("  注册账号并申请知乎 API")
    sys.exit(1)

print(f"\n测试参数：")
print(f"  话题: {TOPIC}")
print(f"  日期范围: {from_date_str} 到 {to_date_str}")
print(f"  深度: {DEPTH}")
print("\n" + "-" * 60)

# 执行搜索
print("\n正在搜索...\n")

result = zhihu.search_and_transcribe(
    TOPIC,
    from_date_str,
    to_date_str,
    depth=DEPTH,
)

# 显示结果
items = zhihu.parse_zhihu_response(result)

if result.get("error"):
    print(f"❌ 搜索失败: {result['error']}")
    sys.exit(1)

print(f"✅ 搜索成功，找到 {len(items)} 个结果\n")

for i, item in enumerate(items[:5], 1):
    print(f"{i}. {item['title']}")
    print(f"   URL: {item['url']}")
    print(f"   作者: {item['author_name']}")
    print(f"   日期: {item['date']}")
    print(f"   赞同: {item['engagement']['upvotes']} | 评论: {item['engagement']['comments']}")
    if item.get('content_snippet'):
        print(f"   摘要: {item['content_snippet'][:100]}...")
    print(f"   相关度: {item['relevance']:.2f}")
    print()

print("=" * 60)
print("✅ API 集成测试通过！")
print("=" * 60)
