from flask import Flask, request, jsonify
import pandas as pd
import os
from ml.data_utils import load_data, split_data
from ml.models import (
    train_algorithm, save_model, load_model, get_available_algorithms,
    train_with_gridsearch, train_with_randomized_search
)
from ml.predict import predict, evaluate
from ml.nlp_utils import TextClassifier, TextPreprocessor
from ml.simple_nlp import SimpleNLP

app = Flask(__name__)

# إنشاء مجلد للنماذج إذا لم يكن موجودًا
os.makedirs("models", exist_ok=True)

# تهيئة Simple NLP
ll = SimpleNLP()

@app.route('/')
def home():
    """الصفحة الرئيسية"""
    return jsonify({
        "message": "نظام التعلم الآلي الشامل",
        "version": "2.0",
        "features": [
            "خوارزميات التصنيف والانحدار والتجميع",
            "معالجة اللغة الطبيعية (NLP)",
            "واجهة برمجية REST API",
            "حفظ واسترجاع النماذج",
            "تقييم تلقائي للنماذج"
        ],
        "endpoints": {
            "/algorithms": "عرض جميع الخوارزميات المتاحة",
            "/train": "تدريب نموذج",
            "/predict": "التنبؤ",
            "/nlp/train": "تدريب نموذج NLP",
            "/nlp/predict": "التنبؤ بـ NLP",
            "/health": "حالة النظام"
        }
    })

@app.route('/algorithms', methods=['GET'])
def get_algorithms():
    """عرض جميع الخوارزميات المتاحة"""
    algorithms = get_available_algorithms()
    return jsonify({
        "message": "جميع الخوارزميات المتاحة",
        "algorithms": algorithms,
        "total_classification": len(algorithms['classification']),
        "total_regression": len(algorithms['regression']),
        "total_clustering": len(algorithms['clustering'])
    })

@app.route('/train', methods=['POST'])
def train():
    """تدريب نموذج"""
    try:
        data = request.json
        
        # التحقق من البيانات المطلوبة
        required_fields = ['data_path', 'target', 'algorithm', 'task_type']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # قراءة البيانات
        df = load_data(data['data_path'])
        
        # تقسيم البيانات (للتجميع لا نحتاج y)
        if data['task_type'] == 'clustering':
            X_train = df
            y_train = None
        else:
            X_train, X_test, y_train, y_test = split_data(
                df, 
                data['target'], 
                test_size=data.get('test_size', 0.2),
                random_state=data.get('random_state', 42)
            )
        
        # معاملات إضافية للخوارزمية
        algorithm_params = data.get('parameters', {})
        
        # تدريب النموذج
        if data.get('use_gridsearch', False):
            # استخدام GridSearchCV
            param_grid = data.get('param_grid', {})
            base_model = train_algorithm(X_train, y_train, data['algorithm'], data['task_type'], **algorithm_params)
            model = train_with_gridsearch(X_train, y_train, base_model, param_grid, cv=data.get('cv', 5))
        elif data.get('use_randomized_search', False):
            # استخدام RandomizedSearchCV
            param_distributions = data.get('param_distributions', {})
            base_model = train_algorithm(X_train, y_train, data['algorithm'], data['task_type'], **algorithm_params)
            model = train_with_randomized_search(X_train, y_train, base_model, param_distributions, n_iter=data.get('n_iter', 100), cv=data.get('cv', 5))
        else:
            # التدريب العادي
            model = train_algorithm(X_train, y_train, data['algorithm'], data['task_type'], **algorithm_params)
        
        # حفظ النموذج
        model_path = f"models/{data['algorithm']}_{data['task_type']}_model.pkl"
        save_model(model, model_path)
        
        # تقييم النموذج (للتجميع لا نحتاج تقييم)
        if data['task_type'] != 'clustering':
            y_pred = predict(model, X_test)
            evaluation = evaluate(y_test, y_pred)
        else:
            evaluation = {"message": "Clustering model trained successfully"}
        
        return jsonify({
            "message": "Model trained successfully",
            "algorithm": data['algorithm'],
            "task_type": data['task_type'],
            "model_path": model_path,
            "evaluation": evaluation
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict_api():
    """التنبؤ"""
    try:
        data = request.json
        
        # التحقق من البيانات المطلوبة
        if 'model_path' not in data or 'features' not in data:
            return jsonify({"error": "Missing required fields: model_path and features"}), 400
        
        # تحميل النموذج
        model = load_model(data['model_path'])
        
        # تحويل البيانات إلى DataFrame
        X = pd.DataFrame(data['features'])
        
        # التنبؤ
        predictions = predict(model, X)
        
        return jsonify({
            "message": "Prediction completed",
            "predictions": predictions.tolist() if hasattr(predictions, 'tolist') else predictions
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =============================================================================
# واجهات معالجة اللغة الطبيعية (NLP)
# =============================================================================

@app.route('/nlp/train', methods=['POST'])
def nlp_train():
    """تدريب نموذج معالجة اللغة الطبيعية"""
    try:
        data = request.json
        
        # التحقق من البيانات المطلوبة
        required_fields = ['data_path', 'text_column', 'target_column']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # إنشاء مصنف النصوص
        classifier = TextClassifier(model_path=data.get('model_path', 'models/nlp_model.pkl'))
        
        # معاملات إضافية
        vectorizer_type = data.get('vectorizer_type', 'tfidf')
        classifier_type = data.get('classifier_type', 'logistic_regression')
        use_gridsearch = data.get('use_gridsearch', False)
        
        # تدريب النموذج
        if use_gridsearch:
            result = classifier.train_with_gridsearch(
                data_path=data['data_path'],
                text_column=data['text_column'],
                target_column=data['target_column'],
                vectorizer_type=vectorizer_type,
                classifier_type=classifier_type,
                param_grid=data.get('param_grid'),
                cv=data.get('cv', 5),
                test_size=data.get('test_size', 0.2),
                random_state=data.get('random_state', 42)
            )
        else:
            result = classifier.train(
                data_path=data['data_path'],
                text_column=data['text_column'],
                target_column=data['target_column'],
                vectorizer_type=vectorizer_type,
                classifier_type=classifier_type,
                test_size=data.get('test_size', 0.2),
                random_state=data.get('random_state', 42),
                **data.get('parameters', {})
            )
        
        return jsonify({
            "message": "NLP model trained successfully",
            "model_path": result['model_path'],
            "classes": result['classes'],
            "accuracy": result['accuracy'],
            "vectorizer_type": vectorizer_type,
            "classifier_type": classifier_type
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nlp/predict', methods=['POST'])
def nlp_predict():
    """التنبؤ باستخدام نموذج NLP"""
    try:
        data = request.json
        
        # التحقق من البيانات المطلوبة
        if 'texts' not in data:
            return jsonify({"error": "Missing required field: texts"}), 400
        
        # إنشاء مصنف النصوص
        classifier = TextClassifier(model_path=data.get('model_path', 'models/nlp_model.pkl'))
        
        # التنبؤ
        texts = data['texts']
        results = classifier.predict(texts)
        
        return jsonify({
            "message": "NLP prediction completed",
            "results": results
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nlp/preprocess', methods=['POST'])
def nlp_preprocess():
    """معالجة النصوص مسبقًا"""
    try:
        data = request.json
        
        # التحقق من البيانات المطلوبة
        if 'data_path' not in data or 'text_column' not in data:
            return jsonify({"error": "Missing required fields: data_path and text_column"}), 400
        
        # معالجة البيانات
        result = TextPreprocessor.preprocess_dataset(
            data_path=data['data_path'],
            text_column=data['text_column'],
            output_path=data.get('output_path'),
            clean_text=data.get('clean_text', True),
            remove_stopwords=data.get('remove_stopwords', True)
        )
        
        return jsonify({
            "message": "Text preprocessing completed",
            "output_path": data.get('output_path'),
            "rows_processed": len(result)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nlp/model_info', methods=['GET'])
def nlp_model_info():
    """معلومات عن نموذج NLP"""
    try:
        model_path = request.args.get('model_path', 'models/nlp_model.pkl')
        classifier = TextClassifier(model_path=model_path)
        info = classifier.model_info()
        
        return jsonify(info)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nlp/evaluate', methods=['POST'])
def nlp_evaluate():
    """تقييم نموذج NLP"""
    try:
        data = request.json
        
        # التحقق من البيانات المطلوبة
        required_fields = ['test_data_path', 'text_column', 'target_column']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # إنشاء مصنف النصوص
        classifier = TextClassifier(model_path=data.get('model_path', 'models/nlp_model.pkl'))
        
        # تقييم النموذج
        result = classifier.evaluate(
            test_data_path=data['test_data_path'],
            text_column=data['text_column'],
            target_column=data['target_column']
        )
        
        return jsonify({
            "message": "NLP model evaluation completed",
            "accuracy": result['accuracy'],
            "classification_report": result['classification_report']
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =============================================================================
# واجهات إضافية
# =============================================================================

@app.route('/health', methods=['GET'])
def health():
    """حالة النظام"""
    return jsonify({
        "status": "healthy",
        "message": "System is running properly",
        "version": "2.0"
    })

@app.route('/model_info/<model_name>', methods=['GET'])
def model_info(model_name):
    """معلومات عن نموذج محدد"""
    model_path = f"models/{model_name}"
    if os.path.exists(model_path):
        model = load_model(model_path)
        return jsonify({
            "model_name": model_name,
            "model_type": type(model).__name__,
            "model_path": model_path,
            "exists": True
        })
    else:
        return jsonify({
            "model_name": model_name,
            "exists": False,
            "message": "Model not found"
        }), 404

@app.route('/list_models', methods=['GET'])
def list_models():
    """عرض جميع النماذج المحفوظة"""
    models_dir = "models"
    if os.path.exists(models_dir):
        models = [f for f in os.listdir(models_dir) if f.endswith('.pkl')]
        return jsonify({
            "models": models,
            "count": len(models)
        })
    else:
        return jsonify({
            "models": [],
            "count": 0,
            "message": "No models directory found"
        })

# =============================================================================
# نقاط النهاية المتقدمة لمعالجة اللغات الطبيعية
# =============================================================================

@app.route('/nlp/sentiment', methods=['POST'])
def analyze_sentiment():
    """تحليل مشاعر النص"""
    try:
        data = request.json
        if 'text' not in data:
            return jsonify({"error": "Missing required field: text"}), 400
        
        sentiment, score = ll.sentiment_analysis_simple(data['text'])
        return jsonify({
            "text": data['text'],
            "sentiment": sentiment,
            "confidence": score
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nlp/entities', methods=['POST'])
def extract_entities():
    """استخراج الكيانات من النص (مبسط)"""
    try:
        data = request.json
        if 'text' not in data:
            return jsonify({"error": "Missing required field: text"}), 400
        
        # استخراج بسيط للكيانات
        words = data['text'].split()
        entities = []
        for word in words:
            if word[0].isupper() and len(word) > 2:
                entities.append({"text": word, "label": "PERSON"})
        
        return jsonify({
            "text": data['text'],
            "entities": entities,
            "method": "simple"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nlp/summarize', methods=['POST'])
def summarize_text():
    """تلخيص النص (مبسط)"""
    try:
        data = request.json
        if 'text' not in data:
            return jsonify({"error": "Missing required field: text"}), 400
        
        max_length = data.get('max_length', 130)
        # تلخيص بسيط
        summary = data['text'][:max_length] + "..." if len(data['text']) > max_length else data['text']
        
        return jsonify({
            "original_text": data['text'],
            "summary": summary,
            "max_length": max_length
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nlp/features', methods=['POST'])
def extract_text_features():
    """استخراج ميزات النص"""
    try:
        data = request.json
        if 'text' not in data:
            return jsonify({"error": "Missing required field: text"}), 400
        
        features = ll.get_text_features(data['text'])
        
        return jsonify({
            "text": data['text'],
            "features": features
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nlp/compare', methods=['POST'])
def compare_texts():
    """مقارنة نصين"""
    try:
        data = request.json
        if 'text1' not in data or 'text2' not in data:
            return jsonify({"error": "Missing required fields: text1 and text2"}), 400
        
        method = data.get('method', 'tfidf')  # tfidf أو simple
        similarity = ll.compare_texts(data['text1'], data['text2'], method)
        
        return jsonify({
            "text1": data['text1'],
            "text2": data['text2'],
            "similarity": float(similarity),
            "method": method
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nlp/analyze', methods=['POST'])
def analyze_text():
    """تحليل شامل للنص"""
    try:
        data = request.json
        if 'text' not in data:
            return jsonify({"error": "Missing required field: text"}), 400
        
        report = ll.generate_text_summary_report(data['text'])
        
        return jsonify({
            "text": data['text'],
            "analysis": report
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 8000
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port) 