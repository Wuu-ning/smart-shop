"""评论 API 路由（含情感分析 + 管理员审核）"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Product, Review, ReviewLike
from app.schemas import ReviewCreate, ReviewResponse, SentimentResult, WordCloudResponse
from app.auth import get_current_user, require_admin
from app.ml.sentiment import predict_sentiment, generate_wordcloud

router = APIRouter(prefix="/api", tags=["评论"])


@router.get("/products/{product_id}/reviews", response_model=list[ReviewResponse])
def list_reviews(
    product_id: int,
    sentiment: Optional[str] = Query(None, pattern="^(正面|负面)$"),
    db: Session = Depends(get_db),
):
    """获取商品评论列表（默认不显示被隐藏的评论）"""
    query = db.query(Review).filter(
        Review.product_id == product_id,
        Review.is_hidden == 0,  # 只显示未被隐藏的
    )
    if sentiment:
        query = query.filter(Review.sentiment == sentiment)
    reviews = query.order_by(Review.created_at.desc()).all()

    return [
        ReviewResponse(
            id=r.id, product_id=r.product_id, user_id=r.user_id,
            username=r.user.username if r.user else "匿名用户",
            content=r.content, rating=r.rating,
            sentiment=r.sentiment, is_hidden=r.is_hidden,
            created_at=r.created_at,
        ) for r in reviews
    ]


@router.post("/products/{product_id}/reviews", response_model=ReviewResponse)
def create_review(
    product_id: int,
    review: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """发表评论（自动情感分析）"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")

    sentiment_result = predict_sentiment(review.content)

    db_review = Review(
        product_id=product_id,
        user_id=current_user.id,
        content=review.content,
        rating=review.rating,
        sentiment=sentiment_result['sentiment'],
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return ReviewResponse(
        id=db_review.id, product_id=db_review.product_id,
        user_id=db_review.user_id, username=current_user.username,
        content=db_review.content, rating=db_review.rating,
        sentiment=db_review.sentiment, is_hidden=db_review.is_hidden,
        created_at=db_review.created_at,
    )


# ========== 管理员评论管理 ==========

@router.get("/admin/reviews", response_model=list[ReviewResponse])
def list_all_reviews(
    include_hidden: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """管理员：查看所有评论（含被隐藏的）"""
    query = db.query(Review)
    if not include_hidden:
        query = query.filter(Review.is_hidden == 0)
    reviews = query.order_by(Review.created_at.desc()).all()
    return [
        ReviewResponse(
            id=r.id, product_id=r.product_id, user_id=r.user_id,
            username=r.user.username if r.user else "匿名用户",
            content=r.content, rating=r.rating,
            sentiment=r.sentiment, is_hidden=r.is_hidden,
            created_at=r.created_at,
        ) for r in reviews
    ]


@router.put("/admin/reviews/{review_id}/hide")
def hide_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """管理员：隐藏不当评论"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="评论不存在")
    review.is_hidden = 1
    db.commit()
    return {"message": "评论已隐藏"}


@router.put("/admin/reviews/{review_id}/show")
def show_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """管理员：恢复显示评论"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="评论不存在")
    review.is_hidden = 0
    db.commit()
    return {"message": "评论已恢复显示"}


@router.delete("/reviews/{review_id}")
def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """删除评论（管理员可删任何评论，用户只能删自己的）"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="评论不存在")
    if current_user.role != "admin" and review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此评论")
    db.delete(review)
    db.commit()
    return {"message": "评论已删除"}


# ========== 评论点赞/踩 ==========

@router.get("/reviews/{review_id}/likes")
def get_review_likes(
    review_id: int,
    db: Session = Depends(get_db),
):
    """获取评论的点赞/踩数"""
    likes = db.query(ReviewLike).filter(ReviewLike.review_id == review_id, ReviewLike.is_like == 1).count()
    dislikes = db.query(ReviewLike).filter(ReviewLike.review_id == review_id, ReviewLike.is_like == 0).count()
    return {"likes": likes, "dislikes": dislikes}


@router.post("/reviews/{review_id}/like")
def like_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """点赞评论"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="评论不存在")
    existing = db.query(ReviewLike).filter(
        ReviewLike.review_id == review_id,
        ReviewLike.user_id == current_user.id,
    ).first()
    if existing:
        if existing.is_like == 1:
            db.delete(existing)
            db.commit()
            return {"message": "已取消点赞", "liked": False, "action": "unlike"}
        existing.is_like = 1
        db.commit()
        return {"message": "已点赞", "liked": True, "action": "like"}
    rl = ReviewLike(review_id=review_id, user_id=current_user.id, is_like=1)
    db.add(rl)
    db.commit()
    return {"message": "点赞成功", "liked": True, "action": "like"}


@router.post("/reviews/{review_id}/dislike")
def dislike_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """点踩评论"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="评论不存在")
    existing = db.query(ReviewLike).filter(
        ReviewLike.review_id == review_id,
        ReviewLike.user_id == current_user.id,
    ).first()
    if existing:
        if existing.is_like == 0:
            db.delete(existing)
            db.commit()
            return {"message": "已取消踩", "disliked": False, "action": "undislike"}
        existing.is_like = 0
        db.commit()
        return {"message": "已踩", "disliked": True, "action": "dislike"}
    rl = ReviewLike(review_id=review_id, user_id=current_user.id, is_like=0)
    db.add(rl)
    db.commit()
    return {"message": "踩成功", "disliked": True, "action": "dislike"}


# ========== 情感分析 ==========

@router.get("/sentiment/analyze", response_model=SentimentResult)
def analyze_sentiment(text: str = Query(..., min_length=1)):
    """分析单条评论的情感"""
    return predict_sentiment(text)


@router.get("/sentiment/wordcloud", response_model=WordCloudResponse)
def get_wordcloud():
    """获取正面/负面词云图"""
    try:
        return generate_wordcloud()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"词云生成失败: {str(e)}")
