"""数据库配置（支持 SQLite 和 MySQL）"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 加载 .env 文件（如果存在）
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', '.env')
load_dotenv(env_path)
# 也尝试加载 backend 目录下的 .env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

# ============================================================
# 数据库连接配置
# 优先读取环境变量 DATABASE_URL
# 如果未设置，默认使用 SQLite (backend/shop.db)
#
# 【MySQL 配置方法】
# 方式一：设置环境变量
#   set DATABASE_URL=mysql+pymysql://root:密码@localhost:3306/shop
#
# 方式二：直接修改下方 DATABASE_URL 为你的连接串
# ============================================================

DEFAULT_SQLITE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'shop.db'
)

# MySQL 连接串格式：
# mysql+pymysql://用户名:密码@主机:端口/数据库名?charset=utf8mb4
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///{DEFAULT_SQLITE_PATH}?check_same_thread=False"
)

# 连接参数
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """依赖注入：获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库，创建所有表"""
    from app.models import User, Product, Order, OrderItem, Review, Favorite, ReviewLike  # noqa
    Base.metadata.create_all(bind=engine)
