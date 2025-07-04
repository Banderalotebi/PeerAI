module.exports = function(RED) {
    function output(config)
    {
        RED.nodes.createNode(this,config);
        var node = this;
        this.on("input", function(msg) {
            node.send(msg);
            var func = require("../../../../modules/projects/server/controllers/projects.server.controller");
            func.dumpData(msg);

        });
    }
    RED.nodes.registerType("Output",output);

};




