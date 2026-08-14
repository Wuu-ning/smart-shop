"""图片上传 API"""
import os
import uuid
import time
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.auth import get_current_user
from app.models import User, UserRole

router = APIRouter(prefix="/api/upload", tags=["上传"])

# 允许的图片格式
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# 图片存储目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'images')
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """上传商品图片，返回可访问的URL路径"""
    # 只允许商家和管理员上传
    if current_user.role not in (UserRole.MERCHANT.value, UserRole.ADMIN.value):
        raise HTTPException(status_code=403, detail="仅商家和管理员可上传图片")

    # 检查文件大小
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="图片不能超过5MB")

    # 验证文件类型
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的图片格式: {ext}，仅支持 {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # 生成唯一文件名：时间戳_uuid.扩展名
    unique_name = f"{int(time.time())}_{uuid.uuid4().hex[:8]}{ext}"
    save_path = os.path.join(UPLOAD_DIR, unique_name)

    # 保存文件
    with open(save_path, 'wb') as f:
        f.write(contents)

    url_path = f"/static/images/{unique_name}"
    return {"url": url_path, "filename": unique_name, "size": len(contents)}
