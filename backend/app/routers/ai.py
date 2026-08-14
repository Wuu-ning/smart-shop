"""AI 商品描述生成"""
import random
from fastapi import APIRouter, Query

router = APIRouter(prefix="/api/ai", tags=["AI"])

# ===== 各品类描述模板 =====
DESC_TEMPLATES = {
    "手机": [
        "{name}，{features}，为您带来{adj}的使用体验。搭载{chip}处理器，配合{screen}显示屏，无论是日常使用还是大型游戏都能{performance}。{camera_desc}。内置{battery}大电池，支持{charge}快充，续航{endurance}。{extra}",
        "{name}采用{design}设计，配备{chip}旗舰芯片，{screen}超清屏幕带来{visual}视觉体验。{camera_system}摄影系统，{photo_perf}。{battery}大容量电池配合{charge}快充，{endurance}。{extra}",
    ],
    "笔记本": [
        "{name}搭载{chip}处理器，{screen}高清屏幕，性能{performance}。{design}机身设计，轻至{weight}，便携{portable}。{battery_desc}。{extra}。无论是办公还是创作，{name}都能{productivity}。",
        "{name}，{features}，专为{target}打造。{chip}处理器配合{ram}内存，{storage}存储，{performance}。{screen}屏幕{visual}。{cooling}散热系统确保{stable}。{extra}",
    ],
    "耳机": [
        "{name}采用{design}设计，{features}。搭载{chip}芯片，支持{codec}高清音频解码，音质{quality}。{noise_cancel}降噪技术，{nc_perf}。续航{endurance}，支持{charge}快充。{extra}",
        "{name}，{features}，{quality}音质表现。{noise_cancel}自适应降噪，{nc_perf}。{design}设计，佩戴{comfort}。续航{endurance}小时，{extra}",
    ],
    "平板": [
        "{name}配备{screen}大屏，{features}。{chip}处理器性能{performance}，{screen_desc}显示效果{visual}。{battery_desc}。支持{accessory}，{productivity}。{extra}",
        "{name}，{features}，{screen}屏幕{visual}。{chip}芯片{performance}，{battery}电池续航{endurance}。{extra}",
    ],
    "穿戴": [
        "{name}，{features}。搭载{chip}处理器，{screen}屏幕{visual}。支持{health_features}健康监测，{sports}运动模式。续航{endurance}，{extra}",
        "{name}采用{design}设计，{features}。{screen}显示屏{visual}，{health_features}全天候健康监测，{sports}种运动模式。电池续航{endurance}，{extra}",
    ],
    "家居": [
        "{name}，{features}。{smart_features}智能联动，支持{control}控制。{design}设计，{extra}",
        "{name}采用{design}设计，{features}。{smart_features}，可通过{control}远程操控。{extra}",
    ],
}

# ===== 词库 =====
ADJ = ["流畅卓越", "极致丝滑", "无与伦比", "非凡出色", "卓越非凡", "令人惊叹", "出类拔萃"]
PERFORMANCE = ["游刃有余", "流畅自如", "轻松应对", "毫无压力", "表现出色"]
VISUAL = ["色彩精准", "细腻逼真", "栩栩如生", "震撼逼真", "清晰锐利"]
ENDURANCE = ["持久耐用", "超长续航", "一整天无忧", "告别电量焦虑"]
COMFORT = ["舒适自在", "轻若无物", "贴合耳廓", "毫无负担"]
CAMERA_PERF = ["细节丰富", "色彩真实", "夜拍清晰", "远近皆清晰", "还原真实色彩"]
CHARGE = ["超级闪充", "无线快充", "极速充电", "快速充电"]
PRODUCTIVITY = ["事半功倍", "高效便捷", "生产力倍增", "创作得心应手"]
STABLE = ["稳定高效", "持久稳定", "冷静应对", "持续高性能"]
QUALITY = ["纯净通透", "饱满有力", "层次丰富", "高保真还原"]
NC_PERF = ["隔绝外界干扰", "沉浸音乐世界", "安静聆听每一刻", "随时随地沉浸"]
HEALTH = ["心率监测", "血氧检测", "睡眠分析", "压力监测"]
SPORTS = ["多种运动模式", "100+运动模式", "专业运动分析"]
SMART = ["智能场景联动", "全屋智能控制", "一键智能场景"]
CONTROL = ["语音控制", "手机APP远程控制", "语音和APP双控"]

# ===== 随机抽取函数 =====
def pick(lst):
    return random.choice(lst)

def generate_description(name: str, category: str, keywords: str = "") -> str:
    """根据商品名、品类和关键词生成描述"""
    
    templates = DESC_TEMPLATES.get(category, DESC_TEMPLATES["手机"])
    template = random.choice(templates)
    
    # 解析关键词
    kw_list = [k.strip() for k in keywords.split() if k.strip()] if keywords else []
    kw_str = "、".join(kw_list[:4]) if kw_list else "多项创新技术"
    
    # 填充变量
    vars_dict = {
        "name": name,
        "features": kw_str,
        "adj": pick(ADJ),
        "chip": pick(["旗舰级", "高性能", "新一代", "先进制程"]),
        "screen": pick(["6.8英寸", "6.7英寸", "6.1英寸", "高刷"]),
        "performance": pick(PERFORMANCE),
        "camera_desc": pick(["后置旗舰三摄系统", "专业影像系统", "超清多摄系统", "AI智能摄影系统"]),
        "camera_system": pick(["后置专业三摄", "旗舰影像系统", "AI三摄系统"]),
        "photo_perf": pick(CAMERA_PERF),
        "battery": pick(["5000mAh", "4800mAh", "5500mAh", "4500mAh"]),
        "charge": pick(CHARGE),
        "endurance": pick(ENDURANCE),
        "extra": pick(["是一款不容错过的优秀产品。", "是同价位中的佼佼者。", "将为您带来全新的使用体验。", ""]),
        "design": pick(["简约时尚", "精致轻薄", "高端大气", "科技感十足"]),
        "visual": pick(VISUAL),
        "weight": pick(["约1.2kg", "约1.4kg", "约1.6kg", "轻至1.0kg"]),
        "portable": pick(["出行无负担", "随身携带方便", "轻松放入背包"]),
        "battery_desc": pick(["续航持久", "电池容量大", "续航表现优异"]),
        "target": pick(["创作者", "商务人士", "游戏玩家", "学生用户"]),
        "ram": pick(["16GB", "32GB", "8GB"]),
        "storage": pick(["512GB", "1TB", "256GB"]),
        "cooling": pick(["高效散热", "液冷散热", "冰霜散热系统"]),
        "stable": pick(STABLE),
        "codec": pick(["LDAC", "AAC", "高解析度"]),
        "quality": pick(QUALITY),
        "noise_cancel": pick(["主动降噪", "自适应降噪", "智能降噪"]),
        "nc_perf": pick(NC_PERF),
        "comfort": pick(COMFORT),
        "screen_desc": pick(["绚丽清晰", "色彩准确", "亮度充足"]),
        "accessory": pick(["手写笔", "键盘", "磁吸配件"]),
        "productivity": pick(PRODUCTIVITY),
        "health_features": pick(HEALTH),
        "sports": pick(SPORTS),
        "smart_features": pick(SMART),
        "control": pick(CONTROL),
    }
    
    desc = template.format(**vars_dict)
    
    # 清理多余标点
    desc = desc.replace("。。", "。").replace("，，", "，").replace("。。", "。")
    desc = desc.strip()
    
    return desc


@router.get("/generate-description")
def generate_description_api(
    name: str = Query(..., description="商品名称"),
    category: str = Query("手机", description="商品分类"),
    keywords: str = Query("", description="关键词（空格分隔）"),
):
    """AI 商品描述生成"""
    if not name:
        return {"error": "请输入商品名称"}
    
    desc = generate_description(name, category, keywords)
    return {"description": desc, "generated_by": "AI"}
