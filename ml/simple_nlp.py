# =============================================================================
# معالجة اللغات الطبيعية المبسطة
# =============================================================================

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import joblib
import os

class SimpleNLP:
    def __init__(self):
        # تصنيف النصوص
        self.vectorizer = None
        self.clf = None

    def train_text_classifier(self, texts, labels):
        """
        تدريب مصنف النصوص
        
        Args:
            texts: قائمة النصوص
            labels: قائمة التصنيفات
            
        Returns:
            المصنف المدرب
        """
        self.vectorizer = TfidfVectorizer()
        X = self.vectorizer.fit_transform(texts)
        self.clf = MultinomialNB()
        self.clf.fit(X, labels)
        return self.clf

    def predict_text_category(self, text):
        """
        التنبؤ بتصنيف النص
        
        Args:
            text: النص المراد تصنيفه
            
        Returns:
            التصنيف المتوقع
        """
        if self.clf and self.vectorizer:
            X = self.vectorizer.transform([text])
            return self.clf.predict(X)[0]
        return None

    def save_model(self, path='models/text_classifier.pkl'):
        """
        حفظ النموذج
        
        Args:
            path: مسار حفظ النموذج
        """
        if self.clf and self.vectorizer:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            joblib.dump((self.vectorizer, self.clf), path)

    def load_model(self, path='models/text_classifier.pkl'):
        """
        تحميل النموذج
        
        Args:
            path: مسار النموذج
        """
        if os.path.exists(path):
            self.vectorizer, self.clf = joblib.load(path)

    def sentiment_analysis_simple(self, text):
        """
        تحليل مشاعر بسيط للنص
        
        Args:
            text: النص المراد تحليل مشاعره
            
        Returns:
            (التصنيف, الثقة)
        """
        # تحليل بسيط للمشاعر
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'like', 'happy', 'best']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'worst', 'horrible', 'sad']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "POSITIVE", 0.8
        elif negative_count > positive_count:
            return "NEGATIVE", 0.8
        else:
            return "NEUTRAL", 0.5

    def text_to_numeric(self, text, method="tfidf", corpus=None):
        """
        تحويل النص إلى تمثيل رقمي
        
        Args:
            text: النص المراد تحويله
            method: الطريقة (tfidf أو count)
            corpus: مجموعة النصوص للتدريب
            
        Returns:
            المتجه الرقمي
        """
        if method == "tfidf":
            vectorizer = TfidfVectorizer()
        else:
            vectorizer = CountVectorizer()
        if corpus:
            vectorizer.fit(corpus)
        else:
            vectorizer.fit([text])
        vector = vectorizer.transform([text])
        return vector.toarray()

    def get_text_features(self, text):
        """
        استخراج ميزات النص
        
        Args:
            text: النص المراد استخراج ميزاته
            
        Returns:
            قاموس الميزات
        """
        words = text.split()
        
        features = {
            'length': len(text),
            'words': len(words),
            'sentences': text.count('.') + text.count('!') + text.count('?'),
            'avg_word_length': np.mean([len(word) for word in words]) if words else 0,
            'unique_words': len(set([word.lower() for word in words])),
            'uppercase_ratio': sum(1 for c in text if c.isupper()) / len(text) if text else 0,
            'digit_ratio': sum(1 for c in text if c.isdigit()) / len(text) if text else 0
        }
        
        return features

    def compare_texts(self, text1, text2, method="tfidf"):
        """
        مقارنة نصين
        
        Args:
            text1: النص الأول
            text2: النص الثاني
            method: طريقة المقارنة
            
        Returns:
            درجة التشابه
        """
        if method == "tfidf":
            vectorizer = TfidfVectorizer()
            vectors = vectorizer.fit_transform([text1, text2])
            similarity = (vectors * vectors.T).toarray()[0, 1]
            return similarity
        else:
            # مقارنة بسيطة بالكلمات المشتركة
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            return len(intersection) / len(union) if union else 0

    def generate_text_summary_report(self, text):
        """
        إنشاء تقرير شامل للنص
        
        Args:
            text: النص المراد تحليله
            
        Returns:
            التقرير الشامل
        """
        report = {
            'text_length': len(text),
            'sentiment': self.sentiment_analysis_simple(text),
            'features': self.get_text_features(text),
            'summary': text[:100] + "..." if len(text) > 100 else text
        }
        
        return report 