"""数据库种子数据（含角色）"""
from app.database import init_db, SessionLocal
from app.models import Product, User, Review
from app.auth import hash_password

products = [
    Product(name="华为 Mate 60 Pro", description="麒麟9000S芯片，卫星通话，昆仑玻璃，超聚光XMAGE影像", price=6999.00, stock=100, image_url="/static/images/mate60pro.png", category="手机", status="上架"),
    Product(name="iPhone 15 Pro Max", description="A17 Pro芯片，钛金属设计，4800万像素主摄，USB-C接口", price=9999.00, stock=50, image_url="/static/images/iphone15promax.png", category="手机", status="上架"),
    Product(name="小米14 Ultra", description="骁龙8Gen3，徕卡光学，小米澎湃OS，大师人像", price=5999.00, stock=80, image_url="/static/images/xiaomi14ultra.png", category="手机", status="上架"),
    Product(name="MacBook Pro 14英寸", description="M3 Pro芯片，Liquid视网膜XDR屏，18小时续航", price=14999.00, stock=30, image_url="/static/images/macbookpro14.png", category="笔记本", status="上架"),
    Product(name="联想 ThinkPad X1 Carbon", description="第13代酷睿i7，14英寸2.8K OLED屏，轻至1.12kg", price=10999.00, stock=25, image_url="/static/images/thinkpadx1.png", category="笔记本", status="上架"),
    Product(name="Sony WH-1000XM5 耳机", description="业界领先降噪，30小时续航，高解析度音频", price=2999.00, stock=200, image_url="/static/images/sonywh1000xm5.png", category="耳机", status="上架"),
    Product(name="AirPods Pro 2", description="H2芯片，自适应降噪，个性化空间音频", price=1899.00, stock=150, image_url="/static/images/airpodspro2.png", category="耳机", status="上架"),
    Product(name="iPad Pro 12.9英寸", description="M2芯片，Liquid视网膜XDR屏，支持Apple Pencil", price=9299.00, stock=40, image_url="/static/images/ipadpro12.png", category="平板", status="上架"),
]

def seed():
    init_db()
    db = SessionLocal()
    if db.query(User).count() > 0:
        print("数据库已有数据，跳过填充")
        db.close()
        return
    admin = User(username="admin", password_hash=hash_password("admin123"), email="admin@shop.com", role="admin")
    merchant = User(username="merchant", password_hash=hash_password("merchant123"), email="merchant@shop.com", role="merchant")
    shopper = User(username="shopper", password_hash=hash_password("shopper123"), email="shopper@shop.com", role="shopper")
    test = User(username="test", password_hash=hash_password("test123"), email="test@test.com", role="shopper")
    db.add_all([admin, merchant, shopper, test]); db.flush()
    for p in products: p.merchant_id = merchant.id; db.add(p)
    db.flush()
    for r in [
        Review(product_id=1, user_id=shopper.id, content="手机非常好用，拍照效果一流", rating=5, sentiment="正面"),
        Review(product_id=1, user_id=test.id, content="续航一般，一天一充", rating=3, sentiment="负面"),
        Review(product_id=2, user_id=shopper.id, content="系统流畅，生态很好", rating=5, sentiment="正面"),
        Review(product_id=3, user_id=test.id, content="性价比很高，值得购买", rating=5, sentiment="正面"),
        Review(product_id=6, user_id=shopper.id, content="降噪效果非常好，音质出色", rating=5, sentiment="正面"),
    ]: db.add(r)
    db.commit(); db.close()
    print(f"已恢复: {len(products)} 个商品")

if __name__ == "__main__": seed()
