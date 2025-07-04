/**
 * Created by saket on 30/3/16.
 */
"use strict";

angular.module("app.usermanagement").controller("UsersController", ["$scope", "$http", "$stateParams", "$window", "$location", "Authentication", "toaster", "Users", "Admin","PasswordValidator",
        "SweetAlert",
// User-Management controller
        function ($scope, $http, $stateParams, $window, $location, Authentication, toaster, Users, Admin, PasswordValidator,
                  SweetAlert) {
            $scope.authentication = Authentication;
            $scope.credentials = {};
            $scope.credentials.roles = ["user"];
            $scope.popoverMsg = PasswordValidator.getPopoverMsg();
            $scope.passwordDetails = {};

            $scope.addNewUser = function () {
                $http.post("/api/auth/signup", $scope.credentials).success(function (response) {
                    var lUser = $scope.credentials.roles;
                    ga("send", "event", "User Management", "User Created",lUser, true);
                     //If successful we assign the response to the global user model
                    //$scope.authentication.user = response;

                    // And redirect to the user list page
                    $location.path("/users");
                }).error(function (response) {
                    $scope.error = response.message;
                });
            };

            //List all users
            $scope.find = function () {
                $scope.users = Admin.query();
            };

            //Find User
            $scope.findUser = function () {
                Admin.get({
                    userId: $stateParams.userId
                }).$promise.then(function (user) {
                    $scope.user = user;
                });
            };

            // Remove User
            $scope.remove = function (user) {
                var lUser =$scope.credentials.roles;
                SweetAlert.swal({
                    title: "Are you sure?",
                    text: "You will not be able to recover this User!",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "Delete!",
                    closeOnConfirm: true
                }, function (isConfirm) {
                    if (isConfirm) {
                        if (user) {
                            user.$remove();
                            for (var i in $scope.users) {
                                if ($scope.users[i] === user) {
                                    $scope.users.splice(i, 1);
                                    //ga('send', 'event', 'User Management', 'User Deleted',lUser, true);
                                }
                            }
                        }
                        else {
                            $scope.user.$remove(function () {
                                $location.path("users");
                               // ga('send', 'event', 'User Management', 'User Deleted',lUser, true);

                            });
                        }
                    }

                });
            };


            // Update existing User
            $scope.update = function (isValid) {
                $scope.error = null;

                if (!isValid) {
                    $scope.$broadcast("show-errors-check-validity", "userForm");

                    return false;
                }
                var user = $scope.user;
                user.$update(function () {
                    $location.path("users");

                }, function (errorResponse) {
                    $scope.error = errorResponse.data.message;
                });
            };
            // Change user password
            $scope.resetUserPassword = function (isValid) {
                $scope.success = $scope.error = null;
        
                if (!isValid) {
                $scope.$broadcast("show-errors-check-validity", "resetPasswordForm");
        
                return false;
                }
                $scope.passwordDetails.aid = $scope.authentication.user._id;
                $scope.passwordDetails.uid = $scope.user._id;
                $http.post("/api/auth/rba", $scope.passwordDetails).success(function (response) {
                // If successful show success message and clear form
                $scope.passwordDetails = null;
                $scope.successpc = response.message;
        
                // And redirect to the index page
                }).error(function (response) {
                    $scope.errorpc = response.message;
                });
            };
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
