# =============================================================================
# جميع خوارزميات التعلم الآلي من scikit-learn والمكتبات الإضافية
# =============================================================================

import joblib
import numpy as np
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

# =============================================================================
# استيراد جميع الخوارزميات
# =============================================================================

from sklearn.linear_model import (
    LogisticRegression, RidgeClassifier, SGDClassifier, Perceptron, PassiveAggressiveClassifier,
    LinearRegression, Ridge, Lasso, ElasticNet, HuberRegressor, PassiveAggressiveRegressor
)

from sklearn.ensemble import (
    RandomForestClassifier, RandomForestRegressor, AdaBoostClassifier, GradientBoostingClassifier,
    BaggingClassifier, ExtraTreesClassifier, GradientBoostingRegressor
)

from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.gaussian_process import GaussianProcessClassifier, GaussianProcessRegressor
from sklearn.cluster import (
    KMeans, DBSCAN, AgglomerativeClustering, SpectralClustering, 
    MeanShift, OPTICS, Birch, MiniBatchKMeans
)

# خوارزميات خارجية
try:
    from xgboost import XGBClassifier, XGBRegressor
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("Warning: XGBoost not available. Install with: pip install xgboost")

try:
    from lightgbm import LGBMClassifier, LGBMRegressor
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    print("Warning: LightGBM not available. Install with: pip install lightgbm")

try:
    from catboost import CatBoostClassifier
    CATBOOST_AVAILABLE = True
except ImportError:
    CATBOOST_AVAILABLE = False
    print("Warning: CatBoost not available. Install with: pip install catboost")

# =============================================================================
# قواميس الخوارزميات
# =============================================================================

# التصنيف
classification_algorithms = {
    "logistic_regression": LogisticRegression,
    "random_forest": RandomForestClassifier,
    "svm": SVC,
    "knn": KNeighborsClassifier,
    "decision_tree": DecisionTreeClassifier,
    "naive_bayes": GaussianNB,
    "neural_network": MLPClassifier,
    "bagging": BaggingClassifier,
    "ada_boost": AdaBoostClassifier,
    "gradient_boosting": GradientBoostingClassifier,
    "extra_trees": ExtraTreesClassifier,
    "ridge_classifier": RidgeClassifier,
    "sgd_classifier": SGDClassifier,
    "perceptron": Perceptron,
    "lda": LinearDiscriminantAnalysis,
    "qda": QuadraticDiscriminantAnalysis,
    "gaussian_process_classifier": GaussianProcessClassifier,
    "passive_aggressive": PassiveAggressiveClassifier,
}

# إضافة الخوارزميات الخارجية إذا كانت متاحة
if CATBOOST_AVAILABLE:
    classification_algorithms["catboost_classifier"] = lambda: CatBoostClassifier(verbose=0)

if XGBOOST_AVAILABLE:
    classification_algorithms["xgboost_classifier"] = XGBClassifier

if LIGHTGBM_AVAILABLE:
    classification_algorithms["lightgbm_classifier"] = LGBMClassifier

# الانحدار
regression_algorithms = {
    "linear_regression": LinearRegression,
    "ridge_regression": Ridge,
    "lasso_regression": Lasso,
    "elastic_net": ElasticNet,
    "random_forest_regressor": RandomForestRegressor,
    "svr": SVR,
    "knn_regressor": KNeighborsRegressor,
    "decision_tree_regressor": DecisionTreeRegressor,
    "neural_network_regressor": MLPRegressor,
    "gradient_boosting_regressor": GradientBoostingRegressor,
    "gaussian_process_regressor": GaussianProcessRegressor,
    "huber_regressor": HuberRegressor,
    "passive_aggressive_regressor": PassiveAggressiveRegressor,
}

# إضافة الخوارزميات الخارجية للانحدار إذا كانت متاحة
if XGBOOST_AVAILABLE:
    regression_algorithms["xgboost_regressor"] = XGBRegressor

if LIGHTGBM_AVAILABLE:
    regression_algorithms["lightgbm_regressor"] = LGBMRegressor

# التجميع
clustering_algorithms = {
    "kmeans": KMeans,
    "dbscan": DBSCAN,
    "agglomerative_clustering": AgglomerativeClustering,
    "spectral_clustering": SpectralClustering,
    "mean_shift": MeanShift,
    "optics": OPTICS,
    "birch": Birch,
    "minibatch_kmeans": MiniBatchKMeans
}

# =============================================================================
# دوال التدريب
# =============================================================================

def train_algorithm(X_train, y_train, algorithm_name, task_type='classification', **kwargs):
    """
    دالة عامة لتدريب أي خوارزمية
    
    Args:
        X_train: بيانات التدريب
        y_train: التصنيفات المستهدفة
        algorithm_name: اسم الخوارزمية
        task_type: نوع المهمة ('classification', 'regression', 'clustering')
        **kwargs: معاملات إضافية للخوارزمية
    
    Returns:
        النموذج المدرب
    """
    
    if task_type == 'classification':
        if algorithm_name in classification_algorithms:
            algorithm_class = classification_algorithms[algorithm_name]
            if callable(algorithm_class):
                model = algorithm_class(**kwargs)
            else:
                model = algorithm_class
            model.fit(X_train, y_train)
            return model
        else:
            raise ValueError(f"Unknown classification algorithm: {algorithm_name}")
    
    elif task_type == 'regression':
        if algorithm_name in regression_algorithms:
            algorithm_class = regression_algorithms[algorithm_name]
            if callable(algorithm_class):
                model = algorithm_class(**kwargs)
            else:
                model = algorithm_class
            model.fit(X_train, y_train)
            return model
        else:
            raise ValueError(f"Unknown regression algorithm: {algorithm_name}")
    
    elif task_type == 'clustering':
        if algorithm_name in clustering_algorithms:
            algorithm_class = clustering_algorithms[algorithm_name]
            if callable(algorithm_class):
                model = algorithm_class(**kwargs)
            else:
                model = algorithm_class
            model.fit(X_train)
            return model
        else:
            raise ValueError(f"Unknown clustering algorithm: {algorithm_name}")
    
    else:
        raise ValueError(f"Unknown task type: {task_type}")

def train_with_gridsearch(X_train, y_train, base_model, param_grid, cv=5):
    """تدريب مع البحث في الشبكة"""
    grid = GridSearchCV(base_model, param_grid, cv=cv, n_jobs=-1)
    grid.fit(X_train, y_train)
    return grid.best_estimator_

def train_with_randomized_search(X_train, y_train, base_model, param_distributions, n_iter=100, cv=5):
    """تدريب مع البحث العشوائي"""
    random_search = RandomizedSearchCV(base_model, param_distributions, n_iter=n_iter, cv=cv, n_jobs=-1)
    random_search.fit(X_train, y_train)
    return random_search.best_estimator_

# =============================================================================
# دوال حفظ واسترجاع النماذج
# =============================================================================

def save_model(model, path):
    """حفظ النموذج"""
    joblib.dump(model, path)

def load_model(path):
    """استرجاع النموذج"""
    return joblib.load(path)

# =============================================================================
# دوال مساعدة
# =============================================================================

def get_available_algorithms():
    """الحصول على قائمة جميع الخوارزميات المتاحة"""
    return {
        'classification': list(classification_algorithms.keys()),
        'regression': list(regression_algorithms.keys()),
        'clustering': list(clustering_algorithms.keys())
    }

def get_algorithm_info():
    """الحصول على معلومات مفصلة عن الخوارزميات"""
    info = {
        'classification': {},
        'regression': {},
        'clustering': {}
    }
    
    for name, algo in classification_algorithms.items():
        info['classification'][name] = {
            'class': algo.__name__ if hasattr(algo, '__name__') else str(algo),
            'available': True
        }
    
    for name, algo in regression_algorithms.items():
        info['regression'][name] = {
            'class': algo.__name__ if hasattr(algo, '__name__') else str(algo),
            'available': True
        }
    
    for name, algo in clustering_algorithms.items():
        info['clustering'][name] = {
            'class': algo.__name__ if hasattr(algo, '__name__') else str(algo),
            'available': True
        }
    
    return info 