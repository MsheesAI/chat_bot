const API_URL = "http://127.0.0.1:8000/chat";

const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");

function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.classList.add("fade-in");

  if (sender === "user") {
    msg.className += " text-right";
    msg.innerHTML = `
      <div class="inline-block bg-blue-500/80 neon-glow text-white px-4 py-2 rounded-xl max-w-[80%]">
        ${text}
      </div>
    `;
  } else {
    msg.className += " text-left";
    msg.innerHTML = `
      <div class="inline-block bg-white/90 text-blue-900 px-4 py-2 rounded-xl max-w-[80%] shadow-md">
        ${text}
      </div>
    `;
  }

  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function showTyping() {
  const typing = document.createElement("div");
  typing.id = "typing";
  typing.className = "text-left fade-in";
  typing.innerHTML = `
    <div class="inline-block bg-white/70 text-blue-700 px-4 py-2 rounded-xl italic shadow">
      Bot is typing<span class="animate-pulse">...</span>
    </div>
  `;
  chatBox.appendChild(typing);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTyping() {
  const typing = document.getElementById("typing");
  if (typing) typing.remove();
}

async function sendMessage() {
  const question = input.value.trim();
  if (!question) return;

  addMessage(question, "user");
  input.value = "";

  showTyping();

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    const data = await res.json();
    removeTyping();
    addMessage(data.answer, "bot");

  } catch (err) {
    removeTyping();
    addMessage("❌ Backend not reachable", "bot");
  }
}
