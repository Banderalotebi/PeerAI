/**=========================================================
 * Module:projects
 =========================================================*/

(function () {
    "use strict";

    angular
        .module("app.projectDatas")
        .controller("ProjectDataController", ProjectDataController);

    ProjectDataController.$inject = ["FileUploader", "Project", "$rootScope", "$http", "DTOptionsBuilder", "DTColumnBuilder", "$compile", "$scope", "ProjectCore", "$timeout", "$state", "$location", "$uibModal", "Eda", "Socket", "ModelTraining", "toaster", "$q", "$resource","Models","$interval","$sce","dynamicForm","Authentication","nlpService","NVD3Config"];
    function ProjectDataController(FileUploader, Project, $rootScope, $http, DTOptionsBuilder, DTColumnBuilder, $compile, $scope, ProjectCore, $timeout, $state, $location, $uibModal, Eda, Socket, ModelTraining, toaster, $q, $resource,Models,$interval,$sce,dynamicForm,Authentication,nlpService,NVD3Config) {
        var vm = this;
        var td3 = d3;
        NVD3Config.setD3Object(td3);
        vm.isNlp = false;
        vm.status = [];
        vm.showAdvancedOptions = false;
        vm.testSize = 20;
        vm.kfold = 10;
        vm.strategies = ["Min", "Median", "Max", "Mean", "Mode", "St.Dev","Binary","Custom"];
        vm.nlpLanguages = nlpService.nlpLanguages;
        vm.nFeatureCounts = nlpService.nFeatureCounts;
        vm.modelAlgorithms = [];
        vm.modelAlgorithm = [];
        vm.edaMode = "auto";
        vm.manualEdaMode = false;
        vm.panelFileUpload = false;
        vm.edaStarted = false;
        vm.trainingStarted = false;
        vm.hideEdaSummaryTab = true;
        vm.isActive = 0;
        vm.featureList = [];
        vm.showLoading = false;
        vm.edaManualMode = false;
        vm.edaAutoMode = false;
        vm.disableStartEda = false;
        vm.selectedTarget = "";

        vm.showTrainingTable = false;

        vm.edaSummary = [];
        vm.selected = [];
        vm.edaData = [];
        vm.edaPreviewData = [];
        vm.correctedDataHeading = [];
        vm.correlationIsMultilabel = false;

        //Datatable
        vm.dtColumnsUpldPreview = [];
        vm.dtInstanceUpldPreview = {};

        vm.dtInstanceEdaStrategy = {};
        vm.dtColumnsEdaStrategy = [];

        vm.dtColumnsEdaSummary = [];
        vm.dtInstanceEdaSummary = {};
        vm.showEdaSummary = false;

        vm.dtColumnsEdaPreview = [];
        vm.dtInstanceEdaPreview = {};

        vm.dtInstanceTraining = {};
        vm.dtColumnsTraining = [];

        vm.edaAutoFeatureList = [];

        vm.edaStages = [];

        $scope.hptPreference = [];
        $scope.formFeilds = {};
        vm.showhptStatus = false;

        vm.problemType = "ML";
        //Custom strategy value holder for manual eda
        vm.cutomEdaStrategy = {};
        //Theme color code
        vm.backGround = "#252525";
        vm.foreGround = "#d3cb71";
        function checkThemeColor(){
            if(Authentication.user.layout && Authentication.user.layout.theme == "themes/theme-l.css"){
                vm.backGround = "#252525";
                vm.foreGround = "#d3cb71";
            }else{
                vm.backGround = "#252525";
                vm.foreGround = "#d3cb71";
            }
        }
        //Feature scaling options
        vm.featureScalingOption="none";

        /**
         * fetch file encodings
         */
        vm.fileEncodings = [];
        vm.fileEncodings = Project.getFileEncodings.filter(function(encoding){
            return encoding;
        });
        vm.getNum = function(){
            return 3;
        };
        // The first item will be set as default
        vm.selectedFileEncoding = vm.fileEncodings[0];

        //Function to set testSize for stratifiedShuffleSplit
        vm.setTestSize = function(){
            if(vm.validationStrategy.strategyValues.technique == "stratifiedShuffleSplit"){
                vm.validationStrategy.strategyValues.testSize = 20;
            }
        };
        //Function to initialize cv strategies
        vm.setCVStrategies = function(){
            vm.validationStrategy = {
                validationStrategyName:"cv",
                strategyValues:{technique:"kFold",nSplit:5}
            };
        };
        //Function to initialize tvh strategies
        vm.setTVHStrategies = function(){
            vm.validationStrategy = {
                validationStrategyName:"tvh"
            };
        };
        //Scatter chart options
        vm.scatterChartOptions = {
            chart: {
                type: "scatterChart",
                height: 450,
                color: d3.scale.category10().range(),
                scatter: {
                    onlyCircles: false
                },
                showDistX: true,
                showDistY: true,
                tooltipContent: function(key) {
                    return "<h3>" + key + "</h3>";
                },
                duration: 350,
                xAxis: {
                    axisLabel: "X Axis",
                    tickFormat: function(d){
                        return d3.format(".02f")(d);
                    }
                },
                yAxis: {
                    axisLabel: "Y Axis",
                    tickFormat: function(d){
                        return d3.format(".02f")(d);
                    },
                    axisLabelDistance: 30
                },
                zoom: {
                    //NOTE: All attributes below are optional
                    enabled: true,
                    scaleExtent: [1, 10],
                    useFixedDomain: true,
                    useNiceScale: false,
                    horizontalOff: false,
                    verticalOff: false,
                    unzoomEventType: "dblclick.zoom"
                }
            }
        };

        //Multi bar chart options for eda graph
        vm.options = {
            chart: {
                type: "multiBarChart",
                height: 450,
                margin: {
                    top: 20,
                    right: 20,
                    bottom: 60,
                    left: 75
                },
                showValues: true,
                showControls: false,
                valueFormat: function (d) {
                    return d3.format(",.4f")(d);
                },
                transitionDuration: 500,
                xAxis: {
                    axisLabel: "Rows"
                },
                yAxis: {
                    axisLabel: "Value"
                }
            }
        };
        function initEdaStages(){
            vm.edaStages = [
                {
                    stageTitle:"Calculating missing values",
                    status:false
                }
            ];
        }
        initEdaStages();
        vm.eda_stages = [
            {
                stageTitle:"Calculating missing values",
                status:false,
                stage:0
            },
            {
                stageTitle:"Calculating statistical details",
                status:false,
                stage:0
            },
            {
                stageTitle:"Initiating process for EDA",
                status:false,
                stage:0
            },
            {
                stageTitle:"Implementing strategies for missing values",
                status:false,
                stage:0
            },
            {
                stageTitle: "Finalizing EDA...",
                status: false,
                stage:0
            }
        ];
        //Get the selected project details
        vm.project = ProjectCore.getProject();
        vm.selectedFileEncoding = vm.project.fileEncoding;
        //Builds uploaded data preview
        vm.show = false;
        vm.buildPreviewTable = function (callback) {
            vm.show = false;
            vm.showLoading = true;
            var projectConf = new Project.readUploadedData({
                filepath: vm.project.filename,
                pid: vm.project._id
            });
            projectConf.$save(function (response) {
                vm.show = true;
                if (vm.dtInstanceUpldPreview.hasOwnProperty("DataTable")) {
                    vm.dtInstanceUpldPreview.DataTable.destroy();
                    vm.dtColumnsUpldPreview.length = 0;
                    vm.featureList.length = 0;
                    vm.edaAutoFeatureList.length = 0;
                    //vm.isNlp = response.previewData.nlpColList.length > 0 ? true:false;
                    vm.dtOptionsUpldPreview = DTOptionsBuilder.fromFnPromise(function () {
                        var defer = $q.defer();
                        defer.resolve(response.previewData.dataFrame);
                        return defer.promise;
                    }).withOption("processing", true)
                        .withOption("deferRender", true)
                        .withPaginationType("full_numbers");
                    for (var i = 0; i < response.head.length; i++) {
                        var obj = {
                            featureName: response.head[i],
                            strategy:"Mean"
                        };
                        vm.featureList.push(obj);
                        vm.dtColumnsUpldPreview.push(DTColumnBuilder.newColumn(response.head[i]).withTitle(response.head[i]));
                    }
                    vm.edaAutoFeatureList = angular.copy(vm.featureList);
                } else {
                    vm.featureList.length = 0;
                    //vm.isNlp = response.previewData.nlpColList.length > 0 ? true:false;
                    vm.dtOptionsUpldPreview = DTOptionsBuilder.fromFnPromise(function () {
                        var defer = $q.defer();
                        defer.resolve(response.previewData.dataFrame);
                        return defer.promise;
                    }).withOption("processing", true)
                        .withPaginationType("full_numbers")
                        .withOption("deferRender", true);
                    for (var i = 0; i < response.head.length; i++) {
                        var obj = {
                            featureName: response.head[i],
                            strategy:"Mean"
                        };
                        vm.featureList.push(obj);
                        vm.dtColumnsUpldPreview.push(DTColumnBuilder.newColumn(response.head[i]).withTitle(response.head[i]));
                    }
                    vm.edaAutoFeatureList = angular.copy(vm.featureList);
                }
                findAndUpdateActivityStatus("read_file","Preview generated");
          
                
                callback({status:"completed"});
                //vm.showLoading = false;
                ga("send", "event", "Projects", "Read uploaded file for preview", true);
            }, function (errorResponse) {
                vm.showLoading = false;
                vm.show = false;
                toaster.pop("error", $scope.app.name,"Oops!, something went wrong while generating preview table", 3000);
            });
        };
        vm.hideEdaProgress = function(){
            vm.edaStarted = false;
        };
        if(vm.project.projectStatus == "Eda Started"){
            vm.edaStarted = true;
            Eda.getEdaProgress.query({projectId:vm.project._id}).$promise.then(function(resp){
                vm.edaStages = resp[0].stages;
                vm.edaStages.push(vm.eda_stages[vm.edaStages.length]);
            },function(err){
                toaster.pop("error", $scope.app.name, "Error fetching eda progress details", 3000);
            });
        }
        if(vm.project.projectStatus != "Project Created"){
            fetchProjectDetails("init");
        }

        //Fetch eda details for the selected project
        vm.findEda = function (tab) {

            
            ga("set", "page", $location.path());
            vm.showLoading = true;
            vm.edaSummary.length = 0;
            vm.showEdaSummary= false;
            vm.showTrainingTable= false;
            vm.edaPreviewData = [];
            //Array to hold target variables
            vm.targetList = [];
            ga("send", "event", "Eda", "Fetching eda details", true);
            Eda.startEda.query({projectId: vm.project._id}).$promise.then(function (resp) {
                vm.edaData = resp[0];
                vm.correctedDataHeading = [];
                if (resp.length) {
                    vm.showLoading = false;
                    //vm.featureList.length = 0;
                    vm.edaSummary = resp[0].edaSummary;
                    vm.edaPreviewData = resp[0].correctedData;
                    if (resp[0].edaSummary.length) {
                        resp[0].edaSummary.forEach(function(data){
                            if(data.data_type !="Datetime"){
                                vm.correctedDataHeading.push(data.col_name);
                            }
                        });
                    }
                    if(vm.project.projectStatus != "EDA Failed"){
                        vm.buildEdaSummaryTable();
                    }
                    vm.buildEdaPreviewTable();
                    //vm.buildTrainingTable();

                    if (resp[0].strategies) {
                        vm.featureList = resp[0].strategies;
                    }
                    if(resp[0].targetFeatures){
                        vm.targetList = resp[0].targetFeatures;
                    }else{
                        vm.edaSummary.forEach(function(column){
                            var obj = {
                                featureName:column.col_name
                            };
                            vm.targetList.push(obj);
                        });
                    }
                    vm.problemType = resp[0].problemType;
                    if(vm.problemType == "NLP"){
                        vm.nlpLanguage = "English";
                        vm.nFeatureCount = 100;
                    }

                    vm.hideEdaSummaryTab = false;
                    vm.edaMode = vm.edaData.edaMode;
                    if (vm.edaData.edaMode == "manual" && tab == "eda") {
                        vm.manualEdaMode = true;
                        vm.disableStartEda = false;
                    } else {
                        vm.manualEdaMode = false;
                        vm.disableStartEda = false;
                    }
                }else{
                    vm.showLoading = false;
                }
                // Set values in training page
                if(tab == "training"){
                    if(vm.project.projectStatus == "Model Generated"){
                        vm.modelAlgorithm = vm.prevTrainingInfo[0].algorithms;
                        vm.target = vm.prevTrainingInfo[0].depVariable;
                        vm.selectedTarget = {col_name:vm.target};
                        vm.indepVariables = vm.prevTrainingInfo[0].indepVariable;
                        vm.kfold = vm.prevTrainingInfo[0].kFold;
                        vm.nlpLanguage = vm.prevTrainingInfo[0].nlpLanguage;
                        vm.nFeatureCount = vm.prevTrainingInfo[0].nFeatureCount;
                        vm.testSize = vm.prevTrainingInfo[0].testSize;
                        vm.featureScalingOption = vm.prevTrainingInfo[0].featureScaling;
                        vm.validationStrategy.validationStrategyName = vm.prevTrainingInfo[0].validationStrategy.validationStrategyName;
                        vm.validationStrategy.strategyValues.technique = vm.prevTrainingInfo[0].validationStrategy.strategyValues.technique;
                        vm.validationStrategy.strategyValues.nSplit = vm.prevTrainingInfo[0].validationStrategy.strategyValues.nSplit;
                        vm.validationStrategy.strategyValues.testSize = vm.prevTrainingInfo[0].validationStrategy.strategyValues.testSize;
                        //All features are selected
                        if((vm.edaSummary.length - 1) == vm.indepVariables.length){
                            vm.selectAll = true;
                        }
                    }
                    if(vm.target){
                        //fc stands for function call
                        vm.showLoading = true;
                        vm.onTargetChange("fc",vm.target);
                    }
                }
            }, function (err) {
                toaster.pop("error", $scope.app.name, "Error fetching eda details", 3000);
            });
        };

        //Fetch project details
        function fetchProjectDetails(type) {
            Project.myProject.query({projectId: vm.project._id}).$promise.then(function (resp) {
                ProjectCore.setProject(resp[0]);
                vm.project = resp[0];
                if(type == "init"){
                    vm.buildPreviewTable(function(data){
                        //Fetch previously trained model info.
                        if(vm.project.projectStatus == "Model Generated"){
                            Models.listModels.query({projectId:vm.project._id}).$promise.then(function(resp){
                                vm.prevTrainingInfo = resp;
                                if((vm.project.projectStatusDetails.length + resp[0].modelMetaData.length) == vm.prevTrainingInfo[0].algorithms.length){
                                    vm.showLoading  = false;
                                }else{
                                    toaster.pop("error", $scope.app.name,"Model generation is going on...", 3000);
                                    vm.showLoading  = true;
                                }
                                ga("send", "event", "Models", "Fetching previously trained models", true);
                            },function(err){
                                toaster.pop("error", $scope.app.name, "Error fetching trained models details", 3000);
                            });
                        }else if(vm.project.projectStatus == "Eda Started"){
                            vm.showLoading = true;
                        } else if(vm.project.projectStatus =="Training Started"){
                            vm.showLoading = true;
                            vm.trainingStarted = true;
                        }else{
                            vm.showLoading = false;
                        }
                    });
                }
            }, function (err) {
            });
            //ga('send', 'event', 'Projects', 'Fetching selected project details', true);
        }
        

        //Listen for correlation result
        Socket.on("hypothisisTest",function(correlationData){
            vm.targetVarType = correlationData.targetVarType;
            vm.isImbalanced = correlationData.isImbalanced;
            vm.correlationAlgoType = correlationData.algoType.toLowerCase();
            vm.correlationIsMultilabel = correlationData.isMultilabel;
            vm.correlationData = correlationData.hypothesisTestingData;
            vm.modelAlgorithms = [];
            vm.modelAlgorithms =ModelTraining.getAlgorithmList.filter(function(algorithm){
                if(vm.correlationIsMultilabel){
                    return algorithm.type == correlationData.algoType.toLowerCase() && algorithm.multilabel == (correlationData.isMultilabel ? correlationData.isMultilabel:false);
                }else{
                    return algorithm.type == correlationData.algoType.toLowerCase();
                }
            });
            vm.buildTrainingTable();
        });

        //Listen for training progress messages
        Socket.on("trainingProgress",function(message){
            $state.go("app.models");
        });

        /**
         * Socket listner for flow completion
         */
        vm.flow_failed_count = 0;
        Socket.on("uddFlowCompleted",function(message){
            if(message.status=="complted"){
                vm.project.filename = message.file;
                vm.status.push({
                    title: "Reading file",
                    value: "",
                    key: "read_file",
                    timestamp: new Date()
                });
                vm.buildPreviewTable(function(data){
                    vm.showLoading = false;
                });
            }
            if(message.status=="flow_failed"){
                vm.flow_failed_count++;
                if(vm.flow_failed_count == 1){
                    vm.status.push({
                        title: "Flow exectuion failed",
                        value: "",
                        key: "read_file",
                        timestamp: new Date()
                    });
                    toaster.pop("error", $scope.app.name, "Error while executing flow", 3000);
                    vm.buildPreviewTable(function(data){
                        vm.showLoading = false;
                    });
                }
                vm.showLoading = false;
            }
            // $state.go("app.models");
        });

        //Listen for eda progress messages
        Socket.on("edaProgress",function(message){
            vm.edaStages.pop();
            if(vm.edaStages.length < 5){
                vm.edaStages.push(message);
                var index = vm.edaStages.length;
                if(vm.eda_stages[index]){
                    vm.edaStages.push(vm.eda_stages[index]);
                }
            }
        });

        // Listen for eda completed messages
        Socket.on("edaCompleted", function (data) {
            fetchProjectDetails("eda");
            var message = data.projectStatus;
            if(message == "EDA Failed"){
                vm.showLoading = false;
                vm.edaStarted = false;
                vm.disableStartEda = false;
                vm.showEdaSummary = false;
                toaster.pop("error", $scope.app.name, "Oops EDA failed, please check the data and try again", 4000);
            }
            if(message == "Model Failed"){
                vm.trainingStarted = false;
                vm.showLoading = false;
                toaster.pop("error", $scope.app.name, "Oops training failed for "+data.algoName, 4000);
            }
            if (message == "Eda Completed") {

                vm.showLoading = false;
                if(vm.edaMode == "manual"){
                    findAndUpdateActivityStatus("eda_manual","Manual EDA completed");
                }else{
                    findAndUpdateActivityStatus("eda_auto","Auto EDA completed");
                }
                ga("send", "event", "Eda", "Eda completed", true);
                //Fetch eda details
                vm.findEda("eda");
                toaster.pop("success", $scope.app.name, "Eda completed now, you can start training.", 3000);

            }
            if(message =="Model Generated"){
                vm.showLoading = false;
                vm.trainingStarted = false;
                findAndUpdateActivityStatus("training","Model training completed");
                ga("send", "event", "Training", "Training completed", true);
                //toaster.pop('success', $scope.app.name, 'Training completed', 3000);
                $state.go("app.models");
            }
        });

        // Remove the event listener when the controller instance is destroyed
        $scope.$on("$destroy", function () {
            Socket.removeListener("edaCompleted");
            Socket.removeListener("trainingProgress");
            Socket.removeListener("uddFlowCompleted");
            //console.log("destroying socket");
        });

        // Eda mode selection
        vm.chooseEdaMode = function (mode) {
            vm.edaMode = mode;
            if (mode == "manual") {
                vm.manualEdaMode = true;
                if (vm.edaManualMode) {
                    //vm.disableStartEda = true;
                } else {
                    vm.disableStartEda = false;
                }
                ga("send", "event", "Eda", "Eda manual mode selected", true);
            } else {
                vm.customEdaStrategy = {};
                vm.manualEdaMode = false;
                if (vm.edaAutoMode) {
                    //vm.disableStartEda = true;
                } else {
                    vm.disableStartEda = false;
                }
                ga("send", "event", "Eda", "Eda auto mode selected", true);
            }
        };

        // Create an empty array for k-fold
        vm.getArray = function (len) {
            return new Array(parseInt(len));
        };

        //Find the target variable details
        function findTargetIndex(o) {

            for (var i = 0; i < vm.edaSummary.length; i++) {
                if (vm.edaSummary[i].col_name == o) {
                    return i;
                }
            }
            return -1;
        }
        //Function triggered when target selection changes
        vm.previousIndex = -1;
        vm.onTargetChange = function (event,target) {
            vm.showLoading = true;
            if(event != "fc"){
                vm.selectAll = false;
            }
            if(vm.project.projectStatus !="Model Generated"){
                vm.modelAlgorithms = [];
                vm.modelAlgorithm = [];
            }
            var target = findTargetIndex(target);
            //vm.selectedTarget = vm.featureList[target];
            vm.selectedTarget = vm.edaSummary[target];
            if(vm.selectedTarget){
                // vm.plotTargetGraph();
                var correlationConf = new ModelTraining.getCorrelation({
                    depVariable: vm.selectedTarget.col_name,
                    indepVariable: vm.edaSummary,
                    pId: vm.project._id,
                    afterEdaDataFilePath:vm.edaData.afterEdaDataFilePath,
                    datetimeColumnName:vm.edaData.datetimeColumnName
                });
                correlationConf.$save(function(res){
                    // vm.showLoading = false;
                },function(err){
                    vm.showLoading = false;
                });
            }
        };

        //Toggele advanced options section
        vm.toggleAdvacedOptions = function () {
            vm.showAdvancedOptions = !vm.showAdvancedOptions;
        };
        function checkEmptyCustomValues(){
            var isEmptyPresent = false;
            for( var k in vm.customEdaStrategy){
                if(vm.customEdaStrategy[k]==undefined ||vm.customEdaStrategy[k]==""){
                    isEmptyPresent = true;
                }
            }
            return isEmptyPresent;
        }
        //Start the eda process
        vm.startEda = function () {
            initEdaStages();
            vm.finalFeatureList = [];
            if(vm.edaMode == "manual"){
                if(checkEmptyCustomValues()){
                    alert("Custom field value cannot be empty!");
                    return 0;
                } 
                vm.finalFeatureList = vm.featureList;
            }else{
                vm.finalFeatureList = vm.edaAutoFeatureList;
            }
            vm.selectedTarget = "";
            if (vm.edaMode == "manual") {
                vm.edaManualMode = true;
                vm.disableStartEda = true;
                vm.status.push({title: "Performing manual EDA", value: "", key: "eda_manual", timestamp: new Date()});
            } else {
                vm.edaAutoMode = true;
                vm.disableStartEda = true;
                vm.status.push({title: "Performing auto EDA", value: "", key: "eda_auto", timestamp: new Date()});
            }
            vm.showLoading = true;
            vm.hideEdaSummaryTab = false;
            vm.edaStarted = true;
            var eda = new Eda.startEda({
                edaMode: vm.edaMode,
                strategies: vm.finalFeatureList,
                pId: vm.project._id,
                customEdaStrategy:vm.customEdaStrategy
            });
            eda.$save(function (response) {
                vm.project = response;
                ga("send", "event", "Projects", "Eda started", true);
            }, function (errorResponse) {
                toaster.pop("error", $scope.app.name,"Oops!, eda could not start", 3000);
            });
            $location.hash("dataPanelEda");

        };
        function findAndUpdateActivityStatus(key,status){
            vm.status.map(function(obj){
                if(obj.key == key){
                    obj.timestamp = new Date();
                    obj.title = status;
                    return obj;
                }
            });
        }
        //Function to form independent variable list
        function generateIndepVariableList(target,type){
            var tSelected = [];
            //lOb - list of objects, which will convert to list of objects
            if(type == "lOb"){
                for(var k in vm.selected){
                    if(vm.selected[k]&& k != target){
                        tSelected.push({col_name:k});
                    }
                }
            }else{
                for(var k in vm.selected){
                    if(vm.selected[k]&& k != target){
                        tSelected.push(k);
                    }
                }
            }
            return tSelected;
        }

        //Start training function
        vm.trainCount = 0;
        vm.doTraining = function () {
            vm.tempSelected =  [] ;
            if (vm.target) {
                // for(var k in vm.selected){
                //     if(vm.selected[k]&& k != vm.target){
                //         vm.tempSelected.push({col_name:k})
                //     }
                // }
                vm.tempSelected = generateIndepVariableList(vm.target,"lOb");
                if(vm.tempSelected.length < 1){
                    toaster.pop("error", $scope.app.name, "Please select features.", 3000);
                    return false;
                }
                if(vm.modelAlgorithm.length < 1){
                    toaster.pop("error", $scope.app.name, "Please select algorithms.", 3000);
                    return false;
                }
                vm.showLoading = true;
                vm.trainingStarted = true;
                checkThemeColor();
                var trainConf = new ModelTraining.startTraining({
                    depVariable: vm.selectedTarget.col_name,
                    indepVariable: vm.tempSelected,
                    algorithms: vm.modelAlgorithm,
                    validationStrategy: vm.validationStrategy,
                    testSize: vm.testSize,
                    pId: vm.project._id,
                    hptPreference:$scope.hptPreference,
                    categoricalColNames:vm.edaData.categoricalColNames,
                    afterEdaDataFilePath:vm.edaData.afterEdaDataFilePath,
                    noOfCol:vm.edaData.edaSummary.length,
                    paragraphColNames:vm.edaData.paragraphColNames,
                    algoType:vm.correlationAlgoType,
                    isMultilabel:vm.correlationIsMultilabel,
                    backGround:vm.backGround,
                    foreGround:vm.foreGround,
                    nFeatureCount:vm.nFeatureCount,
                    nlpLanguage:vm.nlpLanguage,
                    edaId:vm.edaData._id,
                    datetimeColumnName:vm.edaData.datetimeColumnName,
                    problemType:vm.edaData.problemType,
                    featureScaling:vm.featureScalingOption,
                    isImbalanced:vm.isImbalanced
                });
                trainConf.$save(function (res) {
                    vm.trainCount++;
                    if(vm.trainCount > 1){
                        findAndUpdateActivityStatus("training","Model training started");
                    }else{
                        vm.status.push({title: "Model training started", value: "", key: "training", timestamp: new Date()});
                    }
                    ga("send", "event", "Training", "Model training started", true);
                }, function (err) {
                    vm.trainingStarted = false;
                    vm.showLoading = false;
                    toaster.pop("error", $scope.app.name, err.data.message, 4000);
                });
            }else{
                toaster.pop("error", $scope.app.name, "Please select target variable.", 3000);
                return false;
            }
        };

        //Popup to show eda summary data.
        vm.binSizes = [10,15,20,25];
        vm.selectedBin = 10;
        vm.openEdaSummaryGraph = function (size,feature,dataType) {
            vm.edaModalSize = size;
            vm.selectedFeature = feature;
            vm.dataType = dataType;
            var modalInstance;
            var modalScope = $scope.$new();
            modalInstance = $uibModal.open({
                templateUrl: "myModalContent.html",
                size: vm.edaModalSize,
                scope: modalScope,
                backdrop: "static"
            });
            modalScope.cancel = function () {
                window.d3 = td3;
                modalInstance.close(modalScope.selected);
                vm.showLoading = false;
            };
            vm.showLoading = true;
            if(vm.project.projectStatus == "File Uploaded"){
                toaster.pop("error", $scope.app.name, "Graph preview is not available,perform eda and check!", 3000);
                vm.showLoading = false;
                return false;
            }
            if(dataType.toLowerCase() =="Categorical"){
                toaster.pop("error", $scope.app.name, "Graph preview is not available for categorical data!", 3000);
                vm.showLoading = false;
                return false;
            }
            vm.getEdaGraphData();

        };
        vm.getEdaGraphData = function(){
            $scope.content = "<h2 class='text-center'>Loading data...</h2>";
            //Check the theme color
            checkThemeColor();
            var data = {
                afterEdaDataFilePath:vm.edaData.afterEdaDataFilePath,
                colName:vm.selectedFeature,
                backGround:vm.backGround,
                foreGround:vm.foreGround,
                noOfBins:vm.selectedBin
            };
            $http.post("/api/projects/"+vm.project._id+"/eda/edagraph",data).then(function(resp){
                $scope.content = $sce.trustAsHtml(resp.data);
                vm.showLoading = false;
            },function(err){
                vm.showLoading = false;
                toaster.pop("error", $scope.app.name, "Oops!, something went wrong while generating EDA graph.", 3000);
                $scope.content = $sce.trustAsHtml("<h5 class='text-center'>Could not generate EDA graph!</h5>");
            });
        };
        //On change of binsize in eda graph get new graph data.
        vm.onBinSizeChange = function(){
            vm.getEdaGraphData();
        };
        //Find the index of a particular feature
        function myIndexOf(o) {

            for (var i = 0; i < vm.featureList.length; i++) {
                if (vm.featureList[i].featureName == o.featureName) {
                    return i;
                }
            }

            return -1;
        }

        // Called when change eda strategy
        vm.changeStrategy = function (column, strategy) {
            vm.indx = myIndexOf(column);
            vm.featureList[vm.indx].strategy = strategy;
            if(strategy != "Custom" && vm.customEdaStrategy){
                vm.customEdaStrategy.hasOwnProperty([column.featureName]) ? delete vm.customEdaStrategy[column.featureName]:"";
            }
        };

        //Building edaStrategy table
        vm.buildEdaStrategyTable = function(){
            vm.dtOptionsEdaStrategy = DTOptionsBuilder.fromFnPromise(function () {
                var defer = $q.defer();
                defer.resolve(vm.featureList);
                return defer.promise;
            }).withOption("processing", true)
                .withOption("deferRender", true)
                .withPaginationType("full_numbers")
                .withOption("createdRow", createdRow);
            vm.dtColumnsEdaStrategy = [
                DTColumnBuilder.newColumn("featureName").withTitle("Column Name").notSortable(),
                DTColumnBuilder.newColumn(null).withTitle("Strategy").notSortable()
                    .renderWith(actionsHtml)
            ];
        };
        function createdRow(row, data, dataIndex) {
            // Recompiling so we can bind Angular directive to the DT
            $compile(angular.element(row).contents())($scope);
        }
        var m = 0;
        function actionsHtml(data, type, full, meta) {
            m++;
            var initVal = data.value ? data.value:"";
            return "<div class=\"col-md-3\"><select ng-change=\"pdc.changeStrategy({featureName:'"+data.featureName+"'},st["+m+"])\" ng-model=\"st["+m+"]\" ng-init=\"st["+m+"]='"+data.strategy+"'\">"+
                "<option value=\"\" disabled selected>Select strategy</option>"+
                "<option ng-repeat=\"strategy in pdc.strategies\">{{strategy}}</option>"+
                "</select></div>"+
                "&nbsp;<div class=\"col-md-4\"><input class=\"form-control \" placeholder=\"Custom value\" ng-if=\"st["+m+"]=='Custom'\" type=\"text\" ng-model=\"pdc.customEdaStrategy['"+data.featureName+"']\" ng-init=\"pdc.customEdaStrategy['"+data.featureName+"']='"+initVal+"'\"/></div>";
        }

        //Building edaSummary table
        vm.buildEdaSummaryTable = function(){
            if (vm.dtInstanceEdaSummary.hasOwnProperty("DataTable")) {
                vm.dtInstanceEdaSummary.DataTable.destroy();
                vm.dtColumnsEdaSummary.length = 0;
            }
            vm.dtOptionsEdaSummary = DTOptionsBuilder.fromFnPromise(function () {
                var defer = $q.defer();
                defer.resolve(vm.edaSummary);
                return defer.promise;
            }).withOption("processing", true)
                .withOption("deferRender", true)
                .withPaginationType("full_numbers")
                .withOption("createdRow", createdRow);

            vm.dtColumnsEdaSummary = [
                // DTColumnBuilder.newColumn(null).withTitle('Histogram').notSortable()
                //     .renderWith(edaActionsHtml),
                DTColumnBuilder.newColumn("col_name").withTitle("Feature Name"),
                DTColumnBuilder.newColumn("data_type").withTitle("Var Type"),
                DTColumnBuilder.newColumn("data_miss_value").withTitle("Missing"),
                DTColumnBuilder.newColumn("data_unique").withTitle("Unique"),
                DTColumnBuilder.newColumn("data_mean").withTitle("Mean"),
                DTColumnBuilder.newColumn("d_std").withTitle("SD"),
                DTColumnBuilder.newColumn("data_min").withTitle("Min"),
                DTColumnBuilder.newColumn("data_max").withTitle("Max"),
                DTColumnBuilder.newColumn("data_median").withTitle("Median"),
                DTColumnBuilder.newColumn("data_strategy").withTitle("Strategy")
            ];
            vm.showEdaSummary= true;
        };
        function edaActionsHtml(data, type, full, meta){
            return "<em class=\"fa fa-bar-chart pss-chart-hover\" ng-click=\"pdc.openEdaSummaryGraph('lg','"+data.col_name+"','"+data.data_type+"')\"></em>";
        }

        //Building eda preview table
        vm.buildEdaPreviewTable = function(){
            if (vm.dtInstanceEdaPreview.hasOwnProperty("DataTable")) {
                vm.dtInstanceEdaPreview.DataTable.destroy();
                vm.dtColumnsEdaPreview.length = 0;
            }
            vm.dtOptionsEdaPreview = DTOptionsBuilder.fromFnPromise(function () {
                var defer = $q.defer();
                try{
                    var split = vm.edaData.correctedData.split("/");
                    var projectConf = new Project.readUploadedData({
                        filepath: vm.edaData.correctedData,
                        pid: vm.project._id
                    });
                    projectConf.$save(function(res){
                        defer.resolve(res.previewData.dataFrame);
                    },function(err){
                        //console.log(err)
                        //defer.resolve(vm.edaPreviewData);
                    });
                }catch(e){
                    defer.resolve(vm.edaPreviewData);
                }

                //defer.resolve(vm.edaPreviewData);
                return defer.promise;
            }).withOption("processing", true)
                .withPaginationType("full_numbers")
                .withOption("deferRender", true);
            for (var i = 0; i < vm.correctedDataHeading.length; i++) {
                vm.dtColumnsEdaPreview.push(DTColumnBuilder.newColumn(vm.correctedDataHeading[i]).withTitle(vm.correctedDataHeading[i]));
            }
        };

        // Function to check all the checkboxes in training section table.
        vm.toggleAll = function (selectAll, selectedItems) {
            for (var id in selectedItems) {
                if (selectedItems.hasOwnProperty(id) && id != vm.target) {
                    selectedItems[id] = selectAll;
                }
            }
        };

        //Function to checck a particular checkbox in training table.
        vm.toggleOne = function (selectedItems) {
            for (var id in selectedItems) {
                if (selectedItems.hasOwnProperty(id)) {
                    if(!selectedItems[id]) {
                        vm.selectAll = false;
                        return;
                    }
                }
            }
            vm.selectAll = true;
        };

        //Function to check the feature data  type
        function checkFeatureDataType(feature){
            return vm.edaSummary.find(function(f){
                if(f.col_name == feature){
                    return f;
                }
            });
        }

        //Building training feature selection table
        vm.correlationGraphData = [];
        $scope.contentScatter = null;
        vm.openCorrelationGraph = function(size,feature){
            $scope.contentScatter = null;
            vm.correlationGraphData.length = 0;
            if(checkFeatureDataType(feature).data_type == "Categorical" && checkFeatureDataType(vm.target).data_type == "Categorical"){
                toaster.pop("error", $scope.app.name, "Cannot plot graph for categorical data", 3000);
                return 0;
            }
            vm.showLoading = true;
            //Check theme color
            checkThemeColor();
            var obj = {
                afterEdaDataFilePath:vm.edaData.afterEdaDataFilePath,
                indepVar:feature,
                depVar:vm.target,
                backGround:vm.backGround,
                foreGround:vm.foreGround
            };
            $scope.pType = "ML";
            if(vm.edaData.paragraphColNames.indexOf(feature) >-1){
                $scope.pType = "NLP";
            }

            $http.post("/api/projects/"+vm.project._id+"/graph/trainmodel/scatter?problemType="+$scope.pType,obj).then(function(resp){
                var modalInstance;
                var modalScope = $scope.$new();
                modalInstance = $uibModal.open({
                    templateUrl: "correlationGraphModel.html",
                    size: size,
                    scope: modalScope,
                    backdrop: "static"
                });
                modalScope.cancel = function () {
                    modalInstance.close(modalScope.selected);
                    window.d3 = td3;
                };
                if($scope.pType == "NLP"){
                    vm.colDef = [];
                    vm.gdata = resp.data;
                    var firstRecord = vm.gdata[0];
                    for(var key in firstRecord){
                        if(firstRecord.hasOwnProperty(key))
                            vm.colDef.push({ displayName: key,field: key ,minWidth:120, width:"*"});
                    }
                    vm.gridOptions = {
                        flatEntityAccess: true,
                        fastWatch: false,
                        enableFiltering: false,
                        enableSorting: false,
                        columnDefs: vm.colDef,
                        enableHorizontalScrollbar:2,
                        enablePaginationControls: true,
                        totalItems: 0,
                        paginationPageSize:25,
                        paginationPageSizes: [25,50,100],
                        data : vm.gdata
                    };
                }else{
                    $scope.contentScatter = $sce.trustAsHtml(resp.data);
                }


                vm.showLoading = false;
            },function(err){
                vm.showLoading = false;
                if($scope.pType == "NLP"){
                    $scope.contentScatter = $sce.trustAsHtml("<h5>Could not generate scatter plot!</h5>");
                }
                toaster.pop("error", $scope.app.name, "Oops!, something went wrong while generating scatter plot.", 3000);
            });
        };

        //Building training table
        vm.buildTrainingTable = function(){
            vm.showTrainingTable = false;
            vm.showLoading = true;
            vm.selected = [];
            //var titleHtml = '<input type="checkbox" ng-model="pdc.selectAll" ng-click="pdc.checkAll()">';
            var titleHtml = "<input type=\"checkbox\" ng-model=\"pdc.selectAll\" ng-click=\"pdc.toggleAll(pdc.selectAll, pdc.selected)\">";
            if (vm.dtInstanceTraining.hasOwnProperty("DataTable")) {
                vm.dtInstanceTraining.DataTable.destroy();
                vm.dtColumnsTraining.length = 0;

            }
            vm.dtOptionsTraining = DTOptionsBuilder.fromFnPromise(function () {
                    var defer = $q.defer();
                    defer.resolve(vm.correlationData);
                    return defer.promise;
                }).withOption("processing", true)
                    .withPaginationType("full_numbers")
                    .withOption("createdRow", function(row, data, dataIndex){
                        $compile(angular.element(row).contents())($scope);
                    })
                    .withOption("headerCallback", function(header) {
                        $compile(angular.element(header).contents())($scope);
                        if (!vm.headerCompiled) {
                            // Use this headerCompiled field to only compile header once
                            //vm.headerCompiled = true;
                        }
                    });

                vm.dtColumnsTraining = [
                    DTColumnBuilder.newColumn(null).withTitle(titleHtml).notSortable()
                        .renderWith(function(data, type, full, meta) {
                            vm.selected[full.colName] = isExist(full.colName);
                            //console.log(data.isTargetVariable);
                            return "<input type=\"checkbox\" ng-model=\"pdc.selected['"+data.colName+"']\" ng-click=\"pdc.toggleOne(pdc.selected)\" ng-disabled=\""+data.isTargetVariable+"\">";
                        }),
                    DTColumnBuilder.newColumn("colName").withTitle("Feature"),
                    // DTColumnBuilder.newColumn(null).withTitle('Scatter Plot').notSortable()
                    //     .renderWith(function(data,type,full,meta){
                    //         return '<span class="fa fa-bar-chart pss-chart-hover" ng-click="pdc.openCorrelationGraph(\'lg\',\''+data.colName+'\')"></span>'
                    //     }),
                    DTColumnBuilder.newColumn("pValue").withTitle("Importance")
                    .renderWith(function(data, type, full, meta) {
                        if(data >= 0 && data <= 0.05){
                            return "<uib-progressbar uib-tooltip=\"This feature is ideal for model building.\" tooltip-placement=\"bottom\" value=\""+data*1000+"\" type=\"success\" class=\"m0 progress-xs\">{{"+data+"}}%</uib-progressbar>";
                        }else{
                            return "<uib-progressbar uib-tooltip=\"This feature is not ideal for model building.\" tooltip-placement=\"bottom\" value=\""+(100)+"\" type=\"danger\" class=\"m0 progress-xs\">{{"+data+"}}%</uib-progressbar>";
                        }
                    }).withOption("width", "15%")
                ];
                // if(vm.edaData.problemType !="NLP"){
                //     var correlationColumn = DTColumnBuilder.newColumn(null).withTitle('P-Value').notSortable()
                //         .renderWith(function(data, type, full, meta) {
                //             if((data.corrValue*100)>0){
                //                 return '<uib-progressbar value="'+data.corrValue*100+'" type="success" class="m0 progress-xs">{{'+data.corrValue+'}}%</uib-progressbar>'
                //             }else{
                //                 return '<uib-progressbar value="'+(data.corrValue*-100)+'" type="danger" class="m0 progress-xs">{{'+data.corrValue+'}}%</uib-progressbar>'
                //             }
                //         }).withOption('width', '15%')
                //     vm.dtColumnsTraining.push(correlationColumn)
                // }
            $timeout(function () {
                vm.showTrainingTable = true;
                vm.showLoading = false;
            }, 1000);

        };

        //Function to fetch hyper parameter tuning algorithm form fields.
        vm.onHyperParamAlgoChange = function(algorithm){
            vm.showhptStatus = false;
            var dynamicFormFields = angular.copy(dynamicForm.dynamicFormFields);
            if(vm.project.projectStatus == "Model Generated"){
                //Get previously trained data and set it to formFields
                var temp = dynamicForm.getFormFields(vm.prevTrainingInfo[0].hptPreference,algorithm)[0];
                $scope.formFeilds =  temp ? temp: $scope.formFeilds = dynamicForm.getFormFields(dynamicFormFields,algorithm)[0];
            }else{
                $scope.formFeilds = dynamicForm.getFormFields(dynamicFormFields,algorithm)[0];
            }
            //Find the selected algorithm is present in already saved list of algorithm list
            var t = findInHPTPreference(algorithm);
            if(t.length){
                $scope.formFeilds = t[0];
            }

        };
        // Function to find the selected algorithm is present in the saved preference
        function findInHPTPreference(algoName){
            return $scope.hptPreference.filter(function (algoFormData) {
                return algoFormData.algoName == algoName;
            });
        }
        //Function to reset hyper parameter tuning algorithm form fields.
        vm.resetHPTfields = function(algorithm){
            var dynamicFormFields = angular.copy(dynamicForm.dynamicFormFields);
            $scope.formFeilds = dynamicForm.getFormFields(dynamicFormFields,algorithm)[0];
        };

        //Check whether independent feature is selected or not
        function isExist(col_name){
            if(vm.project.projectStatus == "Model Generated"){
                //console.log(vm.indepVariables)
                return vm.indepVariables.indexOf(col_name) > -1 ? true:false;
            }else{
                return false;
            }
        }

        //Wizard navigation to move to eda section
        vm.gotoEda = function () {
            if (vm.project.filename) {
                //If it is an NLP prblem then go t training wizard
                if(vm.isNlp){
                    return 3;
                }
                if(vm.project.projectStatus != "File Uploaded"){
                    vm.findEda("eda");
                }
                vm.buildEdaStrategyTable();
                //Returning the wizard number so it will navigate to that wizard
                return 2;
            } else {
                toaster.pop("error", $scope.app.name, "Please upload file and go ahead.", 3000);
                //Stay on the same wizard, here we are returning the wizard number
                return 1;
            }
        };

        //Wizard navigation to move to training section
        vm.gotoModelTraining = function () {
            vm.kfold = 10;
            vm.testSize = 20;
            vm.selectAll = false;
            var flag = 0;
            var col_names = [];
            vm.edaSummary.forEach(function(data){
                if(data.data_type != "Numeric" && data.data_miss_value > 0 && data.data_strategy !="Mode"){
                    flag = 1;
                }
            });

            if(flag){
                alert("Categorical,Text,Boolean and DateTime feature(s) can have only Mode strategy");
                return 0;
            }
            if(checkEmptyCustomValues()){
                alert("Custom field value cannot be empty!");
                return 0;
            }
            if(vm.project.projectStatus == "Project Created"){
                return 1;
            }
            if(vm.project.projectStatus == "Model Generated" && !vm.prevTrainingInfo){
                return 1;
            }
            var temp = ["Eda Started", "File Uploaded", "Project Created","EDA Failed"];
            //if (temp.indexOf(vm.project.projectStatus) == -1) {
            if (temp.indexOf(vm.project.projectStatus) == -1) {
                if((vm.edaData.edaMode == vm.edaMode || vm.edaData.length == 0)){
                    vm.findEda("training");
                    vm.showTrainingTable = false;
                    //Returning the wizard number
                    return 3;
                }else{
                    toaster.pop("error", $scope.app.name, "Please complete "+vm.edaMode+" EDA.", 3000);
                }

            } else {
                toaster.pop("error", $scope.app.name, "Please complete EDA.", 3000);
                //Returning the wizard number
                return 2;
            }
        };

        //Building preview table for upload data
        vm.buildUploadPreviewTable = function (response) {
            vm.dtOptions = DTOptionsBuilder.fromFnPromise(function () {
                var defer = $q.defer();
                defer.resolve(response.previewData);
                return defer.promise;
            }).withPaginationType("full_numbers");
            for (var i = 0; i < response.head.length; i++) {
                vm.dtColumns.push(DTColumnBuilder.newColumn(response.head[i]).withTitle(response.head[i]));
            }
        };

        //Open HPT modal
        vm.openHPTModal = function(size){
            vm.showhptStatus = false;
            var modalInstance;
            var modalScope = $scope.$new();
            modalInstance = $uibModal.open({
                templateUrl: "HPTModel.html",
                size: "md",
                scope: modalScope
            });
            modalScope.cancel = function () {
                modalInstance.close(modalScope.selected);
            };
            /**
             *
             * Function to save hyper parameter tuning preferences
             * @param hptPreference
             */
            modalScope.saveHPTPreference = function (hptPreference) {
                var index = -1;
                if(hptPreference){
                    $scope.hptPreference.some(function(obj, i) {
                        return obj.algoName === hptPreference.algoName ? index = i : false;
                    });
                    if(index === false || index === -1){
                        $scope.hptPreference.push(hptPreference);
                    }else{
                        $scope.hptPreference[index] = hptPreference;
                    }
                    vm.showhptStatus = true;
                }else{

                }
            };
        };
        //Open HPT modal
        vm.openEncodingModal = function(size){

            var modalInstance;
            var modalScope = $scope.$new();
            modalInstance = $uibModal.open({
                templateUrl: "encodingModel.html",
                size: "sm",
                scope: modalScope
            });
            modalScope.cancel = function () {
                modalInstance.close(modalScope.selected);
            };
            /**
             *
             * Function to save encoding type
             * @param hptPreference
             */
            modalScope.saveFileEncoding= function (selectedFileEncoding) {
                var projectObj = new Project.myProject({
                    fileEncoding: selectedFileEncoding
                });
                projectObj.$update({projectId:vm.project._id}).then(function(resp){
                    modalInstance.close(modalScope.selected);
                },function(err){
                    console.log(err);
                });
            };
        };
        //Function to download edaSummary
        vm.downloadEdaSummary = function(){
            console.log("EdaSummary");
            if(vm.edaSummary){
                //console.log(vm.edaSummary)
                console.log(vm.edaData);
                ga("send", "event", "Models", "Downloading eda summary", true);
                window.open("/api/eda/"+vm.edaData._id+"/edaSummary/download");
            }

        };
        //Open advanced eda modal
        vm.openAdvEda = function(){
            $scope.contentAdvEda = $sce.trustAsHtml("<div class='text-center'><h3>Generating advanced EDA report...</h3><h6>This may take some time, please wait.</h6></div>");
            var modalInstance;
            var modalScope = $scope.$new();
            modalInstance = $uibModal.open({
                templateUrl: "advEdaModel.html",
                size: "xl",
                scope: modalScope
            });
            modalScope.cancel = function () {
                modalInstance.close(modalScope.selected);
            };
            /**
             *
             * Get adv EDA data
             */
            $http.get("/api/projects/"+vm.project._id+"/eda/advedainfo").then(function(resp){
                $scope.contentAdvEda = $sce.trustAsHtml(resp.data);
                vm.showLoading = false;
            },function(err){
                $scope.contentAdvEda = $sce.trustAsHtml("<h5 class='text-center'>Oops!, something went wrong while generating advanced EDA report.</h5>");
                toaster.pop("error", $scope.app.name, "Oops!, something went wrong while generating advanced EDA report", 3000);
            });
        };
        vm.doMultiUniVariateAnalysis = function(){
            window.d3 = td3;
            vm.allFeatures = [];
            $scope.multiUnivariateAnalysis = "";
            vm.edaSummary.forEach(function(data){
                vm.allFeatures.push(data.col_name);
            });
            checkThemeColor();
            var modalInstance;
            var modalScope = $scope.$new();
            modalInstance = $uibModal.open({
                templateUrl: "multiUnivariateAnalysis.html",
                size: "lg",
                scope: modalScope
            });
            modalScope.cancel = function () {
                window.d3 = td3;
                modalInstance.close(modalScope.selected);
            };
            modalScope.submit = function(){
                //Always clear the previous image and display new one.
                document.getElementById("multivariateImage")
                        .setAttribute(
                            "src", ""
                        );
                $scope.multiUnivariateAnalysis = $sce.trustAsHtml("<div class='text-center'><h3>Loading...</h3></div>");
                var obj = {
                    afterEdaDataFilePath:vm.edaData.afterEdaDataFilePath,
                    backGround:vm.backGround,
                    foreGround:vm.foreGround,
                    selectedVariables:vm.multiUniFeatures,
                    edaSummary:vm.edaSummary
                };
                // $scope.pType = "ML"
                // if(vm.edaData.paragraphColNames.indexOf(feature) >-1){
                //     $scope.pType = "NLP"
                // }
                $http.post("/api/projects/"+vm.project._id+"/report/trainmodel/multiunivariate",obj).then(function(resp){
                    var resp = resp.data;
                    $scope.multiUnivariateAnalysis = $sce.trustAsHtml("");
                    if(resp.data.contentType == "html"){
                        $scope.multiUnivariateAnalysis = $sce.trustAsHtml(resp.data.content);
                    }else{
                    document.getElementById("multivariateImage")
                        .setAttribute(
                            "src", "data:image/jpeg;base64," + resp.data.content
                        );
                    }
                    
                },function(err){
                    $scope.multiUnivariateAnalysis = $sce.trustAsHtml("<div class='text-center'><h3>Something went wrong!</h3></div>");
                });
            };
            
        };
        vm.plotTargetGraph = function(){
            checkThemeColor();
            $scope.targetPlot = $sce.trustAsHtml("<div class='text-center'><h3>Loading...</h3></div>");
                var obj = {
                    afterEdaDataFilePath:vm.edaData.afterEdaDataFilePath,
                    backGround:vm.backGround,
                    foreGround:vm.foreGround,
                    selectedVariables:[vm.target],
                    edaSummary:vm.edaSummary
                };
                $http.post("/api/projects/"+vm.project._id+"/report/trainmodel/multiunivariate?target=true",obj).then(function(resp){
                    var resp = resp.data;
                    $scope.targetPlot = $sce.trustAsHtml("");
                    if(resp.data.contentType == "html"){
                        $scope.targetPlot = $sce.trustAsHtml(resp.data.content);
                    }else{
                    }
                    window.d3 = td3;
                },function(err){
                    $scope.targetPlot = $sce.trustAsHtml("<div class='text-center'><h3>Something went wrong!</h3></div>");
                });
           
        };
        activate();
        function activate() {
            //Validation strategy settings initialization
            vm.setCVStrategies();

            var api = "/api/projects/" + vm.project._id + "/data";
            // var api = '/api/projects/' + vm.project._id + '/merge?mtype=file&encoding=utf-8';
            var uploader = vm.uploader = new FileUploader({
                url: api,
                removeAfterUpload: true
            });
            // FILTERS

            uploader.filters.push({
                name: "fileTypeChecker",
                fn: function(item /*{File|FileLikeObject}*/, options) {
                    var type = null;
                    if(item.type){
                        type = "|" + item.type.slice(item.type.lastIndexOf("/") + 1) + "|";
                    }else{
                        var temp = item.name.split(".");
                        type = temp[temp.length - 1];
                    }
                    return "|csv|vnd.ms-excel|zip|x-zip-compressed|vnd.openxmlformats-officedocument.spreadsheetml.sheet|pkl|pk|pl|pickle|".indexOf(type) !== -1;
                }
            });

            // CALLBACKS

            uploader.onWhenAddingFileFailed = function (item /*{File|FileLikeObject}*/, filter, options) {
                toaster.pop("error", $scope.app.name, "Please upload a csv file.", 3000);
            };

            //On after selecting a file,upload it to server
            uploader.onAfterAddingFile = function (fileItem) {
                vm.showLoading = true;
                vm.panelFileUpload = true;
                vm.featureList.length = 0;
                vm.previousIndex = -1;
                vm.selected.length = 0;
                vm.flow_failed_count = 0;
                if (vm.uploader.queue[0]) {
                    ga("send", "event", "Project", "File uploading started", true);
                    vm.uploader.queue[0].upload();
                    vm.uploader.onCompleteItem = function (fileItem, response, status, headers) {

                        if (vm.dtInstanceTraining.hasOwnProperty("DataTable")) {
                            vm.dtInstanceTraining.DataTable.destroy();
                            var t =[];
                            var defer = $q.defer();
                            defer.resolve(t);
                            vm.dtInstanceTraining.changeData(defer.promise);

                        }
                        vm.target = null;
                        $scope.targetPlot = $sce.trustAsHtml("");
                        vm.modelAlgorithms = [];
                        vm.multiUniFeatures = [];
                        //Reset the file input component
                        var fileElement = angular.element("#dataset");
                        angular.element(fileElement).val(null);
                        $scope.$apply();

                        if(status == 400){
                            toaster.pop("error", $scope.app.name,response.message, 4000);
                            vm.showLoading = false;
                            vm.status[0].title = "File uploaded failed";
                            vm.status[0].key = "failed";

                            return 0;
                        }
                        vm.project = response.projectDetails;
                        ProjectCore.setProject(vm.project);
                        if(response.status=="flow_start"){
                            toaster.pop("success", $scope.app.name,"Flow execution started, please wait!", 3000);
                            vm.status[0].title = "File uploaded";
                            vm.status[0].key = "uploaded";
                        }else{
                            ga("send", "event", "Project", "File uploading completed", true);
                        $location.hash("dataPanel");//bottom is an element id
                        
                        vm.showLoading = false;
                        $timeout(function () {
                            vm.panelFileUpload = false;
                        }, 1000);

                        vm.status[0].title = "File uploaded";
                        vm.status[0].key = "uploaded";
                        vm.status.push({
                            title: "Reading file",
                            value: fileItem.file,
                            key: "read_file",
                            timestamp: new Date()
                        });

                        //Reset Eda settings
                        vm.edaMode = "auto";
                        vm.manualEdaMode = false;
                        vm.showEdaSummary = false;


                        //Build preview table for uploaded data
                        vm.buildPreviewTable(function(data){
                            vm.showLoading = false;
                        });
                        vm.uploader.queue.length = 0;

                        vm.edaAutoFeatureList = angular.copy(vm.featureList);
                        }
                        
                    };
                }
            };
            uploader.onAfterAddingAll = function (addedFileItems) {
                vm.status = [];
            };
            uploader.onProgressItem = function (fileItem, progress) {
                //console.info('onProgressItem', fileItem, progress);
                vm.status = [];
                vm.status.push({
                    title: "Uploading file...",
                    value: fileItem.file,
                    key: "upload",
                    timestamp: new Date()
                });
            };

            //Different callback functions for file uploader

            //uploader.onProgressAll = function(progress) {
            //    console.info('onProgressAll', progress);
            //};
            //uploader.onSuccessItem = function(fileItem, response, status, headers) {
            //    console.info('onSuccessItem', fileItem, response, status, headers);
            //};
            //uploader.onErrorItem = function(fileItem, response, status, headers) {
            //    console.info('onErrorItem', fileItem, response, status, headers);
            //};
            //uploader.onCancelItem = function(fileItem, response, status, headers) {
            //    console.info('onCancelItem', fileItem, response, status, headers);
            //};
            //uploader.onCompleteItem = function(fileItem, response, status, headers) {
            //    console.info('onCompleteItem', fileItem, response, status, headers);
            //};
            //uploader.onCompleteAll = function() {
            //    console.info('onCompleteAll');
            //};
        }
    }
})();

//Filter to convert byte to different data units
angular.module("app.projectDatas").filter("bytes", function () {
    return function (bytes, precision) {
        if (isNaN(parseFloat(bytes)) || !isFinite(bytes)) return "-";
        if (typeof precision === "undefined") precision = 1;
        var units = ["bytes", "kB", "MB", "GB", "TB", "PB"],
            number = Math.floor(Math.log(bytes) / Math.log(1024));
        return (bytes / Math.pow(1024, Math.floor(number))).toFixed(precision) + " " + units[number];
    };
});
angular.module("app.projectDatas").directive("histogram", ["$parse", "$window", function($parse, $window){
    return{
        restrict: "E",
        replace: false,
        template: "<svg class='histogram-chart'></div>",
        link: function(scope, elem, attrs) {
            var exp = $parse(attrs.data);
            console.log(exp);
            var d3 = $window.d3;


            /*
             Sortable barchart. Largely taken from:
             http://bl.ocks.org/mbostock/3885705
             */

            // Aesthetic settings
            var margin = {top: 20, right: 50, bottom: 20, left: 50},
                width = 400 - margin.left - margin.right,
                height = 400 - margin.top - margin.bottom,
                barColor = "steelblue",
                axisColor = "whitesmoke",
                axisLabelColor = "grey",
                yText = "Number",
                xText = "IDs";

            // Inputs to the d3 graph
            var data = scope[attrs.data];


        }
    };
}]);
angular.module("app.projectDatas").directive("pssCustomTrigger", function () {
    return {
        restrict: "A",
        scope:true,
        link: function(scope, element,attributes) {
            element.on("change", function (e, param) {
                if(Object.keys(param).indexOf("deselected") !== -1){
                    scope.hptPreference.forEach(function(data,i){
                        if(data.algoName == param["deselected"]){
                            scope.hptPreference.splice(i,1);
                            scope.formFeilds.fields.length = 0;
                        }
                    });
                }
            });
        }
    };
});