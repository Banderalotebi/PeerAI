# -*- coding: utf-8 -*-
# celery -A modules.celery_app.celery worker --pool=solo --loglevel=info

"""
Created on Thr Mar 8 17:28:15 2018

@author: Amey Bhadkamkar
"""

from config import Config
import json
import os
import pickle

import pandas as pd
import requests
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from socketIO_client import SocketIO
#from tensorflow.keras.models import load_model

#from modules.BaggingAlgorithms import Bagging
#from modules.BoostingAlgorithms import Boosting
from modules.CrossValidation import Cross_Validation
from modules.GetDataset import Read_Data
#from modules.GridSearchAlgorithms import GridSearchCV
from modules.Logging import Logger
from modules.Predict import Predict
from modules.Preprocess import ReadAndProcess
from modules.Tests import PS
from modules.TrainingSet import TrainingSet

try:
    from modules.BaggingAlgorithms import Bagging
except ImportError:
    Bagging = None
    logger.warning('Bagging class/module not found. Bagging functionality will be skipped.')
try:
    from modules.BoostingAlgorithms import Boosting
except ImportError:
    Boosting = None
    logger.warning('Boosting class/module not found. Boosting functionality will be skipped.')
try:
    from modules.GridSearchAlgorithms import GridSearchCV
except ImportError:
    GridSearchCV = None
    logger.warning('GridSearchCV class/module not found. GridSearchCV functionality will be skipped.')

logger, log_file_path = Logger().log()


UI_ip_address, UI_port_no, machine_id, PScore_ip_address = Config().configuration()

# A: Socket connection estalishment: used for reporting EDA stages
acc_token = 'qqq'
acc_key = 'q'
socket = SocketIO(UI_ip_address, int(UI_port_no), params={acc_key: acc_token})

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


def machine_settings():
    mach_dict = {'logFilePath': log_file_path,
                 'machineAddress': PScore_ip_address}
    mach_df = pd.DataFrame(mach_dict, index=[0])
    mach_data_to_ui = mach_df.to_json(orient='records')
    res = requests.put(
        "http://" + UI_ip_address + ":" + UI_port_no +
        '/api/settings/pscoreIdCreation/' + machine_id,
        data=mach_data_to_ui, headers={'Content-type': 'application/json'})

    return ()


mach_setting_start = machine_settings()


@app.route('/')
def render_ui():
    return render_template('index.html')


@app.route('/api/create/project', methods=['POST'])
def create_project():
    logger.info('Create Project called: ')
    project_data_from_ui = request.get_json()

    import os
    if not os.path.exists(
            os.path.join(project_data_from_ui['absPath'], 'projects')):
        os.mkdir(os.path.join(project_data_from_ui['absPath'], 'projects'))

    if os.path.exists(
            os.path.join(project_data_from_ui['absPath'], 'projects')):
        p_id_folder_path = os.path.join(project_data_from_ui['absPath'],
                                        'projects',
                                        project_data_from_ui['pId'])
        os.mkdir(path=p_id_folder_path)

    # print(p_id_folder_path)

    return ('done successfully')


@app.route('/api/data/merge', methods=['POST'])
def merge_data():
    logger.info('Merge Data called: ')
    data_for_merge = request.get_json()

    json_data = data_for_merge['data']
    mime_type = data_for_merge['mtype']

    project_details = data_for_merge['projectDetails']
    original_filepath = project_details['originalFilePath']
    created_by = project_details['createdBy']
    file_extension = project_details['fileExt']
    encoding_codec = project_details['encoding']

    if mime_type == 'file':
        newfile_path = json_data['mergeFilePath']
        newfile_encoding = json_data['encoding']
        newfile_ext = project_details['fileExt']
    else:
        pass

    for i in range(2):
        if i == 0:
            if mime_type == 'json':
                new_dataframe = Read_Data(logger,
                                          encoding_codec=None).read_data(
                    json_data, file_extension=None)
            else:
                new_dataframe = Read_Data(logger,
                                          encoding_codec=newfile_encoding).read_data(
                    newfile_path, file_extension=newfile_ext)
        else:
            old_dataframe = Read_Data(logger,
                                      encoding_codec=encoding_codec).read_data(
                original_filepath,
                file_extension=file_extension)

    merged_dataframe = Read_Data(logger, encoding_codec=None).merge_data(
        new_dataframe, old_dataframe)

    if type(merged_dataframe) == str:
        message = merged_dataframe
        return jsonify({"Status": "Failed", "Message": message}), 400
    else:
        Read_Data(logger, encoding_codec=None).send_data(merged_dataframe,
                                                         original_filepath,
                                                         file_extension)

    return jsonify({"Status": "Success", "Message": "Merge Completed"})


@app.route('/api/data/read', methods=['POST'])
def Read_Data_df():
    try:
        import json

        from flask import jsonify

        read_data_from_ui = request.get_json()

        logger.info(
            'Read data df: Received Data from UI:{}'.format(read_data_from_ui))

        data_file_path = read_data_from_ui['filePath']
        data_extension = read_data_from_ui['fileExtension']
        encoding_codec = read_data_from_ui['fileEncoding']

        filename, file_extension = os.path.splitext(data_file_path)
        dataframe_temp = Read_Data(logger,
                                   encoding_codec=encoding_codec).read_data(
            data_file_path, file_extension)

        logger.debug('Read the specific File in ' + file_extension + ' format')

        dataframe_to_UI = dataframe_temp.head(5)
        dataframe_to_UI = dataframe_to_UI.fillna(value='', axis=1)

        list_of_columns = list(dataframe_to_UI)

        df_to_list_of_dicts = dataframe_to_UI.to_dict('records')

        final_data_to_ui = {'dataFrame': df_to_list_of_dicts}

        return (jsonify(head=list_of_columns, previewData=final_data_to_ui,
                        status="success"))

    except Exception as e:

        logger.exception(e)

        logger.debug(
            'Error in read_data_df on : [ /api/data/read ] , response sent to UI')

        return (jsonify(head=list_of_columns, previewData=[], status='error',
                        message='PredictSense: Could not read the data file'),
                400)


# A: api call for starting EDA
@app.route('/api/eda/start', methods=['POST', 'GET'])
def EDAstart():
    try:
        logger.info('EDA started: ')
        EDA_data_from_ui = request.get_json()
        EDA_data_from_ui.update(
            {'UI_ip_address': UI_ip_address, 'UI_port_no': UI_port_no})
        project_id = EDA_data_from_ui['projectId']

        from modules.celery_app import Celery_EDA
        # from Celery_Flask_app import This_Celery
        # print('Celery obj:', celery )
        return_obj_celery_EDA = Celery_EDA.delay(EDA_data_from_ui)
        # return_obj_celery = This_Celery(celery).Celery_EDA.delay(EDA_data_from_ui)

        return (jsonify(taskId=str(return_obj_celery_EDA)))

    except Exception as e:

        logger.exception(" There is Error at EDA")

        res = requests.post(
            "http://" + UI_ip_address + ":" + UI_port_no +
            "/api/projects/" + project_id + "/report",
            data={"projectStatus": 'EDA Failed', "error": e})

        logger.debug(" After error at EDA response : {}".format(res))

        return ("EDA Done")


@app.route('/api/eda/pandasProfile', methods=['POST', 'GET'])
def create_Pandas_Profile():
    try:
        pandas_profile_data_from_UI = request.get_json()

        logger.info(
            'Create Pandas profile: Pandas profile data from UI {}'.format(
                pandas_profile_data_from_UI))

        html_string = ReadAndProcess(logger).Pandas_Profile(
            pandas_profile_data_from_UI)
        # html_string = ReadAndProcess(logger).Pandas_Profile(
        #     pandas_profile_data_from_UI)

        return (jsonify(htmlContent=html_string))

    except Exception as e:

        logger.exception(e)
        logger.debug('Error Response sent to UI')
        return (
            jsonify(message='Could not generate the Advanced EDA report'), 400)


# # A: Function for plotting the EDA histogram
# @app.route('/api/eda/graph', methods=['POST', 'GET'])
# def EDAgraph():
#     try:
#
#         graph_data_from_ui = request.get_json()
#
#         logger.info('Graph Data from UI: {} '.format(graph_data_from_ui))
#
#         encoding_codec = graph_data_from_ui['fileEncoding']
#
#         graph_data_to_ui = PS(logger).graphEDA(encoding_codec, UI_ip_address, UI_port_no, graph_data_from_ui)
#
#         logger.info('Graph data to ui : {}'.format(graph_data_to_ui))
#
#         return (graph_data_to_ui)
#
#     except Exception as e:
#         logger.exception(e)
#
#         logger.debug('Error Response sent to UI')
#
#         return (jsonify(message='Histogram could not be generated'), 400)

@app.route('/api/train/scatter', methods=['POST'])
def trainScatter():
    try:

        scatter_data_from_ui = request.get_json()

        logger.info('Train Scatter: Scatter data from UI {}'.format(
            scatter_data_from_ui))

        encoding_codec = scatter_data_from_ui['fileEncoding']

        scatter_data_to_ui = PS(logger).TrainScatter(encoding_codec,
                                                     UI_ip_address, UI_port_no,
                                                     scatter_data_from_ui)

        logger.info('Scatter data to ui : {}'.format(scatter_data_to_ui))

        return (scatter_data_to_ui)

    except Exception as e:

        logger.exception(e)

        logger.debug('Error Response sent to UI')

        return (jsonify(message='Scatter Plot could not be generated'), 400)


def Fetch_HPT_data(hyper_parameter_data_from_ui):
    no_of_algos = len(hyper_parameter_data_from_ui)
    algo_name_list = []
    HPT_data_dict = {}

    logger.info('Fetch HPT data: Hyper Parameter data from UI'.format(
        hyper_parameter_data_from_ui))

    if hyper_parameter_data_from_ui == []:
        logger.debug('Entered Blank HPT data condition')
        return ('blank', 'blank')

    for i in range(no_of_algos):
        a = (hyper_parameter_data_from_ui[i]['fields'])
        algo_name = hyper_parameter_data_from_ui[i]['algoName']
        HPT_data_dict.update({algo_name: a})
        algo_name_list.append(algo_name)
    return (HPT_data_dict, algo_name_list)


# A: Api call for Training to proceed
@app.route('/api/training/start', methods=['POST', 'GET'])
def TrainStart():
    try:

        training_data_from_ui = request.get_json()
        logger.info('Training started: Training data from UI {}'.format(
            training_data_from_ui))
        project_id = training_data_from_ui['projectId']
        model_id = training_data_from_ui['modelId']
        a = 'algo'

        from modules.celery_app import Celery_Training
        return_obj_celery_Training = Celery_Training.delay(
            training_data_from_ui, UI_ip_address, UI_port_no)

        # algorithm_list = training_data_from_ui['algorithms']
        #
        # hpt_data = training_data_from_ui['hptPreference']
        #
        # logger.info(' HPT Preference data :----------->> {}'.format(hpt_data))
        #
        # hyper_parameter_value, algo_list = Fetch_HPT_data(hpt_data)
        #
        # if hyper_parameter_value == 'blank' and algo_list == 'blank':
        #     hyper_parameter_value = {}
        #
        # # A: Logic for appending blank HPT preferences for which HPT preference is not selected in UI
        # for a in algorithm_list:
        #     if a not in algo_list:
        #         hyper_parameter_value.update({a: []})
        # logger.info('HYPER PARAMETERS VALUE:{}'.format(hyper_parameter_value))
        #
        # # A: Function call for Training functions
        # trainstart_obj = PS(logger).startTraining(UI_ip_address, UI_port_no, hyper_parameter_value,training_data_from_ui)
        #
        # print('returned')
        return ("Training Done")

    except Exception as e:
        logger.exception(" There is error at TRAINING ")

        res = requests.post(
            "http://" + UI_ip_address + ":" + UI_port_no + "/api/projects/" +
            project_id + "/trainmodel/" + model_id + "/done?type=train",
            data={"projectStatus": "Model Failed", "algoName": a, "error": e})

        return ("Training Completed")


@app.route('/api/models/analysisReport/graph', methods=['POST'])
def AnalysisGraph():
    try:

        analysis_graph_data_from_ui = request.get_json()

        logger.info('Analysis Graph: Analysis Graph data from UI {}'.format(
            analysis_graph_data_from_ui))

        analysis_graph_data_to_UI = PS(logger).GraphAnalysisReport(
            analysis_graph_data_from_ui)

        # logger.info('Analysis report to ui: {}'.format(analysis_graph_data_to_UI))

        return (analysis_graph_data_to_UI)
    except Exception as e:
        logger.exception(e)
        logger.debug('Error Response sent to UI')

        return (jsonify(message='Analysis Graph Could not be generated'), 400)


@app.route('/api/models/analysisReport/report', methods=['POST', 'GET'])
def AnalysisReportDF():
    try:
        analysis_report_data_from_ui = request.get_json()
        logger.info(
            'Analysis Report DF: Analysis report data from UI {}'.format(
                analysis_report_data_from_ui))
        # print(analysis_report_data_from_ui)
        multilabel = analysis_report_data_from_ui['isMultilabel']
        y_test = analysis_report_data_from_ui['yTest']
        y_pred = analysis_report_data_from_ui['yPred']
        model_file_path = analysis_report_data_from_ui['modelFilePath']

        dataframe_for_analysis_report_temp = pd.read_csv(
            analysis_report_data_from_ui['dfAnalysisReport'])
        filename = None
        ar_file_name = None
        try:
            list_of_class_names = analysis_report_data_from_ui['classNames']
        except:
            list_of_class_names = None

        # print('**********************************************')

        # print(dataframe_for_analysis_report_temp)

        # print('**********************************************')
        algo_type = analysis_report_data_from_ui['algoType'].lower()

        #
        # analysis_report_file_path_for_this_algo, new_model_path,
        # temp_model_path,
        # ar_file_name

        analysis_report_file_path_for_this_algo, new_model_path, temp_model_path, ar_file_name \
            = Predict(logger, X_test_new=None, algo_name=None,
                      model_file_path=None,
                      y_label_encoder_file_path=analysis_report_data_from_ui[
                          'yLabelFilePath']).analysis_report_creation(
                algo_type, multilabel, list_of_class_names,
                y_test,
                y_pred,
                dataframe_for_analysis_report_temp, filename,
                ar_file_name_ext='ar_df.xlsx')

        # algo_type, multilabel,
        # list_of_class_names, y_test_fp, y_pred_fp,
        # dataframe_for_analysis_report_temp,
        # filename, ar_file_name_ext

        return (jsonify(arFilePath=analysis_report_file_path_for_this_algo,
                        arFileName=ar_file_name))

    except Exception as e:

        logger.exception(e)
        logger.debug('Error Response sent to UI')

        return (jsonify(message='Could not generate Analysis Report'), 400)


@app.route('/api/trainmodel/retrain/start', methods=['POST', 'GET'])
def Hyper_Parameter_Tuning():
    hyper_parameter_data_from_ui = request.get_json()
    logger.info(
        'Hyper Parameter Tuning: Hyper parameter data from UI : {}'.format(
            hyper_parameter_data_from_ui))

    print(hyper_parameter_data_from_ui)

    X_train_file_path = hyper_parameter_data_from_ui['modelData']['xTrain']
    X_test_file_path = hyper_parameter_data_from_ui['modelData']['xTest']
    Y_train_file_path = hyper_parameter_data_from_ui['modelData']['yTrain']
    Y_test_file_path = hyper_parameter_data_from_ui['modelData']['yTest']
    training_pipeline_file_path = hyper_parameter_data_from_ui['modelData'][
        'trainPipeFilePath']
    dataframe_for_analysis_report = hyper_parameter_data_from_ui['modelData'][
        'dfAnalysisReport']
    head_data_file_path = hyper_parameter_data_from_ui['afterEdaFilePath']
    project_id = hyper_parameter_data_from_ui['modelData']['projectId']
    model_id = hyper_parameter_data_from_ui['modelData']['modelId']
    model_filepath = hyper_parameter_data_from_ui['modelFilePath']
    # k_size = 4
    # k_size = hyper_parameter_data_from_ui['kFold']
    hpt_data = hyper_parameter_data_from_ui['hptPreference']
    encoding_codec = hyper_parameter_data_from_ui['fileEncoding']
    color_code_fore_ground_cm = hyper_parameter_data_from_ui['foreGround']
    color_code_back_ground_cm = hyper_parameter_data_from_ui['backGround']
    retrain = 'retrain'
    time_elapsed = 0

    algo_type = hyper_parameter_data_from_ui['algoType']
    # algo_type = 'Regression'
    try:
        list_of_class_names = hyper_parameter_data_from_ui['classNames']
        y_pred_file_path = hyper_parameter_data_from_ui['yPred']
        y_label_encoder_file_path = hyper_parameter_data_from_ui['modelData'][
            'yLabelFilePath']

    except Exception as e:
        # logger.exception(e)
        y_pred_file_path = None
        y_label_encoder_file_path = None

    hyper_parameter_value, algo_name_list = Fetch_HPT_data(hpt_data)

    algo_name = list(hyper_parameter_value)[0]

    if algo_type == 'regression':
        logger.info('Regression algorithm found.')
        multilabel = False
        y_pred_file_path = None
        y_label_encoder_file_path = None
        list_of_class_names = None

        if 'Bagging' in algo_name:
            logger.info('Bagging Algorithm started:')
            hyper_parameter_value = hyper_parameter_value[algo_name_list[0]]

            call_bagging = Bagging(logger, X_train_file_path=X_train_file_path,
                                   Y_train_file_path=Y_train_file_path,
                                   k_size=k_size,
                                   UI_ip_address=UI_ip_address,
                                   UI_port_no=UI_port_no, model_id=model_id,
                                   project_id=project_id, retrain=retrain) \
                .bagging(algo_type, algo_name, X_train_file_path,
                         X_test_file_path, Y_train_file_path, Y_test_file_path,
                         model_filepath, hyper_parameter_data_from_ui,
                         dataframe_for_analysis_report,
                         hyper_parameter_value, training_pipeline_file_path)

        elif 'Boosting' in algo_name:
            logger.info('Boosting Algorithm started:')
            hyper_parameter_value = hyper_parameter_value[algo_name_list[0]]
            call_boosting = Boosting(logger,
                                     X_train_file_path=X_train_file_path,
                                     Y_train_file_path=Y_train_file_path,
                                     k_size=k_size,
                                     UI_ip_address=UI_ip_address,
                                     UI_port_no=UI_port_no, model_id=model_id,
                                     project_id=project_id, retrain=retrain) \
                .boosting(algo_type, algo_name, X_train_file_path,
                          X_test_file_path, Y_train_file_path,
                          Y_test_file_path,
                          model_filepath, hyper_parameter_data_from_ui,
                          dataframe_for_analysis_report,
                          hyper_parameter_value,
                          training_pipeline_file_path)

        elif 'GridSearchCV' in algo_name:
            logger.info('Grid Search CV Algorithm started:')
            hyper_parameter_value = hyper_parameter_value[algo_name_list[0]]
            param_grid = None

            call_gridsearch = GridSearchCV(logger,
                                           X_train_file_path=X_train_file_path,
                                           Y_train_file_path=Y_train_file_path,
                                           k_size=k_size,
                                           UI_ip_address=UI_ip_address,
                                           UI_port_no=UI_port_no,
                                           model_id=model_id,
                                           project_id=project_id,
                                           retrain=retrain) \
                .gridsearch_cv(algo_type, algo_name, X_train_file_path,
                               X_test_file_path, Y_train_file_path,
                               Y_test_file_path,
                               model_filepath, hyper_parameter_data_from_ui,
                               dataframe_for_analysis_report,
                               hyper_parameter_value,
                               training_pipeline_file_path,
                               param_grid=param_grid,
                               y_label_encoder_file_path=y_label_encoder_file_path)

        else:
            logger.info('Fit Algorithm to data started:')
            fit_algo_to_data = PS(logger).Fit_Algo_to_data(multilabel,
                                                           y_label_encoder_file_path,
                                                           color_code_back_ground_cm,
                                                           color_code_fore_ground_cm,
                                                           algo_type,
                                                           list_of_class_names,
                                                           encoding_codec,
                                                           time_elapsed,
                                                           retrain,
                                                           head_data_file_path,
                                                           project_id,
                                                           UI_ip_address,
                                                           UI_port_no,
                                                           model_id,
                                                           algo_name_list,
                                                           X_train_file_path,
                                                           X_test_file_path,
                                                           Y_train_file_path,
                                                           Y_test_file_path,
                                                           dataframe_for_analysis_report,
                                                           hyper_parameter_value,
                                                           training_pipeline_file_path=None,
                                                           y_pred_file_path=y_pred_file_path,
                                                           filepath_validation_dataset=None)

    elif algo_type == 'classification':
        logger.info('Classificaion algorithm found.')
        multilabel = hyper_parameter_data_from_ui['isMultilabel']
        if 'Bagging' in algo_name:
            logger.info('Bagging Algorithm started:')
            hyper_parameter_value = hyper_parameter_value[algo_name_list[0]]

            call_bagging = Bagging(logger, X_train_file_path=X_train_file_path,
                                   Y_train_file_path=Y_train_file_path,
                                   k_size=k_size,
                                   UI_ip_address=UI_ip_address,
                                   UI_port_no=UI_port_no, model_id=model_id,
                                   project_id=project_id, retrain=retrain) \
                .bagging(algo_type, algo_name, X_train_file_path,
                         X_test_file_path, Y_train_file_path, Y_test_file_path,
                         model_filepath, hyper_parameter_data_from_ui,
                         dataframe_for_analysis_report,
                         hyper_parameter_value, training_pipeline_file_path,
                         y_label_encoder_file_path=y_label_encoder_file_path)

        elif 'Boosting' in algo_name:
            logger.info('Boosting Algorithm started:')

            hyper_parameter_value = hyper_parameter_value[algo_name_list[0]]
            call_boosting = Boosting(logger,
                                     X_train_file_path=X_train_file_path,
                                     Y_train_file_path=Y_train_file_path,
                                     k_size=k_size,
                                     UI_ip_address=UI_ip_address,
                                     UI_port_no=UI_port_no, model_id=model_id,
                                     project_id=project_id, retrain=retrain) \
                .boosting(algo_type, algo_name, X_train_file_path,
                          X_test_file_path, Y_train_file_path,
                          Y_test_file_path,
                          model_filepath, hyper_parameter_data_from_ui,
                          dataframe_for_analysis_report,
                          hyper_parameter_value,
                          training_pipeline_file_path,
                          y_label_encoder_file_path=y_label_encoder_file_path)

        elif 'GridSearchCV' in algo_name:
            logger.info('Grid Search CV Algorithm started:')

            hyper_parameter_value = hyper_parameter_value[algo_name_list[0]]
            param_grid = None

            call_gridsearch = GridSearchCV(logger,
                                           X_train_file_path=X_train_file_path,
                                           Y_train_file_path=Y_train_file_path,
                                           k_size=k_size,
                                           UI_ip_address=UI_ip_address,
                                           UI_port_no=UI_port_no,
                                           model_id=model_id,
                                           project_id=project_id,
                                           retrain=retrain) \
                .gridsearch_cv(algo_type, algo_name, X_train_file_path,
                               X_test_file_path, Y_train_file_path,
                               Y_test_file_path,
                               model_filepath, hyper_parameter_data_from_ui,
                               dataframe_for_analysis_report,
                               hyper_parameter_value,
                               training_pipeline_file_path,
                               param_grid=param_grid,
                               y_label_encoder_file_path=y_label_encoder_file_path)

        else:
            logger.info('Fit Algorithm to data started:')
            fit_algo_to_data = PS(logger).Fit_Algo_to_data(
                multilabel=multilabel,
                y_label_encoder_file_path=y_label_encoder_file_path,
                color_code_for_back_ground_cm=color_code_back_ground_cm,
                color_code_for_fore_ground_cm=color_code_fore_ground_cm,
                algo_type=algo_type,
                list_of_class_names=list_of_class_names,
                encoding_codec=encoding_codec, time_elapsed=time_elapsed,
                retrain=retrain, head_data_file_path=head_data_file_path,
                project_id=project_id, UI_ip_address=UI_ip_address,
                UI_port_no=UI_port_no,
                model_id=model_id, algorithms_list=algo_name_list,
                X_train_file_path=X_train_file_path,
                X_test_file_path=X_test_file_path,
                Y_train_file_path=Y_train_file_path,
                Y_test_file_path=Y_test_file_path,
                analysis_report_dataframe_file_path=dataframe_for_analysis_report,
                hyper_parameter_value=hyper_parameter_value,
                filepath_validation_dataset=None,
                y_pred_file_path=y_pred_file_path,
                training_pipeline_file_path=None)

    return (' Hyper Parameter Tunning Completed Successully')


# A: app.py -> Predict/__init__.py
@app.route('/api/classification/roc_auc', methods=['POST'])
def ROC_AUC_Curve():
    try:
        roc_auc_data_from_ui = request.get_json()
        logger.info('Roc Auc Curve: ROC AUC data from UI {}'.format(
            roc_auc_data_from_ui))

        color_code_fore_ground_roc_auc = roc_auc_data_from_ui['foreGround']
        color_code_back_ground_roc_auc = roc_auc_data_from_ui['backGround']
        y_test_file_path = roc_auc_data_from_ui['yTest']
        y_pred_file_path = roc_auc_data_from_ui['yPred']
        project_id = roc_auc_data_from_ui['projectId']
        X_test_file_path = roc_auc_data_from_ui['xTest']
        model_file_path = roc_auc_data_from_ui['modelPath']

        roc_auc_data_to_ui = Predict(logger, X_test_new=X_test_file_path,
                                     algo_name=None, model_file_path=None,
                                     color_code_for_back_ground_cm=color_code_back_ground_roc_auc,
                                     color_code_for_fore_ground_cm=color_code_fore_ground_roc_auc) \
            .roc_auc(y_test_file_path, y_pred_file_path, project_id,
                     model_file_path)

        return (roc_auc_data_to_ui)

    except Exception as e:

        logger.exception(e)
        logger.debug('Error Response sent to UI')

        return (
            jsonify(message='ROC_AUC Curve is not applicable for this model'),
            400)


@app.route('/api/prediction/start', methods=['POST', 'GET'])
def Quick_Prediction():
    import json

    pred_data_from_ui = request.get_json()
    logger.info('Quick Prediction: Prediction data from UI {}'.format(
        pred_data_from_ui))

    pred_data_to_ui, result = PS(logger).Prediction_(pred_data_from_ui)

    logger.info('Prediction Status: {}'.format(result))

    res = requests.post(
        "http://" + UI_ip_address + ":" + UI_port_no +
        "/api/prediction/done?result=" + result,
        data=json.dumps(pred_data_to_ui),
        headers={"Content-type": "application/json"})

    logger.debug(
        '----------------------PREDICTION COMPlETED-------------------------')

    return ('Prediction done')


@app.route('/api/model/classificationReport', methods=['POST', 'GET'])
def Classification_Report():
    try:
        cl_report_data_from_ui = request.get_json()
        logger.info(
            'classification Report: classification report data from UI {}'.format(
                cl_report_data_from_ui))

        data_to_ui = Predict(logger, X_test_new=None, algo_name=None,
                             model_file_path=None).classification_report(
            cl_report_data_from_ui)

        return (data_to_ui)

    except Exception as e:
        logger.exception(e)
        logger.debug('classification Report: Error Response sent to UI')

        return (
            jsonify(message='Could not generate Classification Report'), 400)


@app.route('/api/advAlgo/start', methods=['POST', 'GET'])
def Advanced_Algorithms():
    ui_data = request.get_json()
    logger.info('Advanced_Algorithms: data from UI {}'.format(ui_data))
    model_id = ui_data['modelId']
    model_filepath = ui_data['advAlgoOptions']['modelFilePath']
    algo_type = ui_data['algoType']
    project_id = ui_data['projectId']
    X_train_file_path = ui_data['xTrain']
    Y_train_file_path = ui_data['yTrain']
    X_test_file_path = ui_data['xTest']
    Y_test_file_path = ui_data['yTest']
    training_pipeline_file_path = ui_data['trainPipeFilePath']
    # k_size = ui_data['kFold']
    y_label_encoder_file_path = ui_data['yLabelFilePath']
    dataframe_for_analysis_report = ui_data['dfAnalysisReport']
    hyper_parameter_value = ui_data['advAlgoOptions']['hyperParams']
    algo_name = ui_data['advAlgoOptions']['algoname']
    retrain = 'train'

    if hyper_parameter_value != None:
        logger.info('Hyper parameter value is not None')
        hyper_parameter_value = ui_data['advAlgoOptions']['hyperParams'][
            'fields']

    if 'bagging' in ui_data['advAlgoOptions']['algoname'].lower():
        if Bagging is not None:
            logger.info('Advance Algorithm: bagging started')
            call_bagging = Bagging(logger, X_train_file_path=X_train_file_path,
                                   Y_train_file_path=Y_train_file_path,
                                   UI_ip_address=UI_ip_address,
                                   UI_port_no=UI_port_no, model_id=model_id,
                                   project_id=project_id, retrain=retrain) \
                .bagging(algo_type, algo_name, X_train_file_path, X_test_file_path,
                         Y_train_file_path, Y_test_file_path,
                         model_filepath, ui_data, dataframe_for_analysis_report,
                         hyper_parameter_value,
                         training_pipeline_file_path,
                         y_label_encoder_file_path=y_label_encoder_file_path)
        else:
            logger.warning('Bagging functionality is not available. Skipping Bagging.')
    elif 'boosting' in ui_data['advAlgoOptions']['algoname'].lower():
        if Boosting is not None:
            logger.info('Advance Algorithm: boosting started')
            call_boosting = Boosting(logger, X_train_file_path=X_train_file_path,
                                     Y_train_file_path=Y_train_file_path,
                                     k_size=k_size,
                                     UI_ip_address=UI_ip_address,
                                     UI_port_no=UI_port_no, model_id=model_id,
                                     project_id=project_id, retrain=retrain) \
                .boosting(algo_type, algo_name, X_train_file_path,
                          X_test_file_path, Y_train_file_path, Y_test_file_path,
                          model_filepath, ui_data, dataframe_for_analysis_report,
                          hyper_parameter_value, training_pipeline_file_path,
                          y_label_encoder_file_path=y_label_encoder_file_path)
        else:
            logger.warning('Boosting functionality is not available. Skipping Boosting.')
    elif 'gridsearchcv' in ui_data['advAlgoOptions']['algoname'].lower():
        if GridSearchCV is not None:
            gridsearch_data = ui_data['advAlgoOptions']
            logger.info('Advance Algorithm: Grid search data started')
            if 'gridsearchcv' in ui_data['advAlgoOptions']['hyperParams']['algoName'].lower():
                hyper_parameter_value = ui_data['advAlgoOptions']['hyperParams']['fields']
                param_grid = None
            else:
                hyper_parameter_value = None
                param_grid = ui_data['advAlgoOptions']['hyperParams']['fields']
            call_gridsearch = GridSearchCV(logger,
                                           X_train_file_path=X_train_file_path,
                                           Y_train_file_path=Y_train_file_path,
                                           k_size=k_size,
                                           UI_ip_address=UI_ip_address,
                                           UI_port_no=UI_port_no,
                                           model_id=model_id,
                                           project_id=project_id, retrain=retrain) \
                .gridsearch_cv(algo_type, algo_name, X_train_file_path,
                               X_test_file_path, Y_train_file_path,
                               Y_test_file_path,
                               model_filepath, ui_data,
                               dataframe_for_analysis_report,
                               hyper_parameter_value, training_pipeline_file_path,
                               param_grid=param_grid,
                               y_label_encoder_file_path=y_label_encoder_file_path)
        else:
            logger.warning('GridSearchCV functionality is not available. Skipping GridSearchCV.')

    return ('Executed Advanced ALgorithms')


@app.route('/api/model/learningCurve', methods=['POST', 'GET'])
def plot_learning_curve():
    try:

        learning_curve_data_from_ui = request.get_json()

        filename, file_extension = os.path.splitext(
            learning_curve_data_from_ui['modelFilePath'])

        if file_extension == '.h5':
            model = load_model(
                learning_curve_data_from_ui['modelFilePath'])
        else:

            model = pickle.load(
                open(learning_curve_data_from_ui['modelFilePath'], 'rb'))

        X_train = pickle.load(
            open(learning_curve_data_from_ui['xTrain'], 'rb'))
        Y_train = pickle.load(
            open(learning_curve_data_from_ui['yTrain'], 'rb'))
        algo_name = learning_curve_data_from_ui['algoName']
        n_split = 4
        # n_split = int(learning_curve_data_from_ui['kFold'])
        # cv_technique = learning_curve_data_from_ui['validationStrategy']
        test_size = int(learning_curve_data_from_ui['testSize'])
        back_ground_color = learning_curve_data_from_ui['backGround']
        fore_ground_color = learning_curve_data_from_ui['foreGround']

        html_string = Cross_Validation(logger, UI_ip_address,
                                       UI_port_no).plot_learning_curve(
            back_ground_color=back_ground_color,
            fore_ground_color=fore_ground_color,
            test_size=test_size, cv_technique=learning_curve_data_from_ui,
            algo_name=algo_name,
            model=model,
            X_train=X_train, Y_train=Y_train, ylim=(0.7, 1.01))

        # try:

        # lime_result_to_ui = Predict(logger, X_test_new=None, algo_name=None, model_file_path=None).LIME_result('none')
        # print('Exception===========>>>',e1)

        return (jsonify(htmlContent=html_string))

    except Exception as e:

        logger.exception(e)
        logger.debug('plot_learning_curve: Error Response sent to UI')

        return (jsonify(message='Could not generate Learning Curve'), 400)


@app.route("/api/summarize_data", methods=['POST'])
def getDataSummary():
    from pandas_profiler.PrintProfile import getHTML
    logger.info('get data summary started:')
    data = {}

    if bool(request.json):
        data = request.json
    elif bool(request.data):
        data = json.loads(request.data)
    else:
        try:
            data = request.args.to_dict()
        except:
            return jsonify({"Error": "Something went wrong."})
    html = getHTML(data)

    return jsonify({"HTML": html})


# Added by Saurabh : this api call for performing hypothesis testing between dependent feature and independent feature.
@app.route('/api/training/hypothesisTesting/start', methods=['POST', 'GET'])
def hypothesisTesting():
    hypothesis_testing_data_from_ui = request.get_json()
    hypothesis_testing_data_from_ui.update(
        {'UI_ip_address': UI_ip_address, 'UI_port_no': UI_port_no})

    logger.debug(
        "Hypothesis Testing started: Hypothesis testing data from UI : {}".format(
            hypothesis_testing_data_from_ui))

    try:

        from modules.celery_app import Celery_Hypothesis
        return_obj_celery_Hypothesis = Celery_Hypothesis.delay(
            hypothesis_testing_data_from_ui)

        # hypothesis_testing_data_to_ui = PS(logger).hypothesis_testing(hypothesis_testing_data_from_ui)

        message = "Hpyothesis testing has been completed"
        return (jsonify(taskId=str(return_obj_celery_Hypothesis)))
    except Exception as e:

        logger.exception(
            "There was a problem while performing Hypothesis testing.")
        message = "There was some problem while performing Hypothesis testing."

        return jsonify(message), 400


@app.route("/api/trainmodel/multivariate_analysis", methods=['GET', 'POST'])
def multivariate_analysis():
    is_target = eval(request.args.get('target').capitalize())
    multivariate_data_from_ui = request.get_json()
    logger.info('multivariate_analysis: Multivariate data from UI {}'.format(
        multivariate_data_from_ui))
    try:

        multivariate_analysis_to_ui = TrainingSet(
            logger).multivariate_analysis(multivariate_data_from_ui, is_target)
        return jsonify({'data': multivariate_analysis_to_ui})

    except Exception as e:
        logger.exception("There was some problem in Multivariate Analysis.")
        response_message = {
            'content': '<div><font color="red" >There was some problem while generating graph.</font></div>',
            'contentType': 'html', 'projectDetails': None}
        return jsonify(response_message), 400


@app.route("/api/classification/lime", methods=['POST'])
def lime():
    lime_data_from_ui = request.get_json()
    logger.info('Lime: Lime data from UI {}'.format(lime_data_from_ui))
    # print(lime_data_from_ui)
    try:

        lime_result_to_ui = Predict(logger, X_test_new=None, algo_name=None,
                                    model_file_path=None).LIME_result(
            lime_data_from_ui)

    except Exception as e:
        # print(e)
        logger.exception('An exception occured in lime', e)
        return (jsonify(htmlContent=lime_result_to_ui), 400)

    return (jsonify(htmlContent=lime_result_to_ui))

    # return('LIME')


@app.route("/api/crossValidate", methods=['POST', 'GET'])
def cross_validate():
    a = 0

    validation_data_from_ui = request.get_json()
    # validation_data_from_ui = {'modelId': '5c8a3373c449aab0185dad7d',
    #                            'projectId': '5c8a3094c449aab0185dad74',
    #                            'validationStrategy': {
    #                                'strategyValues': {'nSplit': 5,
    #                                                   'technique': 'kFold'},
    #                                'validationStrategyName': 'cv'},
    #                            'xTrain':
    #                                r'd:\\PredictSense\\psstudio\\projects\\5c8a3094c449aab0185dad74\\5c8a3094c449aab0185dad741552561011X_train.txt',
    #                            'yTrain':
    #                                r'd:\\PredictSense\\psstudio\\projects\\5c8a3094c449aab0185dad74\\5c8a3094c449aab0185dad741552561011Y_train.txt',
    #                            'algoName': 'KNN Classification',
    #                            'algoType': 'classification',
    #                            'hptPreference': None}

    # print(' CV Data:', validation_data_from_ui)

    model_id = validation_data_from_ui['modelId']
    algo_name = validation_data_from_ui['algoName']

    hpt_data = validation_data_from_ui['hptPreference']

    # print('iop1',hpt_data)

    hyper_parameter_value, algo_list = Fetch_HPT_data(hpt_data)

    if hyper_parameter_value == 'blank' and algo_list == 'blank':
        hyper_parameter_value = {}
        ex_li = []
        ex_li.append(algo_name)

        # A: Logic for appending blank HPT preferences for which HPT preference is not selected in UI
        hyper_parameter_value.update({algo_name: []})
    logger.info('HYPER PARAMETERS VALUE:{}'.format(hyper_parameter_value))

    try:

        if validation_data_from_ui['validationStrategy'][
                'validationStrategyName'] == 'cv':

            cvScore = Cross_Validation(logger, UI_ip_address, UI_port_no).cv(
                logger,
                validation_data_from_ui,
                hyper_parameter_value)

            pass

        elif validation_data_from_ui['validationStrategy']['strategyValues'][
            'validationStrategyName'] == \
                'tvh':

            temp = Cross_Validation(logger).tvh()

            pass

        print('does it print')

        logger.info('cvScore : {}'.format(cvScore))

        # /api/models/:modelId/cv/done

        cv_data = {'cvScore': cvScore, 'message': 'success'}

        data_dict = {'cvData': cv_data}
        l1 = []

        l1.append(data_dict)
        train_data_df_Sim_lin = pd.DataFrame(l1)
        train_data_to_ui_Sim_lin = train_data_df_Sim_lin.to_json(
            orient="records")

        res = requests.post(
            "http://" + UI_ip_address + ":" + UI_port_no +
            "/api/models/" + model_id + "/cv/done?algoName=" + algo_name,
            data=train_data_to_ui_Sim_lin,
            headers={"Content-type": "application/json"})

        return (jsonify(cvData=data_dict))

    except Exception as error:
        data_dict = {'message': 'Could not perform CV for this request'}
        logger.info('Cross Validation Failed : ', error)

        # l1 = []
        #
        # l1.append(data_dict)
        # train_data_df_Sim_lin = pd.DataFrame(l1)
        # train_data_to_ui_Sim_lin = train_data_df_Sim_lin.to_json(
        #     orient="records")
        #
        # res = requests.post(
        #     "http://" + UI_ip_address + ":" + UI_port_no +
        #     "/api/models/" + model_id + "/cv/done?algoName=" + algo_name,
        #     data=train_data_to_ui_Sim_lin,
        #     headers={"Content-type": "application/json"})

        return (jsonify(cvData=data_dict), 400)


@app.route("/api/model/holdout", methods=['POST', 'GET'])
def hold_out():
    b = 0

    # xtest
    # ytest
    # model


if __name__ == '__main__':
    # from Celery_file import make_celery
    # print('1')
    # # from Celery_Flask_app import Celery_EDA
    # #
    # # f_app = Flask(__name__)
    # print('2')
    # # f_app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
    # print('3')
    # f_app.config['CELERY_RESULT_BACKEND'] = 'mongodb://localhost:27017'

    # celery = make_celery(f_app)
    # print('4',celery)

    logger.debug(
        '----------------------------------------!!!!!..PredictSense Core is ready..!!!!!--------------------------------------')

    app.run(host='0.0.0.0', threaded=True)
