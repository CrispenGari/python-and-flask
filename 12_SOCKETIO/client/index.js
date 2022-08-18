const socket = io("http://127.0.0.1:3001/chat");
const messages = document.querySelector("#messages");
const message = document.querySelector("#message");
const sendBtn = document.getElementById("sendbutton");

socket.on("connect", function () {
  socket.send("User has connected!");
});

socket.on("new-message", function (msg) {
  const child = document.createElement("li");
  child.innerHTML = msg;
  messages.appendChild(child);
});

sendBtn.addEventListener("click", () => {
  socket.emit("message", message.value);
  message.value = "";
});
