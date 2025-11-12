const express = require("express");
const http = require("http");
const { Server } = require("socket.io");

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: "*" }
});

io.on("connection", (socket) => {
  console.log("Socket connected:", socket.id);

  socket.on("message", (data) => {
    console.log("Message received:", data);
    io.emit("message", data); // broadcast to all connected clients
  });

  socket.on("disconnect", () => {
    console.log("Socket disconnected:", socket.id);
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`✅ Socket.IO server running on port ${PORT}`));
