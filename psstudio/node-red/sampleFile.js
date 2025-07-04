/**
 * Created by prabhatp on 30/3/17.
 */

module.exports = function (RED) {
    function nodeNameNode(n) {
        RED.nodes.createNode(this, n);
        var node = this;
        this.search = "NodeName";
        if (n.replace != "")
            this.replace = n.replace;
        else
            this.replace = "NodeName";

        this.on("input", function (msg) {
            var receivedMsg = msg.payload;
            var selectedKey = {};
            for (var x in receivedMsg) {
                if (x.toLowerCase() === "nodeName") {
                    selectedKey.nodeName = receivedMsg[x];
                    break;
                }
            }
            if (selectedKey != null) {
                var str = JSON.stringify(selectedKey);
                str = str.replace(this.search, this.replace);
                msg.payload = JSON.parse(str);
                node.send(msg);
            } else {
                var str = JSON.stringify(receivedMsg);
                str = str.replace(this.search, this.replace);
                msg.payload = JSON.parse(str);
                node.send(msg);
            }

        });
    }
    RED.nodes.registerType("NodeNameTag", nodeNameNode);
};
