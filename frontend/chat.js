async function fetchUserInfo() {
  const token = localStorage.getItem("token");
  if (!token) {
    return null;
  }

  try {
    const response = await fetch("/mychat/api/auth/verify", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ token })
    });

    if (!response.ok) {
      return null;
    }

    const data = await response.json();
    if (!data.valid) {
      return null;
    }

    return data.payload;
  } catch (err) {
    console.error("Error fetching user info:", err);
    return null;
  }
}

async function initUser() {
  const user = await fetchUserInfo();
  const nicknameElem = document.getElementById("nicknameDisplay");

  if (user) {
    nicknameElem.innerText = user.nickname;
  } else {
    window.location.href = "auth.html";
  }
}

const chatName = localStorage.getItem("currentChat") || "Неизвестный чат";
document.getElementById("chatTitle").innerText = chatName;

const chatId = localStorage.getItem("currentChatId");
const nickname = localStorage.getItem("nickname") || "User";
let messages = [];

async function fetchMessages() {
  const token = localStorage.getItem("token");
  if (!token || !chatId) return [];

  try {
    const response = await fetch(`/mychat/api/chat/${chatId}`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) {
      console.error("Failed to fetch messages:", response.status);
      return [];
    }

    const data = await response.json();
    return data;
  } catch (err) {
    console.error("Error fetching messages:", err);
    return [];
  }
}

function renderMessages() {
  const container = document.getElementById("messagesContainer");
  container.innerHTML = "";
  const user_id = JSON.parse(localStorage.getItem("user"))['id'];

  messages.forEach(msg => {
    const div = document.createElement("div");
    div.classList.add("message");
    div.classList.add(msg.sender_id === user_id ? "mine" : "other");
    div.innerText = msg.text;
    container.appendChild(div);
  });

  container.scrollTop = container.scrollHeight;
}

async function initChat() {
  messages = await fetchMessages();
  renderMessages();
}

initUser();
initChat();

document.getElementById("sendBtn").onclick = async () => {
  const input = document.getElementById("messageInput");
  const text = input.value.trim();
  if (!text) return;

  const token = localStorage.getItem("token");
  try {
    const response = await fetch(`/mychat/api/chat/${chatId}/message`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text })
    });

    if (!response.ok) {
      console.error("Failed to send message:", response.status);
      return;
    }

    messages.push({ sender_id: JSON.parse(localStorage.getItem("user"))['id'], text });
    input.value = "";
    renderMessages();
  } catch (err) {
    console.error("Error sending message:", err);
  }
};

document.getElementById("backBtn").onclick = () => {
  window.location.href = "chat-list.html";
};

document.getElementById("logoutBtn").onclick = () => {
  localStorage.clear();
  window.location.href = "auth.html";
};

document.getElementById("leaveBtn").onclick = async () => {
  const token = localStorage.getItem("token");
  if (!token || !chatId) return;

  try {
    const response = await fetch(`/mychat/api/chat/${chatId}/leave`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) {
      console.error("Failed to leave chat:", response.status);
      return;
    }

    localStorage.removeItem("currentChat");
    localStorage.removeItem("currentChatId");

    window.location.href = "chat-list.html";
  } catch (err) {
    console.error("Error leaving chat:", err);
  }
};

document.getElementById("addUserBtn").onclick = async () => {
  const nicknameToAdd = prompt("Введите ник пользователя для добавления в чат:");
  if (!nicknameToAdd) return;

  const token = localStorage.getItem("token");
  if (!token || !chatId) return;

  try {
    const response = await fetch(`/mychat/api/chat/${chatId}/add-user`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ nickname: nicknameToAdd })
    });

    if (!response.ok) {
      console.error("Failed to add user:", response.status);
      alert("Не удалось добавить пользователя.");
      return;
    }

    alert(`Пользователь ${nicknameToAdd} добавлен в чат.`);
  } catch (err) {
    console.error("Error adding user:", err);
    alert("Произошла ошибка при добавлении пользователя.");
  }
};
