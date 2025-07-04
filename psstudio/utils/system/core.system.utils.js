/**
 * Created by dushyant on 15/7/16.
 */
"use strict";
var path = require("path"),
    mongoose = require("mongoose"),
    logger = require(path.resolve("./logger"));


var commands = {
    restartService: "systemctl restart startApi"
};

var exec = require("child_process").exec;
exports.setDailyCrons = setDailyCrons;

exports.restartService = restartService;

/**
 * Starts Daily cron service
 */
function setDailyCrons(){
    // Set 24 hourly cron job
    var cronJob = require("cron").CronJob;
    new cronJob("0 0 0 * * *", function () {
        setPurgeCrons();
    }, null, true);
}

// function setPurgeCrons(){
//     var purgeDay;
//     Config.find().exec(function (err, config) {
//         if (err) {
//             logger.error('Error while reading purgeDay', {error: err});
//         }
//         else {
//             if(config[0].purgeConfig.isDataPurge){
//                 purgeDay=config[0].purgeConfig.expDay;
//                 var purgeDate = new Date();
//                 purgeDate.setDate(purgeDate.getDate() - purgeDay);
//                 if(config[0].purgeConfig.expDay){

//                 }
//                 DataStream.remove({timestamp:{$lt:purgeDate}}).exec(function (err)
//                 {
//                     if (err){
//                         logger.error('Unable to Purge');
//                     }else{
//                         logger.info('Datastreams Purged');
//                     }
//                 });
//             }

//         }
//     });
// }

function restartService()
{
    logger.warn("Restarting service");

    // Set timeout for restart after 10s
    setTimeout(function ()
    {
        exec(commands.restartService, function (err)
        {
            if (err)
            {
                logger.error("Could not restart Gateway service", {error: err});
            }
        });
    }, 10000);
}

