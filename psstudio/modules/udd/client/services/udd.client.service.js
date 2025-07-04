/**
 * Created by vishnu on 21/11/18.
 */


"use strict";

//UDD service
angular.module("app.udd").factory("UddFlow", ["$resource",
    function ($resource)
    {
        return $resource("api/udd/:uddId", {
            uddId: "@_id"
        }, {
            update: {
                method: "PUT"
            }
        });
    }
]);
//UDD Execution
angular.module("app.udd").factory("UddExecution", ["$resource",
    function ($resource)
    {
        this.startFlow = startFlow($resource);
        function startFlow($resource){
            return $resource("api/project/:projectId/udd/:uddId/execute", {
                uddId: "@_id",
                projectId: "@pId"
            });  
        }
        return this;
    }
]);