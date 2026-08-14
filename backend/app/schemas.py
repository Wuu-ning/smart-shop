"""Pydantic 数据模型（请求/响应）"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, field_validator, Field
import re


# ========== 用户 ==========
class UserRegister(BaseModel):
    username: str = Field(..., min_length=2, max_length=20)
    password: str = Field(..., min_length=6, max_length=50)
    email: Optional[str] = None
    role: str = "shopper"  # shopper / merchant

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]{2,20}$', v):
            raise ValueError("用户名只能包含字母、数字、下划线和中文 (2-20位)")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("密码长度至少6位")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if v:
            if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', v):
                raise ValueError("邮箱格式不正确")
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        if v not in ("shopper", "merchant"):
            raise ValueError("角色只能是 shopper 或 merchant")
        return v


class UserLogin(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    role: str = "shopper"
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ========== 商品 ==========
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)
    image_url: Optional[str] = None
    category: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None  # 上架/下架


class ProductResponse(ProductBase):
    id: int
    merchant_id: Optional[int] = None
    merchant_name: Optional[str] = None
    status: str = "上架"
    created_at: datetime

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    page: int
    page_size: int


# ========== 订单 ==========
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1)


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    address_name: Optional[str] = None
    address_phone: Optional[str] = None
    address_detail: Optional[str] = None


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: Optional[str] = None
    product_image: Optional[str] = None
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    address_name: Optional[str] = None
    address_phone: Optional[str] = None
    address_detail: Optional[str] = None
    created_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True


# ========== 评论 ==========
class ReviewCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)
    rating: Optional[int] = Field(None, ge=1, le=5)


class ReviewResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    username: Optional[str] = None
    content: str
    rating: Optional[int] = None
    sentiment: Optional[str] = None
    is_hidden: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


# ========== 情感分析 ==========
class SentimentResult(BaseModel):
    sentiment: str
    label: int
    confidence: float
    prob_positive: float
    prob_negative: float


class WordCloudResponse(BaseModel):
    positive_wordcloud: str
    negative_wordcloud: str
    stats: dict
