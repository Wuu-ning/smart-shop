"""
为每个商品生成风格化的产品图片
使用 PIL 生成带渐变背景 + 产品名称 + 分类图标的占位图
"""
import os
from PIL import Image, ImageDraw, ImageFont

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
os.makedirs(STATIC_DIR, exist_ok=True)

# 商品图片配置：名字、颜色主题、分类图标文字、文件名
PRODUCTS = [
    {
        "name": "华为 Mate 60 Pro",
        "colors": ["#7B2D8B", "#3A1C71"],
        "icon": "📱",
        "filename": "mate60pro.png",
        "text_color": "#FFFFFF",
    },
    {
        "name": "iPhone 15 Pro Max",
        "colors": ["#333333", "#666666"],
        "icon": "📱",
        "filename": "iphone15promax.png",
        "text_color": "#FFFFFF",
    },
    {
        "name": "小米14 Ultra",
        "colors": ["#FF6B35", "#D63031"],
        "icon": "📱",
        "filename": "xiaomi14ultra.png",
        "text_color": "#FFFFFF",
    },
    {
        "name": "MacBook Pro 14英寸",
        "colors": ["#2C3E50", "#3498DB"],
        "icon": "💻",
        "filename": "macbookpro14.png",
        "text_color": "#FFFFFF",
    },
    {
        "name": "联想 ThinkPad X1 Carbon",
        "colors": ["#1a1a2e", "#16213e"],
        "icon": "💻",
        "filename": "thinkpadx1.png",
        "text_color": "#FFFFFF",
    },
    {
        "name": "Sony WH-1000XM5 耳机",
        "colors": ["#2d3436", "#636e72"],
        "icon": "🎧",
        "filename": "sonywh1000xm5.png",
        "text_color": "#FFFFFF",
    },
    {
        "name": "AirPods Pro 2",
        "colors": ["#FFFFFF", "#E8E8E8"],
        "icon": "🎧",
        "filename": "airpodspro2.png",
        "text_color": "#333333",
    },
    {
        "name": "iPad Pro 12.9英寸",
        "colors": ["#6C5CE7", "#a29bfe"],
        "icon": "📟",
        "filename": "ipadpro12.png",
        "text_color": "#FFFFFF",
    },
]

# 尝试加载中文字体
FONT_PATHS = [
    'C:/Windows/Fonts/simhei.ttf',
    'C:/Windows/Fonts/msyh.ttc',
    'C:/Windows/Fonts/msyhbd.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    None,  # fallback to default
]

def get_font(size):
    for fp in FONT_PATHS:
        try:
            if fp:
                return ImageFont.truetype(fp, size)
            else:
                return ImageFont.load_default()
        except (IOError, OSError):
            continue
    return ImageFont.load_default()


def create_gradient(width, height, color1, color2):
    """创建渐变背景"""
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    for y in range(height):
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        ratio = y / height
        r = int(r1 * (1 - ratio) + r2 * ratio)
        g = int(g1 * (1 - ratio) + g2 * ratio)
        b = int(b1 * (1 - ratio) + b2 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return image


def generate_product_images():
    """为所有商品生成图片"""
    img_w, img_h = 600, 600

    for product in PRODUCTS:
        filename = product["filename"]
        filepath = os.path.join(STATIC_DIR, filename)

        # 如果已经存在则跳过
        if os.path.exists(filepath):
            print(f"  ⏭️  {filename} 已存在，跳过")
            continue

        # 创建渐变背景
        img = create_gradient(img_w, img_h, product["colors"][0], product["colors"][1])
        draw = ImageDraw.Draw(img)

        # 绘制分类图标（Emoji）
        icon_font = get_font(180)
        icon_bbox = draw.textbbox((0, 0), product["icon"], font=icon_font)
        icon_w = icon_bbox[2] - icon_bbox[0]
        icon_x = (img_w - icon_w) // 2
        icon_y = 140
        draw.text((icon_x, icon_y), product["icon"], font=icon_font, fill=product["text_color"])

        # 绘制分隔线
        line_y = icon_y + 200
        draw.line([(120, line_y), (img_w - 120, line_y)],
                  fill=(255, 255, 255, 80) if product["text_color"] == "#FFFFFF" else (0, 0, 0, 80),
                  width=2)

        # 绘制产品名称
        name_font = get_font(40)
        name = product["name"]

        # 处理长名称换行
        max_width = img_w - 80
        lines = []
        current_line = ""
        for char in name:
            test_line = current_line + char
            bbox = draw.textbbox((0, 0), test_line, font=name_font)
            if bbox[2] - bbox[0] > max_width and current_line:
                lines.append(current_line)
                current_line = char
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)

        # 居中绘制每行文字
        total_text_h = len(lines) * 55
        start_y = line_y + 30
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=name_font)
            text_w = bbox[2] - bbox[0]
            x = (img_w - text_w) // 2
            y = start_y + i * 55
            draw.text((x, y), line, font=name_font, fill=product["text_color"])

        # 保存
        img.save(filepath, 'PNG')
        print(f"  ✅ 已生成: {filename} ({product['name']})")

    print(f"\n所有图片已保存到: {STATIC_DIR}")
    print(f"共 {len(PRODUCTS)} 张图片")


if __name__ == "__main__":
    print("🚀 开始生成商品图片...")
    generate_product_images()
