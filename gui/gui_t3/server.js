var express = require('express');
var app = express();
var server = app.listen(3000);
app.use(express.static('public'));

var socket = require('socket.io');
var io = socket(server);
io.sockets.on('connection',newConnection);
console.log("my socket server is running")
function newConnection(socket){
  console.log('new connection: ' + socket.id);
  // socket.on('block' , blockMsg);

  // function blockMsg(data){
  //   socket.broadcast.emit('block',data);
  //   // io.sockets.emit('block',data)//globaly and not to a specific one
  //   console.log(data);
  // }
}
