#PredictSense toolkit

Steps to setup and run the toolkit
1)Install python >=3
2)Extract and navigate to the toolkit folder
3)Do "pip install requirements.txt"
4)Once the installation is completed run "python toolkit_app.py",this will start a local server on port 5005

How to use:
1)Start the server by typing "python toolkit_app.py", if it is already running leave as it is.
2)You can send prediction data to api in one of the following format

    API Endpoint: api/prediction

	1) JSON Format 1
		---------------------
		[
			{
				colName:colValue,
				colName:colValue
			},
			{
				colName:colValue,
				colName:colValue
			}
		]

    2) JSON Format 2
        ---------------------
        {
            "predictionData":"Absolute filepath",
            "fileEncoding":"Appropriate encoding of the file ex:utf-8"
        }


Note:
* You can always replace the default server with unicorn,nginx etc.
* Please add security for api