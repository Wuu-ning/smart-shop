"""收藏夹 API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Product, Favorite
from app.auth import get_current_user

router = APIRouter(prefix="/api/favorites", tags=["收藏夹"])


@router.get("")
def list_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取当前用户的收藏列表"""
    favs = db.query(Favorite).filter(Favorite.user_id == current_user.id)\
        .order_by(Favorite.created_at.desc()).all()
    results = []
    for fav in favs:
        p = fav.product
        results.append({
            "id": fav.id,
            "product_id": p.id,
            "product_name": p.name,
            "product_price": p.price,
            "product_image": p.image_url,
            "created_at": fav.created_at.isoformat(),
        })
    return results


@router.post("/{product_id}")
def add_favorite(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """收藏商品"""
    # 检查商品
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    # 检查是否已收藏
    existing = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.product_id == product_id,
    ).first()
    if existing:
        return {"message": "已收藏", "favorited": True}
    fav = Favorite(user_id=current_user.id, product_id=product_id)
    db.add(fav)
    db.commit()
    return {"message": "收藏成功", "favorited": True}


@router.delete("/{product_id}")
def remove_favorite(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """取消收藏"""
    fav = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.product_id == product_id,
    ).first()
    if fav:
        db.delete(fav)
        db.commit()
    return {"message": "已取消收藏", "favorited": False}


@router.get("/check/{product_id}")
def check_favorite(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """检查是否已收藏某个商品"""
    existing = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.product_id == product_id,
    ).first()
    return {"favorited": existing is not None}
