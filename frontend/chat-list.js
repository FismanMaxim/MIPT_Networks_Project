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
  const nicknameElem = document.getElementById("userNickname");

  if (user) {
    nicknameElem.innerText = user.nickname;
  } else {
    window.location.href = "auth.html";
  }
}

async function fetchChats() {
  const token = localStorage.getItem("token");
  if (!token) return [];

  try {
    const response = await fetch("/mychat/api/chat/", {
      method: "GET",
      headers: { "Authorization": `Bearer ${token}` }
    });

    if (!response.ok) {
      console.error("Failed to fetch chats:", response.status);
      return [];
    }

    const data = await response.json();
    return data;
  } catch (err) {
    console.error("Error fetching chats:", err);
    return [];
  }
}

async function renderChats() {
  const chats = await fetchChats();
  const chatList = document.getElementById("chatList");
  chatList.innerHTML = "";

  chats.forEach(chat => {
    const item = document.createElement("div");
    item.className = "chat-item";
    item.onclick = () => openChat(chat.name, chat.id);

    const spanName = document.createElement("div");
    spanName.className = "chat-name";
    spanName.innerText = chat.name;

    item.appendChild(spanName);

    if (chat.unread > 0) {
      const unread = document.createElement("div");
      unread.className = "unread-indicator";
      unread.innerText = chat.unread;
      item.appendChild(unread);
    }

    chatList.appendChild(item);
  });
}

async function createChat(name) {
  const token = localStorage.getItem("token");
  if (!token || !name) return;

  try {
    const response = await fetch("/mychat/api/chat/", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ name })
    });

    if (!response.ok) {
      console.error("Failed to create chat:", response.status);
      return;
    }

    const data = await response.json();
    console.log("Chat created:", data);
    await renderChats(); // Refresh the chat list
    document.getElementById("newChatName").value = ""; // Clear input
  } catch (err) {
    console.error("Error creating chat:", err);
  }
}

function openChat(name, id) {
  localStorage.setItem("currentChat", name);
  localStorage.setItem("currentChatId", id);
  window.location.href = "chat.html";
}

document.getElementById("logoutBtn").onclick = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("nickname");
  window.location.href = "auth.html";
};

document.getElementById("createChatBtn").onclick = () => {
  const chatName = document.getElementById("newChatName").value.trim();
  createChat(chatName);
};

initUser();
renderChats();