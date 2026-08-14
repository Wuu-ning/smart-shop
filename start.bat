@echo off
chcp 65001 >nul
title 智慧商城

echo =====================================
echo     🛍️  智慧商城 - 一键启动
echo =====================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未安装 Python
    pause
    exit /b
)

echo 📦 安装依赖...
cd /d %~dp0backend
pip install -r requirements.txt -q 2>nul

if "%USE_MYSQL%"=="" (
    if not exist shop.db (
        echo 🗄️  初始化数据库...
        python seed_data.py
        python -m app.ml.train
    )
)

echo 🚀 启动服务...
echo.
echo =====================================
echo   ✅ 生产访问: http://localhost:8001
echo   ✅ 前端开发: http://localhost:8000
echo.
echo   账号: admin / admin123
echo =====================================
echo.
python run.py

pause
