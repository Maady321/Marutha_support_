// minimal Socket.IO server for testing
const express = require("express");
const http = require("http");
const { Server } = require("socket.io");

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: "*" }
});

// simple in-memory store (replace with DB)
const rooms = {}; // { roomId: [{id, user, text, ts}, ...] }
const users = {}; // socketId -> { user, room }

io.on("connection", socket => {
  console.log("socket connected:", socket.id);

  socket.on("join", ({ room, user }, ack) => {
    socket.join(room);
    users[socket.id] = { user, room };
    rooms[room] = rooms[room] || [];
    // broadcast presence
    io.to(room).emit("presence", { user, online: true });
    // send recent history
    const recent = rooms[room].slice(-50);
    ack && ack({ ok: true, history: recent });
  });

  socket.on("message", (payload, cb) => {
    // payload: { room, user, text }
    const msg = {
      id: Date.now().toString(36) + Math.random().toString(36).slice(2,6),
      user: payload.user,
      text: payload.text,
      ts: Date.now()
    };
    rooms[payload.room] = rooms[payload.room] || [];
    rooms[payload.room].push(msg);
    io.to(payload.room).emit("message", msg);
    cb && cb({ ok: true, id: msg.id });
  });

  socket.on("typing", ({ room, user, typing }) => {
    socket.to(room).emit("typing", { user, typing });
  });

  socket.on("disconnect", () => {
    const meta = users[socket.id];
    if (meta) {
      io.to(meta.room).emit("presence", { user: meta.user, online: false });
      delete users[socket.id];
    }
    console.log("socket disconnected:", socket.id);
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Socket.IO server running on ${PORT}`));
