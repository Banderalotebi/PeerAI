/**
 * Created by saket on 2/2/16.
 */
(function() {
"use strict";

// Setting up route
angular.module("app.settings")
       .config(appRoutes);
appRoutes.$inject = ["$stateProvider", "RouteHelpersProvider"];
    function appRoutes($stateProvider, helper)
    {
        // Admin panel routing
        $stateProvider
            .state("app.settings-logger", {
                url: "settings/logger",
                title: "Log Settings",
                templateUrl: "modules/settings/client/views/settings-logger.client.view.html",
                authorization: {
                    allowedRoles: ["admin"]
                }
            })
            .state("app.settings-createpscore", {
                url: "settings/createpscore",
                title: "Create PS Core Id",
                resolve: helper.resolveFor("datatables", "oitozero.ngSweetAlert", "taginput", "inputmask", "localytics.directives", "ui.bootstrap-slider", "ngWig", "filestyle"),
                templateUrl: "modules/settings/client/views/pscore/create-pscore.client.view.html",
                authorization: {
                    allowedRoles: ["admin"]
                }
            })
            .state("app.settings-listpscore", {
                url: "settings/listpscore",
                title: "List PS Core Ids",
                resolve: helper.resolveFor("datatables", "oitozero.ngSweetAlert", "taginput", "inputmask", "localytics.directives", "ui.bootstrap-slider", "ngWig", "filestyle"),
                templateUrl: "modules/settings/client/views/pscore/list-pscore.client.view.html",
                authorization: {
                    allowedRoles: ["admin"]
                }
            })
            .state("app.settings-projectinfo", {
                url: "settings/projectinfo",
                title: "Project info",
                resolve: helper.resolveFor("datatables", "oitozero.ngSweetAlert", "taginput", "inputmask", "localytics.directives", "ui.bootstrap-slider", "ngWig", "filestyle"),
                templateUrl: "modules/settings/client/views/pscore/projectinfo.client.view.html",
                authorization: {
                    allowedRoles: ["admin"]
                }
            });
    }
})();

