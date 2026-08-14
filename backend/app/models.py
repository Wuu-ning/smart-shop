"""SQLAlchemy ORM 模型"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    SHOPPER = "shopper"    # 购物者
    MERCHANT = "merchant"  # 商家
    ADMIN = "admin"        # 管理员


class OrderStatus(str, enum.Enum):
    PENDING = "待付款"
    PAID = "已付款"
    SHIPPED = "已发货"
    DELIVERED = "已送达"
    CANCELLED = "已取消"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    role = Column(String(20), default=UserRole.SHOPPER.value, nullable=False)  # 角色
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    # 商家拥有的商品
    products = relationship("Product", back_populates="merchant", foreign_keys="Product.merchant_id")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    image_url = Column(String(500), nullable=True)
    category = Column(String(100), nullable=True)
    merchant_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # 所属商家
    status = Column(String(20), default="上架")  # 上架/下架
    created_at = Column(DateTime, default=datetime.utcnow)

    merchant = relationship("User", back_populates="products", foreign_keys=[merchant_id])
    reviews = relationship("Review", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String(20), default=OrderStatus.PAID.value)  # 简化默认已付款
    address_name = Column(String(50), nullable=True)   # 收货人
    address_phone = Column(String(20), nullable=True)  # 手机号
    address_detail = Column(String(200), nullable=True) # 收货地址
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, status='{self.status}')>"


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

    def __repr__(self):
        return f"<OrderItem(order_id={self.order_id}, product_id={self.product_id}, qty={self.quantity})>"


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)  # 1-5 星
    sentiment = Column(String(10), nullable=True)  # 正面/负面
    is_hidden = Column(Integer, default=0)  # 管理员隐藏（0=显示, 1=隐藏）
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    def __repr__(self):
        return f"<Review(id={self.id}, product_id={self.product_id}, sentiment='{self.sentiment}')>"


class Favorite(Base):
    """商品收藏"""
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    product = relationship("Product")

    def __repr__(self):
        return f"<Favorite(user_id={self.user_id}, product_id={self.product_id})>"


class ReviewLike(Base):
    """评论点赞/踩"""
    __tablename__ = "review_likes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_like = Column(Integer, default=1)  # 1=点赞, 0=点踩
    created_at = Column(DateTime, default=datetime.utcnow)

    review = relationship("Review")
    user = relationship("User")

    def __repr__(self):
        return f"<ReviewLike(review_id={self.review_id}, user_id={self.user_id}, like={self.is_like})>"
