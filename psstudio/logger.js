/**
 * Created by dushyant on 11/4/16.
 */
var winston = require("winston");

var logger = new (winston.Logger)({
    transports: [
        new(winston.transports.File)({
            filename:"logger.log",
            handleExceptions: true,
            prettyPrint:true
        }),
        //new (winston.transports.DailyRotateFile)({
        //    //name:'infoLogger',
        //    filename: 'logger',
        //    maxFiles:2,
        //    prettyPrint:true,
        //    datePattern:'_yyyy-MM-dd.log'
        //    //,
        //    //level: 'info'
        //}),
        new (winston.transports.Console)({
            level:"silly",
            handleExceptions: true,
            prettyPrint:true
        })
    ],exitOnError:false
});
logger.debug("Created logger");

module.exports=logger;

