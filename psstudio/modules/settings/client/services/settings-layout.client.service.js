angular.module("app.settings")
    .factory("LayoutSettings",
        ["$resource",
            function ($resource)
            {
                return $resource("api/users/:userId/layout", {
                    userId: "@userId"
                });
            }]);