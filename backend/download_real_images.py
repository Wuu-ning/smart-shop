"""
下载8个商品的真实产品图片
使用 curl_cffi 模拟浏览器访问，绕过CDN防盗链
"""
import os
from PIL import Image
import io

try:
    from curl_cffi import requests
    IMPERSONATE = True
except ImportError:
    import requests
    IMPERSONATE = False

SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
os.makedirs(SAVE_DIR, exist_ok=True)

# 每个商品的图片 - 从多个来源尝试
PRODUCT_IMAGES = [
    {
        "name": "华为 Mate 60 Pro",
        "filename": "mate60pro.png",
        "urls": [
            # 华为官方商城
            "https://res.vmallres.com/pimages/product/6942090977555/428_428_1719454795000MpNlN5scJmf0417864.png",
            # IT之家图赏
            "https://img.ithome.com/newsuploadfiles/2023/9/9b3f0e1d-1e3b-4a7d-9c5a-8f7e6d5c4b3a.jpg",
            # 备用
            "https://img1.360buyimg.com/n1/jfs/t1/213691/34/34942/184242/656ea61aF4c1a9c3e/2c5e9e6e4f4e4b4a.jpg",
        ],
    },
    {
        "name": "iPhone 15 Pro Max",
        "filename": "iphone15promax.png",
        "urls": [
            # Apple Store CDN
            "https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/iphone-15-pro-max-finish-select-202309-6-7inch-naturaltitanium?wid=800&fmt=png-alpha",
            # 备用
            "https://www.apple.com/newsroom/images/product/iphone/standard/Apple-iPhone-15-Pro-lineup-hero-230912.jpg.og.jpg",
        ],
    },
    {
        "name": "小米14 Ultra",
        "filename": "xiaomi14ultra.png",
        "urls": [
            "https://cdn.cnbj1.fds.api.mi-img.com/product-images/xiaomi14ultra/pc/h1.png",
            "https://i8.mifile.cn/v1/aI/5f7c2c18-bb21-6a1d-b9a4-71d7e70365c1!720x720.webp",
            "https://img14.360buyimg.com/n1/jfs/t1/166435/18/24711/122076/656ea61aF4c1a9c3e/2c5e9e6e4f4e4b4a.jpg",
        ],
    },
    {
        "name": "MacBook Pro 14英寸",
        "filename": "macbookpro14.png",
        "urls": [
            "https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/mbp14-spaceblack-select-202310?wid=800&fmt=png-alpha",
            "https://www.apple.com/newsroom/images/product/mac/standard/Apple-MacBook-Pro-14-16-inch-hero-171030.jpg.og.jpg",
        ],
    },
    {
        "name": "联想 ThinkPad X1 Carbon",
        "filename": "thinkpadx1.png",
        "urls": [
            "https://www.lenovo.com/medias/lenovo-laptop-thinkpad-x1-carbon-gen-11-hero.png?context=bWFzdGVyfHJvb3R8NDU5OTU3fGltYWdlL3BuZ3xoZGMvaDExLzE2NTUyMDc1MDYzNjE0LnBuZ3w5NjZlNTM3",
            "https://p3-ofp.static.pub//fes/cms/2023/04/13/lq2qk5cjrf9t8d9uo5nni2i0kppdde259596.png",
        ],
    },
    {
        "name": "Sony WH-1000XM5 耳机",
        "filename": "sonywh1000xm5.png",
        "urls": [
            "https://www.sony.com/image/5b7c6e6d6b8e6a9e6c0e6f6b6a6c6e6f?fmt=png&wid=660",
            "https://cdn-files.kimovil.com/default/0004/01/thumb_300726_default_big.jpeg",
        ],
    },
    {
        "name": "AirPods Pro 2",
        "filename": "airpodspro2.png",
        "urls": [
            "https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/MTJV3?wid=800&fmt=png-alpha",
            "https://www.apple.com/newsroom/images/product/airpods/standard/Apple-AirPods-Pro-2nd-gen-hero-220907.jpg.og.jpg",
        ],
    },
    {
        "name": "iPad Pro 12.9英寸",
        "filename": "ipadpro12.png",
        "urls": [
            "https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/ipad-pro-12-9-select-202104?wid=800&fmt=png-alpha",
            "https://www.apple.com/newsroom/images/product/ipad/standard/Apple-iPad-Pro-12-9-inch-hero-210420.jpg.og.jpg",
        ],
    },
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://www.google.com/',
    'Sec-Fetch-Dest': 'image',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
}


def download_image(url, save_path):
    """下载单张图片"""
    try:
        if IMPERSONATE:
            r = requests.get(url, headers=HEADERS, impersonate="chrome120", timeout=20)
        else:
            r = requests.get(url, headers=HEADERS, timeout=20)
        
        if r.status_code == 200 and len(r.content) > 2000:
            # 验证是有效图片
            try:
                img = Image.open(io.BytesIO(r.content))
                # 转为PNG保存
                img.save(save_path, 'PNG', optimize=True)
                print(f"  ✅ {os.path.basename(save_path)} ({len(r.content)//1024}KB, {img.size[0]}x{img.size[1]})")
                return True
            except Exception:
                print(f"  ⚠️  无效图片数据 ({len(r.content)} bytes)")
                return False
        else:
            print(f"  ⚠️  HTTP {r.status_code}, {len(r.content)} bytes")
            return False
    except Exception as e:
        print(f"  ❌ {str(e)[:70]}")
        return False


def main():
    print("=" * 60)
    print("📷 下载8个商品的真实产品图片")
    print(f"   模式: {'curl_cffi (模拟浏览器)' if IMPERSONATE else 'requests'}")
    print("=" * 60)

    success_count = 0
    for product in PRODUCT_IMAGES:
        filename = product["filename"]
        save_path = os.path.join(SAVE_DIR, filename)
        product_name = product["name"]

        print(f"\n▶ {product_name}")
        downloaded = False

        for i, url in enumerate(product["urls"]):
            print(f"  尝试来源{i+1}...", end=" ")
            if download_image(url, save_path):
                downloaded = True
                success_count += 1
                break

        if not downloaded:
            print(f"  ❌ 所有来源均失败，保留原占位图")

    print("\n" + "=" * 60)
    print(f"下载完成！成功: {success_count}/{len(PRODUCT_IMAGES)}")
    print("=" * 60)

    print("\n📂 最终文件列表:")
    total = 0
    for f in sorted(os.listdir(SAVE_DIR)):
        if f.endswith('.png') and f != 'placeholder.png':
            size = os.path.getsize(os.path.join(SAVE_DIR, f))
            total += size
            print(f"  {f:30s} {size//1024:>4d} KB")
    print(f"  {'─'*37}")
    print(f"  {'总计':30s} {total//1024:>4d} KB")


if __name__ == "__main__":
    main()
