(function() {
    "use strict";

    angular
        .module("app.projectDatas")
        .run(coreMenu);

    coreMenu.$inject = ["Menus"];
    function coreMenu(Menus){

        Menus.addMenuItem("sidebar", {
            title: "Data",
            state: "app.data",
            iconClass: "fa fa-database",
            position: 1,
            roles: ["*"]
        });
    }

})();