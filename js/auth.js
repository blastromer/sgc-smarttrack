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
    return;
  }
  initChrome(user);
}

function logout() {
  sessionStorage.clear();
  window.location.href = "index.html";
}

function ico(inner) {
  return `<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${inner}</svg>`;
}

const ICONS = {
  Overview: ico('<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>'),
  Dashboard: ico('<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>'),
  Divisions: ico('<rect x="4" y="10" width="16" height="10"/><path d="M4 10V7l8-4 8 4v3"/><path d="M9 20v-6h6v6"/>'),
  "Users & roles": ico('<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3 19c1.2-3 3.5-4.5 6-4.5S13.8 16 15 19"/><path d="M15 15.5c1.6 0 3.3.8 4.5 3.5"/>'),
  Cycles: ico('<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16"/>'),
  "Validation queue": ico('<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6l1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2"/>'),
  Schools: ico('<path d="M3 10l9-6 9 6v10H3V10z"/><path d="M9 20v-6h6v6"/>'),
  Alerts: ico('<path d="M12 3l9 16H3L12 3z"/><path d="M12 10v4M12 17h.01"/>'),
  "My assessment": ico('<rect x="6" y="3" width="12" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h4"/>'),
  "MOV files": ico('<path d="M3 7h6l2 2h10v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7z"/>'),
  Notifications: ico('<path d="M6 8a6 6 0 0 1 12 0c0 7 3 7 3 9H3c0-2 3-2 3-9"/><path d="M10 20a2 2 0 0 0 4 0"/>'),
  "Sign out": ico('<path d="M10 7V5a2 2 0 0 1 2-2h7v18h-7a2 2 0 0 1-2-2v-2"/><path d="M4 12h11M12 9l3 3-3 3"/>')
};

const NOTICES = {
  super: [
    { unread: true, title: "12 days left in the 2026 cycle", detail: "21 schools are still overdue.", when: "Today" },
    { unread: true, title: "Cadiz submission at 76%", detail: "142 of 186 elementary schools submitted.", when: "Sep 17" },
    { unread: false, title: "19 MOVs returned to schools", detail: "Most common reason: FI3 quorum.", when: "Sep 16" }
  ],
  division: [
    { unread: true, title: "Mabini ES missed the deadline", detail: "No SGC FAT submission on file.", when: "Today" },
    { unread: true, title: "18 assessments in the queue", detail: "San Jose ES is next for validation.", when: "Sep 17" },
    { unread: false, title: "FI3A MOV returned to Sample ES", detail: "Minutes do not show 50%+1 quorum.", when: "Sep 17" }
  ],
  school: [
    { unread: true, title: "FI3A Minimum MOV returned", detail: "Minutes do not show 50%+1 quorum.", when: "Sep 17" },
    { unread: true, title: "T-14 checkpoint", detail: "7 of 12 indicators encoded.", when: "Sep 16" },
    { unread: false, title: "2026 SGC FAT cycle opened", detail: "Deadline Sep 30, 2026.", when: "Sep 1" }
  ]
};

const NOTICE_LINKS = {
  super: "super.html",
  division: "division-alerts.html",
  school: "school-notifications.html"
};

function initChrome(user) {
  if (!document.body.classList.contains("app")) return;
  decorateNav();
  pinSignOut();
  mountNotices(user.role);
}

function decorateNav() {
  document.querySelectorAll(".nav a").forEach((a) => {
    const label = a.textContent.trim();
    if (ICONS[label] && !a.querySelector("svg")) {
      a.insertAdjacentHTML("afterbegin", ICONS[label]);
    }
  });
}

function pinSignOut() {
  const side = document.querySelector(".side");
  if (!side) return;
  const link = [...side.querySelectorAll(".nav a")].find((a) => /sign out/i.test(a.textContent));
  if (!link) return;
  link.classList.add("signout");
  side.appendChild(link);
}

function mountNotices(role) {
  const top = document.querySelector(".top");
  if (!top || top.querySelector(".bell")) return;
  const items = NOTICES[role] || [];
  const unread = items.filter((n) => n.unread).length;
  const actions = document.createElement("div");
  actions.className = "top-actions";
  actions.innerHTML = `<button class="bell" type="button" aria-label="Open notifications" onclick="toggleNotices(event)">${ICONS.Notifications}${unread ? `<span class="dot">${unread}</span>` : ""}</button>`;
  const chip = top.querySelector(".chip");
  if (chip) actions.appendChild(chip);
  top.appendChild(actions);

  const backdrop = document.createElement("div");
  backdrop.className = "notice-backdrop";
  backdrop.id = "notice-backdrop";
  backdrop.onclick = toggleNotices;
  const panel = document.createElement("aside");
  panel.className = "notice-panel";
  panel.id = "notice-panel";
  panel.innerHTML = `
    <div class="notice-head">
      <div>
        <b>Notifications</b>
        <p class="muted">${unread} unread · sample cycle</p>
      </div>
      <button type="button" aria-label="Close" onclick="toggleNotices()">&times;</button>
    </div>
    <div class="notice-list">
      ${items.map((n) => `
        <article class="notice-item${n.unread ? " unread" : ""}">
          <strong>${n.title}</strong>
          <p class="muted">${n.detail}</p>
          <p class="muted">${n.when}</p>
        </article>
      `).join("")}
    </div>
    <div class="notice-foot">
      <a href="${NOTICE_LINKS[role]}">Open notification page</a>
    </div>
  `;
  document.body.appendChild(backdrop);
  document.body.appendChild(panel);
}

function toggleNotices(event) {
  if (event) event.stopPropagation();
  document.getElementById("notice-panel")?.classList.toggle("open");
  document.getElementById("notice-backdrop")?.classList.toggle("open");
}
