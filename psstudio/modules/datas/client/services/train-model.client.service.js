"use strict";

angular.module("app.projectDatas").factory("ModelTraining", ["$resource",
  function ($resource) {
    this.startTraining = startTraining($resource);
    this.getCorrelation = getCorrelation($resource);
    this.getScatterGraphData = getScatterGraphData($resource);
    this.getAlgorithmList = getAlgorithmList();
    this.startReTraining  = startReTraining($resource);
    this.startNlpPreProcessing = startNlpPreProcessing($resource);
    this.findAlgo = findAlgo;
    this.startAdvTraining  = startAdvTraining($resource);
    function startTraining($resource){
      return $resource("api/projects/:projectId/trainmodel", {
        projectId: "@pId"
      }, {
        update: {
          method: "PUT"
        }
      });
    }
    function getCorrelation($resource){
      return $resource("api/projects/:projectId/trainmodel/correlation", {
        projectId: "@pId"
      }, {
        update: {
          method: "PUT"
        }
      });
    }
    function getScatterGraphData($resource){
      return $resource("api/projects/:projectId/graph/trainmodel/correlation?fname=:featureName&tname=:target", {
        projectId: "@pId"
      }, {
        update: {
          method: "PUT"
        }
      });
    }
    function startReTraining($resource){
      return $resource("api/projects/:projectId/retrainmodel/:modelId", {
        projectId: "@pId",
        modelId:"@modelId"
      }, {
        update: {
          method: "PUT"
        }
      });
    }
    function startAdvTraining($resource){
      return $resource("api/projects/:projectId/advtrainmodel/:modelId", {
        projectId: "@projectId",
        modelId:"@modelId"
      }, {
        update: {
          method: "PUT"
        }
      });
    }
    function getAlgorithmList(){
      return [
        {name:"Simple Linear Regression",type:"regression",multilabel:false,id:"1simple_linear_regression",url:"https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html"},
        {name:"Polynomial Regression",type:"regression",multilabel:false,id:"2polynomial_regression", url:"https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html"},
        // {name:'SV Regression',type:'regression',multilabel:false,id:'3sv_regression'},
        {name:"Decision Tree Regression",type:"regression",multilabel:false,id:"4decision_tree_regression", url:"https://scikit-learn.org/stable/auto_examples/tree/plot_tree_regression.html"},
        {name:"Random Forest Regression",type:"regression",multilabel:false,id:"5random_forest_regression", url:"https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html"},
        {name:"SGD Regression",type:"regression",multilabel:false,id:"6sgd_egression", url:"https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDRegressor.html"},
        {name:"Ridge Regression",type:"regression",multilabel:false,id:"7ridge_regression", url:"https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html"},
        {name:"Lasso Regression",type:"regression",multilabel:false,id:"8lasso_regression", url:"https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html"},
        {name:"ElasticNet Regression" , type:"regression",multilabel:false,id:"9elastic_net_regression", url:"https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html"},
        {name:"Passive Aggressive Regression",type:"regression",multilabel:false,id:"10passive_aggressive_regression", url:"https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.PassiveAggressiveRegressor.html"},
        // {name:'Huber Regression',type:'regression',multilabel:false,id:"11huber_regression"},
        {name:"ARD Regression",type:"regression",multilabel:false,id:"12ard_regression", url:"https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ARDRegression.html"},
        {name:"MLP Regression",type:"regression",multilabel:false,id:"13mlp_regression", url:"https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html"},
        {name:"Kernel Ridge Regression",type:"regression",multilabel:false,id:"14kernel_ridge_regression", url:"https://scikit-learn.org/stable/modules/generated/sklearn.kernel_ridge.KernelRidge.html"},
        {name:"nuSV Regression",type:"regression",multilabel:false,id:"15nusv_regression", url:"https://scikit-learn.org/stable/modules/generated/sklearn.svm.NuSVC.html"},
        {name:"LassoLARS Regression",type:"regression",multilabel:false,id:"16lasso_lars_regression", url:"https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LassoLars.html"},
        {name:"Ridge CV Regression",type:"regression",multilabel:false,id:"17ridge_cv_regression", url:"https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeCV.html"},
        {name:"Bayesian Ridge Regression",type:"regression",multilabel:false,id:"18bayesian_ridge_regression", url:"https://scikit-learn.org/stable/auto_examples/linear_model/plot_bayesian_ridge.html"},
        {name:"TheilSen Regression",type:"regression",multilabel:false,id:"19theil_sen_regression", url:"https://scikit-learn.org/stable/auto_examples/linear_model/plot_theilsen.html"},
        {name:"KNN Classification",type:"classification",multilabel:true,id:"20knn_classification", url:"https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html"},
        // {name:'SVM Classification',type:'classification',multilabel:false,id:"21svm_classification"},
        {name:"Logistic Regression",type:"classification",multilabel:false,id:"22logistic_regression", url:"https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html"},
        {name:"Gaussian NB Classification",type:"classification",multilabel:false,id:"23gaussian_nb_classification", url:"https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html"},
        {name:"Decision Tree Classification",type:"classification",multilabel:true,id:"24decision_tree_classification", url:"https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html"},
        {name:"Random Forest Classification",type:"classification",multilabel:true,id:"25random_forest_classification", url:"https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html"},
        {name:"Extra Tree Classification",type:"classification",multilabel:true,id:"26extra_tree_classification", url:"https://scikit-learn.org/stable/modules/generated/sklearn.tree.ExtraTreeClassifier.html"},
        {name:"Ensemble Extra Trees Classification",type:"classification",multilabel:true,id:"27ensemble_extra_trees_classification", url:"https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html"},
        {name:"MLP Classification",type:"classification",multilabel:true,id:"28mlp_classification", url:"https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html"},
        {name:"Nearest Centroid Classification",type:"classification",multilabel:false,id:"29nearest_centroid_classification", url:"https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestCentroid.html"},
        {name:"Ridge Classification",type:"classification",multilabel:false,id:"30ridge_classification", url:"https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeClassifier.html"},
        {name:"Ridge Classification with Cross Validation",type:"classification",multilabel:true,id:"31ridge_classification_with_cross_validation", url:"https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeClassifierCV.html"},
        {name:"Logistic Regression with Cross Validation",type:"classification",multilabel:false,id:"32logistic_regression_with_cross_validation", url:"https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegressionCV.html"},
        {name:"Passive Aggressive Classification" , type:"classification",multilabel:false,id:"33passive_aggressive_classification", url:"https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.PassiveAggressiveClassifier.html"},
        {name:"Artificial Neural Network Classification" , type:"classification",multilabel:false,id:"34artificial_neural_network_classification", url:"https://www.tensorflow.org/api_docs/python/tf/keras/wrappers/scikit_learn/KerasClassifier"},
        {name:"Artificial Neural Network Regression" , type:"regression",multilabel:false,id:"35artificial_neural_network_regression", url:"https://www.tensorflow.org/api_docs/python/tf/keras/wrappers/scikit_learn/KerasRegressor"}
      ];
    }
    function startNlpPreProcessing($resource){
      return $resource("api/projects/:projectId/nlp/preprocess", {
        projectId: "@pId"
      }, {
        update: {
          method: "PUT"
        }
      });
    }

    /**
     * Function will return the algorithm type if we pass the algorithm name
     * @param algorithmName , pass the algorithm name
     * @returns algorithm type,eg:regression/classification
       */
    function findAlgo(algorithmName){
      var algoType = getAlgorithmList().filter(function(algorithm){
        return algorithm.name == algorithmName;
      });
      return algoType[0];
    }
    return this;
  }
]);
