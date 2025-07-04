"use strict";

angular.module("app.projectDatas").factory("dynamicForm", [function () {

    var dynamicForm = {};

    /**
     * Form fields for dynamic form
     * @type {*[]}
     */
    dynamicForm.dynamicFormFields = [
        {
            algoName: "Simple Linear Regression",
            fields: [
                {
                    type: "radio",
                    name: "fit_intercept",
                    label: "fit_intercept",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "normalize",
                    label: "normalize",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "copy_X",
                    label: "copy_X",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                }
            ]
        },
        {
            algoName: "Polynomial Regression",
            fields: [
                {type: "number", name: "degree", label: "degree", required: false, data: 2},
                {
                    type: "radio",
                    name: "interaction_only",
                    label: "interaction_only",
                    required: true,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "include_bias",
                    label: "include_bias",
                    required: true,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
            ]
        },
        {
            algoName: "SV Regression",
            fields: [
                {type: "number", name: "C", label: "C", required: false, data: 1.0},
                {type: "number", name: "epsilon", label: "epsilon", required: false, data: 0.1},
                {
                    type: "select",
                    name: "kernel",
                    label: "kernel",
                    required: true,
                    data: "rbf",
                    select_options: [
                        {option_label: "rbf", value: "rbf",},
                        {option_label: "linear", value: "linear"},
                        {option_label: "poly", value: "poly"},
                        {option_label: "sigmoid", value: "sigmoid"}
                    ],
                    placeholder_text:"Select kernal",
                    sub_ui_elemets:[
                        {type: "text", name: "gamma", label: "gamma", required: false, display_if:"rbf",data: 5,display_for:["rbf","poly","sigmoid"]}
                    ]
                },
                {type: "number", name: "degree", label: "degree", required: false, data: 3},
                {type: "number", name: "coef0", label: "coef0", required: false, data: 0.0},
                {
                    type: "radio",
                    name: "shrinking",
                    label: "shrinking",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "tol", label: "tol", required: false, data: 0.0},
                {type: "number", name: "cache_size", label: "cache_size", required: false, data: 0},
                {
                    type: "radio",
                    name: "verbose",
                    label: "verbose",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "max_iter", label: "max_iter", required: false, data: -1}
            ]
        },
        {
            algoName: "Decision Tree Regression",
            fields: [
                {
                    type: "select",
                    name: "criterion",
                    label: "criterion",
                    required: false,
                    data: "mse",
                    select_options: [
                        {option_label: "mse", value: "mse",},
                        {option_label: "friedman_mse", value: "friedman_mse"},
                        {option_label: "mae", value: "mae"},
                    ]
                },
                {
                    type: "radio",
                    name: "splitter",
                    label: "splitter",
                    required: false,
                    data: "best",
                    radio_btns: [{radio_label: "best", value: "best"}, {radio_label: "random", value: "random"}]
                },
                {type: "text", name: "max_depth", label: "max_depth", required: false, data: "None"},
                {type: "number", name: "min_samples_split", label: "min_samples_split", required: false, data: 2},
                {type: "number", name: "min_samples_leaf", label: "min_samples_leaf", required: false, data: 1},
                {type: "number", name: "min_weight_fraction_leaf", label: "min_weight_fraction_leaf", required: false, data: 0},
                {type: "text", name: "max_features", label: "max_features", required: false, data: "None"},
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None"},
                {type: "text", name: "max_leaf_nodes", label: "max_leaf_nodes", required: false, data: "None"},
                {type: "number", name: "min_impurity_decrease", label: "min_impurity_decrease", required: false, data: 0},
                {
                    type: "radio",
                    name: "presort",
                    label: "presort",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                }
            ]
        },
        {
            algoName: "Random Forest Regression",
            fields: [
                {type: "number", name: "n_estimators", label: "n_estimators", required: false, data: 10},
                {
                    type: "radio",
                    name: "criterion",
                    label: "criterion",
                    required: false,
                    data: "mse",
                    radio_btns: [{radio_label: "mse", value: "mse"}, {radio_label: "mae", value: "mae"}]
                },
                {type: "text", name: "max_features", label: "max_features", required: false, data: "None"},
                {type: "text", name: "max_depth", label: "max_depth", required: false, data: "None"},
                {type: "number", name: "min_samples_split", label: "min_samples_split", required: false, data: 2},
                {type: "number", name: "min_samples_leaf", label: "min_samples_leaf", required: false, data: 1},
                {type: "number", name: "min_weight_fraction_leaf", label: "min_weight_fraction_leaf", required: false, data: 0},
                {type: "text", name: "max_leaf_nodes", label: "max_leaf_nodes", required: false, data: "None"},
                {type: "number", name: "min_impurity_decrease", label: "min_impurity_decrease", required: false, data: 0},
                {
                    type: "radio",
                    name: "bootstrap",
                    label: "bootstrap",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "oob_score",
                    label: "oob_score",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None"},
                {type: "number", name: "verbose", label: "verbose", required: false, data: 0},
                {
                    type: "radio",
                    name: "warm_start",
                    label: "warm_start",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                }
            ]
        },
        {
            algoName: "KNN Classification",
            fields: [
                {type: "number", name: "n_neighbors", label: "n_neighbors", required: false, data: 5},
                {
                    type: "select",
                    name: "weights",
                    label: "weights",
                    required: true,
                    data: "uniform",
                    select_options: [
                        {option_label: "uniform", value: "uniform",},
                        {option_label: "distance", value: "distance"}
                    ]
                },
                {
                    type: "select",
                    name: "algorithm",
                    label: "algorithm",
                    required: true,
                    data: "auto",
                    select_options: [
                        {option_label: "auto", value: "auto"},
                        {option_label: "ball_tree", value: "ball_tree"},
                        {option_label: "kd_tree", value: "kd_tree"},
                        {option_label: "brute", value: "brute"}
                    ]
                },
                {type: "number", name: "leaf_size", label: "leaf_size", required: false, data: 30},
                {type: "number", name: "p", label: "p", required: false, data: 2},
                {type: "text", name: "metric", label: "metric", required: false, data: "minkowski"},
                {type: "text", name: "metric_params", label: "metric_params", required: false, data: "None"}
            ]
        },
        {
            algoName: "SVM Classification",
            fields: [
                {type: "number", name: "C", label: "C", required: false, data: 1.0},
                {
                    type: "select",
                    name: "kernel",
                    label: "kernel",
                    required: true,
                    data: "rbf",
                    select_options: [
                        {option_label: "rbf", value: "rbf",},
                        {option_label: "linear", value: "linear"},
                        {option_label: "poly", value: "poly"},
                        {option_label: "sigmoid", value: "sigmoid"}
                    ],
                    placeholder_text:"Select kernal",
                    sub_ui_elemets:[
                        {type: "text", name: "gamma", label: "gamma", required: false, display_if:"rbf",data: 5,display_for:["rbf","poly","sigmoid"]}
                    ]
                },
                {type: "number", name: "degree", label: "degree", required: false, data: 3},
                {type: "number", name: "coef0", label: "coef0", required: false, data: 0.0},
                {
                    type: "radio",
                    name: "probability",
                    label: "probability",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "shrinking",
                    label: "shrinking",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "tol", label: "tol", required: false, data: 0.0},
                {type: "number", name: "cache_size", label: "cache_size", required: false, data: 0},
                {type: "text", name: "class_weight", label: "class_weight", required: false, data: "None"},
                {
                    type: "radio",
                    name: "verbose",
                    label: "verbose",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "max_iter", label: "max_iter", required: false, data: -1},
                {
                    type: "radio",
                    name: "decision_function_shape",
                    label: "decision_function_shape",
                    required: false,
                    data: "ovr",
                    radio_btns: [{radio_label: "ovr", value: "ovr"}, {radio_label: "ovo", value: "ovo"}]
                },
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None"}
            ]
        },
        {
            algoName: "Logistic Regression",
            fields: [
                {type: "text", name: "penalty", label: "penalty", required: false, data: "l2"},
                {
                    type: "radio",
                    name: "dual",
                    label: "dual",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "tol", label: "tol", required: false, data: 0.0001},
                {type: "number", name: "C", label: "C", required: false, data: 1.0},
                {
                    type: "radio",
                    name: "fit_intercept",
                    label: "fit_intercept",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "intercept_scaling", label: "intercept_scaling", required: false, data: 1},
                {type: "text", name: "class_weight", label: "class_weight", required: false, data: "None"},
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None"},
                {type: "text", name: "solver", label: "solver", required: false, data: "liblinear"},
                {type: "number", name: "max_iter", label: "max_iter", required: false, data: 100},
                {type: "text", name: "multi_class", label: "multi_class", required: false, data: "ovr"},
                {type: "number", name: "verbose", label: "verbose", required: false, data: 0},
                {
                    type: "radio",
                    name: "warm_start",
                    label: "warm_start",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                }
            ]
        },
        {
            algoName: "Gaussian NB Classification",
            fields: [
                {type: "text", name: "priors", label: "priors", required: false, data: "None"},
            ]
        },
        {
            algoName: "Random Forest Classification",
            fields: [
                {type: "number", name: "n_estimators", label: "n_estimators", required: false, data: 10},
                {type: "text", name: "criterion", label: "criterion", required: false, data: "gini"},
                {type: "text", name: "max_features", label: "max_features", required: false, data: "auto"},
                {type: "text", name: "max_depth", label: "max_depth", required: false, data: "None"},
                {type: "number", name: "min_samples_split", label: "min_samples_split", required: false, data: 2},
                {type: "number", name: "min_samples_leaf", label: "min_samples_leaf", required: false, data: 1},
                {type: "number", name: "min_weight_fraction_leaf", label: "min_weight_fraction_leaf", required: false, data: 0},
                {type: "text", name: "max_leaf_nodes", label: "max_leaf_nodes", required: false, data: "None"},
                {type: "number", name: "min_impurity_decrease", label: "min_impurity_decrease", required: false, data: 0},
                {
                    type: "radio",
                    name: "bootstrap",
                    label: "bootstrap",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "oob_score",
                    label: "oob_score",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None"},
                {type: "number", name: "verbose", label: "verbose", required: false, data: 0},
                {
                    type: "radio",
                    name: "warm_start",
                    label: "warm_start",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "text", name: "class_weight", label: "class_weight", required: false, data: "None"}
            ]
        },
        {
            algoName: "Decision Tree Classification",
            fields: [
                {type: "text", name: "criterion", label: "criterion", required: false, data: "gini"},
                {type: "text", name: "splitter", label: "splitter", required: false, data: "best"},
                {type: "text", name: "max_depth", label: "max_depth", required: false, data: "None"},
                {type: "number", name: "min_samples_split", label: "min_samples_split", required: false, data: 2},
                {type: "number", name: "min_samples_leaf", label: "min_samples_leaf", required: false, data: 1},
                {type: "number", name: "min_weight_fraction_leaf", label: "min_weight_fraction_leaf", required: false, data: 0},
                {type: "text", name: "max_features", label: "max_features", required: false, data: "None"},
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None"},
                {type: "text", name: "max_leaf_nodes", label: "max_leaf_nodes", required: false, data: "None"},
                {type: "number", name: "min_impurity_decrease", label: "min_impurity_decrease", required: false, data: 0},
                {type: "text", name: "class_weight", label: "class_weight", required: false, data: "None"},
                {
                    type: "radio",
                    name: "presort",
                    label: "presort",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                }
            ]
        },
        {
            algoName: "SGD Regression",
            fields: [
                {type: "text", name: "loss", label: "loss", required: false, data: "squared_loss"},
                {type: "text", name: "penalty", label: "penalty", required: false, data: "l2"},
                {type: "number", name: "alpha", label: "alpha", required: false, data: 0.0001},
                {type: "number", name: "l1_ratio", label: "l1_ratio", required: false, data: 0.15},
                {
                    type: "radio",
                    name: "fit_intercept",
                    label: "fit_intercept",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "max_iter", label: "max_iter", required: false, data: 1000},
                {type: "number", name: "tol", label: "tol", required: false, data: 0.0183},
                {
                    type: "radio",
                    name: "shuffle",
                    label: "shuffle",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "verbose", label: "verbose", required: false, data: 0},
                {type: "number", name: "epsilon", label: "epsilon", required: false, data: 0},
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None"},
                {
                    type: "select",
                    name: "learning_rate",
                    label: "learning_rate",
                    required: true,
                    data: "optimal",
                    select_options: [
                        {option_label: "constant", value: "constant"},
                        {option_label: "optimal", value: "optimal"},
                        {option_label: "invscaling", value: "invscaling"}
                    ],
                    placeholder_text:"Select solver"
                },
                {type: "number", name: "eta0", label: "eta0", required: false, data: 0.01},
                {type: "number", name: "power_t", label: "power_t", required: false, data: 0.25},
                {
                    type: "radio",
                    name: "warm_start",
                    label: "warm_start",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "average",
                    label: "average",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "text", name: "n_iter", label: "n_iter", required: false, data: "None"}
            ]
        },{
            algoName: "Ridge Regression",
            fields: [
                {type: "number", name: "alpha", label: "alpha", required: false, data: 1.0},
                {
                    type: "radio",
                    name: "fit_intercept",
                    label: "fit_intercept",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "normalize",
                    label: "normalize",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "copy_X",
                    label: "copy_X",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "max_iter", label: "max_iter", required: false, data: 1000},
                {type: "number", name: "tol", label: "tol", required: false, data: 0.001},
                {
                    type: "select",
                    name: "solver",
                    label: "solver",
                    required: true,
                    data: "auto",
                    select_options: [
                        {option_label: "auto", value: "auto"},
                        {option_label: "svd", value: "svd"},
                        {option_label: "cholesky", value: "cholesky"},
                        {option_label: "lsqr", value: "lsqr"},
                        {option_label: "sparse_cg", value: "sparse_cg"},
                        {option_label: "sag", value: "sag"},
                        {option_label: "saga", value: "saga"}
                    ],
                    placeholder_text:"Select solver"
                },
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None", placeholder_text:"None or Integer"}
            ]
        }
        ,{
            algoName: "Lasso Regression",
            fields: [
                {type: "number", name: "alpha", label: "alpha", required: false, data: 1.0},
                {
                    type: "radio",
                    name: "fit_intercept",
                    label: "fit_intercept",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "normalize",
                    label: "normalize",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "precompute",
                    label: "precompute",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "copy_X",
                    label: "copy_X",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "max_iter", label: "max_iter", required: false, data: 100},
                {type: "number", name: "tol", label: "tol", required: false, data: 0.0001},
                {
                    type: "radio",
                    name: "warm_start",
                    label: "warm_start",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "positive",
                    label: "positive",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None"},
                {type: "text", name: "selection", label: "selection", required: false, data: "cyclic"},
            ]
        },
        {
            algoName: "ElasticNet Regression",
            fields: [
                {type: "number", name: "alpha", label: "alpha", required: false, data: 1.0},
                {type: "number", name: "l1_ratio", label: "l1_ratio", required: false, data: 0.5},
                {
                    type: "radio",
                    name: "fit_intercept",
                    label: "fit_intercept",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "normalize",
                    label: "normalize",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "precompute",
                    label: "precompute",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "copy_X",
                    label: "copy_X",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "max_iter", label: "max_iter", required: false, data: 100},
                {type: "number", name: "tol", label: "tol", required: false, data: 0.0001},
                {
                    type: "radio",
                    name: "warm_start",
                    label: "warm_start",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "positive",
                    label: "positive",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None"},
                {type: "text", name: "selection", label: "selection", required: false, data: "cyclic"},
            ]
        },
        {
            algoName: "Passive Aggressive Regression",
            fields: [
                {type: "number", name: "C", label: "C", required: false, data: 1.0},
                {
                    type: "radio",
                    name: "fit_intercept",
                    label: "fit_intercept",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "max_iter", label: "max_iter", required: false, data: 5},
                {type: "number", name: "tol", label: "tol", required: false, data: 0.001},
                {
                    type: "radio",
                    name: "shuffle",
                    label: "shuffle",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "verbose", label: "verbose", required: false, data: 0},
                {
                    type: "select",
                    name: "loss",
                    label: "loss",
                    required: true,
                    data: "epsilon_insensitive",
                    select_options: [
                        {option_label: "epsilon_insensitive", value: "epsilon_insensitive"},
                        {option_label: "squared_epsilon_insensitive", value: "squared_epsilon_insensitive"}
                    ],
                    placeholder_text:"Select loss"
                },
                {type: "number", name: "epsilon", label: "epsilon", required: false, data: 0.1},
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None"},
                {
                    type: "radio",
                    name: "warm_start",
                    label: "warm_start",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "average",
                    label: "average",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "n_iter", label: "n_iter", required: false, data: 0.21}
            ]
        },
        {
            algoName: "Huber Regression",
            fields: [
                {type: "number", name: "epsilon", label: "epsilon", required: false, data: 1.35},
                {type: "number", name: "max_iter", label: "max_iter", required: false, data: 100},
                {type: "number", name: "alpha", label: "alpha", required: false, data: 0.0001},
                {
                    type: "radio",
                    name: "warm_start",
                    label: "warm_start",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "fit_intercept",
                    label: "fit_intercept",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "tol", label: "tol", required: false, data: 0.006}
            ]
        },
        {
            algoName: "ARD Regression",
            fields: [
                {type: "number", name: "n_iter", label: "n_iter", required: false, data: 300},
                {type: "number", name: "tol", label: "tol", required: false, data: 0.049},
                {type: "number", name: "alpha_1", label: "alpha_1", required: false, data: 0.002},
                {type: "number", name: "alpha_2", label: "alpha", required: false, data: 0.002},
                {type: "number", name: "lambda_1", label: "lambda_1", required: false, data: 0.002},
                {type: "number", name: "lambda_2", label: "lambda_2", required: false, data: 0.002},
                {type: "number", name: "threshold_lambda", label: "threshold_lambda", required: false, data: 54.598},
                {
                    type: "radio",
                    name: "fit_intercept",
                    label: "fit_intercept",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "compute_score",
                    label: "compute_score",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "normalize",
                    label: "normalize",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "copy_X",
                    label: "copy_X",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "verbose",
                    label: "verbose",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                }
            ]
        },
        {
            algoName: "MLP Regression",
            fields: [
                {type: "text", name: "hidden_layer_sizes", label: "hidden_layer_sizes", required: false, data: 100},
                {type: "text", name: "activation", label: "activation", required: false, data: "relu"},
                {
                    type: "select",
                    name: "activation",
                    label: "activation",
                    required: true,
                    data: "relu",
                    select_options: [
                        {option_label: "identity", value: "identity"},
                        {option_label: "logistic", value: "logistic"},
                        {option_label: "tanh", value: "tanh"},
                        {option_label: "relu", value: "relu"},
                    ],
                    placeholder_text:"Select activation"
                },
                {
                    type: "select",
                    name: "solver",
                    label: "solver",
                    required: true,
                    data: "adam",
                    select_options: [
                        {option_label: "lbfgs", value: "lbfgs"},
                        {option_label: "sgd", value: "sgd"},
                        {option_label: "adam", value: "adam"},
                    ],
                    placeholder_text:"Select solver"
                },
                {type: "number", name: "beta_1", label: "beta_1", required: false,data: 0.9},
                {type: "number", name: "beta_2", label: "beta_2", required: false,data: 0.999},
                {type: "number", name: "epsilon", label: "epsilon", required: false,data: 0.0003},
                {type: "number", name: "alpha", label: "alpha", required: false, data: 0.0001},
                {type: "text", name: "batch_size", label: "batch_size", required: false, data: "auto"},
                {type: "text", name: "learning_rate", label: "learning_rate", required: false, data: "constant"},
                {type: "number", name: "learning_rate_init", label: "learning_rate_init", required: false, data: 0.001},
                {type: "number", name: "power_t", label: "power_t", required: false, data: 0.5},
                {type: "number", name: "max_iter", label: "max_iter", required: false, data: 200},
                {
                    type: "radio",
                    name: "shuffle",
                    label: "shuffle",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None"},
                {type: "number", name: "tol", label: "tol", required: false, data: 0.018},
                {
                    type: "radio",
                    name: "verbose",
                    label: "verbose",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "warm_start",
                    label: "warm_start",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "momentum", label: "momentum", required: false, data: 0.9},
                {
                    type: "radio",
                    name: "nesterovs_momentum",
                    label: "nesterovs_momentum",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "early_stopping",
                    label: "early_stopping",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "validation_fraction", label: "validation_fraction", required: false, data: 0.1}
            ]
        },
        {
            algoName: "Kernel Ridge Regression",
            fields: [
                {type: "number", name: "alpha", label: "alpha", required: false, data: 1},
                {
                    type: "select",
                    name: "kernel",
                    label: "kernel",
                    required: true,
                    data: "linear",
                    select_options: [
                        {option_label: "linear", value: "linear"},
                        {option_label: "poly", value: "poly"},
                        {option_label: "rbf", value: "rbf"},
                        {option_label: "sigmoid", value: "sigmoid"}
                    ],
                    placeholder_text:"Select kernel"
                },
                {type: "text", name: "gamma", label: "alpha_1", required: false, data: "None"},
                {type: "number", name: "degree", label: "degree", required: false, data: 3},
                {type: "number", name: "coef0", label: "coef0", required: false, data: 1},
                {type: "text", name: "kernel_params", label: "kernel_params", required: false, data: "None"}
            ]
        },
        {
            algoName: "LassoLARS Regression",
            fields: [
                {type: "number", name: "alpha", label: "alpha", required: false, data: 1.0},
                {
                    type: "radio",
                    name: "fit_intercept",
                    label: "fit_intercept",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "verbose",
                    label: "verbose",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "normalize",
                    label: "normalize",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "select",
                    name: "precompute",
                    label: "precompute",
                    required: true,
                    data: "auto",
                    select_options: [
                        {option_label: "auto", value: "auto"},
                        {option_label: "True", value: true},
                        {option_label: "False", value: false}
                    ],
                    placeholder_text:"Select precompute"
                },
                {type: "text", name: "max_iter", label: "max_iter", required: false, data: 100},
                {type: "text", name: "eps", label: "eps", required: false, data: "2.220446049250313e-16"},
                {
                    type: "radio",
                    name: "copy_X",
                    label: "copy_X",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "fit_path",
                    label: "fit_path",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "positive",
                    label: "positive",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                }
            ]
        },
        {
            algoName: "Ridge CV Regression",
            fields: [
                {type: "text", name: "alphas", label: "alphas", required: false, data: "0.1, 1.0, 10.0"},
                {
                    type: "radio",
                    name: "fit_intercept",
                    label: "fit_intercept",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "normalize",
                    label: "normalize",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "text", name: "scoring", label: "scoring", required: false, data: "None"},
                {type: "text", name: "cv", label: "cv", required: false, data: "None"},
                {
                    type: "select",
                    name: "gcv_mode",
                    label: "gcv_mode",
                    required: true,
                    data: "auto",
                    select_options: [
                        {option_label: "auto", value: "auto"},
                        {option_label: "svd", value: "svd"},
                        {option_label: "eigen", value: "eigen"}
                    ],
                    placeholder_text:"Select gcv_mode",
                    sub_ui_elemets:[]
                },
                {
                    type: "radio",
                    name: "store_cv_values",
                    label: "store_cv_values",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                }
            ]
        },
        {
            algoName: "Bayesian Ridge Regression",
            fields: [
                {type: "number", name: "n_iter", label: "n_iter", required: false, data: 300},
                {type: "number", name: "tol", label: "tol", required: false, data: 0.049},
                {type: "number", name: "alpha_1", label: "alpha_1", required: false, data: 0.0024},
                {type: "number", name: "alpha_2", label: "alpha_2", required: false, data: 0.0024},
                {type: "number", name: "lambda_1", label: "lambda_1", required: false, data: 0.0024},
                {type: "number", name: "lambda_2", label: "lambda_2", required: false, data: 0.0024},
                {
                    type: "radio",
                    name: "compute_score",
                    label: "compute_score",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "fit_intercept",
                    label: "fit_intercept",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "normalize",
                    label: "normalize",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "copy_X",
                    label: "copy_X",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "verbose",
                    label: "verbose",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                }
            ]
        },
        {
            algoName: "TheilSen Regression",
            fields: [
                {
                    type: "radio",
                    name: "fit_intercept",
                    label: "fit_intercept",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "copy_X",
                    label: "copy_X",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "max_subpopulation", label: "max_subpopulation", required: false, data: 54.598},
                {type: "text", name: "n_subsamples", label: "n_subsamples", required: false, data: "None"},
                {type: "number", name: "max_iter", label: "max_iter", required: false, data: 300},
                {type: "number", name: "tol", label: "tol", required: false, data: 0.0001},
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None"},
                {
                    type: "radio",
                    name: "verbose",
                    label: "verbose",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                }
            ]
        },
        {
            algoName: "nuSV Regression",
            fields: [
                {type: "number", name: "C", label: "C", required: false, data: 1.0},
                {type: "number", name: "nu", label: "nu", required: false, data: 0.5},
                {
                    type: "select",
                    name: "kernel",
                    label: "kernel",
                    required: true,
                    data: "rbf",
                    select_options: [
                        {option_label: "linear", value: "linear"},
                        {option_label: "poly", value: "poly"},
                        {option_label: "rbf", value: "rbf"},
                        {option_label: "sigmoid", value: "sigmoid"},
                        {option_label: "precomputed", value: "precomputed"}
                    ],
                    placeholder_text:"Select kernel"
                },
                {type: "text", name: "gamma", label: "gamma", required: false, data: "auto"},
                {type: "number", name: "degree", label: "degree", required: false, data: 3},
                {type: "number", name: "coef0", label: "coef0", required: false, data: 0.0},
                {
                    type: "radio",
                    name: "shrinking",
                    label: "shrinking",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "tol", label: "tol", required: false, data: 0.049},
                {
                    type: "radio",
                    name: "verbose",
                    label: "verbose",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "max_iter", label: "max_iter", required: false, data: -1}
            ]
        },
        {
            algoName: "Extra Tree Classification",
            fields: [
                {type: "text", name: "criterion", label: "criterion", required: false, data: "gini"},
                {type: "text", name: "splitter", label: "splitter", required: false, data: "best"},
                {type: "text", name: "max_depth", label: "max_depth", required: false, data: "None"},
                {type: "number", name: "min_samples_split", label: "min_samples_split", required: false, data: 2},
                {type: "number", name: "min_samples_leaf", label: "min_samples_leaf", required: false, data: 1},
                {type: "number", name: "min_weight_fraction_leaf", label: "min_weight_fraction_leaf", required: false, data: 0},
                {type: "text", name: "max_features", label: "max_features", required: false, data: "None"},
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None"},
                {type: "text", name: "max_leaf_nodes", label: "max_leaf_nodes", required: false, data: "None"},
                {type: "number", name: "min_impurity_decrease", label: "min_impurity_decrease", required: false, data: 0},
                {type: "text", name: "class_weight", label: "class_weight", required: false, data: "None"}
            ]
        },
        {
            algoName: "Ensemble Extra Trees Classification",
            fields: [
                {type: "number", name: "n_estimators", label: "n_estimators", required: false, data: 10},
                {type: "text", name: "criterion", label: "criterion", required: false, data: "gini"},
                {type: "text", name: "max_features", label: "max_features", required: false, data: "auto"},
                {type: "text", name: "max_depth", label: "max_depth", required: false, data: "None"},
                {type: "number", name: "min_samples_split", label: "min_samples_split", required: false, data: 2},
                {type: "number", name: "min_samples_leaf", label: "min_samples_leaf", required: false, data: 1},
                {type: "number", name: "min_weight_fraction_leaf", label: "min_weight_fraction_leaf", required: false, data: 0},
                {type: "text", name: "max_leaf_nodes", label: "max_leaf_nodes", required: false, data: "None"},
                {type: "number", name: "min_impurity_decrease", label: "min_impurity_decrease", required: false, data: 0},
                {
                    type: "radio",
                    name: "bootstrap",
                    label: "bootstrap",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "oob_score",
                    label: "oob_score",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None"},
                {type: "number", name: "verbose", label: "verbose", required: false, data: 0},
                {
                    type: "radio",
                    name: "warm_start",
                    label: "warm_start",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "text", name: "class_weight", label: "class_weight", required: false, data: "None"}
            ]
        },
        {
            algoName: "Ensemble Extra Trees Classification",
            fields: [
                {type: "number", name: "n_estimators", label: "n_estimators", required: false, data: 10},
                {type: "text", name: "criterion", label: "criterion", required: false, data: "gini"},
                {type: "text", name: "max_features", label: "max_features", required: false, data: "auto"},
                {type: "text", name: "max_depth", label: "max_depth", required: false, data: "None"},
                {type: "number", name: "min_samples_split", label: "min_samples_split", required: false, data: 2},
                {type: "number", name: "min_samples_leaf", label: "min_samples_leaf", required: false, data: 1},
                {type: "number", name: "min_weight_fraction_leaf", label: "min_weight_fraction_leaf", required: false, data: 0},
                {type: "text", name: "max_leaf_nodes", label: "max_leaf_nodes", required: false, data: "None"},
                {type: "number", name: "min_impurity_decrease", label: "min_impurity_decrease", required: false, data: 0},
                {
                    type: "radio",
                    name: "bootstrap",
                    label: "bootstrap",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "oob_score",
                    label: "oob_score",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None"},
                {type: "number", name: "verbose", label: "verbose", required: false, data: 0},
                {
                    type: "radio",
                    name: "warm_start",
                    label: "warm_start",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "text", name: "class_weight", label: "class_weight", required: false, data: "None"}
            ]
        },
        {
            algoName: "MLP Classification",
            fields: [
                {type: "text", name: "hidden_layer_sizes", label: "hidden_layer_sizes", required: false, data: 100},
                {
                    type: "select",
                    name: "activation",
                    label: "activation",
                    required: true,
                    data: "relu",
                    select_options: [
                        {option_label: "identity", value: "identity"},
                        {option_label: "logistic", value: "logistic"},
                        {option_label: "tanh", value: "tanh"},
                        {option_label: "relu", value: "relu"},
                    ],
                    placeholder_text:"Select activation",
                    sub_ui_elemets:[]
                },
                {
                    type: "select",
                    name: "solver",
                    label: "solver",
                    required: true,
                    data: "adam",
                    select_options: [
                        {option_label: "lbfgs", value: "lbfgs"},
                        {option_label: "sgd", value: "sgd"},
                        {option_label: "adam", value: "adam"},
                    ],
                    placeholder_text:"Select solver"
                },
                {type: "number", name: "beta_1", label: "beta_1", required: false,data: 0.9},
                {type: "number", name: "beta_2", label: "beta_2", required: false,data: 0.999},
                {type: "number", name: "epsilon", label: "epsilon", required: false,data: 0.0003},
                {type: "number", name: "alpha", label: "alpha", required: false, data: 0.0001},
                {type: "text", name: "batch_size", label: "batch_size", required: false, data: "auto"},
                {
                    type: "select",
                    name: "learning_rate",
                    label: "learning_rate",
                    required: true,
                    data: "constant",
                    select_options: [
                        {option_label: "constant", value: "constant"},
                        {option_label: "invscaling", value: "invscaling"},
                        {option_label: "adaptive", value: "adaptive"}
                    ],
                    placeholder_text:"Select learning_rate",
                    sub_ui_elemets:[]
                },
                {type: "number", name: "learning_rate_init", label: "learning_rate_init", required: false, data: 0.001},
                {type: "number", name: "power_t", label: "power_t", required: false, data: 0.5},
                {type: "number", name: "max_iter", label: "max_iter", required: false, data: 200},
                {
                    type: "radio",
                    name: "shuffle",
                    label: "shuffle",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None"},
                {type: "number", name: "tol", label: "tol", required: false, data: 0.018},
                {
                    type: "radio",
                    name: "verbose",
                    label: "verbose",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "warm_start",
                    label: "warm_start",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "momentum", label: "momentum", required: false, data: 0.9},
                {
                    type: "radio",
                    name: "nesterovs_momentum",
                    label: "nesterovs_momentum",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "early_stopping",
                    label: "early_stopping",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "validation_fraction", label: "validation_fraction", required: false, data: 0.1}
            ]
        },
        {
            algoName: "Nearest Centroid Classification",
            fields: [
                {
                    type: "select",
                    name: "metric",
                    label: "metric",
                    required: true,
                    data: "euclidean",
                    select_options: [
                        {option_label: "euclidean", value: "euclidean"},
                        {option_label: "manhattan", value: "manhattan"},
                        {option_label: "minkowski", value: "minkowski"},
                        {option_label: "mahalanobis", value: "mahalanobis"},
                    ],
                    placeholder_text:"Select metric",
                    sub_ui_elemets:[]
                },
                {type: "text", name: "shrink_threshold", label: "shrink_threshold", required: false, data: "None"}
            ]
        },
        {
            algoName: "Ridge Classification",
            fields: [
                {type: "number", name: "alpha", label: "alpha", required: false, data: 1.0},
                {
                    type: "radio",
                    name: "fit_intercept",
                    label: "fit_intercept",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "normalize",
                    label: "normalize",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "copy_X",
                    label: "copy_X",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "text", name: "max_iter", label: "max_iter", required: false, data: "None"},
                {type: "number", name: "tol", label: "tol", required: false, data: 0.001},
                {type: "text", name: "class_weight", label: "class_weight", required: false, data: "None"},
                {
                    type: "select",
                    name: "solver",
                    label: "solver",
                    required: true,
                    data: "auto",
                    select_options: [
                        {option_label: "auto", value: "auto"},
                        {option_label: "svd", value: "svd"},
                        {option_label: "cholesky", value: "cholesky"},
                        {option_label: "lsqr", value: "lsqr"},
                        {option_label: "sparse_cg", value: "sparse_cg"},
                        {option_label: "sag", value: "sag"},
                        {option_label: "saga", value: "saga"}
                    ],
                    placeholder_text:"Select solver",
                    sub_ui_elemets:[]
                },
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None"}
            ]
        },
        {
            algoName: "Ridge Classification with Cross Validation",
            fields: [
                {type: "text", name: "alphas", label: "alphas", required: false, data: "0.1,1.0,10.0"},
                {
                    type: "radio",
                    name: "fit_intercept",
                    label: "fit_intercept",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "radio",
                    name: "normalize",
                    label: "normalize",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "text", name: "scoring", label: "scoring", required: false, data: "None"},
                {type: "text", name: "cv", label: "cv", required: false, data: "None"},
                {type: "text", name: "class_weight", label: "class_weight", required: false, data: "None"}
            ]
        },
        {
            algoName: "Logistic Regression with Cross Validation",
            fields: [
                {type: "number", name: "Cs", label: "Cs", required: false, data: 10},
                {
                    type: "radio",
                    name: "fit_intercept",
                    label: "fit_intercept",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "cv", label: "cv", required: false, data: 3},
                {
                    type: "radio",
                    name: "dual",
                    label: "dual",
                    required: false,
                    data: false,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {
                    type: "select",
                    name: "penalty",
                    label: "penalty",
                    required: true,
                    data: "l2",
                    select_options: [
                        {option_label: "l1", value: "l1"},
                        {option_label: "l2", value: "l2"}
                    ],
                    placeholder_text:"Select penalty",
                    sub_ui_elemets:[]
                },
                {type: "text", name: "scoring", label: "scoring", required: false, data: "accuracy"},
                {
                    type: "select",
                    name: "solver",
                    label: "solver",
                    required: true,
                    data: "lbfgs",
                    select_options: [
                        {option_label: "newton-cg", value: "newton-cg"},
                        {option_label: "lbfgs", value: "lbfgs"},
                        {option_label: "liblinear", value: "liblinear"},
                        {option_label: "sag", value: "sag"},
                        {option_label: "saga", value: "saga"}
                    ],
                    placeholder_text:"Select solver",
                    sub_ui_elemets:[]
                },
                {type: "number", name: "tol", label: "tol", required: false, data: 0.001},
                {type: "number", name: "max_iter", label: "max_iter", required: false, data: 100},
                {type: "text", name: "class_weight", label: "class_weight", required: false, data: "None"},
                {type: "number", name: "verbose", label: "verbose", required: false, data: 5},
                {
                    type: "radio",
                    name: "refit",
                    label: "refit",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "intercept_scaling", label: "intercept_scaling", required: false, data: 1},
                {
                    type: "select",
                    name: "multi_class",
                    label: "multi_class",
                    required: true,
                    data: "ovr",
                    select_options: [
                        {option_label: "ovr", value: "ovr"},
                        {option_label: "multinomial", value: "multinomial"}
                    ],
                    placeholder_text:"Select solver",
                    sub_ui_elemets:[]
                },
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None"}
            ]
        },
        {
            algoName: "Passive Aggressive Classification",
            fields: [
                {type: "number", name: "C", label: "C", required: false, data: 1.0},
                {
                    type: "radio",
                    name: "fit_intercept",
                    label: "fit_intercept",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "max_iter", label: "max_iter", required: false, data: 100},
                {type: "number", name: "tol", label: "tol", required: false, data: 0.001},
                {
                    type: "radio",
                    name: "shuffle",
                    label: "shuffle",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "number", name: "verbose", label: "verbose", required: false, data: 5},
                {
                    type: "select",
                    name: "loss",
                    label: "loss",
                    required: true,
                    data: "hinge",
                    select_options: [
                        {option_label: "squared_hinge", value: "squared_hinge"},
                        {option_label: "hinge", value: "hinge"}
                    ],
                    placeholder_text:"Select solver",
                    sub_ui_elemets:[]
                },
                {type: "text", name: "random_state", label: "random_state", required: false, data: "None"},
                {
                    type: "radio",
                    name: "warm_start",
                    label: "warm_start",
                    required: false,
                    data: true,
                    radio_btns: [{radio_label: "true", value: true}, {radio_label: "false", value: false}]
                },
                {type: "text", name: "class_weight", label: "class_weight", required: false, data: "balanced"},
                {type: "text", name: "average", label: "average", required: false, data: 10},
                {type: "text", name: "n_iter", label: "n_iter", required: false, data: "None"}
            ]
        }
    ];

    /**
     *
     * @param algorithmName, pass the algorithm name
     */
    dynamicForm.getFormFields = function (hptDefaultPref,algorithmName) {
        return hptDefaultPref.filter(function (algoFormData) {
            return algoFormData.algoName == algorithmName;
        });
    };

    dynamicForm.test = function () {
        alert("Test");
    };
    return dynamicForm;

}]);
