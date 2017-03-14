var app = require('http').createServer(handler) 
 , io = require('socket.io').listen(app)
 , fs = require('fs');
app.listen(8124);

function handler (req, res) { 
 fs.readFile(__dirname + '/chat.html', function (err, data) {
     if (err) { 
                res.writeHead(500);
         return res.end('Error loading chat.html'); 
            }
     res.writeHead(200);
     res.end(data); 
        });
}
io.sockets.on('connection', function (socket) {
	console.log('One user connecting');
 
 socket.on('sendchat', function(data) { 
  io.sockets.emit('data', data);
 });

 socket.on('disconnect', function() {
  io.sockets.emit('chat', 'SERVER', socket.username + ' has left the building');
 });
});