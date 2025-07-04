/**=========================================================
 * Module:
 =========================================================*/

(function() {
    "use strict";

    angular
        .module("app.help")
        .controller("HelpController", HelpController);

    HelpController.$inject = ["$state","$scope"];
    function HelpController($state,$scope) {
        var vm = this;

        activate();

        function activate() {

        }
    }
})();
