const ACCOUNTS = {
  "romer.necesario@sgcsmarttrack.gov.ph": { role: "super", name: "Romer Necesario", password: "SmartTrack2026" },
  "jovel.oberio@deped.gov.ph": { role: "division", name: "Jovel J. Oberio", password: "SmartTrack2026" },
  "school.head@deped.gov.ph": { role: "school", name: "Maria Santos", password: "SmartTrack2026" }
};

const PORTALS = {
  super: "super.html",
  division: "division.html",
  school: "school.html"
};

function routeByRole(role) {
  sessionStorage.setItem("sgc_role", role);
  window.location.href = PORTALS[role];
}

function sampleLogin(role) {
  const entry = Object.entries(ACCOUNTS).find(([, v]) => v.role === role);
  if (!entry) return;
  sessionStorage.setItem("sgc_user", JSON.stringify({ email: entry[0], ...entry[1] }));
  routeByRole(role);
}

function handleLogin(event) {
  event.preventDefault();
  const email = document.getElementById("email").value.trim().toLowerCase();
  const password = document.getElementById("password").value;
  const err = document.getElementById("err");
  const acc = ACCOUNTS[email];
  if (!acc || acc.password !== password) {
    err.style.display = "block";
    err.textContent = "Invalid credentials. Use a sample account below or the demo password SmartTrack2026.";
    return;
  }
  sessionStorage.setItem("sgc_user", JSON.stringify({ email, ...acc }));
  routeByRole(acc.role);
}

function handleRegister(event) {
  event.preventDefault();
  window.location.href = "pending.html";
}

function requireAuth(expected) {
  const raw = sessionStorage.getItem("sgc_user");
  if (!raw) {
    window.location.href = "index.html";
    return;
  }
  const user = JSON.parse(raw);
  if (expected && user.role !== expected) {
    window.location.href = PORTALS[user.role];
  }
}

function logout() {
  sessionStorage.clear();
  window.location.href = "index.html";
}
