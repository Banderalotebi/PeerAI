# =============================================================================
# معالجة البيانات
# =============================================================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os

def load_data(file_path):
    """
    تحميل البيانات من ملف CSV
    
    Args:
        file_path: مسار ملف البيانات
        
    Returns:
        DataFrame: البيانات المحملة
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"ملف البيانات غير موجود: {file_path}")
    
    # تحديد نوع الملف
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        data = pd.read_excel(file_path)
    else:
        raise ValueError(f"نوع الملف غير مدعوم: {file_path}")
    
    return data

def split_data(data, target_column, test_size=0.2, random_state=42, stratify=None):
    """
    تقسيم البيانات إلى تدريب واختبار
    
    Args:
        data: DataFrame البيانات
        target_column: اسم عمود الهدف
        test_size: نسبة بيانات الاختبار
        random_state: البذرة العشوائية
        stratify: التقسيم الطبقي (للتصنيف)
        
    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    # التحقق من وجود عمود الهدف
    if target_column not in data.columns:
        raise ValueError(f"عمود الهدف غير موجود: {target_column}")
    
    # فصل الميزات والهدف
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    # التقسيم الطبقي للتصنيف
    if stratify is None and y.dtype == 'object':
        stratify = y
    
    # تقسيم البيانات
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=stratify
    )
    
    return X_train, X_test, y_train, y_test

def preprocess_data(data, target_column=None, scale_features=True, encode_categorical=True):
    """
    معالجة البيانات مسبقًا
    
    Args:
        data: DataFrame البيانات
        target_column: اسم عمود الهدف (اختياري)
        scale_features: تطبيع الميزات الرقمية
        encode_categorical: ترميز الميزات الفئوية
        
    Returns:
        DataFrame: البيانات المعالجة
    """
    processed_data = data.copy()
    
    # ترميز الميزات الفئوية
    if encode_categorical:
        label_encoders = {}
        for column in processed_data.columns:
            if processed_data[column].dtype == 'object' and column != target_column:
                le = LabelEncoder()
                processed_data[column] = le.fit_transform(processed_data[column].astype(str))
                label_encoders[column] = le
    
    # تطبيع الميزات الرقمية
    if scale_features:
        numeric_columns = processed_data.select_dtypes(include=[np.number]).columns
        if target_column and target_column in numeric_columns:
            numeric_columns = numeric_columns.drop(target_column)
        
        if len(numeric_columns) > 0:
            scaler = StandardScaler()
            processed_data[numeric_columns] = scaler.fit_transform(processed_data[numeric_columns])
    
    return processed_data

def get_data_info(data):
    """
    الحصول على معلومات عن البيانات
    
    Args:
        data: DataFrame البيانات
        
    Returns:
        dict: معلومات البيانات
    """
    info = {
        'shape': data.shape,
        'columns': list(data.columns),
        'dtypes': data.dtypes.to_dict(),
        'missing_values': data.isnull().sum().to_dict(),
        'numeric_columns': list(data.select_dtypes(include=[np.number]).columns),
        'categorical_columns': list(data.select_dtypes(include=['object']).columns),
        'memory_usage': data.memory_usage(deep=True).sum() / 1024 / 1024  # MB
    }
    
    return info

def validate_data(data, required_columns=None, min_rows=10):
    """
    التحقق من صحة البيانات
    
    Args:
        data: DataFrame البيانات
        required_columns: الأعمدة المطلوبة
        min_rows: الحد الأدنى لعدد الصفوف
        
    Returns:
        bool: صحة البيانات
    """
    # التحقق من عدد الصفوف
    if len(data) < min_rows:
        raise ValueError(f"عدد الصفوف أقل من الحد الأدنى: {len(data)} < {min_rows}")
    
    # التحقق من الأعمدة المطلوبة
    if required_columns:
        missing_columns = set(required_columns) - set(data.columns)
        if missing_columns:
            raise ValueError(f"الأعمدة المفقودة: {missing_columns}")
    
    # التحقق من القيم المفقودة
    missing_percentage = data.isnull().sum().sum() / (len(data) * len(data.columns)) * 100
    if missing_percentage > 50:
        raise ValueError(f"نسبة القيم المفقودة عالية جداً: {missing_percentage:.2f}%")
    
    return True

def create_sample_data():
    """
    إنشاء بيانات تجريبية
    
    Returns:
        tuple: (iris_data, housing_data)
    """
    from sklearn.datasets import load_iris, fetch_california_housing
    
    # بيانات Iris للتصنيف
    iris = load_iris()
    iris_data = pd.DataFrame(iris.data, columns=iris.feature_names)
    iris_data['species'] = iris.target_names[iris.target]
    
    # بيانات California Housing للانحدار
    housing = fetch_california_housing()
    housing_data = pd.DataFrame(housing.data, columns=housing.feature_names)
    housing_data['target'] = housing.target
    
    return iris_data, housing_data

def save_sample_data():
    """
    حفظ البيانات التجريبية
    """
    iris_data, housing_data = create_sample_data()
    
    # إنشاء مجلد البيانات إذا لم يكن موجودًا
    os.makedirs('sample_data', exist_ok=True)
    
    # حفظ البيانات
    iris_data.to_csv('sample_data/iris.csv', index=False)
    housing_data.to_csv('sample_data/housing.csv', index=False)
    
    print("تم حفظ البيانات التجريبية في مجلد sample_data/") 