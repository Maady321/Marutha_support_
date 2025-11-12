// server.js
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: "*", methods: ["GET","POST"] }
});

// simple in-memory rooms/messages (demo only)
const history = {}; // { roomId: [ { from, text, ts } ] }

io.on('connection', socket => {
  console.log('socket connected', socket.id);

  socket.on('join', ({ room }) => {
    if(!room) return;
    socket.join(room);
    console.log(`${socket.id} joined ${room}`);
  });

  socket.on('history', ({ room }, cb) => {
    cb(history[room] || []);
  });

  socket.on('message', (data) => {
    // data: { room, text }
    if(!data || !data.room) return;
    const msg = { room: data.room, text: data.text, from: socket.id, ts: Date.now() };
    history[data.room] = history[data.room] || [];
    history[data.room].push(msg);
    // broadcast to room
    io.to(data.room).emit('message', msg);
  });

  socket.on('typing', (data) => {
    if(data && data.room){
      socket.to(data.room).emit('typing', { room: data.room, typing: data.typing });
    }
  });

  socket.on('disconnect', () => {
    console.log('socket disconnect', socket.id);
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, ()=> console.log('Socket.IO server running on', PORT));
