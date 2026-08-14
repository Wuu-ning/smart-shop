# 智慧商城平台 — AI 评论情感分析系统

一个内置 AI 能力的全栈电商平台：基于朴素贝叶斯的**评论情感分析**、**AI 商品描述自动生成**、**智能模糊搜索**，支持购物者 / 商家 / 管理员三种角色。

## ✨ 核心功能

- **AI 评论情感分析**：jieba 中文分词 → CountVectorizer 特征提取（1500 维）→ 多项式朴素贝叶斯（alpha=0.3），自建 5600+ 条中文评论训练集，**测试准确率 99.1%**，支持情感词云可视化
- **AI 商品描述生成**：商家一键生成商品描述文案
- **智能模糊搜索**：多关键词 AND 匹配 + difflib 容错 + 品牌别名映射（如搜"苹果"可找到 iPhone / iPad / MacBook）
- **三角色权限体系**：购物者 / 商家 / 管理员，JWT 认证 + RBAC 权限控制
- **完整电商流程**：商品浏览、购物车、订单、收藏、评论点赞/踩、个人中心
- **图片上传**：商品图片上传与静态资源服务

## 🛠 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Python FastAPI、SQLAlchemy、JWT、jieba、scikit-learn |
| 前端 | Vue 3（Composition API）、Pinia、Vue Router、Element Plus、ECharts |
| 数据库 | MySQL 8 / SQLite 双引擎可切换（环境变量 `USE_MYSQL` 控制） |
| 部署 | 前端构建产物由后端统一托管，单命令启动 |

## 🚀 快速开始

### 后端（默认 SQLite，零配置）

```bash
cd backend
pip install -r requirements.txt
python run.py          # 启动于 http://localhost:8001
```

### 使用 MySQL 8

```bash
# 1. 在 Navicat/命令行执行 backend/setup_mysql.sql 初始化数据库
# 2. 设置环境变量后启动
set USE_MYSQL=1        # Windows
# export USE_MYSQL=1   # Linux/Mac
python run.py
```

### 前端（开发模式）

```bash
cd frontend
npm install
npm run dev            # http://localhost:5173
```

### 初始化数据

```bash
cd backend
python seed_data.py    # 生成商品、用户、评论等演示数据
```

### 内置账号

| 角色 | 账号 | 密码 |
|---|---|---|
| 管理员 | admin | admin123 |
| 商家 | merchant | merchant123 |
| 购物者 | shopper | shopper123 |

## 📁 目录结构

```
backend/
├── app/
│   ├── ml/            # 情感分析模型（训练脚本、模型、数据）
│   │   ├── train.py       # 模型训练：jieba + CountVectorizer + 朴素贝叶斯
│   │   ├── sentiment.py   # 情感预测服务
│   │   └── model.pkl      # 训练好的模型
│   ├── routers/       # 业务路由（商品/评论/订单/用户/AI/上传等）
│   ├── auth.py        # JWT 认证
│   ├── database.py    # SQLite/MySQL 双引擎
│   └── main.py        # 应用入口
├── seed_data.py       # 演示数据生成
├── generate_training_data.py  # 评论训练集生成
├── requirements.txt
└── run.py
frontend/
├── src/
│   ├── views/         # 页面（首页/商品/购物车/情感分析/商家后台/管理后台等）
│   ├── stores/        # Pinia 状态（购物车/用户）
│   ├── router/        # 路由与登录守卫
│   └── api/           # 接口封装
└── package.json
```

## 🧠 情感分析模型

- 分词：jieba 精确模式 + 自定义停用词表
- 特征：CountVectorizer，1500 维，去除低频词
- 模型：多项式朴素贝叶斯（alpha=0.3）
- 训练数据：5600+ 条中文商品评论（手机/平板/电脑等品类），由 `generate_training_data.py` 生成
- 评估：测试集准确率 **99.1%**

## 📌 备注

- 商品图片由 `backend/generate_product_images.py` 程序化生成，可重新生成
- 数据库文件（*.db）不入库，通过 `seed_data.py` 重建
