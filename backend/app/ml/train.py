"""
训练脚本：jieba分词 → 去停用词 → CountVectorizer → MultinomialNB → 保存模型
"""
import os
import jieba
import joblib
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'vectorizer.pkl')


def load_stopwords(path):
    """加载停用词表"""
    stopwords = set()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            if word:
                stopwords.add(word)
    return stopwords


def load_reviews(path):
    """加载评论数据，返回(评论列表, 标签列表)"""
    texts = []
    labels = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # 格式：评论内容|标签
            parts = line.rsplit('|', 1)
            if len(parts) == 2:
                texts.append(parts[0])
                labels.append(int(parts[1]))
    return texts, labels


def tokenize(text, stopwords):
    """jieba分词 + 去停用词"""
    words = jieba.cut(text)
    return ' '.join([w for w in words if w.strip() and w not in stopwords])


def main():
    print("=" * 50)
    print("购物平台评论情感分析 - 模型训练")
    print("=" * 50)

    # 1. 加载数据
    print("\n[1/5] 加载评论数据...")
    reviews_path = os.path.join(DATA_DIR, 'phone_reviews.txt')
    stopwords_path = os.path.join(DATA_DIR, 'stopwords.txt')
    texts, labels = load_reviews(reviews_path)
    stopwords = load_stopwords(stopwords_path)
    print(f"  共加载 {len(texts)} 条评论，其中正面 {sum(labels)} 条，负面 {len(labels) - sum(labels)} 条")
    print(f"  停用词表共 {len(stopwords)} 个词")

    # 2. 分词预处理
    print("\n[2/5] jieba分词 + 去停用词...")
    processed_texts = []
    for text in texts:
        processed_texts.append(tokenize(text, stopwords))
    print(f"  示例（原句 → 分词后）：")
    print(f"  原句: {texts[0]}")
    print(f"  分词: {processed_texts[0]}")

    # 3. CountVectorizer词袋向量化
    print("\n[3/5] CountVectorizer词袋向量化...")
    vectorizer = CountVectorizer(max_features=1500)
    X = vectorizer.fit_transform(processed_texts)
    y = np.array(labels)
    print(f"  词汇表大小: {len(vectorizer.get_feature_names_out())}")
    print(f"  向量矩阵形状: {X.shape}")

    # 4. 训练朴素贝叶斯
    print("\n[4/5] 训练 MultinomialNB 模型...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = MultinomialNB(alpha=0.3)
    model.fit(X_train, y_train)

    # 评估
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n  测试集准确率: {accuracy:.2%}")
    print("\n  分类报告:")
    print(classification_report(y_test, y_pred, target_names=['负面(0)', '正面(1)']))

    # 5. 保存模型
    print("\n[5/5] 保存模型...")
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"  模型已保存到: {MODEL_PATH}")
    print(f"  向量器已保存到: {VECTORIZER_PATH}")

    # 测试预测
    print("\n" + "=" * 50)
    print("测试预测示例")
    print("=" * 50)
    test_reviews = [
        "性价比高，值得买",
        "这手机太差了，卡得要命",
        "屏幕清晰，拍照效果很好",
        "电池一天都撑不住，续航太烂了",
    ]
    for review in test_reviews:
        processed = tokenize(review, stopwords)
        vec = vectorizer.transform([processed])
        pred = model.predict(vec)[0]
        proba = model.predict_proba(vec)[0]
        sentiment = "正面 👍" if pred == 1 else "负面 👎"
        print(f"  「{review}」 → {sentiment} (置信度: {proba[pred]:.2%})")

    print("\n训练完成！")


if __name__ == '__main__':
    main()
