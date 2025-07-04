#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف اختبار شامل لنظام التعلم الآلي
يختبر جميع الخوارزميات المتاحة
"""

import requests
import json
import time
import pandas as pd
from ml.models import get_available_algorithms

# تكوين الخادم
BASE_URL = "http://localhost:5000"

def test_server_health():
    """اختبار حالة الخادم"""
    print("🔍 اختبار حالة الخادم...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ الخادم يعمل بشكل صحيح")
            return True
        else:
            print("❌ الخادم لا يستجيب")
            return False
    except Exception as e:
        print(f"❌ خطأ في الاتصال بالخادم: {e}")
        return False

def test_algorithms_endpoint():
    """اختبار نقطة نهاية الخوارزميات"""
    print("\n🔍 اختبار نقطة نهاية الخوارزميات...")
    try:
        response = requests.get(f"{BASE_URL}/algorithms")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ تم العثور على {data['total_classification']} خوارزمية تصنيف")
            print(f"✅ تم العثور على {data['total_regression']} خوارزمية انحدار")
            print(f"✅ تم العثور على {data['total_clustering']} خوارزمية تجميع")
            return data['algorithms']
        else:
            print("❌ فشل في الحصول على الخوارزميات")
            return None
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return None

def test_classification_algorithms(algorithms):
    """اختبار خوارزميات التصنيف"""
    print("\n🔍 اختبار خوارزميات التصنيف...")
    
    # اختبار الخوارزميات الأساسية
    basic_algorithms = [
        'logistic_regression',
        'random_forest', 
        'decision_tree',
        'naive_bayes',
        'knn'
    ]
    
    for algo in basic_algorithms:
        if algo in algorithms['classification']:
            print(f"✅ اختبار {algo}...")
            try:
                train_data = {
                    "data_path": "sample_data.csv",
                    "target": "target_classification",
                    "algorithm": algo,
                    "task_type": "classification"
                }
                
                response = requests.post(f"{BASE_URL}/train", json=train_data)
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ تم تدريب {algo} بنجاح")
                    
                    # اختبار التنبؤ
                    predict_data = {
                        "model_path": result["model_path"],
                        "features": [[1.2, 3.4, 5.6, 7.8]]
                    }
                    
                    pred_response = requests.post(f"{BASE_URL}/predict", json=predict_data)
                    if pred_response.status_code == 200:
                        print(f"   ✅ تم التنبؤ بـ {algo} بنجاح")
                    else:
                        print(f"   ❌ فشل التنبؤ بـ {algo}")
                        
                else:
                    print(f"   ❌ فشل تدريب {algo}: {response.text}")
                    
            except Exception as e:
                print(f"   ❌ خطأ في {algo}: {e}")
        else:
            print(f"⚠️  {algo} غير متاح")

def test_regression_algorithms(algorithms):
    """اختبار خوارزميات الانحدار"""
    print("\n🔍 اختبار خوارزميات الانحدار...")
    
    # اختبار الخوارزميات الأساسية
    basic_algorithms = [
        'linear_regression',
        'ridge_regression',
        'random_forest_regressor',
        'decision_tree_regressor'
    ]
    
    for algo in basic_algorithms:
        if algo in algorithms['regression']:
            print(f"✅ اختبار {algo}...")
            try:
                train_data = {
                    "data_path": "sample_data.csv",
                    "target": "target_regression",
                    "algorithm": algo,
                    "task_type": "regression"
                }
                
                response = requests.post(f"{BASE_URL}/train", json=train_data)
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ تم تدريب {algo} بنجاح")
                    
                    # اختبار التنبؤ
                    predict_data = {
                        "model_path": result["model_path"],
                        "features": [[1.2, 3.4, 5.6, 7.8]]
                    }
                    
                    pred_response = requests.post(f"{BASE_URL}/predict", json=predict_data)
                    if pred_response.status_code == 200:
                        print(f"   ✅ تم التنبؤ بـ {algo} بنجاح")
                    else:
                        print(f"   ❌ فشل التنبؤ بـ {algo}")
                        
                else:
                    print(f"   ❌ فشل تدريب {algo}: {response.text}")
                    
            except Exception as e:
                print(f"   ❌ خطأ في {algo}: {e}")
        else:
            print(f"⚠️  {algo} غير متاح")

def test_clustering_algorithms(algorithms):
    """اختبار خوارزميات التجميع"""
    print("\n🔍 اختبار خوارزميات التجميع...")
    
    # اختبار الخوارزميات الأساسية
    basic_algorithms = [
        'kmeans',
        'dbscan'
    ]
    
    for algo in basic_algorithms:
        if algo in algorithms['clustering']:
            print(f"✅ اختبار {algo}...")
            try:
                train_data = {
                    "data_path": "sample_data.csv",
                    "algorithm": algo,
                    "task_type": "clustering"
                }
                
                response = requests.post(f"{BASE_URL}/train", json=train_data)
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ تم تدريب {algo} بنجاح")
                    
                    # اختبار التنبؤ
                    predict_data = {
                        "model_path": result["model_path"],
                        "features": [[1.2, 3.4, 5.6, 7.8]]
                    }
                    
                    pred_response = requests.post(f"{BASE_URL}/predict", json=predict_data)
                    if pred_response.status_code == 200:
                        print(f"   ✅ تم التنبؤ بـ {algo} بنجاح")
                    else:
                        print(f"   ❌ فشل التنبؤ بـ {algo}")
                        
                else:
                    print(f"   ❌ فشل تدريب {algo}: {response.text}")
                    
            except Exception as e:
                print(f"   ❌ خطأ في {algo}: {e}")
        else:
            print(f"⚠️  {algo} غير متاح")

def test_advanced_algorithms():
    """اختبار الخوارزميات المتقدمة"""
    print("\n🔍 اختبار الخوارزميات المتقدمة...")
    
    # اختبار XGBoost إذا كان متاحًا
    try:
        train_data = {
            "data_path": "sample_data.csv",
            "target": "target_classification",
            "algorithm": "xgboost_classifier",
            "task_type": "classification",
            "parameters": {
                "n_estimators": 50,
                "max_depth": 3,
                "learning_rate": 0.1
            }
        }
        
        response = requests.post(f"{BASE_URL}/train", json=train_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ تم تدريب XGBoost بنجاح")
        else:
            print(f"⚠️  XGBoost غير متاح أو فشل: {response.text}")
    except Exception as e:
        print(f"⚠️  XGBoost غير متاح: {e}")

def test_gridsearch():
    """اختبار GridSearchCV"""
    print("\n🔍 اختبار GridSearchCV...")
    try:
        train_data = {
            "data_path": "sample_data.csv",
            "target": "target_classification",
            "algorithm": "random_forest",
            "task_type": "classification",
            "use_gridsearch": True,
            "param_grid": {
                "n_estimators": [10, 20],
                "max_depth": [3, 5]
            }
        }
        
        response = requests.post(f"{BASE_URL}/train", json=train_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ تم تدريب GridSearchCV بنجاح")
        else:
            print(f"❌ فشل GridSearchCV: {response.text}")
    except Exception as e:
        print(f"❌ خطأ في GridSearchCV: {e}")

def test_model_management():
    """اختبار إدارة النماذج"""
    print("\n🔍 اختبار إدارة النماذج...")
    
    # قائمة النماذج
    try:
        response = requests.get(f"{BASE_URL}/list_models")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ تم العثور على {data['count']} نموذج محفوظ")
            
            # معلومات عن نموذج محدد
            if data['models']:
                model_name = data['models'][0]
                info_response = requests.get(f"{BASE_URL}/model_info/{model_name}")
                if info_response.status_code == 200:
                    info = info_response.json()
                    print(f"✅ معلومات النموذج: {info['model_type']}")
                else:
                    print("❌ فشل في الحصول على معلومات النموذج")
        else:
            print("❌ فشل في قائمة النماذج")
    except Exception as e:
        print(f"❌ خطأ في إدارة النماذج: {e}")

def main():
    """الدالة الرئيسية للاختبار"""
    print("🚀 بدء اختبار نظام التعلم الآلي الشامل")
    print("=" * 50)
    
    # اختبار حالة الخادم
    if not test_server_health():
        print("❌ فشل في الاتصال بالخادم. تأكد من تشغيل app.py")
        return
    
    # اختبار نقطة نهاية الخوارزميات
    algorithms = test_algorithms_endpoint()
    if not algorithms:
        print("❌ فشل في الحصول على الخوارزميات")
        return
    
    # اختبار الخوارزميات المختلفة
    test_classification_algorithms(algorithms)
    test_regression_algorithms(algorithms)
    test_clustering_algorithms(algorithms)
    test_advanced_algorithms()
    test_gridsearch()
    test_model_management()
    
    print("\n" + "=" * 50)
    print("🎉 انتهى اختبار النظام!")
    print("✅ جميع الاختبارات الأساسية مكتملة")

if __name__ == "__main__":
    main() 