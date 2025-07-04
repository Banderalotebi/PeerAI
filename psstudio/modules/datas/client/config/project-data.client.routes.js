"use strict";

// Setting up route
angular.module("app.projectDatas").config(["$stateProvider","RouteHelpersProvider",
  function ($stateProvider,helper) {
    // Users state routing
    $stateProvider
      .state("app.data", {
        url: "data",
        templateUrl: "modules/datas/client/views/project-data.client.view.html",
        resolve: helper.resolveFor("datatables","angularFileUpload","taginput", "inputmask", "localytics.directives", "ui.bootstrap-slider", "ngWig", "filestyle", "summernote","ui.select"),
        controller:"ProjectDataController as pdc",
        authorization: {
            allowedRoles: ["user", "admin"]
        }
      });
  }
]);
