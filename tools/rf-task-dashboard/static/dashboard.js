const COLUMNS = [
  { status: "unclaimed", label: "Unclaimed", color: "var(--muted)" },
  { status: "in_progress", label: "In Progress", color: "var(--cyan)" },
  { status: "pr_raised", label: "Pending Review", color: "var(--amber)" },
  { status: "changes_requested", label: "Changes Requested", color: "var(--violet)" },
  { status: "merged", label: "Merged", color: "var(--green)" },
  { status: "blocked", label: "Blocked", color: "var(--red)" },
];

const REPO_URL = "https://github.com/choongyin72/ChoongYin_OS/pull/";

let refreshTimer = null;

async function fetchTasks() {
  const res = await fetch("/api/tasks");
  return res.json();
}

async function fetchTask(id) {
  const res = await fetch(`/api/tasks/${id}`);
  return res.json();
}

function renderReadout(tasks) {
  const readout = document.getElementById("readout");
  readout.innerHTML = "";
  COLUMNS.forEach((col) => {
    const count = tasks.filter((t) => t.status === col.status).length;
    const chip = document.createElement("div");
    chip.className = "readout__chip";
    chip.innerHTML = `
      <span class="readout__dot" style="background:${col.color}"></span>
      <span class="readout__count">${count}</span>
      <span class="readout__label">${col.label}</span>
    `;
    readout.appendChild(chip);
  });
}

function cardHtml(task) {
  const prLink = task.pr_number
    ? `<a class="card__pr" href="${REPO_URL}${task.pr_number}" target="_blank" rel="noopener" onclick="event.stopPropagation()">#${task.pr_number}</a>`
    : "";
  return `
    <div class="card" data-status="${task.status}" data-id="${task.id}">
      <div class="card__name">${escapeHtml(task.screen_name)}</div>
      <div class="card__meta">
        <span class="card__pattern">${task.pattern}</span>
        ${task.claimed_by ? `<span>${escapeHtml(task.claimed_by)}</span>` : ""}
        ${prLink}
      </div>
    </div>
  `;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str ?? "";
  return div.innerHTML;
}

function renderBoard(tasks) {
  const board = document.getElementById("board");
  board.innerHTML = "";
  COLUMNS.forEach((col) => {
    const colTasks = tasks.filter((t) => t.status === col.status);
    const column = document.createElement("div");
    column.className = "column";
    column.innerHTML = `
      <div class="column__header">
        <div class="column__header-left">
          <span class="readout__dot" style="background:${col.color}"></span>
          ${col.label}
        </div>
        <span class="column__count">${colTasks.length}</span>
      </div>
      <div class="column__body">
        ${
          colTasks.length
            ? colTasks.map(cardHtml).join("")
            : '<div class="column__empty">— empty —</div>'
        }
      </div>
    `;
    board.appendChild(column);
  });

  document.querySelectorAll(".card").forEach((card) => {
    card.addEventListener("click", () => openTaskDetail(card.dataset.id));
  });
}

async function refresh() {
  try {
    const tasks = await fetchTasks();
    renderReadout(tasks);
    renderBoard(tasks);
    document.getElementById("last-refreshed").textContent =
      "updated " + new Date().toLocaleTimeString();
  } catch (err) {
    document.getElementById("last-refreshed").textContent = "connection lost";
  }
}

async function openTaskDetail(id) {
  const task = await fetchTask(id);
  const dialog = document.getElementById("task-detail-dialog");
  const content = document.getElementById("task-detail-content");
  const history = (task.history || [])
    .map(
      (h) =>
        `<div class="history__item"><b>${h.to_status}</b> — ${h.note || ""} <span style="float:right">${new Date(h.timestamp).toLocaleString()}</span></div>`
    )
    .join("");
  content.innerHTML = `
    <h2>${escapeHtml(task.screen_name)}</h2>
    <div class="detail__row"><span>Status</span><span>${task.status}</span></div>
    <div class="detail__row"><span>Pattern</span><span>${task.pattern}</span></div>
    <div class="detail__row"><span>Claimed by</span><span>${task.claimed_by || "—"}</span></div>
    <div class="detail__row"><span>PR</span><span>${task.pr_number ? "#" + task.pr_number : "—"}</span></div>
    ${task.blocker_note ? `<div class="detail__row"><span>Blocker</span><span>${escapeHtml(task.blocker_note)}</span></div>` : ""}
    <div class="history">${history}</div>
  `;
  dialog.showModal();
}

document.getElementById("close-detail").addEventListener("click", () => {
  document.getElementById("task-detail-dialog").close();
});

document.getElementById("add-task-btn").addEventListener("click", () => {
  document.getElementById("add-task-dialog").showModal();
});

document.getElementById("cancel-add-task").addEventListener("click", () => {
  document.getElementById("add-task-dialog").close();
});

document.getElementById("add-task-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const screen_name = document.getElementById("new-screen-name").value;
  const pattern = document.getElementById("new-screen-pattern").value;
  await fetch("/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ screen_name, pattern }),
  });
  document.getElementById("add-task-dialog").close();
  document.getElementById("add-task-form").reset();
  refresh();
});

refresh();
refreshTimer = setInterval(refresh, 4000);
