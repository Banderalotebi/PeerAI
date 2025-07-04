/**
 * Created by dushyant on 13/4/16.
 */
angular.module("app.settings")
    .factory("PsCoreConfig",
        ["$resource",
            function ($resource)
            {
                return {
                    psCore: $resource("/api/settings/pscoreIdCreation/:pscoreConfigId", null, {
                        save: {method: "post"}
                    })
                };
            }]);
