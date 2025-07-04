/**
 * Created by vishnu on 01/12/17.
 */
(function ()
{
    "use strict";

    angular
        .module("app.usermanagement")
        .config(appRoutes);
    appRoutes.$inject = ["$stateProvider", "RouteHelpersProvider"];

    function appRoutes($stateProvider, helper)
    {
        $stateProvider
            .state("app.user-create", {
                url: "users/create",
                title: "Add User",
                templateUrl: "modules/usermanagement/client/views/create-user.client.view.html",
                resolve: helper.resolveFor("datatables", "oitozero.ngSweetAlert", "taginput", "inputmask", "localytics.directives", "ui.bootstrap-slider", "ngWig", "filestyle"),
                authorization: {
                    allowedRoles: ["admin"]
                }
            })
            .state("app.user-view", {
                url: "users",
                title: "User List",
                resolve: helper.resolveFor("angular-jqcloud", "datatables", "oitozero.ngSweetAlert"),
                templateUrl: "modules/usermanagement/client/views/list-user.client.view.html",
                authorization: {
                    allowedRoles: ["admin"]
                }
            })
            .state("app.user-edit", {
                url: "users/:userId/edit",
                title: "Edit User",
                resolve: helper.resolveFor("datatables", "oitozero.ngSweetAlert", "taginput", "inputmask", "localytics.directives", "ui.bootstrap-slider", "ngWig", "filestyle"),
                templateUrl: "modules/usermanagement/client/views/edit-user.client.view.html",
                authorization: {
                    allowedRoles: ["admin"]
                }
            })
        ;
    }
})();
