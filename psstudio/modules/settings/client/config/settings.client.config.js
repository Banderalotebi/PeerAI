/**ame:  Winjit IOT Gateway
 ID:  5790c5b56f8778401d86795b
 Gateway Version:  0.8.4
 Firmware Version:  0.1.2
 Description:  IOT Gateway developed by Winjit
 * Created by saket on 2/2/16.
 */

"use strict";

(function ()
{
    angular
        .module("app.settings")
        .run(coreMenu);

    coreMenu.$inject = ["Menus"];
    function coreMenu(Menus)
    {
        Menus.addMenuItem("sidebar", {
            title: "Settings",
            state: "app.settings",
            type: "dropdown",
            iconClass: "fa fa-cog",
            position: 12,
            roles: ["admin"]
        });

        // Add the dropdown list item
        Menus.addSubMenuItem("sidebar", "app.settings", {
            title: "Log",
            state: "app.settings-logger",
            roles: ["admin"]
        });
        Menus.addSubMenuItem("sidebar", "app.settings", {
            title: "Core Config",
            state: "app.settings-listpscore",
            roles: ["admin"]
        });
        Menus.addSubMenuItem("sidebar", "app.settings", {
            title: "Project Info",
            state: "app.settings-projectinfo",
            roles: ["admin"]
        });

        // Add the dropdown list item
    }
})();
