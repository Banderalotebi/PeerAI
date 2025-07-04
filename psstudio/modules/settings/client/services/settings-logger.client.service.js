/**
 * Created by dushyant on 13/4/16.
 */
angular.module("app.settings")
    .factory("Logger",
        ["$resource",
            function ($resource)
            {
                return {
                    logs: $resource("/api/export-logs", null,
                        {
                            export: {method: "POST", isArray: true}
                        }),
                    routeAccessLogs: $resource("/api/export-route-logs", null,
                        {
                            export: {method: "GET"}
                        }),
                    OSLogs: $resource("/api/export-os-logs", null,
                        {
                            export: {method: "POST"}
                        }),
                    repair: $resource("/api/export-logs/repair", null,
                        {
                            execute: {method: "GET"}
                        }),
                    PsCoreLogs: $resource("/api/export-pscore-app-logs/:pscoreConfigId", null,
                        {
                            export: {method: "GET"}
                        })
                };
            }]);
