/**
 * Created by vishnu on 22/11/18.
 */

"use strict";

var acl = require("acl");
acl = new acl(new acl.memoryBackend());


exports.invokeRolesPolicies = function ()
{
    acl.allow([
        {
            roles: ["sudo", "admin","user"],
            allows: [{
                resources: "/api/udd",
                permissions: ["*"]
            },
            {
                resources: "/api/udd/:uddId",
                permissions: ["*"]
            },
            {
                resources: "/api/project/:projectId/udd/:uddId/execute",
                permissions: ["*"]
            }]
        }, {
            roles: ["user"],
            allows: [{
                resources: "/api/udd/:uddId",
                permissions: ["*"]
            }]
        }
    ]);

    exports.isAllowed = function (req, res, next)
    {
        var roles = (req.user) ? req.user.roles : ["guest"];

        acl.areAnyRolesAllowed(roles, req.route.path, req.method.toLowerCase(), function (err, isAllowed)
        {
            if (err)
            {
                // An authorization error occurred.
                return res.status(500).send("Unexpected authorization error");
            }
            else
            {
                if (isAllowed)
                {
                    // Access granted! Invoke next middleware
                    return next();
                }
                else
                {
                    return res.status(403).json({
                        message: "User is not authorized"
                    });
                }
            }
        });
    };
};
