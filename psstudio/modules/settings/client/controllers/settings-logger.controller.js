/**
 * Created by dushyant on 13/4/16.
 */
angular.module("app.settings")
    .controller("SettingsLoggerController",
        ["$scope", "toaster", "Logger","PsCoreConfig",
            function ($scope, toaster, Logger, PsCoreConfig)
            {
                $scope.psScoreData = null;
                $scope.PsCoreExportOptions = {};
                $scope.loggerSettings = {};
                $scope.exportOptions = {};
                $scope.OSExportOptions = {};
                $scope.OSExportOptions.order = "desc";
                $scope.prettify = true;
                var controller = this;

                $scope.exportOptions = {
                    startDate: moment().subtract(1, "days").startOf("day"),
                    endDate:moment().endOf("day")
                };

                $scope.OSExportOptions = {
                    startDate: moment().subtract(1, "days").startOf("day"),
                    endDate:moment().endOf("day")
                };

                $scope.opts = {
                    applyClass: "btn-green",
                    timePicker: true, //for adding time picker
                    //timePickerIncrement: 10,
                    locale: {
                        applyLabel: "Apply",
                        fromLabel: "From",
                        format: "MM/DD/YYYY h:mm A", //will give you 2017-01-06
                        //format: "D-MMM-YY", //will give you 6-Jan-17
                        //format: "D-MMMM-YY", //will give you 6-January-17
                        toLabel: "To",
                        cancelLabel: "Cancel",
                        customRangeLabel: "Custom range"
                    },
                    ranges: {
                        "Today": [moment(), moment()],
                        "Yesterday": [moment().subtract(1, "days").startOf("day"), moment().subtract(1, "days").endOf("day")],
                        "Last 7 Days": [moment().subtract(6, "days").startOf("day"), moment().endOf("day")],
                        "Last 30 Days": [moment().subtract(29, "days").startOf("day"), moment().endOf("day")]
                    }
                };

                // Fetch the pscore machine details
                $scope.fetchPsCoreMachines = function(){
                    PsCoreConfig.psCore.query().$promise.then(function(list){
                        $scope.machines = list;
                    },function(err){

                    });
                };

//Export Logs
                $scope.exportLogs = function (isValid)
                {
                    $scope.error = null;
                    if (!isValid)
                    {
                        $scope.$broadcast("show-errors-check-validity", "exportLogForm");
                        return false;
                    }
                    toaster.pop("wait", $scope.app.name, "Exporting system Log...", 3000);
                    Logger.logs.export({exportOptions: $scope.exportOptions}).$promise.then(function (response)
                    {
                        if ($scope.prettify)
                        {
                            response = JSON.stringify(response, null, 4);
                        }
                        else
                        {
                            response = JSON.stringify(response);
                        }
                        var blob = new Blob([response], {type: "text/json"});
                        if (window.navigator && window.navigator.msSaveOrOpenBlob)
                        {
                            window.navigator.msSaveOrOpenBlob(blob);
                        }
                        else
                        {

                            var e = document.createEvent("MouseEvents"),
                                a = document.createElement("a");

                            a.download = "PredictSense.log";
                            a.href = window.URL.createObjectURL(blob);
                            a.dataset.downloadurl = ["text/json", a.download, a.href].join(":");
                            e.initEvent("click", true, false, window,
                                0, 0, 0, 0, 0, false, false, false, false, 0, null);
                            a.dispatchEvent(e);
                        }
                    }, function (err)
                    {
                        toaster.pop("error", $scope.app.name, "Problem exporting log. " + err.statusText, 3000);
                    });
                };
//Route Access Logs
                $scope.exportRouteAccessLogs = function ()
                {
                    Logger.routeAccessLogs.export().$promise.then(function (response)
                    {

                        if (!response.logs)
                        {
                            toaster.pop("error", $scope.app.name, "Server sent response in unrecognized structure", 3000);

                        }
                        var blob = new Blob([response.logs], {type: "text/json"});
                        if (window.navigator && window.navigator.msSaveOrOpenBlob)
                        {
                            window.navigator.msSaveOrOpenBlob(blob);
                        }
                        else
                        {

                            var e = document.createEvent("MouseEvents"),
                                a = document.createElement("a");

                            a.download = "Route Access.log";
                            a.href = window.URL.createObjectURL(blob);
                            a.dataset.downloadurl = ["text/plain", a.download, a.href].join(":");
                            e.initEvent("click", true, false, window,
                                0, 0, 0, 0, 0, false, false, false, false, 0, null);
                            a.dispatchEvent(e);
                        }

                    }, function (err)
                    {
                        toaster.pop("error", $scope.app.name, "Problem exporting route access log. " + err.statusText, 3000);
                    });
                };
//Export OS Logs
                $scope.exportOSLogs = function ()
                {

                    Logger.OSLogs.export({
                        exportOptions: $scope.OSExportOptions
                    }).$promise.then(function (response)
                    {

                        if (!response.logs)
                        {
                            toaster.pop("error", $scope.app.name, "Server sent response in unrecognized structure", 3000);

                        }

                        var blob = new Blob([response.logs], {type: "text/json"});
                        if (window.navigator && window.navigator.msSaveOrOpenBlob)
                        {
                            window.navigator.msSaveOrOpenBlob(blob);
                        }
                        else
                        {

                            var e = document.createEvent("MouseEvents"),
                                a = document.createElement("a");

                            a.download = "Operating System Logs.log";
                            a.href = window.URL.createObjectURL(blob);
                            a.dataset.downloadurl = ["text/plain", a.download, a.href].join(":");
                            e.initEvent("click", true, false, window,
                                0, 0, 0, 0, 0, false, false, false, false, 0, null);
                            a.dispatchEvent(e);
                        }

                    }, function (err)
                    {
                        toaster.pop("error", $scope.app.name, "Problem exporting operating system log. " + err.statusText, 3000);
                    });
                };
//Repair Logs
                $scope.repairLogs = function ()
                {
                    Logger.repair.execute().$promise.then(function (response)
                        {
                            toaster.pop("wait", $scope.app.name, "Repairing Logs...", 3000);
                        },
                        function (err)
                        {
                            toaster.pop("error", $scope.app.name, err.statusText, 3000);
                        });
                };
//Save Logger Settings
                $scope.saveLoggerSettings = function (isValid)
                {
                    $scope.error = null;
                    if (!isValid)
                    {
                        $scope.$broadcast("show-errors-check-validity", "logSettingsForm");
                        return false;
                    }
                    toaster.pop("wait", $scope.app.name, "Saving log settings...", 3000);
                    Logger.settings.save({loggerSettings: $scope.loggerSettings}).$promise.then(function (response)
                        {
                            toaster.pop("success", $scope.app.name, "Log Settings saved", 4000);
                        },
                        function (err)
                        {
                            toaster.pop("error", $scope.app.name, "Couldn't save Log Settings. " + err.statusText, 3000);
                        });
                };
                //Export ps core logs
                $scope.exportPsCoreLogs = function(isValid){
                    $scope.error = null;
                    if (!isValid)
                    {
                        $scope.$broadcast("show-errors-check-validity", "psCoreLogForm");
                        return false;
                    }
                    toaster.pop("wait", $scope.app.name, "Exporting PS Core Log...", 3000);
                    Logger.PsCoreLogs.export({pscoreConfigId:$scope.PsCoreExportOptions.machineId}).$promise.then(function (response)
                    {
                        if ($scope.prettify)
                        {
                            response = JSON.stringify(response, null, 4);
                        }
                        else
                        {
                            response = JSON.stringify(response);
                        }
                        var blob = new Blob([response], {type: "text/json"});
                        if (window.navigator && window.navigator.msSaveOrOpenBlob)
                        {
                            window.navigator.msSaveOrOpenBlob(blob);
                        }
                        else
                        {

                            var e = document.createEvent("MouseEvents"),
                                a = document.createElement("a");

                            a.download = "PSCore.log";
                            a.href = window.URL.createObjectURL(blob);
                            a.dataset.downloadurl = ["text/json", a.download, a.href].join(":");
                            e.initEvent("click", true, false, window,
                                0, 0, 0, 0, 0, false, false, false, false, 0, null);
                            a.dispatchEvent(e);
                        }
                    }, function (err)
                    {
                        toaster.pop("error", $scope.app.name, "Problem exporting log. " + err.data.statusText, 3000);
                    });
                };
//Load Logger Settings
                $scope.loadLoggerSettings = function ()
                {
                    Logger.settings.get().$promise.then(function (settings)
                    {
                        $scope.loggerSettings = settings.loggerSettings;
                    });
                };
                //Create pscore id.

                $scope.createPsScore = function(){
                    Logger.createPsCore.save({machineName:$scope.machineName}).$promise.then(function(resp){
                        $scope.psScoreData = resp;
                    },function(err){
                        toaster.pop("error", $scope.app.name, "Couldn't save pscore config, " + err.statusText, 3000);
                    });
                };
            }])

    //Convert bytees to MB and vice versa for LoggerSettings
    .directive("byter", function ()
    {
        return {
            restrict: "A",
            require: "ngModel",
            link: function (scope, element, attrs, ngModel)
            {

                //format text going to user (model to view)
                ngModel.$formatters.push(function (value)
                {
                    return value / 1024 / 1024;
                });

                //format text from the user (view to model)
                ngModel.$parsers.push(function (value)
                {
                    return value * 1024 * 1024;
                });
            }
        };
    });
