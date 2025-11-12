// Doctor-side Socket.IO chat
const socket = io("http://localhost:3000");

const patientsList = document.getElementById("patientsList");
const chatMessages = document.getElementById("chatMessages");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");

let currentPatient = null;
const doctor = { id: "doc-" + Math.random().toString(36).slice(2, 8), name: "Dr. Aadhavan" };

// Example active patients (mock)
const patients = [
  { id: "p1", name: "Riya Patel", avatar: "images/patient1.jpg" },
  { id: "p2", name: "Suresh Kumar", avatar: "images/patient2.jpg" },
  { id: "p3", name: "Anita Raj", avatar: "images/patient3.jpg" },
];

// Render patient list
patients.forEach(p => {
  const card = document.createElement("div");
  card.className = "patient-card";
  card.innerHTML = `<img src="${p.avatar}" alt="${p.name}" /><div><h4>${p.name}</h4><p class="status">Offline</p></div>`;
  card.addEventListener("click", () => selectPatient(p));
  patientsList.appendChild(card);
});

function selectPatient(p) {
  currentPatient = p;
  document.getElementById("patientName").textContent = p.name;
  document.getElementById("patientAvatar").src = p.avatar;
  document.getElementById("patientStatus").textContent = "Online";
  chatMessages.innerHTML = "";
  socket.emit("join", { room: p.id, user: doctor });
}

// Send message
sendBtn.addEventListener("click", sendMessage);
messageInput.addEventListener("keydown", e => {
  if (e.key === "Enter") sendMessage();
});

function sendMessage() {
  const text = messageInput.value.trim();
  if (!text || !currentPatient) return;
  appendMessage(text, "outgoing");
  socket.emit("message", { room: currentPatient.id, user: doctor.name, text });
  messageInput.value = "";
}

// Append message
function appendMessage(text, type) {
  const msg = document.createElement("div");
  msg.className = `message ${type}`;
  msg.textContent = text;
  chatMessages.appendChild(msg);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Receive incoming messages
socket.on("message", msg => {
  if (currentPatient && msg.room === currentPatient.id && msg.user !== doctor.name) {
    appendMessage(msg.text, "incoming");
  }
});
