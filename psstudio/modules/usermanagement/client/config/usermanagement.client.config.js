/**
 * Created by saket on 29/3/16.
 */
"use strict";

(function ()
{
    angular
        .module("app.usermanagement")
        .run(coreMenu);

    coreMenu.$inject = ["Menus"];
    function coreMenu(Menus)
    {
        Menus.addMenuItem("sidebar", {
            title: "Users",
            state: "app.user-view",
            iconClass:"fa fa-users",
            position:3,
            roles: ["admin"]
        });
    }
})();
