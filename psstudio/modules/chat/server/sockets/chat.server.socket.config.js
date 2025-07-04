"use strict";
// Create the chat configuration
module.exports = function (io, socket) {
  // Emit the status event when a new socket client is connected
  var user = socket.request.user;
  //io.emit('edaCompleted', {
  //  type: 'status',
  //  text: 'Is now connected',
  //  created: Date.now(),
  //  profileImageURL: socket.request.user.profileImageURL,
  //  username: socket.request.user.username
  //});


  // Emit the status event when a socket client is disconnected
  socket.on("disconnect", function () {
    //io.emit('edaCompleted', {
    //  type: 'status',
    //  text: 'disconnected',
    //  created: Date.now(),
    //  username: socket.request.user.username
    //});
  });
};
