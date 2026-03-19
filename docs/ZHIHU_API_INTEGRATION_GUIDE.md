# 知乎 API 集成完整指南

## 📋 你需要做什么

### 第一步：注册快代理账号

1. 访问：https://www.kuaidaili.com/
2. 点击「注册」按钮
3. 填写信息（需要手机号实名认证）
4. 验证手机号，完成注册
5. 登录进入控制台

### 第二步：申请知乎 API

1. 在控制台顶部导航栏选择「API 产品」
2. 找到「知乎 API」或「问答搜索 API」
3. 点击「申请」或「免费试用」
4. 完成申请后，在「我的API」页面获取 API Key
5. 复制 API Key（类似：`a1b2c3d4e5f6g7h8i9j0k1l2m`）

### 第三步：配置环境变量

#### 方法 1：在 Shell 中配置（临时）

```bash
export ZHIHU_API_KEY="your_api_key_here"
```

#### 方法 2：在 ~/.bashrc 或 ~/.zshrc 中配置（永久）

```bash
echo 'export ZHIHU_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

#### 方法 3：在 .env 文件中配置（推荐）

创建 `.env` 文件：

```bash
cd /root/.openclaw/workspace/skills/last30days-cn
echo 'ZHIHU_API_KEY=your_api_key_here' > .env
```

然后在代码中读取：

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ZHIHU_API_KEY")
```

### 第四步：测试 API 连接

```bash
# 设置 API Key
export ZHIHU_API_KEY="your_api_key_here"

# 运行测试
python3 test_zhihu_api.py
```

### 第五步：运行完整搜索

```bash
# 使用知乎搜索
python3 scripts/last30days.py 人工智能 --sources=zhihu
```

---

## 💰 费用说明

快代理知乎 API 按量计费：

- **免费额度**：新用户通常有免费额度（约 100-500 次调用）
- **单价**：每次搜索约 0.001-0.005 元
- **充值**：按需充值，最低 10 元

**示例**：
- 搜索 100 次：约 0.1-0.5 元
- 搜索 1000 次：约 1-5 元

---

## 🔧 代码修改指南

### 文件结构

```
scripts/lib/
├── zhihu.py              # 主入口（后端选择）
└── zhihu_kuaidaili.py  # 快代理API实现
```

### 主入口 (zhihu.py)

**功能**：
- 检测环境变量 `ZHIHU_BACKEND`（默认：kuaidaili）
- 根据后端选择调用对应的实现
- 统一的接口和返回格式

**支持的 后端**：
- `kuaidaili`：快代理API（推荐）
- `official`：官方API（待实现）
- `custom`：自定义爬虫（待实现）

### 快代理实现 (zhihu_kuaidaili.py)

**功能**：
- 调用快代理知乎搜索 API
- 解析 JSON 响应
- 计算相关度
- 日期过滤
- 数据标准化

**API 格式**（示例）：

```python
url = f"{API_BASE_URL}/zhihu/search"
params = {
    "q": topic,
    "count": count,
    "sort": "time_desc",
}
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}
```

---

## 📝 使用示例

### 基础搜索

```bash
export ZHIHU_API_KEY="your_api_key_here"
python3 scripts/last30days.py "人工智能" --sources=zhihu
```

### 深度搜索

```bash
export ZHIHU_API_KEY="your_api_key_here"
python3 scripts/last30days.py "人工智能" --sources=zhihu --deep
```

### 多平台搜索（B站 + 知乎）

```bash
export ZHIHU_API_KEY="your_api_key_here"
python3 scripts/last30days.py "人工智能" --sources=bilibili,zhihu
```

---

## ⚠️ 注意事项

### 1. API 密钥安全

**不要**：
- ❌ 把 API Key 提交到 Git 仓库
- ❌ 在公开的代码中硬编码
- ❌ 在不安全的渠道分享

**应该**：
- ✅ 使用环境变量
- ✅ 使用 `.env` 文件（已加入 .gitignore）
- ✅ 在服务器环境变量中配置

### 2. 速率限制

- ❌ 不要短时间内大量调用（会被限流）
- ✅ 适当设置 `--depth` 参数控制调用次数
- ✅ 添加缓存机制减少重复调用

### 3. 错误处理

- ✅ 检查 API 返回的错误码
- ✅ 处理超时情况
- ✅ 捕获异常并提供友好的错误信息

### 4. 数据质量

- ✅ 验证 API 返回的数据格式
- ✅ 处理缺失字段（如 author 可能为空）
- ✅ 过滤无效数据

---

## 🧪 测试清单

- [ ] API Key 已配置
- [ ] 可以连接到 API 服务器
- [ ] 搜索功能正常
- [ ] 日期过滤正确
- [ ] 相关度评分正常
- [ ] 错误处理完善
- [ ] 多平台并发正常

---

## 🆘 常见问题

### Q: API Key 在哪里配置？

A: 有三种方式：
1. 环境变量：`export ZHIHU_API_KEY="xxx"`
2. .env 文件：创建 `.env` 文件，写入 `ZHIHU_API_KEY=xxx`
3. 直接修改代码（不推荐）：在代码中硬编码

### Q: 搜索结果为空？

A: 可能的原因：
1. API Key 无效或过期
2. 话题关键词过于生僻
3. API 调用次数超限
4. 网络连接问题

### Q: 如何查看 API 使用情况？

A: 登录快代理控制台 → 我的API → 查看调用统计

### Q: 可以用其他 API 服务吗？

A: 可以。修改 `zhihu_kuaidaili.py` 中的 API 调用逻辑即可。

---

## 📚 参考链接

- 快代理官网：https://www.kuaidaili.com/
- 快代理 API 文档：https://www.kuaidaili.com/doc
- 知乎官方 API：https://open.zhihu.com/

---

**最后更新**: 2026-03-19
