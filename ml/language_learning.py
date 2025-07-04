# =============================================================================
# معالجة اللغات الطبيعية المتقدمة
# =============================================================================

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from transformers import pipeline, AutoTokenizer, AutoModel, AutoModelForSequenceClassification
import spacy
import numpy as np
import torch
import joblib
import os

class LanguageLearning:
    def __init__(self):
        # تصنيف النصوص
        self.vectorizer = None
        self.clf = None

        # تحليل المشاعر
        try:
            self.sentiment_analyzer = pipeline("sentiment-analysis")
        except:
            self.sentiment_analyzer = None

        # استخراج الكيانات
        try:
            self.ner_tagger = pipeline("ner", aggregation_strategy="simple")
        except:
            self.ner_tagger = None

        # نماذج spaCy
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            self.nlp = spacy.blank("en")

        # تمثيل BERT و GPT
        self.tokenizer_bert = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.model_bert = AutoModel.from_pretrained("bert-base-uncased")

        self.tokenizer_gpt = AutoTokenizer.from_pretrained("gpt2")
        self.model_gpt = AutoModel.from_pretrained("gpt2")

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

    def sentiment_analysis(self, text):
        """
        تحليل مشاعر النص
        
        Args:
            text: النص المراد تحليل مشاعره
            
        Returns:
            (التصنيف, الثقة)
        """
        if self.sentiment_analyzer is None:
            return "NEUTRAL", 0.5
        try:
            result = self.sentiment_analyzer(text)[0]
            return result['label'], result['score']
        except:
            return "NEUTRAL", 0.5

    def extract_entities(self, text):
        """
        استخراج الكيانات باستخدام Transformers
        
        Args:
            text: النص المراد استخراج الكيانات منه
            
        Returns:
            قائمة الكيانات
        """
        if self.ner_tagger is None:
            return []
        try:
            return self.ner_tagger(text)
        except:
            return []

    def extract_entities_spacy(self, text):
        """
        استخراج الكيانات باستخدام spaCy
        
        Args:
            text: النص المراد استخراج الكيانات منه
            
        Returns:
            قائمة الكيانات
        """
        doc = self.nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]

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

    def get_bert_embeddings(self, text):
        """
        الحصول على تمثيل BERT للنص
        
        Args:
            text: النص المراد تمثيله
            
        Returns:
            متجه التمثيل
        """
        inputs = self.tokenizer_bert(text, return_tensors="pt", truncation=True, padding=True)
        outputs = self.model_bert(**inputs)
        emb = outputs.last_hidden_state[:, 0, :]
        return emb.squeeze().detach().cpu().numpy()

    def get_gpt_embeddings(self, text):
        """
        الحصول على تمثيل GPT للنص
        
        Args:
            text: النص المراد تمثيله
            
        Returns:
            متجه التمثيل
        """
        inputs = self.tokenizer_gpt(text, return_tensors="pt", truncation=True, padding=True)
        outputs = self.model_gpt(**inputs)
        last_hidden = outputs.last_hidden_state
        emb = last_hidden.mean(dim=1)
        return emb.squeeze().detach().cpu().numpy()

    def classify_with_bert(self, text, model_name="nlptown/bert-base-multilingual-uncased-sentiment"):
        """
        تصنيف النص باستخدام BERT
        
        Args:
            text: النص المراد تصنيفه
            model_name: اسم النموذج
            
        Returns:
            نتيجة التصنيف
        """
        clf = pipeline("sentiment-analysis", model=model_name)
        return clf(text)

    def summarize_text(self, text, max_length=130):
        """
        تلخيص النص
        
        Args:
            text: النص المراد تلخيصه
            max_length: الحد الأقصى لطول الملخص
            
        Returns:
            النص الملخص
        """
        summarizer = pipeline("summarization")
        return summarizer(text, max_length=max_length, min_length=30, do_sample=False)[0]['summary_text']

    def translate_text(self, text, model_name="Helsinki-NLP/opus-mt-en-ar"):
        """
        ترجمة النص
        
        Args:
            text: النص المراد ترجمته
            model_name: اسم نموذج الترجمة
            
        Returns:
            النص المترجم
        """
        translator = pipeline("translation_en_to_ar", model=model_name)
        return translator(text)[0]['translation_text']

    def get_text_features(self, text):
        """
        استخراج ميزات النص
        
        Args:
            text: النص المراد استخراج ميزاته
            
        Returns:
            قاموس الميزات
        """
        doc = self.nlp(text)
        
        features = {
            'length': len(text),
            'words': len(doc),
            'sentences': len(list(doc.sents)),
            'entities': len(doc.ents),
            'noun_chunks': len(list(doc.noun_chunks)),
            'verbs': len([token for token in doc if token.pos_ == 'VERB']),
            'adjectives': len([token for token in doc if token.pos_ == 'ADJ']),
            'avg_word_length': np.mean([len(token.text) for token in doc]),
            'unique_words': len(set([token.text.lower() for token in doc]))
        }
        
        return features

    def compare_texts(self, text1, text2, method="cosine"):
        """
        مقارنة نصين
        
        Args:
            text1: النص الأول
            text2: النص الثاني
            method: طريقة المقارنة
            
        Returns:
            درجة التشابه
        """
        if method == "cosine":
            vec1 = self.get_bert_embeddings(text1)
            vec2 = self.get_bert_embeddings(text2)
            similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
            return similarity
        elif method == "tfidf":
            vectorizer = TfidfVectorizer()
            vectors = vectorizer.fit_transform([text1, text2])
            similarity = (vectors * vectors.T).A[0, 1]
            return similarity
        else:
            raise ValueError("Method not supported")

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
            'sentiment': self.sentiment_analysis(text),
            'entities': self.extract_entities(text),
            'features': self.get_text_features(text),
            'summary': self.summarize_text(text) if len(text) > 100 else text
        }
        
        return report 