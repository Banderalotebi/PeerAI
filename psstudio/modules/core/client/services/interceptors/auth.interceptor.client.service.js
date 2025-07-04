"use strict";

angular.module("core").factory("authInterceptor", ["$q", "$injector","ProjectCore",
  function ($q, $injector, ProjectCore) {
    return {
      responseError: function(rejection) {
        if (!rejection.config.ignoreAuthModule) {
          switch (rejection.status) {
            case 401:
              $injector.get("$state").transitionTo("authentication.signin");
              break;
            case 403:
              $injector.get("$window").location.href="/";
              break;
          }
        }
        // otherwise, default behaviour
        return $q.reject(rejection);
      }
    };
  }
]);
