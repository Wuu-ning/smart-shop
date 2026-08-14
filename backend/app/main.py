"""FastAPI 应用入口 — 托管后端 API + 前端页面"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from app.database import init_db
from app.routers import products, users, orders, reviews, favorites, upload, ai

app = FastAPI(
    title="购物平台 - 评论情感分析系统",
    description="Shopping Platform with Sentiment Analysis",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'static')               # 商品图片
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend_dist')       # 前端页面
FRONTEND_INDEX = os.path.join(FRONTEND_DIR, 'index.html')

# ===== API 路由 =====
app.include_router(products.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(reviews.router)
app.include_router(favorites.router)
app.include_router(upload.router)
app.include_router(ai.router)


# ===== 静态文件（商品图片） =====
@app.get("/static/{file_path:path}")
def serve_static(file_path: str):
    safe_path = os.path.normpath(file_path).lstrip(os.sep)
    full_path = os.path.join(STATIC_ROOT, safe_path)
    if not full_path.startswith(STATIC_ROOT) or not os.path.isfile(full_path):
        placeholder = os.path.join(STATIC_ROOT, 'images', 'placeholder.png')
        if os.path.isfile(placeholder):
            return FileResponse(placeholder, media_type='image/png')
        return JSONResponse(status_code=404, content={"detail": "Not found"})
    return FileResponse(full_path)


# ===== 前端构建产物（JS/CSS） =====
@app.get("/assets/{file_path:path}")
def serve_assets(file_path: str):
    full_path = os.path.join(FRONTEND_DIR, 'assets', file_path)
    if os.path.isfile(full_path):
        return FileResponse(full_path)
    return JSONResponse(status_code=404, content={"detail": "Not found"})


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


# ===== 首页 =====
@app.get("/")
def root():
    if os.path.isfile(FRONTEND_INDEX):
        return FileResponse(FRONTEND_INDEX, media_type="text/html")
    return {"message": "购物平台 API 服务运行中", "version": "1.0.0"}


# ===== SPA 路由（所有非 API 路径返回 index.html） =====
@app.get("/{catchall:path}")
def spa_fallback(catchall: str):
    if os.path.isfile(FRONTEND_INDEX):
        return FileResponse(FRONTEND_INDEX, media_type="text/html")
    return {"message": "购物平台 API 服务运行中", "version": "1.0.0"}
