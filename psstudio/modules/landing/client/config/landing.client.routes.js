"use strict";

// Setting up route
angular.module("app.landing").config(["$stateProvider",
  function($stateProvider) {
    // Users state routing
    $stateProvider.
    state("landing", {
      url: "/landing",
      templateUrl: "modules/landing/client/views/landing.client.view.html",
      controller:"LandingController"
    });
  }
]);
