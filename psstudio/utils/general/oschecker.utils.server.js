"use strict";
var os = require("os");
exports.checkOs = function(){
    if (os.platform().toString().indexOf("win32") !== -1){
        //windows
        return "windows";
    }else{
        //linux
        return "linux";
    }
};