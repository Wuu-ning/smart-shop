"""订单 API 路由（含地址）"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Order, OrderItem, Product, OrderStatus
from app.schemas import OrderCreate, OrderResponse, OrderItemResponse
from app.auth import get_current_user, require_admin

router = APIRouter(prefix="/api/orders", tags=["订单"])


@router.post("", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """创建订单（修复：地址信息现在会保存）"""
    if not order_data.items:
        raise HTTPException(status_code=400, detail="订单不能为空")

    total_price = 0.0
    order_items = []

    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"商品 {item.product_id} 不存在")
        if product.status != "上架":
            raise HTTPException(status_code=400, detail=f"商品 {product.name} 已下架")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"商品 {product.name} 库存不足")

        price = product.price * item.quantity
        total_price += price
        order_items.append(OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            price=product.price,
        ))
        product.stock -= item.quantity

    db_order = Order(
        user_id=current_user.id,
        total_price=round(total_price, 2),
        status=OrderStatus.PAID.value,
        address_name=order_data.address_name,
        address_phone=order_data.address_phone,
        address_detail=order_data.address_detail,
    )
    db.add(db_order)
    db.flush()

    for oi in order_items:
        oi.order_id = db_order.id
        db.add(oi)

    db.commit()
    db.refresh(db_order)
    return _format_order(db_order)


@router.get("", response_model=list[OrderResponse])
def list_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取当前用户的订单列表"""
    orders = db.query(Order).filter(Order.user_id == current_user.id)\
        .order_by(Order.created_at.desc()).all()
    return [_format_order(o) for o in orders]


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取订单详情"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="无权查看此订单")
    return _format_order(order)


def _format_order(order: Order) -> OrderResponse:
    """格式化订单响应"""
    items = []
    for item in order.items:
        items.append(OrderItemResponse(
            id=item.id,
            product_id=item.product_id,
            product_name=item.product.name if item.product else None,
            product_image=item.product.image_url if item.product else None,
            quantity=item.quantity,
            price=item.price,
        ))
    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        total_price=order.total_price,
        status=order.status,
        address_name=order.address_name,
        address_phone=order.address_phone,
        address_detail=order.address_detail,
        created_at=order.created_at,
        items=items,
    )
