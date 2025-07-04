/**
 * Created by saket on 31/3/16.
 */

"use strict";

// Users service used for authorizing the users
angular
    .module("app.usermanagement").factory("Authorization", ["$state", "Authentication",
    function ($state, Authentication)
    {
        var isAuthorized = function (state)
        {
            if (state)
            {
                return isAllowed($state.get(state));
            }
            else
                return isAllowed($state.current);
        };
        var loggedIn = false;
        //Check Authorization from config.routes
        function isAllowed(state)
        {
            if (Authentication.user.roles)
            {
                loggedIn = true;
                for (var i = 0; i < state.authorization.allowedRoles.length; i++)
                {
                    for (var j = 0; j < Authentication.user.roles.length; j++)
                    {
                        if (state.authorization.allowedRoles[i] == Authentication.user.roles[j])
                        {
                            return true;

                        }
                    }
                }
                return false;
            }
            else
            {
                loggedIn = false;
            }
        }

        var go = function (fallback)
        {
            if (loggedIn)
            {
                if( fallback.name){
                    $state.go(fallback.name);
                }
                else
                    $state.go("app.home");
            }
            else
            {
                $state.go("page.authentication.signin");
            }
        };
        return {
            authorized: this.authorized,
            isAuthorized: isAuthorized,
            go: go
        };
    }
])
;
