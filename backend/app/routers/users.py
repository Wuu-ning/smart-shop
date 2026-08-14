"""用户 API 路由（含角色管理）"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, UserRole
from app.schemas import UserRegister, UserLogin, UserResponse, TokenResponse
from app.auth import hash_password, verify_password, create_access_token, get_current_user, require_admin

router = APIRouter(prefix="/api", tags=["用户"])


@router.post("/register", response_model=TokenResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):
    """用户注册（自动登录并返回token）"""
    # 不允许注册为管理员
    role = user.role
    if role == UserRole.ADMIN.value:
        role = UserRole.SHOPPER.value

    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=409, detail="该用户名已被注册，请换一个")
    if user.email:
        existing_email = db.query(User).filter(User.email == user.email).first()
        if existing_email:
            raise HTTPException(status_code=409, detail="该邮箱已被其他账号使用")

    db_user = User(
        username=user.username,
        password_hash=hash_password(user.password),
        email=user.email,
        role=role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    token = create_access_token(data={"user_id": db_user.id, "role": db_user.role})
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(db_user),
    )


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """用户登录（支持用户名或邮箱）"""
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user and "@" in user.username:
        db_user = db.query(User).filter(User.email == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名/邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(data={"user_id": db_user.id, "role": db_user.role})
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(db_user),
    )


@router.get("/users/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return UserResponse.model_validate(current_user)


@router.put("/users/profile", response_model=UserResponse)
def update_profile(
    email: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """更新个人资料"""
    if email is not None:
        if email and not __import__("re").match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            raise HTTPException(status_code=400, detail="邮箱格式不正确")
        existing = db.query(User).filter(User.email == email, User.id != current_user.id).first()
        if existing:
            raise HTTPException(status_code=409, detail=u90aeu7bb1u5df2u88abu5176u4ed6u8d26u53f7u4f7fu7528)
        current_user.email = email
    db.commit()
    return UserResponse.model_validate(current_user)


# ========== 管理员接口 ==========

@router.get("/users", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """管理员：查看所有用户"""
    users = db.query(User).order_by(User.created_at.desc()).all()
    return [UserResponse.model_validate(u) for u in users]


@router.put("/users/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    new_role: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """管理员：修改用户角色"""
    if new_role not in [r.value for r in UserRole]:
        raise HTTPException(status_code=400, detail="无效的角色")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user.role = new_role
    db.commit()
    return UserResponse.model_validate(user)
