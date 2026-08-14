"""商品 API 路由（含商家管理）"""
from typing import Optional
import difflib
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models import Product, User, UserRole
from app.schemas import ProductResponse, ProductListResponse, ProductCreate, ProductUpdate
from app.auth import get_current_user, require_merchant_or_admin

router = APIRouter(prefix="/api/products", tags=["商品"])


def _apply_fuzzy_search(query, keyword):
    """
    模糊搜索逻辑：
    1. 品牌别名扩展（如"苹果"→iPhone/iPad/MacBook）
    2. 将关键词按空格拆分为多个词
    3. 每个词在 name / description / category 中搜索 (OR)
    4. 不同词之间是 AND 关系
    """
    # 品牌别名映射
    BRAND_ALIASES = {
        "苹果": ["iPhone", "iPad", "MacBook", "Apple"],
        "华为": ["Huawei", "华为"],
        "小米": ["Xiaomi", "小米"],
        "三星": ["Samsung", "三星"],
        "oppo": ["OPPO"],
        "vivo": ["vivo"],
        "荣耀": ["Honor", "荣耀"],
        "一加": ["OnePlus", "一加"],
        "联想": ["Lenovo", "联想"],
        "华硕": ["ASUS", "华硕"],
        "戴尔": ["Dell", "戴尔"],
        "惠普": ["HP", "惠普"],
        "索尼": ["Sony", "索尼"],
        "bose": ["Bose"],
    }
    
    terms = [t.strip() for t in keyword.split() if t.strip()]
    if not terms:
        return query
    
    # 扩展关键词（品牌别名展开：同一品牌的不同别名间是OR关系）
    for term in terms:
        if term in BRAND_ALIASES:
            aliases = BRAND_ALIASES[term]
            # 品牌别名之间是OR关系
            query = query.filter(
                or_(*[Product.name.contains(a) for a in aliases],
                    *[Product.description.contains(a) for a in aliases],
                    *[Product.category.contains(a) for a in aliases])
            )
        else:
            query = query.filter(
                or_(
                    Product.name.contains(term),
                    Product.description.contains(term),
                    Product.category.contains(term),
                )
            )
    return query


def _fuzzy_fallback(db, keyword, limit=20):
    """
    模糊容错：
    1. 用 difflib 在商品名中找最接近的匹配
    2. 如果多个词，先用最后一个词做 difflib 匹配
    3. 回退到单字 OR 匹配
    """
    all_products = db.query(Product).filter(
        Product.status == "上架"
    ).all()

    # 提取最后一个词用于模糊匹配
    terms = [t.strip() for t in keyword.split() if t.strip()]
    search_term = terms[-1] if terms else keyword

    names = [p.name for p in all_products]
    matches = difflib.get_close_matches(search_term, names, n=limit, cutoff=0.3)

    if matches:
        return db.query(Product).filter(
            Product.name.in_(matches),
            Product.status == "上架",
        )

    # 终极回退：拆成单字符 OR 匹配
    chars = [c for c in keyword if c.strip() and ord(c) > 0x4e00]  # 只取中文字符
    if len(chars) >= 1:
        char_filters = [
            or_(
                Product.name.contains(c),
                Product.description.contains(c),
                Product.category.contains(c),
            ) for c in chars
        ]
        if char_filters:
            return db.query(Product).filter(
                or_(*char_filters),
                Product.status == "上架",
            )
    return None


@router.get("", response_model=ProductListResponse)
def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    category: Optional[str] = None,
    keyword: Optional[str] = None,
    merchant_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """获取商品列表（分页+筛选，支持模糊搜索）"""
    query = db.query(Product)

    if category:
        query = query.filter(Product.category == category)
    if keyword:
        # 先尝试标准模糊搜索
        query = _apply_fuzzy_search(query, keyword)
    if merchant_id:
        query = query.filter(Product.merchant_id == merchant_id)

    query = query.filter(Product.status == "上架")

    # 如果标准搜索没结果，触发模糊容错
    if keyword:
        temp_count = query.count()
        if temp_count == 0:
            fallback = _fuzzy_fallback(db, keyword)
            if fallback is not None:
                query = fallback

    total = query.count()
    items = query.order_by(Product.created_at.desc())\
        .offset((page - 1) * page_size).limit(page_size).all()

    return ProductListResponse(
        items=[_format_product(p) for p in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/suggestions", response_model=list[str])
def product_suggestions(
    keyword: str = Query(..., min_length=1),
    limit: int = Query(8, ge=1, le=20),
    db: Session = Depends(get_db),
):
    """搜索建议：模糊匹配商品名（支持多关键词）"""
    query = db.query(Product).filter(Product.status == "上架")
    query = _apply_fuzzy_search(query, keyword)
    products = query.limit(limit).all()

    # 如果标准搜索没结果，用 difflib 容错
    if not products:
        all_products = db.query(Product.name).filter(
            Product.status == "上架"
        ).all()
        names = [p[0] for p in all_products]
        matches = difflib.get_close_matches(keyword, names, n=limit, cutoff=0.4)
        return matches

    return [p.name for p in products]


@router.get("/all", response_model=ProductListResponse)
def list_all_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """商家/管理员：查看所有商品（含下架）"""
    query = db.query(Product)
    if current_user.role == UserRole.MERCHANT.value:
        query = query.filter(Product.merchant_id == current_user.id)
    total = query.count()
    items = query.order_by(Product.created_at.desc())        .offset((page - 1) * page_size).limit(page_size).all()
    return ProductListResponse(
        items=[_format_product(p) for p in items],
        total=total,
        page=page,
        page_size=page_size,
    )




@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """获取商品详情"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return _format_product(product)


@router.post("", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_merchant_or_admin),
):
    """商家/管理员：创建商品"""
    db_product = Product(
        **product.model_dump(),
        merchant_id=current_user.id,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return _format_product(db_product)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """商家/管理员：更新商品（商家只能改自己的）"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="商品不存在")
    # 权限检查
    if current_user.role == UserRole.MERCHANT.value and db_product.merchant_id != current_user.id:
        raise HTTPException(status_code=403, detail="只能修改自己的商品")

    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return _format_product(db_product)


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """商家/管理员：删除商品（商家只能删自己的）"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="商品不存在")
    if current_user.role == UserRole.MERCHANT.value and db_product.merchant_id != current_user.id:
        raise HTTPException(status_code=403, detail="只能删除自己的商品")

    db.delete(db_product)
    db.commit()
    return {"message": "商品已删除"}


def _format_product(product: Product) -> ProductResponse:
    """格式化商品响应"""
    merchant_name = product.merchant.username if product.merchant else None
    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        image_url=product.image_url,
        category=product.category,
        merchant_id=product.merchant_id,
        merchant_name=merchant_name,
        status=product.status,
        created_at=product.created_at,
    )
