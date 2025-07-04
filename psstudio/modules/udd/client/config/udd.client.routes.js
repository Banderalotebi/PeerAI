/**
 * Created by vishnu on 21/11/18.
 */
(function () {
    "use strict";

    angular
        .module("app.udd")
        .config(appRoutes);
    appRoutes.$inject = ["$stateProvider", "RouteHelpersProvider"];

    function appRoutes($stateProvider, helper) {
        $stateProvider
            .state("app.udd-create", {
                url: "udd/create",
                title: "Create Flow",
                templateUrl: "modules/udd/client/views/create-udd.client.view.html",
                //resolve: helper.resolveFor('taginput', 'inputmask', 'datatables', 'codemirror', 'ui.codemirror', 'codemirror-modes-web'),
                resolve: helper.resolveFor("taginput", "oitozero.ngSweetAlert", "inputmask", "datatables", "codemirror", "ui.codemirror", "codemirror-modes-web","ngWig"),
                authorization: {
                    allowedRoles: ["admin", "user"]
                }
            })
            .state("app.udd-view", {
                url: "udd",
                title: "UDD List",
                resolve: helper.resolveFor("datatables", "oitozero.ngSweetAlert"),
                templateUrl: "modules/udd/client/views/list-udd.client.view.html",
                authorization: {
                    allowedRoles: ["admin", "user"]
                }
            })
            .state("app.udd-edit", {
                url: "udd/:uddId/edit",
                title: "Edit UDD",
                resolve: helper.resolveFor("datatables", "oitozero.ngSweetAlert", "taginput", "inputmask"),
                templateUrl: "modules/udd/client/views/edit-udd.client.view.html",
                authorization: {
                    allowedRoles: ["admin", "user"]
                }
            })
            .state("app.udd-selectDevice", {
                url: "udd/select",
                title: "Select Device",
                templateUrl: "modules/udd/client/views/select-device.client.view.html",
                resolve: helper.resolveFor("oitozero.ngSweetAlert", "datatables"),
                controller: "UDDController",
                authorization: {
                    allowedRoles: ["admin", "user"]
                }
            });

    }
})();
