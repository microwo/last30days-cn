# 知乎 API 集成指南

## 推荐的 API 服务

### 1. 快代理（推荐）

**网站**：https://www.kuaidaili.com/

**优点**：
- ✅ 价格相对便宜
- ✅ 稳定可靠
- ✅ 支持知乎搜索和问答获取
- ✅ 完善的文档

**缺点**：
- ❌ 需要付费（按量计费）
- ❌ 需要实名认证

### 2. 其他第三方服务

- **极光数据**（https://www.jiguang.cn/）
- **天行数据**（https://www.tianapi.com/）
- **聚合数据**（https://www.juhe.cn/）

### 3. 官方 API（不推荐）

**网站**：https://open.zhihu.com/

**缺点**：
- ❌ 申请门槛高（需要企业账号）
- ❌ 配额限制严格
- ❌ 审核周期长

---

## 快代理知乎 API 集成步骤

### 步骤 1：注册账号

1. 访问 https://www.kuaidaili.com/
2. 注册账号（需要手机号实名认证）
3. 登录后进入控制台

### 步骤 2：申请 API 密钥

1. 在控制台选择「API 产品」→「知乎 API」
2. 申请知乎搜索 API
3. 获取 API Key（类似：`a1b2c3d4e5f6g7h8i9j0k1l2m`）

### 步骤 3：安装 requests 库

```bash
pip3 install requests
```

### 步骤 4：修改 zhihu.py 代码
