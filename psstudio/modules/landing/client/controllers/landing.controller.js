/**=========================================================
 * Module:
 =========================================================*/

(function() {
    "use strict";

    angular
        .module("app.landing")
        .controller("LandingController", LandingController);

    LandingController.$inject = ["$state","$scope"];
    function LandingController($state,$scope) {
        var vm = this;

        activate();

        ////////////////
        $scope.gotoLogin = function(){
            //console.log($state.go('page.authentication.signin'))
            window.location= "page/authentication/signin";
        };
        function activate() {

        }
    }
})();
