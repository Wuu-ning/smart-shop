"""启动脚本"""
import uvicorn


if __name__ == "__main__":
    print("🚀 后端服务启动于 http://localhost:8001")
    print("📖 API文档: http://localhost:8001/docs")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )
