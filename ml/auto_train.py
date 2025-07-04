import pandas as pd
from ml.models import classification_algorithms, regression_algorithms, clustering_algorithms
from ml.data_utils import load_data, split_data, preprocess_data
from ml.predict import evaluate
import warnings

def auto_train_best_algorithm(
    data_path, target_column=None, task_type='classification', test_size=0.2, random_state=42
):
    """
    يجرب جميع الخوارزميات المتاحة لنوع المهمة ويطبع النتائج مرتبة ويحدد الأفضل.
    Args:
        data_path: مسار ملف البيانات
        target_column: اسم عمود الهدف (ليس مطلوباً للتجميع)
        task_type: 'classification' أو 'regression' أو 'clustering'
        test_size: نسبة بيانات الاختبار
        random_state: البذرة العشوائية
    """
    data = load_data(data_path)
    if task_type != 'clustering':
        data = preprocess_data(data, target_column)
        X_train, X_test, y_train, y_test = split_data(data, target_column, test_size, random_state)
    else:
        data = preprocess_data(data)
        X_train = data
    
    if task_type == 'classification':
        algos = classification_algorithms
        metric = lambda y_true, y_pred: evaluate(y_true, y_pred, 'classification')['accuracy']
    elif task_type == 'regression':
        algos = regression_algorithms
        metric = lambda y_true, y_pred: evaluate(y_true, y_pred, 'regression')['r2_score']
    elif task_type == 'clustering':
        algos = clustering_algorithms
        metric = lambda X, labels: evaluate(None, labels, 'clustering', X)['silhouette_score']
    else:
        raise ValueError("Unknown task_type")

    results = []
    for name, algo in algos.items():
        try:
            print(f"Training {name} ...")
            model = algo()
            if task_type == 'clustering':
                model.fit(X_train)
                labels = model.predict(X_train)
                score = metric(X_train, labels)
            else:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                score = metric(y_test, y_pred)
            results.append((name, score))
        except Exception as e:
            print(f"Failed: {name} ({e})")
            continue

    # ترتيب النتائج
    results.sort(key=lambda x: x[1], reverse=True)
    print("\n=== Results ===")
    for name, score in results:
        print(f"{name}: {score:.4f}")

    if results:
        print(f"\nBest algorithm: {results[0][0]} (score: {results[0][1]:.4f})")
    else:
        print("No algorithm succeeded.")

# مثال الاستخدام:
# auto_train_best_algorithm('sample_data/iris.csv', 'species', task_type='classification')
# auto_train_best_algorithm('sample_data/housing.csv', 'target', task_type='regression')
# auto_train_best_algorithm('sample_data/iris.csv', task_type='clustering') 