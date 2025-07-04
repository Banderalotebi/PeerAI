#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار شامل لنظام التعلم الآلي - الإصدار 2.0
يشمل اختبارات الخوارزميات الأساسية ومعالجة اللغة الطبيعية
"""

import requests
import json
import time
import os
from datetime import datetime

# إعدادات الخادم
BASE_URL = "http://localhost:5000"
TIMEOUT = 30

def print_header(title):
    """طباعة عنوان الاختبار"""
    print("\n" + "="*60)
    print(f"🧪 {title}")
    print("="*60)

def print_success(message):
    """طباعة رسالة نجاح"""
    print(f"✅ {message}")

def print_error(message):
    """طباعة رسالة خطأ"""
    print(f"❌ {message}")

def print_info(message):
    """طباعة رسالة معلومات"""
    print(f"ℹ️  {message}")

def test_server_health():
    """اختبار حالة الخادم"""
    print_header("اختبار حالة الخادم")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print_success(f"الخادم يعمل بشكل صحيح - الإصدار: {data.get('version', 'غير محدد')}")
            return True
        else:
            print_error(f"الخادم لا يستجيب - رمز الحالة: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"لا يمكن الاتصال بالخادم: {e}")
        return False

def test_algorithms_endpoint():
    """اختبار نقطة نهاية الخوارزميات"""
    print_header("اختبار عرض الخوارزميات المتاحة")
    
    try:
        response = requests.get(f"{BASE_URL}/algorithms", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            algorithms = data.get('algorithms', {})
            
            print_success("تم جلب الخوارزميات بنجاح")
            print_info(f"خوارزميات التصنيف: {len(algorithms.get('classification', []))}")
            print_info(f"خوارزميات الانحدار: {len(algorithms.get('regression', []))}")
            print_info(f"خوارزميات التجميع: {len(algorithms.get('clustering', []))}")
            
            # عرض بعض الخوارزميات
            print("\n📋 أمثلة على الخوارزميات:")
            for task_type, algos in algorithms.items():
                print(f"\n{task_type.upper()}:")
                for i, algo in enumerate(algos[:5]):  # أول 5 خوارزميات فقط
                    print(f"  {i+1}. {algo}")
                if len(algos) > 5:
                    print(f"  ... و {len(algos)-5} خوارزميات أخرى")
            
            return True
        else:
            print_error(f"فشل في جلب الخوارزميات - رمز الحالة: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"خطأ في الاتصال: {e}")
        return False

def test_classification_training():
    """اختبار تدريب نموذج تصنيف"""
    print_header("اختبار تدريب نموذج التصنيف")
    
    # بيانات التدريب
    train_data = {
        "data_path": "sample_data/iris.csv",
        "target": "species",
        "algorithm": "random_forest",
        "task_type": "classification",
        "test_size": 0.2,
        "random_state": 42,
        "parameters": {
            "n_estimators": 50,
            "max_depth": 5
        }
    }
    
    try:
        print_info("بدء تدريب نموذج الغابة العشوائية...")
        response = requests.post(f"{BASE_URL}/train", json=train_data, timeout=TIMEOUT*2)
        
        if response.status_code == 200:
            result = response.json()
            print_success("تم تدريب النموذج بنجاح")
            print_info(f"مسار النموذج: {result.get('model_path')}")
            print_info(f"الخوارزمية: {result.get('algorithm')}")
            
            # عرض نتائج التقييم
            evaluation = result.get('evaluation', {})
            if 'accuracy' in evaluation:
                print_info(f"الدقة: {evaluation['accuracy']:.4f}")
            
            return result.get('model_path')
        else:
            print_error(f"فشل في تدريب النموذج - رمز الحالة: {response.status_code}")
            print_error(f"الخطأ: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print_error(f"خطأ في الاتصال: {e}")
        return None

def test_regression_training():
    """اختبار تدريب نموذج انحدار"""
    print_header("اختبار تدريب نموذج الانحدار")
    
    # بيانات التدريب
    train_data = {
        "data_path": "sample_data/boston.csv",
        "target": "medv",
        "algorithm": "linear_regression",
        "task_type": "regression",
        "test_size": 0.2,
        "random_state": 42
    }
    
    try:
        print_info("بدء تدريب نموذج الانحدار الخطي...")
        response = requests.post(f"{BASE_URL}/train", json=train_data, timeout=TIMEOUT*2)
        
        if response.status_code == 200:
            result = response.json()
            print_success("تم تدريب النموذج بنجاح")
            print_info(f"مسار النموذج: {result.get('model_path')}")
            print_info(f"الخوارزمية: {result.get('algorithm')}")
            
            # عرض نتائج التقييم
            evaluation = result.get('evaluation', {})
            if 'r2_score' in evaluation:
                print_info(f"معامل التحديد (R²): {evaluation['r2_score']:.4f}")
            if 'mean_squared_error' in evaluation:
                print_info(f"متوسط مربع الخطأ: {evaluation['mean_squared_error']:.4f}")
            
            return result.get('model_path')
        else:
            print_error(f"فشل في تدريب النموذج - رمز الحالة: {response.status_code}")
            print_error(f"الخطأ: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print_error(f"خطأ في الاتصال: {e}")
        return None

def test_clustering_training():
    """اختبار تدريب نموذج تجميع"""
    print_header("اختبار تدريب نموذج التجميع")
    
    # بيانات التدريب
    train_data = {
        "data_path": "sample_data/iris.csv",
        "algorithm": "kmeans",
        "task_type": "clustering",
        "parameters": {
            "n_clusters": 3,
            "random_state": 42
        }
    }
    
    try:
        print_info("بدء تدريب نموذج K-means...")
        response = requests.post(f"{BASE_URL}/train", json=train_data, timeout=TIMEOUT*2)
        
        if response.status_code == 200:
            result = response.json()
            print_success("تم تدريب النموذج بنجاح")
            print_info(f"مسار النموذج: {result.get('model_path')}")
            print_info(f"الخوارزمية: {result.get('algorithm')}")
            
            return result.get('model_path')
        else:
            print_error(f"فشل في تدريب النموذج - رمز الحالة: {response.status_code}")
            print_error(f"الخطأ: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print_error(f"خطأ في الاتصال: {e}")
        return None

def test_prediction(model_path, task_type="classification"):
    """اختبار التنبؤ"""
    print_header(f"اختبار التنبؤ ({task_type})")
    
    if not model_path:
        print_error("لا يوجد نموذج للتنبؤ")
        return False
    
    # بيانات التنبؤ
    if task_type == "classification":
        features = [[5.1, 3.5, 1.4, 0.2], [6.2, 3.4, 5.4, 2.3]]
    elif task_type == "regression":
        features = [[0.00632, 18.0, 2.31, 0, 0.538, 6.575, 65.2, 4.09, 1, 296, 15.3, 396.9, 4.98]]
    else:
        features = [[5.1, 3.5, 1.4, 0.2], [6.2, 3.4, 5.4, 2.3]]
    
    predict_data = {
        "model_path": model_path,
        "features": features
    }
    
    try:
        print_info("بدء التنبؤ...")
        response = requests.post(f"{BASE_URL}/predict", json=predict_data, timeout=TIMEOUT)
        
        if response.status_code == 200:
            result = response.json()
            print_success("تم التنبؤ بنجاح")
            print_info(f"التنبؤات: {result.get('predictions')}")
            return True
        else:
            print_error(f"فشل في التنبؤ - رمز الحالة: {response.status_code}")
            print_error(f"الخطأ: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"خطأ في الاتصال: {e}")
        return False

def test_nlp_training():
    """اختبار تدريب نموذج NLP"""
    print_header("اختبار تدريب نموذج معالجة اللغة الطبيعية")
    
    # بيانات التدريب
    train_data = {
        "data_path": "sample_data/text_data.csv",
        "text_column": "text",
        "target_column": "label",
        "vectorizer_type": "tfidf",
        "classifier_type": "logistic_regression",
        "use_gridsearch": False,
        "test_size": 0.2,
        "random_state": 42
    }
    
    try:
        print_info("بدء تدريب نموذج تصنيف النصوص...")
        response = requests.post(f"{BASE_URL}/nlp/train", json=train_data, timeout=TIMEOUT*3)
        
        if response.status_code == 200:
            result = response.json()
            print_success("تم تدريب نموذج NLP بنجاح")
            print_info(f"مسار النموذج: {result.get('model_path')}")
            print_info(f"نوع المتجه: {result.get('vectorizer_type')}")
            print_info(f"نوع المصنف: {result.get('classifier_type')}")
            print_info(f"الدقة: {result.get('accuracy', 0):.4f}")
            print_info(f"الفئات: {result.get('classes')}")
            
            return result.get('model_path')
        else:
            print_error(f"فشل في تدريب نموذج NLP - رمز الحالة: {response.status_code}")
            print_error(f"الخطأ: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print_error(f"خطأ في الاتصال: {e}")
        return None

def test_nlp_prediction(model_path):
    """اختبار التنبؤ بـ NLP"""
    print_header("اختبار التنبؤ بـ NLP")
    
    if not model_path:
        print_error("لا يوجد نموذج NLP للتنبؤ")
        return False
    
    # نصوص للتنبؤ
    texts = [
        "هذا المنتج ممتاز جدا",
        "أنا غير راضي بالمرة",
        "منتج عادي لا أكثر",
        "خدمة عملاء ممتازة",
        "توصيل بطيء وغير منظم"
    ]
    
    predict_data = {
        "texts": texts,
        "model_path": model_path
    }
    
    try:
        print_info("بدء التنبؤ بتصنيف النصوص...")
        response = requests.post(f"{BASE_URL}/nlp/predict", json=predict_data, timeout=TIMEOUT)
        
        if response.status_code == 200:
            result = response.json()
            print_success("تم التنبؤ بـ NLP بنجاح")
            
            # عرض النتائج
            results = result.get('results', [])
            print("\n📋 نتائج التنبؤ:")
            for i, res in enumerate(results):
                print(f"  {i+1}. النص: {res.get('text', '')[:30]}...")
                print(f"     التصنيف: {res.get('prediction', '')}")
                print(f"     الثقة: {res.get('confidence', 0):.4f}")
                print()
            
            return True
        else:
            print_error(f"فشل في التنبؤ بـ NLP - رمز الحالة: {response.status_code}")
            print_error(f"الخطأ: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"خطأ في الاتصال: {e}")
        return False

def test_nlp_preprocessing():
    """اختبار معالجة النصوص مسبقًا"""
    print_header("اختبار معالجة النصوص مسبقًا")
    
    # بيانات المعالجة
    preprocess_data = {
        "data_path": "sample_data/text_data.csv",
        "text_column": "text",
        "output_path": "sample_data/processed_text_data.csv",
        "clean_text": True,
        "remove_stopwords": True
    }
    
    try:
        print_info("بدء معالجة النصوص...")
        response = requests.post(f"{BASE_URL}/nlp/preprocess", json=preprocess_data, timeout=TIMEOUT*2)
        
        if response.status_code == 200:
            result = response.json()
            print_success("تم معالجة النصوص بنجاح")
            print_info(f"عدد الصفوف المعالجة: {result.get('rows_processed')}")
            print_info(f"مسار الملف المعالج: {result.get('output_path')}")
            return True
        else:
            print_error(f"فشل في معالجة النصوص - رمز الحالة: {response.status_code}")
            print_error(f"الخطأ: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"خطأ في الاتصال: {e}")
        return False

def test_nlp_model_info(model_path):
    """اختبار معلومات نموذج NLP"""
    print_header("اختبار معلومات نموذج NLP")
    
    if not model_path:
        print_error("لا يوجد نموذج NLP")
        return False
    
    try:
        print_info("جلب معلومات النموذج...")
        response = requests.get(f"{BASE_URL}/nlp/model_info?model_path={model_path}", timeout=TIMEOUT)
        
        if response.status_code == 200:
            result = response.json()
            print_success("تم جلب معلومات النموذج بنجاح")
            print_info(f"المتجه: {result.get('vectorizer')}")
            print_info(f"المصنف: {result.get('classifier')}")
            print_info(f"عدد الفئات: {result.get('n_classes')}")
            print_info(f"حجم النموذج: {result.get('model_size_mb', 0):.2f} MB")
            return True
        else:
            print_error(f"فشل في جلب معلومات النموذج - رمز الحالة: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"خطأ في الاتصال: {e}")
        return False

def test_list_models():
    """اختبار قائمة النماذج"""
    print_header("اختبار قائمة النماذج المحفوظة")
    
    try:
        response = requests.get(f"{BASE_URL}/list_models", timeout=TIMEOUT)
        if response.status_code == 200:
            result = response.json()
            models = result.get('models', [])
            print_success(f"تم العثور على {len(models)} نموذج")
            
            if models:
                print("\n📋 النماذج المحفوظة:")
                for i, model in enumerate(models[:10]):  # أول 10 نماذج فقط
                    print(f"  {i+1}. {model}")
                if len(models) > 10:
                    print(f"  ... و {len(models)-10} نموذج آخر")
            
            return True
        else:
            print_error(f"فشل في جلب قائمة النماذج - رمز الحالة: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"خطأ في الاتصال: {e}")
        return False

def run_comprehensive_test():
    """تشغيل الاختبار الشامل"""
    print_header("بدء الاختبار الشامل لنظام التعلم الآلي - الإصدار 2.0")
    print(f"⏰ وقت البدء: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # نتائج الاختبارات
    test_results = {}
    
    # 1. اختبار حالة الخادم
    test_results['server_health'] = test_server_health()
    if not test_results['server_health']:
        print_error("فشل في اختبار حالة الخادم. تأكد من تشغيل الخادم أولاً.")
        return
    
    # 2. اختبار عرض الخوارزميات
    test_results['algorithms'] = test_algorithms_endpoint()
    
    # 3. اختبار تدريب النماذج
    print("\n" + "="*60)
    print("🚀 اختبار تدريب النماذج")
    print("="*60)
    
    # تدريب نموذج التصنيف
    classification_model = test_classification_training()
    test_results['classification_training'] = classification_model is not None
    
    # تدريب نموذج الانحدار
    regression_model = test_regression_training()
    test_results['regression_training'] = regression_model is not None
    
    # تدريب نموذج التجميع
    clustering_model = test_clustering_training()
    test_results['clustering_training'] = clustering_model is not None
    
    # 4. اختبار التنبؤ
    print("\n" + "="*60)
    print("🔮 اختبار التنبؤ")
    print("="*60)
    
    if classification_model:
        test_results['classification_prediction'] = test_prediction(classification_model, "classification")
    
    if regression_model:
        test_results['regression_prediction'] = test_prediction(regression_model, "regression")
    
    if clustering_model:
        test_results['clustering_prediction'] = test_prediction(clustering_model, "clustering")
    
    # 5. اختبار معالجة اللغة الطبيعية
    print("\n" + "="*60)
    print("📝 اختبار معالجة اللغة الطبيعية (NLP)")
    print("="*60)
    
    # معالجة النصوص مسبقًا
    test_results['nlp_preprocessing'] = test_nlp_preprocessing()
    
    # تدريب نموذج NLP
    nlp_model = test_nlp_training()
    test_results['nlp_training'] = nlp_model is not None
    
    # التنبؤ بـ NLP
    if nlp_model:
        test_results['nlp_prediction'] = test_nlp_prediction(nlp_model)
        test_results['nlp_model_info'] = test_nlp_model_info(nlp_model)
    
    # 6. اختبارات إضافية
    print("\n" + "="*60)
    print("🔧 اختبارات إضافية")
    print("="*60)
    
    test_results['list_models'] = test_list_models()
    
    # 7. ملخص النتائج
    print_header("ملخص نتائج الاختبار")
    
    total_tests = len(test_results)
    passed_tests = sum(test_results.values())
    failed_tests = total_tests - passed_tests
    
    print(f"📊 إجمالي الاختبارات: {total_tests}")
    print(f"✅ الاختبارات الناجحة: {passed_tests}")
    print(f"❌ الاختبارات الفاشلة: {failed_tests}")
    print(f"📈 نسبة النجاح: {(passed_tests/total_tests)*100:.1f}%")
    
    print(f"\n⏰ وقت الانتهاء: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if failed_tests == 0:
        print_success("🎉 جميع الاختبارات نجحت! النظام يعمل بشكل مثالي.")
    else:
        print_error(f"⚠️  {failed_tests} اختبار فشل. راجع الأخطاء أعلاه.")
    
    return test_results

if __name__ == "__main__":
    # التحقق من وجود ملفات البيانات
    required_files = [
        "sample_data/iris.csv",
        "sample_data/boston.csv", 
        "sample_data/text_data.csv"
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print_error("الملفات التالية مفقودة:")
        for f in missing_files:
            print(f"  - {f}")
        print_info("يرجى إنشاء هذه الملفات قبل تشغيل الاختبار")
        exit(1)
    
    # تشغيل الاختبار الشامل
    run_comprehensive_test() 