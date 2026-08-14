-- ============================================================
-- MySQL 初始化脚本
-- 在 Navicat 中执行此文件来创建数据库
-- 
-- 使用方法:
-- 1. 打开 Navicat → 连接你的 MySQL 8.0.44
-- 2. 新建查询 (Ctrl+Q)
-- 3. 复制粘贴以下 SQL 执行
-- 4. 或者直接运行这个文件
-- ============================================================

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS `shop`
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE `shop`;

-- 说明：数据表会在首次运行项目时由 SQLAlchemy 自动创建
-- 不需要手动建表！
-- 
-- 配置完成后：
-- 1. 复制 .env.example 为 .env
-- 2. 修改 .env 中的数据库连接信息
-- 3. 运行 python seed_data.py 初始化数据
-- 4. 运行 python run.py 启动服务
