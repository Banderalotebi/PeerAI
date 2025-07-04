# celery -A Celery_Flask_app.celery worker --pool=solo -l warning


"""
Created on Mon Dec 7 17:28:15 2018

@author: Amey Bhadkamkar
"""

from flask import Flask
from modules.Tests import PS
import requests
from modules.Logging import Logger
from celery_worker import make_celery
from socketIO_client import SocketIO

logger, log_file_path = Logger().log()


f_app = Flask(__name__)
f_app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
# f_app.config['CELERY_RESULT_BACKEND'] = 'mongodb://localhost:27017'

celery = make_celery(f_app)


def Fetch_HPT_data(hyper_parameter_data_from_ui):
    # print('2')
    no_of_algos = len(hyper_parameter_data_from_ui)
    algo_name_list = []
    HPT_data_dict = {}

    logger.info(''.format(hyper_parameter_data_from_ui))

    if hyper_parameter_data_from_ui == []:
        logger.debug('Entered Blank HPT data condition')
        return ('blank', 'blank')

    for i in range(no_of_algos):
        a = (hyper_parameter_data_from_ui[i]['fields'])
        algo_name = hyper_parameter_data_from_ui[i]['algoName']
        HPT_data_dict.update({algo_name: a})
        algo_name_list.append(algo_name)

    print('xxx', HPT_data_dict)
    return (HPT_data_dict, algo_name_list)


@celery.task(name='celery_app.Celery_EDA')
def Celery_EDA(EDA_data_from_ui):

    try:

        print('Inside CELERY EDA')

        project_id = EDA_data_from_ui['projectId']

        encoding_codec, UI_ip_address, UI_port_no = EDA_data_from_ui[
            'fileEncoding'], EDA_data_from_ui['UI_ip_address'], EDA_data_from_ui['UI_port_no']

        from socketIO_client import SocketIO
        acc_token = 'qqq'
        acc_key = 'q'
        socket = SocketIO(UI_ip_address, int(UI_port_no),
                          params={acc_key: acc_token})

        edastart_obj = PS(logger).startEDA(EDA_data_from_ui,
                                           encoding_codec, UI_ip_address, UI_port_no, socket)

        print('Completed CELERY EDA')

        return('done')

    except Exception as e:

        logger.exception(" there is Error at EDA in CELERY ")

        res = requests.post("http://" + UI_ip_address + ":" + UI_port_no + "/api/projects/" + project_id + "/report",
                            data={"projectStatus": 'EDA Failed', "error": e})

        logger.debug(" EDA Failed response : {}".format(res))

        return ("EDA Done")


@celery.task(name='celery_app.Celery_Training')
def Celery_Training(training_data_from_ui, UI_ip_address, UI_port_no):
    a = 0

    try:

        project_id = training_data_from_ui['projectId']
        model_id = training_data_from_ui['modelId']
        algorithm_list = training_data_from_ui['algorithms']

        hpt_data = training_data_from_ui['hptPreference']

        logger.info(' HPT Preference data :----------->> {}'.format(hpt_data))

        hyper_parameter_value, algo_list = Fetch_HPT_data(hpt_data)

        if hyper_parameter_value == 'blank' and algo_list == 'blank':
            hyper_parameter_value = {}

        # A: Logic for appending blank HPT preferences for which HPT preference is not selected in UI
        for a in algorithm_list:
            if a not in algo_list:
                hyper_parameter_value.update({a: []})
        logger.info('HYPER PARAMETERS VALUE:{}'.format(hyper_parameter_value))

        # A: Function call for Training functions
        trainstart_obj = PS(logger).startTraining(
            UI_ip_address, UI_port_no, hyper_parameter_value, training_data_from_ui)
    except Exception as e:
        logger.exception(" there is error at TRAINING ")

        res = requests.post(
            "http://" + UI_ip_address + ":" + UI_port_no + "/api/projects/" +
            project_id + "/trainmodel/" + model_id + "/done?type=train",
            data={"projectStatus": "Model Failed", "algoName": a, "error": e})

    return ("Training Complete")


@celery.task(name='celery_app.Celery_Hypothesis')
def Celery_Hypothesis(hypothesis_testing_data_from_ui):

    hypothesis_testing_data_to_ui = PS(logger).hypothesis_testing(
        hypothesis_testing_data_from_ui)

    return ('Hypothesis completed')
