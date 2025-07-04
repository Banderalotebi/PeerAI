# =============================================================================
# وحدة معالجة اللغة الطبيعية (NLP)
# =============================================================================

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import os
import pandas as pd
import numpy as np

class TextClassifier:
    """
    مصنف النصوص المتقدم مع دعم متعدد للخوارزميات والميزات
    """
    
    def __init__(self, model_path='models/nlp_model.pkl'):
        self.model_path = model_path
        self.pipeline = None
        self.vectorizer = None
        self.classifier = None
        self.classes = None
        
    def create_pipeline(self, vectorizer_type='tfidf', classifier_type='logistic_regression', **kwargs):
        """
        إنشاء خط أنابيب معالجة النصوص
        
        Args:
            vectorizer_type: نوع المتجه ('tfidf', 'count')
            classifier_type: نوع المصنف
            **kwargs: معاملات إضافية
        """
        
        # اختيار المتجه
        if vectorizer_type == 'tfidf':
            self.vectorizer = TfidfVectorizer(**kwargs)
        elif vectorizer_type == 'count':
            self.vectorizer = CountVectorizer(**kwargs)
        else:
            raise ValueError(f"Unknown vectorizer type: {vectorizer_type}")
        
        # اختيار المصنف
        if classifier_type == 'logistic_regression':
            self.classifier = LogisticRegression(**kwargs)
        elif classifier_type == 'naive_bayes':
            self.classifier = MultinomialNB(**kwargs)
        elif classifier_type == 'svm':
            self.classifier = SVC(**kwargs)
        elif classifier_type == 'random_forest':
            self.classifier = RandomForestClassifier(**kwargs)
        elif classifier_type == 'sgd':
            self.classifier = SGDClassifier(**kwargs)
        else:
            raise ValueError(f"Unknown classifier type: {classifier_type}")
        
        # إنشاء الخط الأنابيب
        self.pipeline = Pipeline([
            ('vectorizer', self.vectorizer),
            ('classifier', self.classifier)
        ])
        
        return self.pipeline

    def train(self, data_path, text_column, target_column, vectorizer_type='tfidf', 
              classifier_type='logistic_regression', test_size=0.2, random_state=42, **kwargs):
        """
        تدريب نموذج تصنيف النصوص
        
        Args:
            data_path: مسار ملف البيانات
            text_column: اسم عمود النصوص
            target_column: اسم عمود التصنيف
            vectorizer_type: نوع المتجه
            classifier_type: نوع المصنف
            test_size: نسبة بيانات الاختبار
            random_state: البذرة العشوائية
            **kwargs: معاملات إضافية
        """
        
        # قراءة البيانات
        data = pd.read_csv(data_path)
        X = data[text_column]
        y = data[target_column]
        
        # تقسيم البيانات
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # إنشاء الخط الأنابيب
        self.create_pipeline(vectorizer_type, classifier_type, **kwargs)
        
        # تدريب النموذج
        self.pipeline.fit(X_train, y_train)
        
        # التنبؤ والتقييم
        y_pred = self.pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # حفظ النموذج
        joblib.dump(self.pipeline, self.model_path)
        
        # حفظ المعلومات
        self.classes = list(self.pipeline.classes_)
        
        return {
            'model_path': self.model_path,
            'classes': self.classes,
            'accuracy': accuracy,
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }

    def train_with_gridsearch(self, data_path, text_column, target_column, 
                             vectorizer_type='tfidf', classifier_type='logistic_regression',
                             param_grid=None, cv=5, test_size=0.2, random_state=42):
        """
        تدريب مع البحث في الشبكة للحصول على أفضل المعاملات
        """
        
        # قراءة البيانات
        data = pd.read_csv(data_path)
        X = data[text_column]
        y = data[target_column]
        
        # تقسيم البيانات
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # إنشاء الخط الأنابيب
        self.create_pipeline(vectorizer_type, classifier_type)
        
        # معاملات البحث الافتراضية
        if param_grid is None:
            if classifier_type == 'logistic_regression':
                param_grid = {
                    'classifier__C': [0.1, 1, 10],
                    'classifier__penalty': ['l1', 'l2']
                }
            elif classifier_type == 'naive_bayes':
                param_grid = {
                    'classifier__alpha': [0.1, 1, 10]
                }
            elif classifier_type == 'svm':
                param_grid = {
                    'classifier__C': [0.1, 1, 10],
                    'classifier__kernel': ['linear', 'rbf']
                }
            elif classifier_type == 'random_forest':
                param_grid = {
                    'classifier__n_estimators': [50, 100],
                    'classifier__max_depth': [None, 10, 20]
                }
        
        # البحث في الشبكة
        grid_search = GridSearchCV(self.pipeline, param_grid, cv=cv, n_jobs=-1, scoring='accuracy')
        grid_search.fit(X_train, y_train)
        
        # أفضل نموذج
        self.pipeline = grid_search.best_estimator_
        
        # التنبؤ والتقييم
        y_pred = self.pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # حفظ النموذج
        joblib.dump(self.pipeline, self.model_path)
        
        # حفظ المعلومات
        self.classes = list(self.pipeline.classes_)
        
        return {
            'model_path': self.model_path,
            'classes': self.classes,
            'accuracy': accuracy,
            'best_params': grid_search.best_params_,
            'best_score': grid_search.best_score_,
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }

    def predict(self, texts, load_model=True):
        """
        التنبؤ بتصنيف النصوص
        
        Args:
            texts: قائمة النصوص أو نص واحد
            load_model: تحميل النموذج إذا لم يكن محملًا
        """
        
        # تحميل النموذج إذا لزم الأمر
        if self.pipeline is None and load_model:
            if os.path.exists(self.model_path):
                self.pipeline = joblib.load(self.model_path)
                self.classes = list(self.pipeline.classes_)
            else:
                raise FileNotFoundError(f"Model not found at {self.model_path}")
        
        # تحويل النص الواحد إلى قائمة
        if isinstance(texts, str):
            texts = [texts]
        
        # التنبؤ
        predictions = self.pipeline.predict(texts)
        probabilities = self.pipeline.predict_proba(texts)
        
        # تنسيق النتائج
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            result = {
                'text': texts[i],
                'prediction': pred,
                'confidence': float(max(prob)),
                'probabilities': dict(zip(self.classes, prob.tolist()))
            }
            results.append(result)
        
        return results if len(results) > 1 else results[0]

    def predict_batch(self, texts_file, output_file=None):
        """
        التنبؤ بمجموعة كبيرة من النصوص من ملف
        
        Args:
            texts_file: مسار ملف النصوص
            output_file: مسار ملف النتائج (اختياري)
        """
        
        # قراءة النصوص
        if texts_file.endswith('.csv'):
            data = pd.read_csv(texts_file)
            texts = data.iloc[:, 0].tolist()  # العمود الأول
        else:
            with open(texts_file, 'r', encoding='utf-8') as f:
                texts = [line.strip() for line in f if line.strip()]
        
        # التنبؤ
        results = self.predict(texts, load_model=True)
        
        # حفظ النتائج
        if output_file:
            df_results = pd.DataFrame(results)
            df_results.to_csv(output_file, index=False)
        
        return results

    def model_info(self):
        """معلومات عن النموذج"""
        if os.path.exists(self.model_path):
            self.pipeline = joblib.load(self.model_path)
            return {
                'model_path': self.model_path,
                'vectorizer': type(self.pipeline.named_steps['vectorizer']).__name__,
                'classifier': type(self.pipeline.named_steps['classifier']).__name__,
                'classes': list(self.pipeline.classes_),
                'n_classes': len(self.pipeline.classes_),
                'model_size_mb': os.path.getsize(self.model_path) / (1024 * 1024)
            }
        else:
            return {'error': 'Model not found'}

    def evaluate(self, test_data_path, text_column, target_column):
        """
        تقييم النموذج على بيانات اختبار جديدة
        """
        
        if self.pipeline is None:
            if os.path.exists(self.model_path):
                self.pipeline = joblib.load(self.model_path)
            else:
                raise FileNotFoundError(f"Model not found at {self.model_path}")
        
        # قراءة بيانات الاختبار
        test_data = pd.read_csv(test_data_path)
        X_test = test_data[text_column]
        y_test = test_data[target_column]
        
        # التنبؤ
        y_pred = self.pipeline.predict(X_test)
        y_prob = self.pipeline.predict_proba(X_test)
        
        # التقييم
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        conf_matrix = confusion_matrix(y_test, y_pred)
        
        return {
            'accuracy': accuracy,
            'classification_report': report,
            'confusion_matrix': conf_matrix.tolist(),
            'predictions': y_pred.tolist(),
            'probabilities': y_prob.tolist()
        }

class TextPreprocessor:
    """
    معالج النصوص المسبق
    """
    
    @staticmethod
    def clean_text(text):
        """تنظيف النص الأساسي"""
        import re
        
        # إزالة الأحرف الخاصة
        text = re.sub(r'[^\w\s]', '', text)
        
        # إزالة المسافات الزائدة
        text = re.sub(r'\s+', ' ', text)
        
        # تحويل إلى أحرف صغيرة
        text = text.lower().strip()
        
        return text
    
    @staticmethod
    def remove_stopwords(text, stopwords_list=None):
        """إزالة الكلمات الوظيفية"""
        if stopwords_list is None:
            # قائمة كلمات وظيفية عربية أساسية
            stopwords_list = [
                'في', 'من', 'إلى', 'على', 'عن', 'مع', 'هذا', 'هذه', 'ذلك', 'تلك',
                'التي', 'الذي', 'الذين', 'اللاتي', 'اللائي', 'هنا', 'هناك', 'حيث',
                'متى', 'كيف', 'لماذا', 'ما', 'من', 'أي', 'كل', 'بعض', 'أكثر', 'أقل'
            ]
        
        words = text.split()
        filtered_words = [word for word in words if word not in stopwords_list]
        return ' '.join(filtered_words)
    
    @staticmethod
    def preprocess_dataset(data_path, text_column, output_path=None, 
                          clean_text=True, remove_stopwords=True):
        """
        معالجة مجموعة بيانات كاملة
        """
        
        data = pd.read_csv(data_path)
        
        if clean_text:
            data[text_column] = data[text_column].apply(TextPreprocessor.clean_text)
        
        if remove_stopwords:
            data[text_column] = data[text_column].apply(TextPreprocessor.remove_stopwords)
        
        if output_path:
            data.to_csv(output_path, index=False)
        
        return data 