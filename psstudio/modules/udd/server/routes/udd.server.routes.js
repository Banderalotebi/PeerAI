/**
 * Created by vishnu on 22/11/18.
 */

"use strict";

/**
 * Module dependencies.
 */
var udd = require("../controllers/udd.server.controller"),
    uddPolicy = require("../policies/udd.server.policy"),
    projectController = require("../../../projects/server/controllers/projects.server.controller");

uddPolicy.invokeRolesPolicies();
module.exports = function (app)
{

    app.route("/api/udd").all(uddPolicy.isAllowed)
        .get(udd.list)
        .post(udd.create);

    app.route("/api/udd/:uddId").all(uddPolicy.isAllowed)
        .get(udd.read)
        .put(udd.update)
        .delete(udd.delete);

    app.route("/api/project/:projectId/udd/:uddId/execute").all(uddPolicy.isAllowed)
        .get(udd.startUddFlow);
    // Finish by binding the Udd Flow middleware
    app.param("uddId", udd.uddByID);
    app.param("projectId", projectController.projectById);

};
