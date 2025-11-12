// Connect to Socket.IO server
const socket = io("http://localhost:3000");

const doctorGrid = document.getElementById("doctorGrid");
const chatMessages = document.getElementById("chatMessages");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");

let currentDoctor = null;
const user = { id: "user-" + Math.random().toString(36).slice(2,8), name: "Patient" };

// Example doctor data (can come from DB)
const doctors = [
  { id: "doc1", name: "Dr. Aadhavan", avatar: "images/doctor1.jpg" },
  { id: "doc2", name: "Dr. Priya", avatar: "images/doctor2.jpg" },
  { id: "doc3", name: "Dr. Ramesh", avatar: "images/doctor3.jpg" },
  { id: "doc4", name: "Dr. Kavya", avatar: "images/doctor4.jpg" },
  { id: "doc5", name: "Dr. Nithin", avatar: "images/doctor5.jpg" },
  { id: "doc6", name: "Dr. Ananya", avatar: "images/doctor6.jpg" }
];

// render doctors
doctors.forEach(d => {
  const card = document.createElement("div");
  card.className = "doctor-card";
  card.innerHTML = `<img src="${d.avatar}" alt="${d.name}" /><p>${d.name}</p>`;
  card.addEventListener("click", () => selectDoctor(d));
  doctorGrid.appendChild(card);
});

function selectDoctor(d) {
  currentDoctor = d;
  document.getElementById("doctorName").textContent = d.name;
  document.getElementById("doctorAvatar").src = d.avatar;
  document.getElementById("doctorStatus").textContent = "Online";
  chatMessages.innerHTML = "";
  socket.emit("join", { room: d.id, user });
}

// send message
sendBtn.addEventListener("click", sendMessage);
messageInput.addEventListener("keydown", e => {
  if (e.key === "Enter") sendMessage();
});

function sendMessage() {
  const text = messageInput.value.trim();
  if (!text || !currentDoctor) return;

  appendMessage(text, "outgoing");
  socket.emit("message", { room: currentDoctor.id, user: user.name, text });
  messageInput.value = "";
}

// append message
function appendMessage(text, type) {
  const msg = document.createElement("div");
  msg.className = `message ${type}`;
  msg.textContent = text;
  chatMessages.appendChild(msg);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// receive messages
socket.on("message", msg => {
  if (currentDoctor && msg.room === currentDoctor.id && msg.user !== user.name) {
    appendMessage(msg.text, "incoming");
  }
});
