#!/usr/bin/env python3
"""
测试知乎搜索功能

使用方法：
1. 设置环境变量 ZHIHU_API_KEY
2. 运行此脚本

示例：
export ZHIHU_API_KEY="your_api_key_here"
python3 test_zhihu_search.py
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Add lib to path
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR / "scripts"))

from lib import zhihu

# Test parameters
TOPIC = "人工智能"
DEPTH = "default"  # quick | default | deep

# Date range: last 30 days
to_date = datetime.now(timezone.utc)
from_date = to_date - timedelta(days=30)
from_date_str = from_date.strftime("%Y-%m-%d")
to_date_str = to_date.strftime("%Y-%m-%d")

print("=" * 70)
print("知乎搜索功能测试")
print("=" * 70)
print()

# 检查 API Key
api_key = os.getenv("ZHIHU_API_KEY")
if api_key:
    print(f"✅ API Key 已配置: {api_key[:20]}...")
else:
    print("❌ API Key 未配置！")
    print()
    print("请先获取 API Key：")
    print("1. 访问 https://www.kuaidaili.com/")
    print("2. 注册账号（需要手机号实名）")
    print("3. 申请知乎搜索 API")
    print("4. 获取 API Key")
    print()
    print("然后设置环境变量：")
    print("  export ZHIHU_API_KEY='your_api_key_here'")
    print()
    sys.exit(1)

print()
print(f"搜索话题: {TOPIC}")
print(f"时间范围: {from_date_str} 到 {to_date_str}")
print(f"搜索深度: {DEPTH}")
print()
print("-" * 70)
print()

# 执行搜索
print("正在搜索...")
print()

try:
    result = zhihu.search_and_transcribe(
        TOPIC,
        from_date_str,
        to_date_str,
        depth=DEPTH,
    )

    items = zhihu.parse_zhihu_response(result)

    if result.get("error"):
        print(f"❌ 搜索失败: {result['error']}")
        sys.exit(1)

    print(f"✅ 搜索成功！找到 {len(items)} 个结果")
    print()

    # 显示前 5 个结果
    print("搜索结果（前 5 个）：")
    print("-" * 70)

    for i, item in enumerate(items[:5], 1):
        print(f"\n{i}. {item.get('title', 'N/A')}")
        print(f"   URL: {item.get('url', 'N/A')}")
        print(f"   作者: {item.get('author_name', 'N/A')}")
        print(f"   日期: {item.get('date', 'N/A')}")
        
        engagement = item.get('engagement', {})
        print(f"   数据: 浏览{engagement.get('views', 0)} | 赞同{engagement.get('upvotes', 0)} | 评论{engagement.get('comments', 0)}")
        
        if item.get('content_snippet'):
            print(f"   内容: {item['content_snippet'][:100]}...")
        
        print(f"   相关度: {item.get('relevance', 0):.2f}")

    print()
    print("=" * 70)
    print(f"✅ 测试完成！")
    print(f"📊 总结果数: {len(items)}")
    print("=" * 70)

except Exception as e:
    print(f"❌ 执行出错: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
