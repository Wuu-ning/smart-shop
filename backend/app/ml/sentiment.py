"""
情感分析模型封装 - 供FastAPI后端调用
提供：单条预测、词云生成
"""
import os
import io
import base64
import jieba
import joblib
import numpy as np
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'vectorizer.pkl')

# 全局变量，延迟加载
_model = None
_vectorizer = None
_stopwords = None


def load_stopwords():
    """加载停用词表（缓存）"""
    global _stopwords
    if _stopwords is None:
        _stopwords = set()
        path = os.path.join(DATA_DIR, 'stopwords.txt')
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word:
                    _stopwords.add(word)
    return _stopwords


def load_model():
    """加载模型和向量器（延迟加载，缓存）"""
    global _model, _vectorizer
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    if _vectorizer is None:
        _vectorizer = joblib.load(VECTORIZER_PATH)
    return _model, _vectorizer


def tokenize(text):
    """jieba分词 + 去停用词"""
    stopwords = load_stopwords()
    words = jieba.cut(text)
    return ' '.join([w for w in words if w.strip() and w not in stopwords])


def predict_sentiment(text):
    """
    预测单条评论情感
    
    Args:
        text: 评论文本
        
    Returns:
        dict: {sentiment: 正面/负面, label: 1/0, confidence: 置信度}
    """
    model, vectorizer = load_model()
    processed = tokenize(text)
    vec = vectorizer.transform([processed])
    pred = model.predict(vec)[0]
    proba = model.predict_proba(vec)[0]
    
    return {
        'sentiment': '正面' if pred == 1 else '负面',
        'label': int(pred),
        'confidence': float(proba[pred]),
        'prob_positive': float(proba[1]),
        'prob_negative': float(proba[0]),
    }


def generate_wordcloud():
    """
    生成正面和负面评论的词云，返回base64编码的图片
    
    Returns:
        dict: {positive_wordcloud: base64, negative_wordcloud: base64}
    """
    model, vectorizer = load_model()
    stopwords = load_stopwords()
    
    # 加载原始评论数据
    reviews_path = os.path.join(DATA_DIR, 'phone_reviews.txt')
    positive_texts = []
    negative_texts = []
    
    with open(reviews_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.rsplit('|', 1)
            if len(parts) == 2:
                text, label = parts[0], int(parts[1])
                if label == 1:
                    positive_texts.append(text)
                else:
                    negative_texts.append(text)
    
    # 分词去停用词
    def process_texts(texts):
        words = []
        for text in texts:
            seg_list = jieba.cut(text)
            for w in seg_list:
                if w.strip() and w not in stopwords and len(w) > 1:
                    words.append(w)
        return ' '.join(words)
    
    pos_text = process_texts(positive_texts)
    neg_text = process_texts(negative_texts)
    
    # 配置中文字体
    font_path = None
    # 尝试常见的中文字体路径
    possible_fonts = [
        'C:/Windows/Fonts/simhei.ttf',
        'C:/Windows/Fonts/msyh.ttc',
        'C:/Windows/Fonts/simsun.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
    ]
    for fp in possible_fonts:
        if os.path.exists(fp):
            font_path = fp
            break
    
    def make_wordcloud(text, title, color):
        wc = WordCloud(
            font_path=font_path,
            width=800,
            height=400,
            background_color='white',
            max_words=100,
            max_font_size=80,
            min_font_size=10,
            colormap=color,
            collocations=False,
            random_state=42
        )
        wc.generate(text)
        
        # 转为base64
        img_buffer = io.BytesIO()
        wc.to_image().save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        img_buffer.close()
        return img_base64
    
    result = {
        'positive_wordcloud': make_wordcloud(pos_text, '正面评论词云', 'Greens'),
        'negative_wordcloud': make_wordcloud(neg_text, '负面评论词云', 'Reds'),
        'stats': {
            'positive_count': len(positive_texts),
            'negative_count': len(negative_texts),
        }
    }
    
    return result


if __name__ == '__main__':
    # 简单测试
    print("测试情感预测:")
    test_reviews = [
        "性价比高，值得买",
        "这手机太差了，卡得要命",
    ]
    for r in test_reviews:
        result = predict_sentiment(r)
        print(f"  '{r}' → {result['sentiment']} (置信度: {result['confidence']:.2%})")
    
    print("\n生成词云...")
    wc_result = generate_wordcloud()
    print(f"  词云生成完成，正面评论{wc_result['stats']['positive_count']}条，负面{wc_result['stats']['negative_count']}条")
