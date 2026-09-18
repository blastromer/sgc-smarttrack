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
  Submit: ico('<path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4 20-7z"/>'),
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
  if (user.role === "school") insertSchoolSubmitNav();
  decorateNav();
  pinSignOut();
  decorateKpis();
  mountNotices(user.role);
  if (user.role === "school") mountSchoolFlow();
}

function decorateNav() {
  document.querySelectorAll(".nav a").forEach((a) => {
    const label = a.textContent.trim();
    if (ICONS[label] && !a.querySelector("svg")) {
      a.insertAdjacentHTML("afterbegin", ICONS[label]);
    }
  });
}

const KPI_ICONS = {
  Files: ico('<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5"/>'),
  Valid: ico('<circle cx="12" cy="12" r="8"/><path d="M8.5 12.5l2.5 2.5 5-5"/>'),
  Returned: ico('<path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5"/>'),
  Complete: ico('<circle cx="12" cy="12" r="8"/><path d="M8.5 12.5l2.5 2.5 5-5"/>'),
  "Not started": ico('<circle cx="12" cy="12" r="8"/><path d="M12 8v4l3 2"/>'),
  Unread: ico('<path d="M6 8a6 6 0 0 1 12 0c0 7 3 7 3 9H3c0-2 3-2 3-9"/><path d="M10 20a2 2 0 0 0 4 0"/>'),
  "This cycle": ico('<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16"/>'),
  "Indicators met": ico('<path d="M4 19V9l8-5 8 5v10"/><path d="M9 19v-6h6v6"/>'),
  "MOVs uploaded": ico('<path d="M3 7h6l2 2h10v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7z"/>'),
  "Self-score": ico('<path d="M12 3l2.2 6.6H21l-5.4 4 2.1 6.4L12 16.8 6.3 20l2.1-6.4L3 9.6h6.8z"/>'),
  Schools: ico('<path d="M3 10l9-6 9 6v10H3V10z"/><path d="M9 20v-6h6v6"/>'),
  Submitted: ico('<path d="M12 3v12"/><path d="M7 8l5-5 5 5"/><path d="M5 21h14"/>'),
  Overdue: ico('<circle cx="12" cy="12" r="8"/><path d="M12 7v6l4 2"/>'),
  Functional: ico('<path d="M8.5 12.5l2.5 2.5 5-5"/><rect x="4" y="4" width="16" height="16" rx="2"/>'),
  Queue: ico('<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6l1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2"/>'),
  "TA flagged": ico('<path d="M12 3l9 16H3L12 3z"/><path d="M12 10v4M12 17h.01"/>'),
  "Avg FIs met": ico('<path d="M4 18V8M10 18V4M16 18v-7M22 18V6"/>'),
  "Schools in cycle": ico('<path d="M3 10l9-6 9 6v10H3V10z"/><path d="M9 20v-6h6v6"/>'),
  "Functional SGCs": ico('<path d="M8.5 12.5l2.5 2.5 5-5"/><rect x="4" y="4" width="16" height="16" rx="2"/>'),
  "Submission rate": ico('<path d="M4 18V10M10 18V6M16 18v-5M22 18V8"/>'),
  Validated: ico('<circle cx="12" cy="12" r="8"/><path d="M8.5 12.5l2.5 2.5 5-5"/>'),
  "Under review": ico('<circle cx="11" cy="11" r="6"/><path d="M20 20l-3.5-3.5"/>'),
  "Returned MOVs": ico('<path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5"/>'),
  "Admin accounts": ico('<circle cx="9" cy="8" r="3"/><path d="M3 19c1.2-3 3.5-4.5 6-4.5S13.8 16 15 19"/>'),
  "Active SDOs": ico('<rect x="4" y="10" width="16" height="10"/><path d="M4 10V7l8-4 8 4v3"/>'),
  "Schools mapped": ico('<path d="M3 10l9-6 9 6v10H3V10z"/><path d="M9 20v-6h6v6"/>'),
  "Division Admins": ico('<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3 19c1.2-3 3.5-4.5 6-4.5S13.8 16 15 19"/>'),
  "Total users": ico('<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3 19c1.2-3 3.5-4.5 6-4.5S13.8 16 15 19"/>'),
  "Super Admin": ico('<path d="M12 3l2.2 6.6H21l-5.4 4 2.1 6.4L12 16.8 6.3 20l2.1-6.4L3 9.6h6.8z"/>'),
  "Division Admin": ico('<rect x="4" y="10" width="16" height="10"/><path d="M4 10V7l8-4 8 4v3"/>'),
  "School Admin": ico('<path d="M3 10l9-6 9 6v10H3V10z"/><path d="M9 20v-6h6v6"/>'),
  "Open cycles": ico('<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16"/>'),
  "Days remaining": ico('<circle cx="12" cy="12" r="8"/><path d="M12 7v6l4 2"/>'),
  "On-time target": ico('<circle cx="12" cy="12" r="8"/><path d="M8.5 12.5l2.5 2.5 5-5"/>'),
  Listed: ico('<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>'),
  "Not yet": ico('<circle cx="12" cy="12" r="8"/><path d="M12 8v4l3 2"/>'),
  "Awaiting review": ico('<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6l1 1 2-2"/>'),
  Resubmitted: ico('<path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5"/>'),
  "Validated today": ico('<circle cx="12" cy="12" r="8"/><path d="M8.5 12.5l2.5 2.5 5-5"/>'),
  "Overdue schools": ico('<circle cx="12" cy="12" r="8"/><path d="M12 7v6l4 2"/>'),
  "Emails queued": ico('<path d="M4 6h16v12H4z"/><path d="M4 7l8 6 8-6"/>')
};

const KPI_TONE = {
  Returned: "bad",
  "Returned MOVs": "bad",
  Overdue: "bad",
  "Overdue schools": "bad",
  "Not started": "warn",
  "Not yet": "warn",
  "TA flagged": "warn",
  Unread: "warn",
  "Under review": "warn",
  "Awaiting review": "warn"
};

function decorateKpis() {
  document.querySelectorAll(".kpi").forEach((kpi) => {
    if (kpi.querySelector(".kpi-head")) return;
    const labelNode = [...kpi.childNodes].find((n) => n.nodeType === Node.TEXT_NODE && n.textContent.trim());
    if (!labelNode) return;
    const text = labelNode.textContent.trim();
    const head = document.createElement("div");
    head.className = "kpi-head";
    head.innerHTML = `${KPI_ICONS[text] || ICONS.Dashboard}<span>${text}</span>`;
    kpi.replaceChild(head, labelNode);
    if (KPI_TONE[text]) kpi.classList.add(KPI_TONE[text]);
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

function insertSchoolSubmitNav() {
  const nav = document.querySelector(".nav");
  if (!nav || nav.querySelector('a[href="school-submit.html"]')) return;
  const movs = nav.querySelector('a[href="school-movs.html"]');
  if (!movs) return;
  const a = document.createElement("a");
  a.href = "school-submit.html";
  a.textContent = "Submit";
  if (location.pathname.endsWith("school-submit.html")) a.classList.add("active");
  movs.after(a);
}

function mountSchoolFlow() {
  const top = document.querySelector(".top");
  if (!top || document.querySelector(".flow-wrap")) return;
  const page = location.pathname.split("/").pop();
  const steps = [
    { n: "1", label: "Encode", hint: "7 / 12 FIs", href: "school-assessment.html", state: "done" },
    { n: "2", label: "MOVs", hint: "1 returned", href: "school-movs.html", state: "now" },
    { n: "3", label: "School Head QA", hint: "Not started", href: "school-submit.html", state: "lock" },
    { n: "4", label: "Submit", hint: "Blocked", href: "school-submit.html", state: "lock" },
    { n: "5", label: "Division", hint: "Waiting", href: "school-submit.html", state: "lock" },
    { n: "6", label: "Result", hint: "Not yet", href: "school-submit.html", state: "lock" }
  ];
  const wrap = document.createElement("div");
  wrap.className = "flow-wrap";
  wrap.innerHTML = `
    <div class="flow">
      ${steps.map((s) => `
        <a class="flow-step ${s.state}" href="${s.href}">
          <div class="flow-dot">${s.state === "done" ? "✓" : s.n}</div>
          <b>${s.label}</b>
          <small>${s.hint}</small>
        </a>
      `).join("")}
    </div>
    <div class="flow-banner">
      <div>
        <b>You are here: fix returned MOV, then submit</b>
        <p class="muted">Path: Encode → MOVs → School Head QA → Submit to Division → Validation → Functional (10/12).</p>
      </div>
      ${page === "school-submit.html" ? "" : `<a class="btn inline" href="school-submit.html">Open submit</a>`}
    </div>
  `;
  top.after(wrap);
}
