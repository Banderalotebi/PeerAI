/**
 * Created by vishnu on 21/11/18.
 */
"use strict";
angular.module("app.udd").controller("UDDController", ["$scope", "$state", "$stateParams", "toaster", "UddFlow", "SweetAlert", "UddExecution","Project","ProjectCore", "Socket",
        function ($scope, $state, $stateParams, toaster,
            UddFlow, SweetAlert, UddExecution, Project, ProjectCore, Socket) {
            var vm = this;
            vm.showLoading= false;
            $scope.flowType = "interceptor";

            $scope.flowURL = null;
            vm.project = ProjectCore.getProject();
            $scope.selectedFlow = vm.project.flowId ? vm.project.flowId:"No active flow";

            $scope.iconPath = "./modules/udd/client/img/node-red.png";

            //refresh on select
            $scope.refresh = function () {
                var iframe = document.getElementById("myiframe");
                iframe.src = iframe.src;

            };

            $scope.refreshEdit = function () {
                var myFrame = document.querySelector("iframe");
                myFrame.contentWindow.location.reload(true);
            };

            //to prohibit user to save a flow without any node in iframe
            $scope.checknone = function () {
                var iframeHtml = window.frames["myiframe"].contentDocument.getElementsByClassName("header-toolbar");
                if (!iframeHtml[0].innerHTML.includes("deploy-button disabled")) {
                    return false;
                } else {
                    return true;
                }

            };

            // Create New Udd Flow
            $scope.create = function (isValid) {
                $scope.error = null;
                if (!isValid) {
                    $scope.$broadcast("show-errors-check-validity", "flowForm");

                    return false;
                }
                var iframe = $("iframe");
                var btn_deploy = iframe.contents().find("#btn-deploy")[0];
                var $urls = $(this).attr("title");
                var urlString = document.getElementById("myiframe").contentWindow.location.href;
                var position = urlString.lastIndexOf("/");
                var flowId = urlString.substring(position + 1, urlString.length);
                btn_deploy.click();

                // Create new Sync Option object

                var uddFlow = new UddFlow({
                    flowName: this.flowName,
                    flowId: flowId,
                    flowType:this.flowType
                });
                uddFlow.$save(function (response) {
                    ga("send", "event", "UDD Management", "UDD Flow Created", true);
                    $state.go("app.udd-view");
                }, function (errorResponse) {
                    $scope.error = errorResponse.data.message;
                });


            };

            // Find a list of Udd Flows
            $scope.find = function () {
                $scope.uddFlows = UddFlow.query();
            };

            // Find existing Udd Flow
            $scope.findOne = function () {
                $scope.uddFlows = UddFlow.get({
                    uddId: $stateParams.uddId
                }).$promise.then(function (option) {
                    try {
                        $scope.uddFlow = option;
                        $scope.flowURL = "/!/#flow/" + option.flowId;

                    } catch (e) {}
                });

            };

            //Create New Flow
            $scope.createNewFlow = function () {
                $scope.newflowURL = "/!/";

            };

            // Update existing Udd Flow
            $scope.update = function (isValid) {
                $scope.error = null;
                if (!isValid) {
                    $scope.$broadcast("show-errors-check-validity", "uddFlowForm");

                    return false;
                }

                var iframe = $("iframe");
                var btn_deploy = iframe.contents().find("#btn-deploy")[0];
                var $urls = $(this).attr("title");
                var urlString = document.getElementById("myiframe").contentWindow.location.href;
                var position = urlString.lastIndexOf("/");
                var flowId = urlString.substring(position + 1, urlString.length);
                btn_deploy.click();

                var uddFlow = $scope.uddFlow;
                uddFlow.flowId = flowId;
                uddFlow.$update(function (response) {
                    $state.go("app.udd-view");

                }, function (errorResponse) {
                    $scope.error = errorResponse.data.message;
                });
            };

            //Delete Udd Flow
            $scope.remove = function (uddFlow) {
                SweetAlert.swal({
                    title: "Are you sure?",
                    text: "You will not be able to recover this udd Flow!",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "Delete!",
                    closeOnConfirm: true
                }, function (isConfirm) {
                    if (isConfirm) {
                        if (uddFlow) {
                            uddFlow.$remove().then(function (success) {
                                for (var i in $scope.uddFlows) {
                                    if ($scope.uddFlows[i] === uddFlow) {
                                        $scope.uddFlows.splice(i, 1);
                                        ga("send", "event", "UDD Management", "UDD Flow Deleted", true);
                                    }
                                }
                            }, function (err) {
                                toaster.pop("error", $scope.app.name, err.statusText, 3000);
                            });
                        } else {
                            $scope.uddFlow.$remove().then(function (success) {
                                    $state.go("app.udd-list");
                                    ga("send", "event", "UDD Management", "UDD Flow Deleted", true);
                                },
                                function (err) {
                                    toaster.pop("error", $scope.app.name, err.statusText, 3000);
                                });
                        }
                    }
                });
            };


            $scope.activateFlow = function(uddFlow){
                if(uddFlow){
                    var project = new Project.myProject({
                        flowId:uddFlow
                    });
                    project.$update({projectId:vm.project._id}).then(function(resp){
                        toaster.pop("success", $scope.app.name, "Activated flow for this project", 3000);
                    },function(err){
                        toaster.pop("error", $scope.app.name, err.statusText, 3000);
                    });
                }
            };

            $scope.startFlow = function(uddFlow){
                vm.showLoading = true;
                // var uddExecution =new ({_id:uddFlow._id});
                UddExecution.startFlow.get({uddId:uddFlow._id,projectId:vm.project._id}).$promise.then(function scb(resp){
                    toaster.pop("success", $scope.app.name, "Started flow execution.", 3000);
                },function ecb(err){
                    vm.showLoading = false;
                    toaster.pop("error", $scope.app.name, err.statusText, 3000);
                });
            };

            Socket.on("uddFlowCompleted",function(message){
                if(message.status=="complted"){
                    vm.showLoading = false;
                    toaster.pop("success", $scope.app.name, "Flow execution completed", 3000);
                    $state.go("app.data");
                }
                if(message.status=="flow_failed"){
                    toaster.pop("error", $scope.app.name, message.err_msg, 3000);
                    vm.showLoading = false;
                }
                // $state.go("app.models");
            });
            // Remove the event listener when the controller instance is destroyed
            $scope.$on("$destroy", function () {
                Socket.removeListener("uddFlowCompleted");
            });
        }
    ])

    //put focus on element
    .directive("focus", function () {
        return {
            link: function (scope, element, attrs) {
                element[0].focus();
            }
        };
    });
