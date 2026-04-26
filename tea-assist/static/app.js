const chatWidget = document.getElementById("chatWidget");
const chatLog = document.getElementById("chatLog");
const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const suggestions = document.getElementById("suggestions");

const openChat = () => {
  chatWidget.classList.remove("hidden");
  chatInput.focus();
};

document.getElementById("openChat").addEventListener("click", openChat);
document.getElementById("floatingChat").addEventListener("click", openChat);
document.getElementById("closeChat").addEventListener("click", () => chatWidget.classList.add("hidden"));

function addMessage(role, text) {
  const msg = document.createElement("div");
  msg.className = `msg ${role}`;
  msg.textContent = text;
  chatLog.appendChild(msg);
  chatLog.scrollTop = chatLog.scrollHeight;
}

function renderSuggestions(items = []) {
  suggestions.innerHTML = "";
  items.forEach((item) => {
    const btn = document.createElement("button");
    btn.className = "suggestion-btn";
    btn.type = "button";
    btn.textContent = item;
    btn.addEventListener("click", () => {
      chatInput.value = item;
      chatForm.requestSubmit();
    });
    suggestions.appendChild(btn);
  });
}

async function sendMessage(message) {
  addMessage("user", message);

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Unable to get response");

    const tipText = data.tips?.length ? `\n\nTips:\n• ${data.tips.join("\n• ")}` : "";
    addMessage("bot", `${data.reply}${tipText}`);
    renderSuggestions(data.suggestions || []);
  } catch (err) {
    addMessage("bot", `I hit a server issue: ${err.message}. Please try again.`);
  }
}

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = chatInput.value.trim();
  if (!message) return;

  chatInput.value = "";
  await sendMessage(message);
});

addMessage("bot", "Welcome! I can help with tea crop nutrition, pest management, weather preparation, and market planning.");
renderSuggestions([
  "Create a fertilizer plan for this season",
  "How do I control red spider mites?",
  "What to do before heavy rain?",
]);
