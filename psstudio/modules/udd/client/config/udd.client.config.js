
/**
 * Created by vishnu on 21/11/18.
 */
(function ()
{
    "use strict";

    angular
        .module("app.udd")
        .run(coreMenu);
    coreMenu.$inject = ["Menus"];
    function coreMenu(Menus)
    {
        // if (window.menuConfig.isUDD) {
        //     Menus.addMenuItem('sidebar', {
        //         title: 'UDD Management',
        //         state: 'app.udd-view',
        //         iconClass: 'fa fa-random',
        //         position: 8,
        //         roles: ['sudo', 'admin','user']
        //     });
        // }
    }
})();
