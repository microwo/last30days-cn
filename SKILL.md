---
name: last30days-cn
version: "1.0.0"
description: "Research a topic from the last 30 days on Chinese social platforms (Bilibili, Zhihu, Weibo, Xiaohongshu, Douyin). Become an expert and write copy-paste-ready prompts. 国内社交平台舆情调研：B站、知乎、微博、小红书、抖音。"
argument-hint: 'last30 人工智能视频, last30 编程教程推荐, last30 热门话题'
allowed-tools: Bash, Read, Write, AskUserQuestion, WebSearch
homepage: https://github.com/microwo/last30days-cn
repository: https://github.com/microwo/last30days-cn
author: microwo
license: MIT
user-invocable: true
metadata:
  openclaw:
    emoji: "🇨🇳"
    requires:
      bins:
        - python3
      pip:
        - bilibili-api-python
    primaryEnv: null
    files:
      - "scripts/*"
    homepage: https://github.com/microwo/last30days-cn
    tags:
      - research
      - bilibili
      - zhihu
      - weibo
      - xiaohongshu
      - douyin
      - social-media
      - trends
      - chinese
---

# last30days-cn v1.0.0: 国内社交平台舆情调研

> **Permissions overview:** 读取公开的社交媒体数据。不使用任何 API 密钥（B站搜索完全免费）。

研究过去30天内任意话题，覆盖国内主流社交平台：B站、知乎、微博、小红书、抖音。了解大家真正在讨论、推荐、热议什么。

## 当前支持的平台

| 平台 | 状态 | 数据类型 | 需要密钥 |
|------|------|----------|----------|
| **B站** | ✅ 已支持 | 视频、UP主、播放量、点赞、评论、描述 | ❌ 免费 |
| **知乎** | 🚧 开发中 | 问答、回答、赞同数、评论 | 🔜 需要 API |
| **微博** | 🚧 开发中 | 帖子、转发、点赞、评论 | 🔜 需要 API |
| **小红书** | 🚧 开发中 | 笔记、点赞、收藏、评论 | 🔜 需要 API |
| **抖音** | 🚧 开发中 | 视频、播放、点赞、评论 | 🔜 需要 API |

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

### 命令行选项

```
positional arguments:
  topic                  搜索话题

options:
  --emit=MODE            输出模式: compact|json|md (默认: compact)
  --sources=MODE         数据源选择: bilibili|web|all (默认: bilibili)
  --days=N               搜索天数，默认 30 天
  --quick                快速模式（较少结果）
  --deep                 深度模式（更多结果）
  --debug                启用调试日志
```

## 数据模型

### B站视频数据结构

```json
{
  "bvid": "BV1QK41zFETe",
  "title": "【AI零基础入门】2026年最全人工智能课程",
  "url": "https://www.bilibili.com/video/BV1QK41zFETe",
  "uploader_name": "机器学习教程",
  "date": "2025-10-13",
  "engagement": {
    "views": 1265436,
    "likes": 64313,
    "comments": 8209
  },
  "duration": "3259:28",
  "relevance": 1.0,
  "transcript_snippet": "本课程为人工智能零基础入门课程..."
}
```

## 架构设计

```
主脚本: last30days.py
  ├── 平台搜索模块 (lib/*.py)
  │   ├── bilibili.py     → B站数据 (已实现)
  │   ├── zhihu.py        → 知乎数据 (开发中)
  │   ├── weibo.py        → 微博数据 (开发中)
  │   ├── xiaohongshu.py  → 小红书数据 (开发中)
  │   └── douyin.py       → 抖音数据 (开发中)
  ├── 共享模块
  │   ├── models.py       → 数据模型
  │   ├── schema.py       → 数据结构
  │   ├── render.py       → 渲染输出
  │   ├── score.py        → 评分排序
  │   ├── dedupe.py       → 去重
  │   ├── normalize.py    → 数据标准化
  │   └── dates.py       → 日期处理
  └── 并发执行: ThreadPoolExecutor
```

## 技术栈

- **Python**: 3.11+
- **B站数据源**: bilibili-api-python (https://github.com/Nemo2011/bilibili-api)
- **其他平台**: 计划使用第三方 API

## 开发计划

### 已完成
- ✅ B站搜索模块
- ✅ 数据标准化
- ✅ 相关度评分
- ✅ 基础架构

### 进行中
- 🚧 知乎搜索模块
- 🚧 微博搜索模块

### 待开发
- 📋 小红书搜索模块
- 📋 抖音搜索模块
- 📋 多平台并发优化
- 📋 数据去重增强
- 📋 渲染输出优化

## 贡献指南

欢迎贡献！如果你想：

1. **实现新平台**：参考 `bilibili.py` 的结构，创建新的搜索模块
2. **优化现有功能**：提交 Issue 或 Pull Request
3. **报告 Bug**：在 GitHub 上提交 Issue

## 原项目

本项目基于 [last30days](https://github.com/mvanhorn/last30days-skill) 改造，针对国内社交平台进行了适配。

原项目支持 Reddit、X、YouTube、TikTok、Instagram 等国外平台。

## 许可证

MIT License - 详见 LICENSE 文件
