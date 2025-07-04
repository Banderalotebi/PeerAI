# =============================================================================
# التنبؤ والتقييم
# =============================================================================

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix,
    mean_squared_error, mean_absolute_error, r2_score,
    silhouette_score, calinski_harabasz_score
)

def predict(model, X):
    """
    التنبؤ باستخدام النموذج
    
    Args:
        model: النموذج المدرب
        X: بيانات التنبؤ
        
    Returns:
        array: التنبؤات
    """
    if hasattr(model, 'predict'):
        return model.predict(X)
    else:
        raise ValueError("النموذج لا يحتوي على دالة predict")

def predict_proba(model, X):
    """
    التنبؤ بالاحتمالات (للتصنيف)
    
    Args:
        model: النموذج المدرب
        X: بيانات التنبؤ
        
    Returns:
        array: احتمالات التنبؤ
    """
    if hasattr(model, 'predict_proba'):
        return model.predict_proba(X)
    else:
        raise ValueError("النموذج لا يحتوي على دالة predict_proba")

def evaluate_classification(y_true, y_pred, y_prob=None):
    """
    تقييم نموذج التصنيف
    
    Args:
        y_true: القيم الحقيقية
        y_pred: التنبؤات
        y_prob: احتمالات التنبؤ (اختياري)
        
    Returns:
        dict: مقاييس التقييم
    """
    evaluation = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average='weighted'),
        'recall': recall_score(y_true, y_pred, average='weighted'),
        'f1_score': f1_score(y_true, y_pred, average='weighted'),
        'classification_report': classification_report(y_true, y_pred, output_dict=True),
        'confusion_matrix': confusion_matrix(y_true, y_pred).tolist()
    }
    
    # إضافة مقاييس إضافية إذا كانت الاحتمالات متاحة
    if y_prob is not None:
        from sklearn.metrics import roc_auc_score, log_loss
        try:
            evaluation['roc_auc'] = roc_auc_score(y_true, y_prob, multi_class='ovr')
            evaluation['log_loss'] = log_loss(y_true, y_prob)
        except:
            pass
    
    return evaluation

def evaluate_regression(y_true, y_pred):
    """
    تقييم نموذج الانحدار
    
    Args:
        y_true: القيم الحقيقية
        y_pred: التنبؤات
        
    Returns:
        dict: مقاييس التقييم
    """
    from sklearn.metrics import explained_variance_score
    
    evaluation = {
        'r2_score': r2_score(y_true, y_pred),
        'mean_squared_error': mean_squared_error(y_true, y_pred),
        'root_mean_squared_error': np.sqrt(mean_squared_error(y_true, y_pred)),
        'mean_absolute_error': mean_absolute_error(y_true, y_pred),
        'explained_variance': explained_variance_score(y_true, y_pred)
    }
    
    return evaluation

def evaluate_clustering(X, labels):
    """
    تقييم نموذج التجميع
    
    Args:
        X: البيانات
        labels: تسميات العناقيد
        
    Returns:
        dict: مقاييس التقييم
    """
    evaluation = {
        'silhouette_score': silhouette_score(X, labels),
        'calinski_harabasz_score': calinski_harabasz_score(X, labels),
        'n_clusters': len(np.unique(labels)),
        'cluster_sizes': np.bincount(labels).tolist()
    }
    
    return evaluation

def evaluate(y_true, y_pred, task_type='classification', X=None, y_prob=None):
    """
    تقييم عام للنموذج
    
    Args:
        y_true: القيم الحقيقية
        y_pred: التنبؤات
        task_type: نوع المهمة ('classification', 'regression', 'clustering')
        X: البيانات (مطلوب للتجميع)
        y_prob: احتمالات التنبؤ (اختياري للتصنيف)
        
    Returns:
        dict: مقاييس التقييم
    """
    if task_type == 'classification':
        return evaluate_classification(y_true, y_pred, y_prob)
    elif task_type == 'regression':
        return evaluate_regression(y_true, y_pred)
    elif task_type == 'clustering':
        if X is None:
            raise ValueError("البيانات مطلوبة لتقييم التجميع")
        return evaluate_clustering(X, y_pred)
    else:
        raise ValueError(f"نوع المهمة غير مدعوم: {task_type}")

def cross_validate_model(model, X, y, cv=5, task_type='classification'):
    """
    التحقق المتقاطع من النموذج
    
    Args:
        model: النموذج
        X: البيانات
        y: الهدف
        cv: عدد الطيات
        task_type: نوع المهمة
        
    Returns:
        dict: نتائج التحقق المتقاطع
    """
    from sklearn.model_selection import cross_val_score
    
    if task_type == 'classification':
        scoring = 'accuracy'
    elif task_type == 'regression':
        scoring = 'r2'
    else:
        scoring = 'accuracy'
    
    scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
    
    return {
        'cv_scores': scores.tolist(),
        'mean_score': scores.mean(),
        'std_score': scores.std(),
        'min_score': scores.min(),
        'max_score': scores.max()
    }

def plot_confusion_matrix(y_true, y_pred, classes=None):
    """
    رسم مصفوفة الارتباك
    
    Args:
        y_true: القيم الحقيقية
        y_pred: التنبؤات
        classes: أسماء الفئات
        
    Returns:
        matplotlib figure: الرسم البياني
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=classes, yticklabels=classes)
    plt.title('مصفوفة الارتباك')
    plt.ylabel('القيم الحقيقية')
    plt.xlabel('التنبؤات')
    plt.tight_layout()
    
    return plt.gcf()

def plot_regression_results(y_true, y_pred):
    """
    رسم نتائج الانحدار
    
    Args:
        y_true: القيم الحقيقية
        y_pred: التنبؤات
        
    Returns:
        matplotlib figure: الرسم البياني
    """
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(10, 4))
    
    # رسم التنبؤات مقابل القيم الحقيقية
    plt.subplot(1, 2, 1)
    plt.scatter(y_true, y_pred, alpha=0.5)
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--', lw=2)
    plt.xlabel('القيم الحقيقية')
    plt.ylabel('التنبؤات')
    plt.title('التنبؤات مقابل القيم الحقيقية')
    
    # رسم الفروق
    plt.subplot(1, 2, 2)
    residuals = y_true - y_pred
    plt.scatter(y_pred, residuals, alpha=0.5)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel('التنبؤات')
    plt.ylabel('الفروق')
    plt.title('تحليل الفروق')
    
    plt.tight_layout()
    return plt.gcf()

def generate_prediction_report(model, X_test, y_test, task_type='classification'):
    """
    إنشاء تقرير شامل للتنبؤ
    
    Args:
        model: النموذج المدرب
        X_test: بيانات الاختبار
        y_test: القيم الحقيقية للاختبار
        task_type: نوع المهمة
        
    Returns:
        dict: التقرير الشامل
    """
    # التنبؤ
    y_pred = predict(model, X_test)
    
    # الحصول على الاحتمالات للتصنيف
    y_prob = None
    if task_type == 'classification' and hasattr(model, 'predict_proba'):
        try:
            y_prob = predict_proba(model, X_test)
        except:
            pass
    
    # التقييم
    evaluation = evaluate(y_test, y_pred, task_type, X_test, y_prob)
    
    # معلومات إضافية
    report = {
        'task_type': task_type,
        'model_type': type(model).__name__,
        'n_samples': len(X_test),
        'n_features': X_test.shape[1] if hasattr(X_test, 'shape') else len(X_test[0]),
        'predictions': y_pred.tolist() if hasattr(y_pred, 'tolist') else y_pred,
        'evaluation': evaluation
    }
    
    # إضافة الاحتمالات إذا كانت متاحة
    if y_prob is not None:
        report['probabilities'] = y_prob.tolist()
    
    return report 