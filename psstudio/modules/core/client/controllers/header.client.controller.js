"use strict";

angular.module("core").controller("HeaderController", ["$scope", "$state", "Authentication", "Menus", "ProjectCore", "Socket", "LayoutSettings",
    function ($scope, $state, Authentication, Menus, ProjectCore, Socket, LayoutSettings) {
        // Expose view variables
        $scope.$state = $state;
        $scope.authentication = Authentication;
        $scope.projectName = ProjectCore.getProject().name;
        if(Authentication.user.layout){
            $scope.app.layout.theme = Authentication.user.layout.theme;
        }

        $scope.onChangeTheme = function (theme) {
            var layoutSettings = new LayoutSettings({
                layout:{
                    theme:theme
                }
            });

            layoutSettings.$save({userId:$scope.authentication.user._id},function (res) {
                window.user.layout.theme = theme;
            }, function (err) {

            });
        };

        //Socket
        // Make sure the Socket is connected
        if (!Socket.socket) {
            Socket.connect();
        }
        //Join to the socket server
        Socket.emit("join", ProjectCore.getProject());

        // Get the topbar menu
        $scope.menu = Menus.getMenu("topbar");

        // Toggle the menu items
        $scope.isCollapsed = false;
        $scope.toggleCollapsibleMenu = function () {
            $scope.isCollapsed = !$scope.isCollapsed;
        };

        // Collapsing the menu after navigation
        $scope.$on("$stateChangeSuccess", function () {
            $scope.isCollapsed = false;
        });
    }
]);
