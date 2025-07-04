"use strict";

// Setting up route
angular.module("app.help").config(["$stateProvider","RouteHelpersProvider",
  function ($stateProvider,helper) {
    // Users state routing
    $stateProvider
      .state("app.help", {
        url: "help",
        templateUrl: "modules/help/client/views/help.client.view.html",
        resolve: helper.resolveFor("inputmask", "localytics.directives", "ui.bootstrap-slider", "ngWig", "filestyle", "summernote"),
        controller:"HelpController as help",
        authorization: {
            allowedRoles: ["user", "admin"]
        }
      });
  }
]);
