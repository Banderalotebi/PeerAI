## Predictsense 1.7.0 has been released with the following headline features:
- **Code Optimization**: Remove the redundant code for Preprocess, Multivariate, Hypothesis.
- **Preprocessing EDA**: Create each functions in preprocessing module for date handling, calculate datatypes, calculate missing values, calculate statistics, imputation, eda summary.
- **EDA Datatype Calculation**: Boolean:1. Number - contains unique value should be 2
                                        2. Text - contains True and False

                                Numeric:1. Number - contains category (int)
                                        2. Number - contains continuous value - int or float

                                Categorical:Text - Contains category except True and False

                                Date:1. Date - Contains only date
                                     2. Timestamp

                                Text - Contains text (unique values)
- **Python code optimization**: Python code optimization related changes for Preprocess, Multivariate, Hypothesis.
- **UI Changes**: Removal of histogram, Rename advance EDA to EDA report, Removal of P value score to progress bar in correlation, Scatter plot removal, Removal of activity bar and Provide a loader in Quick prediction while changing algorithms.
- **Add logger info**: Added logger info for all modules.
- **EDA- Unique values computation** : Calculate and show unique value for each column after EDA along with column name.
- **Treat balnk in EDA**: Treat blank space, n/a and NAN (any case) to null values.
- **Remove special charcter in table headers**: Convert any special chars to _ if present in column name/taable headers.
- **Tensorflow - ANN**: Added a new tensorflow algorithm for both regression and classification data.
- **Re-Engineering Kfold + Cross Validation**: Added validation strategy for calculating CV score under advance options. The new added strategies are stratified k fold, stratified shuffle split and timeseries split.


## Predictsense 1.6.0 has been released with the following headline features:
 - **Toolkit licensing**: Toolkit will be  expired based on the expiry date mentioned and number of predictions which ever condition meet first, it will get expired.
 - **Merge Api**: Add new data to existing data, it can be a single data or a complete dataset file.
 - **Python modules obfuscation**: Enhance obfuscation logic for python modules based on the new file structure.
 - **Ps_Core architechture**: Maintain proper flask file structure.
 - **Licensing**: User will require a license file to run predictsense. License is done base on number of projects, number of user, number of trainings per project and expiry date. Whichever condition meets first, predictsense app will get expired. 
 - **Lime**: LIME modifies a single data sample by improving the feature values and observes the resulting impact on the output. 
 - **Celery integration for Training and Hypothesis**: Give the training and hypothesis testing task to celery.




## Predictsense 1.2.0 has been released with the following headline features:
  -  **Multivariate analysis**: Analyse patterns and relationships between several variables simultaneously.
  -  **Custom EDA**: Added custom EDA functionality in manual EDA for user define imputation of missing values.
  -  **Quick Prediction**: Support for single value inputs and show prediction probabilities of classification datasets.
  -  **Celery**: Give large tasks to other process and continue with the usual routine.
  -  **Smote**: Handle imbalanced dataset if assigned as a target feature.
  -  **Feature Scaling**: To overcome the noise for dataset containing features highly varying in terms of magnitudes, units and range.
  -  **Advance algorithm parameter**: User can design his choices to build the model architecture for bagging, boosting and Gridsearch CV.
  -  **Node-Red**: Extended node red functionalities to support mongodb and sql even perform dataset operations.
  -  **User Management(admin)**: Admin will get the option to reset user password
Options.
  -  **Help Sections**: Added user manual and demo videos under this section.
  -  **Performance metrics filter**: Added filter option in the model to customize the user needs.
  -  **Analysis Report**: Change the logic from Numpy arrays to DataFrames to maintain the records in the Analysis Report.




## Predictsense 1.1.0 has been released with the following headline features:
  - **Node-Red**: Designed Node-Red basic flow, for data upload.
  - **Nginx-Server**: Integrated Nginx server for balancing load to avoid performance issues.
  - **Toolkit**: Fixed some minor bug fixes and introduced toolkit UI for passing single data output.
  - **Learning Curve**: To show the comparision graph of training score and cross validation score.
  - **Target Feature Enhancement**: Added hypothesis testing feature between dependent and independent features. which will compute the p value (helps to find the feature significance).
  - **Advance algorithms**: Added bagging,boosting and gridsearch cv for every algorithms as advance option.
  - **ANN algorithm**: Added ANN algorithm for classification belonging to deep learning category.
  - **Api improvements**:  /api/eda/pandasProfile
                           /api/eda/graph
                           /api/data/read
                           /api/train/scatter
                           /api/models/analysisReport/graph
                           /api/models/analysisReport/report
                           /api/classification/roc_auc
                           /api/model/classificationReport
                           /api/model/learningCurve
                           Given error messages incase any of the following operations gets failed.
      



## Predictsense 1.0 has been released with the following headline features:
  - **Hyperparameter Tuning**: User can design his choices to build the model architecture. He can select the parameters according to his dataset demands.
 - **NLP Support**: Support for NLP dataset with suitable algorithms. Now predictsense can build model for text data and wordcloud for the nlp data visualisation.
 - **Histogram Binning**: Makes easier for the viewer to interpret the data. 
 - **Winjit Blue Theme**: Added blue theme for better design.
 - **Toolkit**: Basic utilisation is done, user can download .sav model.
 - **Regularization algo**: Avoid predictsense models from overfitting we added some algorithms like logistic, ridge, lasso.
  - **Trees Algorithm**: Whenever an element is to be searched, start searching from the root node. It can handle both numerical and categorical data. Can also handle multi-output problems. Decision Tree algorithm is added in predictsense to support both type of data's.
  - **Download EDA summary**: User can download the computed EDA summary.
  - **Show complete training history**: Save the last 5 trained set of models for every individual projects.
  - **Class weight classification algorithms**: For X-train, X-test split, split_weights must have an equal probability.
  

