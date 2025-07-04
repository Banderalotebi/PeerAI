/**
 * Created by vishnu on 22/03/18.
 */
angular.module("app.settings")
    .controller("PsCoreConfigController",
        ["$scope", "toaster", "PsCoreConfig","SweetAlert", "ProjectCore",
            function ($scope, toaster, PsCoreConfig, SweetAlert, ProjectCore)
            {
                $scope.psScoreData = null;
                $scope.psScoreMachines = null;


                //Find ps core machines
                $scope.find = function(){
                    PsCoreConfig.psCore.query().$promise.then(function(list){
                        $scope.psScoreMachines = list;
                    },function(err){

                    });
                };
                $scope.project = ProjectCore.getProject();
                //Delete pscore config
                $scope.delete = function(config){
                    SweetAlert.swal({
                        title: "Are you sure?",
                        text: "You will not be able to recover this project",
                        type: "warning",
                        showCancelButton: true,
                        confirmButtonColor: "#DD6B55",
                        confirmButtonText: "Delete!",
                        closeOnConfirm: true
                    }, function (isConfirm) {
                        if (isConfirm) {
                            config.$remove({pscoreConfigId:config._id}).then(
                                function (success) {
                                    $scope.find();
                                    ga("send", "event", "PSCore Config", "PSCore config deleted", true);
                                }, function (err) {
                                    toaster.pop("error", $scope.app.name, err.statusText, 3000);
                                });
                        }
                    });
                };
                //Create pscore id.
                $scope.createPsScore = function(){
                    PsCoreConfig.psCore.save({machineName:$scope.machineName}).$promise.then(function(resp){
                        $scope.psScoreData = resp;
                    },function(err){
                        toaster.pop("error", $scope.app.name, "Couldn't save pscore config, " + err.statusText, 3000);
                    });
                };
            }]);
