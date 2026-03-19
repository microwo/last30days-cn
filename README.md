# last30days-cn - 国内社交平台舆情调研工具

> 🇨🇳 研究过去30天内国内主流社交平台（B站、知乎、微博、小红书、抖音）上的任意话题

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## 简介

last30days-cn 是一个国内社交平台舆情调研工具，基于 [last30days](https://github.com/mvanhorn/last30days-skill) 改造，专门针对国内网络环境优化。

**当前支持：**
- ✅ B站 - 视频搜索、播放量、点赞、评论（已实现）
- 🚧 知乎 - 框架已实现，需要 API 密钥
- 🚧 小红书 - 框架已实现，需要 API 密钥
- 🚧 微博 - 开发中
- 🚧 抖音 - 开发中

## 功能特点

- 🔍 **多平台搜索**：一次搜索，覆盖多个国内社交平台
- 📊 **互动数据**：播放量、点赞、评论等关键指标
- 🎯 **相关度评分**：智能计算话题相关度
- 📝 **内容提取**：提取视频描述作为内容摘要
- ⚡ **并发执行**：多平台并行搜索，快速获取结果
- 💰 **免费使用**：B站搜索完全免费，无需 API 密钥

## 安装

### 前置要求

- Python 3.11 或更高版本
- pip 包管理器

### 安装依赖

```bash
# 安装 bilibili-api-python
pip3 install bilibili-api-python

# 或者从本项目安装
pip3 install -r requirements.txt
```

### 验证安装

```bash
# 测试 B站搜索
python3 test_bilibili.py
```

## 使用方法

### 基础用法

```bash
# 搜索 B站 上的"人工智能"相关内容
python3 scripts/last30days.py 人工智能

# 深度搜索（更多结果）
python3 scripts/last30days.py 人工智能 --deep

# 快速搜索（较少结果）
python3 scripts/last30days.py 人工智能 --quick
```

### 高级用法

```bash
# 指定搜索天数
python3 scripts/last30days.py 编程 --days=7

# 输出为 Markdown 格式
python3 scripts/last30days.py 人工智能 --emit=md

# 输出为 JSON 格式
python3 scripts/last30days.py 人工智能 --emit=json

# 调试模式
python3 scripts/last30days.py 人工智能 --debug
```

### 命令行选项

```
位置参数:
  topic                  搜索话题

选项:
  --emit=MODE            输出模式: compact|json|md (默认: compact)
  --sources=MODE         数据源选择: bilibili|web|all (默认: bilibili)
  --days=N               搜索天数，默认 30 天
  --quick                快速模式（较少结果，约10个视频）
  --deep                 深度模式（更多结果，约40个视频）
  --debug                启用调试日志
```

## 输出示例

### compact 模式（默认）

```
✅ All agents reported back!
├─ 🔵 Bilibili: 10 videos │ 5,716,140 views │ 3,278 likes
└─ 🌐 Web: 5 pages — 知乎, CSDN, 博客园

🏆 Most mentioned:

【AI零基础入门】2026年最全人工智能课程 - 3x mentions
UP主: 机器学习教程
播放: 1,265,436 | 点赞: 64,313 | 评论: 8,209
```

### json 模式

```json
{
  "bilibili": [
    {
      "bvid": "BV1QK41zFETe",
      "title": "【AI零基础入门】2026年最全人工智能课程",
      "url": "https://www.bilibili.com/video/BV1QK41zFETe",
      "uploader_name": "机器学习教程",
      "engagement": {
        "views": 1265436,
        "likes": 64313,
        "comments": 8209
      },
      "relevance": 1.0,
      "transcript_snippet": "本课程为人工智能零基础入门课程..."
    }
  ]
}
```

## 数据模型

### B站视频数据

```json
{
  "bvid": "BV1QK41zFETe",
  "title": "视频标题",
  "url": "https://www.bilibili.com/video/BV1QK41zFETe",
  "uploader_name": "UP主名称",
  "date": "2025-10-13",
  "engagement": {
    "views": 1265436,
    "likes": 64313,
    "comments": 8209
  },
  "duration": "3259:28",
  "relevance": 1.0,
  "transcript_snippet": "视频描述内容..."
}
```

## 架构设计

```
last30days-cn/
├── scripts/
│   ├── last30days.py          # 主脚本
│   └── lib/
│       ├── bilibili.py         # B站搜索模块 ✅
│       ├── zhihu.py           # 知乎搜索模块 🚧（框架）
│       ├── weibo.py           # 微博搜索模块 🚧
│       ├── xiaohongshu.py     # 小红书搜索模块 🚧（框架）
│       ├── douyin.py          # 抖音搜索模块 🚧
│       ├── models.py          # 数据模型
│       ├── schema.py          # 数据结构
│       ├── render.py          # 渲染输出
│       ├── score.py           # 评分算法
│       ├── dedupe.py          # 去重模块
│       ├── normalize.py       # 数据标准化
│       └── dates.py          # 日期处理
├── test_bilibili.py          # B站测试脚本
├── test_zhihu_xhs.py       # 知乎/小红书测试脚本
├── SKILL.md                   # OpenClaw 技能描述
└── README.md                  # 本文件
```

## 技术栈

- **Python**: 3.11+
- **B站数据源**: [bilibili-api-python](https://github.com/Nemo2011/bilibili-api)
- **并发执行**: ThreadPoolExecutor
- **数据解析**: asyncio

## 开发计划

### 已完成 ✅
- [x] B站搜索模块（已实现并测试）
- [x] 数据标准化
- [x] 相关度评分算法
- [x] 基础架构设计
- [x] 知乎搜索框架
- [x] 小红书搜索框架

### 进行中 🚧
- [ ] 知乎搜索 API 集成
- [ ] 小红书搜索 API 集成
- [ ] 微博搜索模块

### 待开发 📋
- [ ] 抖音搜索模块
- [ ] 多平台并发优化
- [ ] 数据去重增强
- [ ] 渲染输出优化
- [ ] Web 界面

## 贡献指南

欢迎贡献！如果你想：

1. **实现新平台**：参考 `bilibili.py` 的结构，创建新的搜索模块
2. **优化现有功能**：提交 Issue 或 Pull Request
3. **报告 Bug**：在 GitHub 上提交 Issue

### 开发新平台

1. 在 `scripts/lib/` 下创建新文件（如 `zhihu.py`）
2. 实现搜索函数：
   ```python
   async def search_platform_async(topic, from_date, to_date, depth):
       # 实现搜索逻辑
       pass
   
   def search_and_transcribe(topic, from_date, to_date, depth):
       # 同步包装器
       pass
   
   def parse_platform_response(response):
       # 解析结果
       pass
   ```
3. 在 `last30days.py` 中添加 import 和并发调用
4. 更新 `SKILL.md` 和 `README.md`

## 常见问题

### Q: 为什么有些平台需要 API 密钥？

A: B站搜索使用公开接口，完全免费。知乎、微博、小红书、抖音等平台需要使用第三方 API，因为官方 API 申请门槛较高或限制较多。

### Q: 如何获取 API 密钥？

A: 查看各平台的文档：
- 知乎：推荐使用快代理知乎 API
- 微博：推荐使用微博开放平台 API
- 小红书：推荐使用快代理小红书 API
- 抖音：推荐使用快代理抖音 API

### Q: 搜索结果不准确？

A: 尝试以下方法：
1. 使用更精确的关键词
2. 使用 `--deep` 模式获取更多结果
3. 检查相关度评分（`relevance` 字段）

### Q: 支持批量搜索吗？

A: 当前版本不支持批量搜索。你可以使用 shell 脚本循环调用：
```bash
for topic in "人工智能" "机器学习" "深度学习"; do
    python3 scripts/last30days.py "$topic" --emit=json > "$topic.json"
done
```

## 原项目

本项目基于 [last30days](https://github.com/mvanhorn/last30days-skill) 改造，原项目支持 Reddit、X、YouTube、TikTok、Instagram 等国外平台。

## 许可证

[MIT License](LICENSE)

## 作者

[microwo](https://github.com/microwo)

## 致谢

- [last30days](https://github.com/mvanhorn/last30days-skill) - 原项目
- [bilibili-api-python](https://github.com/Nemo2011/bilibili-api) - B站 API 封装
- 所有贡献者

---

⭐ 如果这个项目对你有帮助，请给个 Star！
