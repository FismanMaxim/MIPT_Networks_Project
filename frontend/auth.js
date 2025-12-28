const tabLogin = document.getElementById("tabLogin");
const tabRegister = document.getElementById("tabRegister");
const nicknameField = document.getElementById("nickname");
const submitBtn = document.getElementById("submitBtn");

let mode = "login";

tabLogin.onclick = () => {
  mode = "login";
  tabLogin.classList.add("active");
  tabRegister.classList.remove("active");
  nicknameField.style.display = "none";
};

tabRegister.onclick = () => {
  mode = "register";
  tabRegister.classList.add("active");
  tabLogin.classList.remove("active");
  nicknameField.style.display = "block";
};

submitBtn.onclick = async () => {
  const login = document.getElementById("login").value.trim();
  const password = document.getElementById("password").value.trim();
  const nickname = document.getElementById("nickname").value.trim();

  if (!login || !password) {
    alert("Введите логин и пароль");
    return;
  }

  if (mode === "register" && !nickname) {
    alert("Введите никнейм");
    return;
  }

  try {
    const url =
      mode === "register"
        ? "/mychat/api/auth/register"
        : "/mychat/api/auth/login";

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ login, password, nickname })
    });

    const data = await response.json();

    if (!response.ok) { 
      alert(data.error || "Ошибка авторизации");
      return;
    }

    localStorage.setItem("token", data.token);
    localStorage.setItem("user", JSON.stringify(data.user));

    window.location.href = "chat-list.html";
  } catch (err) {
    console.error(err);
    alert("Ошибка сети");
  }
};
