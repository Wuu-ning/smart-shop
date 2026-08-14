"""
============================================================
📷 真实产品图片下载脚本
============================================================
在您的电脑上运行此脚本，它会自动下载8个商品的真实产品图。
需要网络连接（科学上网可提高Apple图片的下载成功率）。

使用方法：
    cd backend
    python download_real_images_v2.py

依赖：pip install requests curl_cffi pillow
============================================================
"""
import os
import sys
from PIL import Image
import io

# 尝试导入curl_cffi，如果失败则使用requests
try:
    from curl_cffi import requests
    IMPERSONATE = True
    print("✅ 使用 curl_cffi (模拟Chrome浏览器, 绕过CDN反爬)")
except ImportError:
    import requests
    IMPERSONATE = False
    print("⚠️ 使用普通requests (部分CDN可能拒绝)")
    print("   建议: pip install curl_cffi 以获得更好的下载成功率")

SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
os.makedirs(SAVE_DIR, exist_ok=True)

# ============================================================
# 每个商品多个备选图片来源（按优先级排列）
# ============================================================
PRODUCTS = [
    {
        "name": "华为 Mate 60 Pro",
        "file": "mate60pro.png",
        "urls": [
            # 华为商城/Vmall
            "https://res.vmallres.com/pimages/product/6942090977555/428_428_1719454795000MpNlN5scJmf0417864.png",
            # IT之家
            "https://img.ithome.com/newsuploadfiles/2023/9/20230904_104100_580.jpg",
            # ZOL中关村
            "https://img2.zol.com.cn/product/155/50/cehW5MNkINsY6.jpg",
        ],
    },
    {
        "name": "iPhone 15 Pro Max",
        "file": "iphone15promax.png",
        "urls": [
            # Apple Store (需要curl_cffi)
            "https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/iphone-15-pro-max-finish-select-202309-6-7inch-naturaltitanium?wid=800&fmt=png-alpha",
            # Apple 新闻室
            "https://www.apple.com/newsroom/images/product/iphone/standard/Apple-iPhone-15-Pro-lineup-hero-230912.jpg.og.jpg",
            # 备用
            "https://img1.baidu.com/it/u=1351894409,3819328015&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=800",
        ],
    },
    {
        "name": "小米14 Ultra",
        "file": "xiaomi14ultra.png",
        "urls": [
            "https://cdn.cnbj1.fds.api.mi-img.com/product-images/xiaomi14ultra/pc/h1.png",
            "https://i8.mifile.cn/v1/aI/5f7c2c18-bb21-6a1d-b9a4-71d7e70365c1!720x720.webp",
            "https://img2.baidu.com/it/u=2390427880,138577527&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=800",
        ],
    },
    {
        "name": "MacBook Pro 14英寸",
        "file": "macbookpro14.png",
        "urls": [
            "https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/mbp14-spaceblack-select-202310?wid=800&fmt=png-alpha",
            "https://www.apple.com/newsroom/images/product/mac/standard/Apple-MacBook-Pro-14-16-inch-hero-171030.jpg.og.jpg",
        ],
    },
    {
        "name": "联想 ThinkPad X1 Carbon",
        "file": "thinkpadx1.png",
        "urls": [
            "https://www.lenovo.com/medias/lenovo-laptop-thinkpad-x1-carbon-gen-11-hero.png?context=bWFzdGVyfHJvb3R8NDU5OTU3fGltYWdlL3BuZ3xoZGMvaDExLzE2NTUyMDc1MDYzNjE0LnBuZ3w5NjZlNTM3",
            "https://p3-ofp.static.pub//fes/cms/2023/04/13/lq2qk5cjrf9t8d9uo5nni2i0kppdde259596.png",
        ],
    },
    {
        "name": "Sony WH-1000XM5",
        "file": "sonywh1000xm5.png",
        "urls": [
            "https://www.sony.com/image/5b7c6e6d6b8e6a9e6c0e6f6b6a6c6e6f?fmt=png&wid=660",
            "https://cdn-files.kimovil.com/default/0004/01/thumb_300726_default_big.jpeg",
        ],
    },
    {
        "name": "AirPods Pro 2",
        "file": "airpodspro2.png",
        "urls": [
            # 这个来源已验证可工作
            "https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/MTJV3?wid=800&fmt=png-alpha",
            "https://www.apple.com/newsroom/images/product/airpods/standard/Apple-AirPods-Pro-2nd-gen-hero-220907.jpg.og.jpg",
        ],
    },
    {
        "name": "iPad Pro 12.9英寸",
        "file": "ipadpro12.png",
        "urls": [
            "https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/ipad-pro-12-9-select-202104?wid=800&fmt=png-alpha",
            "https://www.apple.com/newsroom/images/product/ipad/standard/Apple-iPad-Pro-12-9-inch-hero-210420.jpg.og.jpg",
        ],
    },
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}


def download(url, save_path):
    """尝试下载一张图片"""
    try:
        if IMPERSONATE:
            r = requests.get(url, headers=HEADERS, impersonate="chrome120", timeout=25)
        else:
            r = requests.get(url, headers=HEADERS, timeout=25)

        if r.status_code != 200 or len(r.content) < 2000:
            return False, f"HTTP {r.status_code}, {len(r.content)}B"

        # 验证是图片
        try:
            img = Image.open(io.BytesIO(r.content))
            img.save(save_path, 'PNG', optimize=True)
            return True, f"✅ {img.size[0]}x{img.size[1]}, {len(r.content)//1024}KB"
        except Exception:
            return False, f"无效图片数据 ({len(r.content)}B)"
    except Exception as e:
        return False, str(e)[:60]


def main():
    print("=" * 65)
    print("  📷 真实产品图片下载工具")
    print("=" * 65)
    print(f"  保存路径: {SAVE_DIR}")
    print()

    success = 0
    for product in PRODUCTS:
        name = product["name"]
        filename = product["file"]
        save_path = os.path.join(SAVE_DIR, filename)

        print(f"  ▶ {name}")
        downloaded = False

        for i, url in enumerate(product["urls"]):
            ok, msg = download(url, save_path)
            status = "✅" if ok else "❌"
            print(f"    来源{i+1}: {status} {msg}")
            if ok:
                downloaded = True
                success += 1
                break

        if not downloaded:
            print(f"    ⚠️  所有来源失败，保留已有图片")
        print()

    print("=" * 65)
    print(f"  结果: {success}/{len(PRODUCTS)} 个商品下载成功")
    print()
    print("  📂 图片文件列表:")
    total_size = 0
    for f in sorted(os.listdir(SAVE_DIR)):
        if f.endswith(('.png', '.jpg')) and f != 'placeholder.png':
            size = os.path.getsize(os.path.join(SAVE_DIR, f))
            total_size += size
            source = "真实图片" if size > 15000 else "占位图"
            print(f"    {f:30s} {size//1024:>4d} KB  [{source}]")
    print(f"    {'─'*45}")
    print(f"    {'总计':30s} {total_size//1024:>4d} KB")
    print("=" * 65)


if __name__ == "__main__":
    main()
