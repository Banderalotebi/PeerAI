/**
 * Created by vishnu on 22/11/18.
 */

"use strict";

/**
 * Module dependencies.
 */
var path = require("path"),
    logger = require(path.resolve("./logger")),
    mongoose = require("mongoose"),
    fs = require("fs"),
    errorHandler = require("../../../core/server/controllers/errors.server.controller"),
    // ownerShip = require("../../../../utils/ownership/ownership-admin.utils"),
    UddFlow = mongoose.model("UddFlow"),
    ProjectController = require("../../../projects/server/controllers/projects.server.controller");
    var socket = require("../../../../utils/socket/core.socket.utils");

var curFlowId;
var destination = "./projects/";
exports.getFlowId = function (res) {
    curFlowId = res;
};

function createUddFlow(config, res, callback) {
    var uddFlow = new UddFlow(config);

    uddFlow.save(function (err)

        {
            if (err) {
                logger.error("Error while creating Udd Flow", {
                    error: err
                });

                if (res)
                    return res.status(400).send({
                        message: errorHandler.getErrorMessage(err)
                    });
                else
                    callback(null);
            } else {
                if (res)
                    res.json(uddFlow);
                else
                    callback(uddFlow);
            }
        });
}

/**
 * Create a Sync Option
 */
exports.create = function (req, res) {
    req.body.createdBy = req.user._id;
    createUddFlow(req.body, res);
};

/**
 * Show the current Sync Option
 */
exports.read = function (req, res) {
    res.json(req.uddFlow);
};

/**
 * Update a Sync Option
 */
exports.update = function (req, res, callback) {
    var uddFlow = req.uddFlow;
    uddFlow.flowName = req.body.flowName;
    uddFlow.flowId = req.body.flowId;
    uddFlow.flowType = req.body.flowType;

    uddFlow.save(function (err) {
        if (err) {
            logger.error("Error while updating Udd Flow " + uddFlow._id, {
                error: err
            });
            if (res) {
                return res.status(400).send({
                    message: errorHandler.getErrorMessage(err)
                });
            } else if (callback) {
                callback({
                    message: errorHandler.getErrorMessage(err) || "ERROR"
                });
            }
        } else {
            if (res)
                res.json(uddFlow);
            else if (callback)
                callback(null);

            logger.info("Updated Udd Flow " + uddFlow._id);
        }
    });
};

/**
 * Delete a Sync Option
 */
exports.delete = function (req, res, callback) {

    var uddFlow = req.uddFlow;

    uddFlow.remove(function (err) {
        if (err) {
            logger.error("Error while deleting Udd Flow " + uddFlow._id, {
                error: err
            });
            if (res)
                return res.status(400).send({
                    message: errorHandler.getErrorMessage(err)
                });
            else if (callback)
                callback({
                    message: errorHandler.getErrorMessage(err)
                });
        } else {
            if (res)
                res.json(uddFlow);
            else if (callback)
                callback(null);
            logger.info("Deleted Udd Flow option " + uddFlow._id);

        }
    });
};

exports.startUddFlow = function(req,res){
    var uddFlow = req.uddFlow;
    // executeFlow(uddFlow.flowId)
    req.project.flowId = uddFlow.flowId;
    ProjectController.executeFlow({project:req.project,filePath:null,destination:destination+req.project._id});
    res.json({status:"flow_start",projectDetails:req.project});

};

// function executeFlow(flowId) {

//     fs.readFile('./node-red/flows/psflow.json', 'utf8', function (err, data) {
//         if (err) throw err;
//         else {
//             var flows = JSON.parse(data);

//             flows.forEach(function (selectedFlowObject) {
//                 // console.log(selectedFlowObject)
//                 // if (selectedFlowObject.z === flowId && selectedFlowObject.type === 'input') {
//                 if (selectedFlowObject.z === flowId) {
//                     var id = selectedFlowObject.id;

//                     var msg = {};
//                     // msg.dataStream = _dataStream;
//                     // msg.res = res;
//                     // msg._id=_dataStream._id;
//                     // msg.deviceId=_dataStream.deviceId;
//                     // msg.timestamp = _dataStream.timestamp;
//                     // msg.payload = _dataStream.data;

//                     // var dataTagCount = Object.keys(msg.payload).length;

//                     var RED = require(path.resolve("./config/config")).RED;
//                     // console.log(RED)
//                     // var injector = require("../../../../node-red/nodes/core/storage/50-file")(RED);
//                     var node = RED.nodes.getNode(id);
//                     node.receive()

//                 }
//             });
//         }
//     });

// }

// exports.dumpData = function(msg){
//     console.log("*******DUMP DATA********")
//     console.log(msg)
//     console.log("*******DUMP DATA********")

//     if(msg.payload){
//         var x = JSON.stringify(msg.payload)
//         fs.appendFile("/home/vishnu/Documents/projects/Data/Regression/test.json",x,function(err){
//             if (err) throw err;
//             socket.emit("flowCompleted",{},{_id:msg.projectId,createdBy:msg.createdBy});
//             console.log("Completed flow")
//         })
//     }
// }

/**
 * List of Udd Flow
 */
exports.list = function (req, res) {
    var query = {};
    //to get udd flows owned by user
    query = {
        createdBy: req.user._id
    };
    return listOwnedUddFlows(req, res, query);
};

function listOwnedUddFlows(req, res, query) {

    UddFlow.find(query).exec(function (err, uddFlow) {
        if (err) {
            logger.error("Error while listing Udd Flow ", {
                error: err
            });
            return res.status(400).send({
                message: errorHandler.getErrorMessage(err)
            });
        } else {
            res.json(uddFlow);
        }
    });
}

/**
 * Udd Flow middleware
 */
exports.uddByID = function (req, res, next, id) {
    UddFlow.findById(id).exec(function (err, uddFlow) {
        if (err) {
            logger.error("Error while finding Udd Flow " + uddFlow._id, {
                error: err
            });
            return next(err);
        }
        if (!uddFlow) {

            return next(new Error("Failed to load Udd Flow " + id));
        }
        req.uddFlow = uddFlow;
        next();
    });
};

exports.findById = findById;

function findById(id, callback) {
    UddFlow.findById(id).exec(function (err, uddFlow) {
        if (err) {
            logger.error("Error while finding Udd Flow " + id, {
                error: err
            });
            return callback(null);
        } else if (!uddFlow)
            return callback(null);
        callback(uddFlow);
    });
}