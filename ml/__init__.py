# =============================================================================
# حزمة التعلم الآلي
# =============================================================================

from .models import (
    train_algorithm, save_model, load_model, get_available_algorithms,
    train_with_gridsearch, train_with_randomized_search, get_algorithm_info
)

from .data_utils import (
    load_data, split_data, preprocess_data, get_data_info, 
    validate_data, create_sample_data, save_sample_data
)

from .predict import (
    predict, predict_proba, evaluate, evaluate_classification,
    evaluate_regression, evaluate_clustering, cross_validate_model
)

from .nlp_utils import TextClassifier, TextPreprocessor

__version__ = "2.0.0"
__author__ = "ML System Team" 