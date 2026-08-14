"""
更新数据库中所有商品的图片路径为本地文件
"""
from app.database import init_db, SessionLocal
from app.models import Product

# 商品名称 → 本地图片文件名映射
IMAGE_MAP = {
    "华为 Mate 60 Pro": "/static/images/mate60pro.png",
    "iPhone 15 Pro Max": "/static/images/iphone15promax.png",
    "小米14 Ultra": "/static/images/xiaomi14ultra.png",
    "MacBook Pro 14英寸": "/static/images/macbookpro14.png",
    "联想 ThinkPad X1 Carbon": "/static/images/thinkpadx1.png",
    "Sony WH-1000XM5 耳机": "/static/images/sonywh1000xm5.png",
    "AirPods Pro 2": "/static/images/airpodspro2.png",
    "iPad Pro 12.9英寸": "/static/images/ipadpro12.png",
}


def update_images():
    init_db()
    db = SessionLocal()
    updated = 0

    for product in db.query(Product).all():
        if product.name in IMAGE_MAP:
            new_url = IMAGE_MAP[product.name]
            if product.image_url != new_url:
                product.image_url = new_url
                updated += 1
                print(f"  ✅ {product.name}: {new_url}")

    if updated:
        db.commit()
        print(f"\n已更新 {updated} 个商品的图片路径")
    else:
        print("所有商品图片路径已是最新")

    db.close()


def update_seed_data():
    """更新 seed_data.py 中的图片URL配置"""
    import seed_data as sd

    for i, p in enumerate(sd.products):
        if p["name"] in IMAGE_MAP:
            sd.products[i]["image_url"] = IMAGE_MAP[p["name"]]

    print(f"已更新 seed_data.py 中的 {len(sd.products)} 个商品图片路径")

    # 重写 seed_data.py
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seed_data.py')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    for name, url in IMAGE_MAP.items():
        old_url = f'image_url="https://'
        # Find the specific product in the file
        import re
        # Replace image_url for each product
        pattern = rf'(name="{name}".*?image_url=)"[^"]*"'
        replacement = rf'\1"{url}"'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("seed_data.py 已更新")


if __name__ == "__main__":
    import os
    print("🚀 更新商品图片路径...")
    update_images()
    print("\n✅ 数据库更新完成！")
