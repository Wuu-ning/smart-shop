"""
============================================================
📊 情感分析训练数据生成器
============================================================
生成5000+条高质量中文商品评论，覆盖多品类、多维度，
让朴素贝叶斯模型学到更丰富的特征词。

用法: python generate_training_data.py
输出: app/ml/data/phone_reviews.txt (覆盖原文件)
============================================================
"""
import os
import random

random.seed(42)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'ml', 'data')
OUTPUT_PATH = os.path.join(DATA_DIR, 'phone_reviews.txt')

# ============================================================
# 评论模板（主语 + 评价）
# ============================================================

# 正面评价模板
POSITIVE_TEMPLATES = [
    # 外观设计
    "外观设计{adj}，{praise}",
    "{product}的颜值{adv}{adj}，{praise}",
    "做工{adj}，{praise}",
    "做工精致，手感{adj}",
    "手感{adv}{adj}，{praise}",
    "颜值{adv}{adj}，{praise}",
    "外观{adj}，拿出去{adv}有面子",
    "外观颜色{adj}，{praise}",
    "机身{adj}，{praise}",
    "设计{adj}，{praise}",
    "材质手感{adj}，{praise}",

    # 屏幕
    "屏幕显示效果{adv}{adj}，{praise}",
    "屏幕{adj}，{praise}",
    "分辨率{adv}{adj}，{praise}",
    "色彩还原{adj}，{praise}",
    "屏幕亮度{adv}{adj}，{praise}",
    "看视频效果{adv}{adj}，{praise}",
    "屏幕刷新率{adv}{adj}，滑动起来{praise}",
    "显示效果{adj}，{praise}",
    "画质{adj}，{praise}",
    "屏幕素质{adj}，{praise}",

    # 拍照
    "拍照效果{adv}{adj}，{praise}",
    "摄像头{adv}{adj}，{praise}",
    "夜景模式{adv}{adj}，{praise}",
    "拍照{adj}，{praise}",
    "像素{adv}{adj}，照片{adj}",
    "人像模式{adj}，{praise}",
    "视频拍摄{adj}，{praise}",
    "超广角{adj}，{praise}",
    "微距拍摄{adj}，{praise}",
    "防抖效果{adv}{adj}，{praise}",
    "相机{adj}，{praise}",
    "拍照清晰度{adj}，{praise}",

    # 性能
    "运行{adv}{adj}，{praise}",
    "性能{adv}{adj}，{praise}",
    "系统{adv}{adj}，{praise}",
    "玩游戏{adj}，{praise}",
    "多任务处理{adj}，{praise}",
    "打开应用速度{adv}{adj}，{praise}",
    "日常使用{adj}，{praise}",
    "手机运行速度{adv}{adj}，{praise}",
    "系统动画{adj}，{praise}",
    "大型游戏{adj}，{praise}",
    "性能释放{adv}{adj}，{praise}",
    "日常使用{adv}{adj}，一点也不卡",

    # 续航
    "续航{adv}{adj}，{praise}",
    "电池{adv}{adj}，{praise}",
    "待机时间{adv}{adj}，{praise}",
    "一天下来还有{percent}电，{praise}",
    "充满电可以用{time}，{praise}",
    "续航能力{adv}{adj}，{praise}",
    "正常使用{time}没问题",
    "电池耐用，{praise}",
    "耗电{adj}，{praise}",
    "电量管理{adj}，{praise}",

    # 充电
    "充电速度{adv}{adj}，{praise}",
    "快充{adv}{adj}，{praise}",
    "充满电只要{time}，{praise}",
    "无线充电{adj}，{praise}",
    "充电{time}就能用{time2}，{praise}",

    # 系统功能
    "系统功能{adj}，{praise}",
    "{feature}功能{adv}{adj}，{praise}",
    "系统优化{adv}{adj}，{praise}",
    "UI设计{adj}，{praise}",
    "操作{adj}，{praise}",
    "系统流畅度{adv}{adj}，{praise}",
    "功能{adj}，{praise}",
    "系统体验{adj}，{praise}",
    "界面{adj}，{praise}",

    # 音质
    "音质{adv}{adj}，{praise}",
    "外放声音{adv}{adj}，{praise}",
    "低音{adj}，高音{adj2}",
    "通话质量{adj}，{praise}",
    "耳机音质{adj}，{praise}",
    "喇叭{adj}，{praise}",
    "声音效果{adj}，{praise}",

    # 物流服务
    "物流{adv}{adj}，{praise}",
    "配送速度{adv}{adj}，{praise}",
    "包装{adj}，{praise}",
    "快递{adv}{adj}，{praise}",
    "发货速度{adj}，{praise}",
    "送货上门服务{adj}，{praise}",

    # 综合
    "性价比{adv}{adj}，{praise}",
    "总体来说{adv}{adj}，{praise}",
    "{product}非常值得购买，{praise}",
    "整体体验{adv}{adj}，{praise}",
    "对比同价位产品{adv}{adj}，{praise}",
    "用了{time}感觉{adj}，{praise}",
    "给家人买的，{praise}",
    "朋友推荐的，{praise}",
    "第二次购买了，{praise}",
    "比预期好{adv}，{praise}",
    "这个价格买到{adj}，{praise}",
    "质量{adj}，{praise}",
    "使用体验{adj}，{praise}",
    "总体满意，{praise}",
]

# 负面评价模板
NEGATIVE_TEMPLATES = [
    # 外观设计
    "外观设计{adj}，{complaint}",
    "做工{adj}，{complaint}",
    "手感{adv}{adj}，{complaint}",
    "手机{adj}，拿着{adv}不舒服",
    "边框{adj}，{complaint}",
    "后盖{adj}，{complaint}",

    # 屏幕
    "屏幕{adj}，{complaint}",
    "屏幕亮度{adv}{adj}，{complaint}",
    "屏幕{adj}，{complaint}",
    "屏幕有{problem}，{complaint}",
    "显示效果{adj}，{complaint}",
    "屏幕发{color}，{complaint}",
    "阳光下看不清屏幕，{complaint}",
    "屏幕触控{adj}，{complaint}",

    # 拍照
    "拍照效果{adv}{adj}，{complaint}",
    "相机{adj}，{complaint}",
    "前置摄像头{adj}，{complaint}",
    "夜景模式{adj}，{complaint}",
    "拍照{adj}，{complaint}",
    "视频拍摄{adj}，{complaint}",
    "像素{adv}{adj}，{complaint}",
    "防抖{adj}，{complaint}",
    "对焦速度{adj}，{complaint}",

    # 性能
    "运行{adv}{adj}，{complaint}",
    "系统{adj}，{complaint}",
    "经常{problem}，{complaint}",
    "玩游戏{adj}，{complaint}",
    "手机{adv}{adj}，{complaint}",
    "用了一段时间就开始{problem}，{complaint}",
    "开多个应用就会{problem}，{complaint}",
    "系统更新后{problem}，{complaint}",

    # 续航
    "续航{adv}{adj}，{complaint}",
    "电池{adv}{adj}，{complaint}",
    "一天要充{time}次电，{complaint}",
    "待机时间{adv}{adj}，{complaint}",
    "掉电{adv}{adj}，{complaint}",
    "电池健康度下降{adj}，{complaint}",

    # 充电
    "充电速度{adv}{adj}，{complaint}",
    "充满电要{time}，{complaint}",
    "充电接口{problem}，{complaint}",
    "充电时{problem}，{complaint}",
    "无线充电{adj}，{complaint}",
    "充电发热{adj}，{complaint}",

    # 发热
    "手机发热{adj}，{complaint}",
    "玩游戏时机身{adj}，{complaint}",
    "充电时{adj}，{complaint}",
    "散热效果{adj}，{complaint}",
    "看视频都{adj}，{complaint}",

    # 系统问题
    "系统{problem}，{complaint}",
    "广告推送{adv}{adj}，{complaint}",
    "预装软件{adj}，{complaint}",
    "系统bug{adj}，{complaint}",
    "通知{adj}，{complaint}",
    "系统优化{adj}，{complaint}",
    "手机经常{problem}，{complaint}",

    # 综合
    "性价比{adv}{adj}，{complaint}",
    "总体来说{adv}{adj}，{complaint}",
    "后悔买了，{complaint}",
    "这个价格{adj}，{complaint}",
    "用了{time}就{problem}，{complaint}",
    "物流{adj}，{complaint}",
    "客服{adj}，{complaint}",
    "售后{adj}，{complaint}",
    "配件{adj}，{complaint}",
    "包装{adj}，{complaint}",
    "信号{adj}，{complaint}",
    "GPS定位{adj}，{complaint}",
    "指纹识别{adj}，{complaint}",
    "人脸识别{adj}，{complaint}",
    "NFC功能{adj}，{complaint}",
]

# ============================================================
# 词库
# ============================================================

POSITIVE_ADJ = [
    "很棒", "很好", "不错", "非常好", "出色", "一流", "惊艳",
    "完美", "优秀", "给力", "满意", "没话说", "无可挑剔",
    "超预期", "杠杠的", "一级棒", "相当好", "特别好", "真心好",
    "绝了", "太赞了", "没毛病", "满分", "极好",
]

NEGATIVE_ADJ = [
    "很差", "不好", "一般", "非常差", "糟糕", "垃圾", "不行",
    "太烂", "不满意", "很一般", "差劲", "令人失望", "不值",
    "太次了", "不咋地", "很垃圾", "不好用", "有问题", "不够好",
    "太差了", "很糟糕", "太让人失望了", "真的很差",
]

POSITIVE_PRAISE = [
    "非常满意", "值得推荐", "爱了爱了", "强烈推荐", "效果杠杠的",
    "体验很好", "真心不错", "物超所值", "没让人失望", "推荐购买",
    "性价比超高", "用起来很爽", "一次愉快的购物", "还会回购",
    "太好用了", "效果超出预期", "真的没话说", "值得拥有",
]

NEGATIVE_COMPLAINT = [
    "非常后悔", "建议大家谨慎购买", "踩雷了", "不如预期",
    "这个价格不值", "不会再买了", "太让人失望了", "影响心情",
    "希望大家避坑", "真的踩坑了", "不建议购买", "很影响使用体验",
    "想退货", "完全不推荐", "浪费时间金钱", "真的受不了",
]

PRODUCT_NAMES = [
    "这手机", "这款", "这个", "", "这个产品",
]

FEATURES_POS = [
    "指纹解锁", "人脸识别", "NFC", "无线充电", "双卡双待",
    "分屏功能", "护眼模式", "快速充电", "防水", "内存扩展",
    "语音助手", "手势操作", "暗黑模式", "省电模式",
]

FEATURES_NEG = [
    "指纹解锁", "人脸识别", "NFC", "无线充电",
    "语音助手", "手势操作",
]

TIMES = [
    "一整天", "两天", "一天半", "大半天", "七八个小时",
    "一周", "一个月", "三个月", "半年", "两个月",
]

PERCENTS = ["30%", "40%", "50%", "60%", "70%", "20%"]

PROBLEMS = [
    "死机", "卡顿", "闪退", "重启", "黑屏", "蓝屏", "自动关机",
    "卡死", "无响应", "发热", "掉帧", "断流", "断触",
]

COLORS = ["黄", "红", "绿", "蓝"]

PRODUCTS = ["手机", "耳机", "笔记本", "平板", "手表"]

def pick(lst):
    return random.choice(lst)

def fill_template(template, is_positive):
    """填充模板生成一条评论"""
    kwargs = {}
    if is_positive:
        kwargs["adj"] = pick(POSITIVE_ADJ)
        kwargs["adj2"] = pick(POSITIVE_ADJ)
        kwargs["adv"] = pick(["非常", "相当", "十分", "特别", "真的", "确实", "很", ""])
        kwargs["praise"] = pick(POSITIVE_PRAISE)
        kwargs["feature"] = pick(FEATURES_POS)
        kwargs["product"] = pick(PRODUCT_NAMES)
        kwargs["time"] = pick(TIMES)
        kwargs["time2"] = pick(TIMES)
        kwargs["percent"] = pick(PERCENTS)
    else:
        kwargs["adj"] = pick(NEGATIVE_ADJ)
        kwargs["adj2"] = pick(NEGATIVE_ADJ)
        kwargs["adv"] = pick(["非常", "相当", "十分", "特别", "真的", "确实", "很", "太", "有点", "有些"])
        kwargs["complaint"] = pick(NEGATIVE_COMPLAINT)
        kwargs["problem"] = pick(PROBLEMS)
        kwargs["feature"] = pick(FEATURES_NEG)
        kwargs["product"] = pick(PRODUCT_NAMES)
        kwargs["color"] = pick(COLORS)
        kwargs["time"] = pick(TIMES)
        kwargs["percent"] = pick(PERCENTS)
        kwargs["time2"] = pick(TIMES)

    text = template.format(**kwargs)
    # 清理多余空格标点
    text = text.replace("  ", "").replace("，，", "，").replace("。。", "。").replace("！！", "！").replace("？？", "？")
    return text


def generate_reviews(count=3000):
    """生成指定数量的评论"""
    reviews = []
    # 半正半负
    half = count // 2

    for _ in range(half):
        template = pick(POSITIVE_TEMPLATES)
        text = fill_template(template, True)
        reviews.append((text, 1))

    for _ in range(half):
        template = pick(NEGATIVE_TEMPLATES)
        text = fill_template(template, False)
        reviews.append((text, 0))

    random.shuffle(reviews)
    return reviews


def main():
    print("=" * 60)
    print("📊 情感分析训练数据生成器")
    print("=" * 60)

    # 生成5000条
    reviews = generate_reviews(5000)

    # 保留原来101条并混入
    original_path = OUTPUT_PATH.replace('.txt', '_original.txt')
    if os.path.exists(OUTPUT_PATH):
        os.rename(OUTPUT_PATH, original_path)
        with open(original_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    reviews.append((line.rsplit('|', 1)[0], int(line.rsplit('|', 1)[1])))
        print(f"📥 已合并 {len(reviews) - 5000} 条原始数据")

    # 去重
    seen = set()
    unique_reviews = []
    for text, label in reviews:
        if text not in seen:
            seen.add(text)
            unique_reviews.append((text, label))

    # 写入文件
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        for text, label in unique_reviews:
            f.write(f"{text}|{label}\n")

    pos_count = sum(1 for _, l in unique_reviews if l == 1)
    neg_count = sum(1 for _, l in unique_reviews if l == 0)

    print(f"\n📈 生成统计:")
    print(f"  正面评论: {pos_count} 条")
    print(f"  负面评论: {neg_count} 条")
    print(f"  总  计: {len(unique_reviews)} 条 (去重后)")
    print(f"  去重: {len(reviews) - len(unique_reviews)} 条")
    print(f"\n📁 输出文件: {OUTPUT_PATH}")
    print()

    # 打印示例
    print("📝 示例评论:")
    for i, (text, label) in enumerate(unique_reviews[:5]):
        sentiment = "正面 👍" if label == 1 else "负面 👎"
        print(f"  [{sentiment}] {text}")
    print()

    # 清理备份
    if os.path.exists(original_path):
        os.remove(original_path)
        print("🧹 临时文件已清理")


if __name__ == "__main__":
    main()
