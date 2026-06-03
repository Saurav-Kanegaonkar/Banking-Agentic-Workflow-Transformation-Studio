const state = {
  payload: null,
  selectedId: null,
  activeTab: "intake",
};

const formatNumber = new Intl.NumberFormat("en-US");

function scoreClass(value) {
  if (value >= 75) return "strong";
  if (value >= 60) return "watch";
  return "hold";
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function selectedUseCase() {
  return state.payload.use_cases.find((item) => item.use_case_id === state.selectedId);
}

function renderSummary() {
  const summary = state.payload.summary;
  document.getElementById("releasePill").textContent = `${summary.pilot_ready} controlled pilot${summary.pilot_ready === 1 ? "" : "s"}`;
  document.getElementById("summaryGrid").innerHTML = [
    ["Use cases", summary.use_cases],
    ["Avg priority", summary.avg_priority],
    ["Avg readiness", summary.avg_readiness],
    ["Weekly hours saved", formatNumber.format(summary.estimated_weekly_hours_saved)],
  ]
    .map(
      ([label, value]) => `
        <div class="metric">
          <span>${escapeHtml(label)}</span>
          <strong>${escapeHtml(value)}</strong>
        </div>
      `
    )
    .join("");
}

function renderQueue() {
  document.getElementById("queueList").innerHTML = state.payload.use_cases
    .map(
      (item) => `
        <button class="queue-item ${item.use_case_id === state.selectedId ? "selected" : ""}" type="button" data-id="${item.use_case_id}">
          <span class="queue-rank">${escapeHtml(item.use_case_id)}</span>
          <span class="queue-title">${escapeHtml(item.workflow)}</span>
          <span class="queue-meta">${escapeHtml(item.banking_domain)} | ${escapeHtml(item.release_decision)}</span>
          <span class="queue-score ${scoreClass(Number(item.priority_score))}">${escapeHtml(item.priority_score)}</span>
        </button>
      `
    )
    .join("");

  document.querySelectorAll(".queue-item").forEach((button) => {
    button.addEventListener("click", () => {
      state.selectedId = button.dataset.id;
      renderQueue();
      renderDetail();
    });
  });
}

function scoreBar(label, value, invert = false) {
  const numeric = Number(value);
  const barClass = invert ? scoreClass(100 - numeric) : scoreClass(numeric);
  return `
    <div class="score-row">
      <span>${escapeHtml(label)}</span>
      <div class="bar" aria-hidden="true"><i class="${barClass}" style="width:${Math.max(8, Math.min(100, numeric))}%"></i></div>
      <strong>${escapeHtml(value)}</strong>
    </div>
  `;
}

function renderIntake(item) {
  return `
    <div class="surface-head">
      <p class="eyebrow">${escapeHtml(item.current_status)}</p>
      <h2>${escapeHtml(item.workflow)}</h2>
      <p>${escapeHtml(item.problem_statement)}</p>
    </div>
    <div class="two-column">
      <section class="block">
        <h3>Product Hypothesis</h3>
        <p>${escapeHtml(item.agent_role)}</p>
        <dl class="fact-list">
          <div><dt>Primary user</dt><dd>${escapeHtml(item.primary_persona)}</dd></div>
          <div><dt>Product owner</dt><dd>${escapeHtml(item.product_owner)}</dd></div>
          <div><dt>Weekly cases</dt><dd>${formatNumber.format(item.weekly_case_volume)}</dd></div>
          <div><dt>Target cycle time</dt><dd>${escapeHtml(item.target_cycle_time_hours)} hours</dd></div>
        </dl>
      </section>
      <section class="block">
        <h3>Scoring Model</h3>
        ${scoreBar("Business value", item.business_value_score)}
        ${scoreBar("Implementation readiness", item.implementation_readiness_score)}
        ${scoreBar("Data quality", item.data_quality_score)}
        ${scoreBar("Risk exposure", item.risk_exposure_score, true)}
        ${scoreBar("Adoption friction", item.adoption_friction_score, true)}
      </section>
    </div>
  `;
}

function renderPrd(item) {
  const controlRows = item.journey
    .map(
      (step) => `
        <tr>
          <td>${escapeHtml(step.journey_step)}</td>
          <td>${escapeHtml(step.agent_action)}</td>
          <td>${escapeHtml(step.control)}</td>
          <td>${escapeHtml(step.escalation_trigger)}</td>
        </tr>
      `
    )
    .join("");

  const stories = item.backlog
    .map(
      (story) => `
        <article class="story">
          <span>${escapeHtml(story.sprint)} | ${escapeHtml(story.status)} | ${escapeHtml(story.effort_points)} pts</span>
          <h3>${escapeHtml(story.epic)}</h3>
          <p>${escapeHtml(story.story)}</p>
          <b>${escapeHtml(story.acceptance_criteria)}</b>
        </article>
      `
    )
    .join("");

  return `
    <div class="surface-head">
      <p class="eyebrow">Workflow PRD Builder</p>
      <h2>Human Review and Story Cards</h2>
      <p>The use case is translated into journey controls, escalation paths, and Agile-ready acceptance criteria.</p>
    </div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr><th>Step</th><th>Agent action</th><th>Control</th><th>Escalation trigger</th></tr>
        </thead>
        <tbody>${controlRows}</tbody>
      </table>
    </div>
    <div class="story-grid">${stories}</div>
  `;
}

function renderGates(item) {
  const tests = item.tests
    .map(
      (test) => `
        <li>
          <span>${escapeHtml(test.test_id)}</span>
          <strong>${escapeHtml(test.pass_rate)}%</strong>
          <p>${escapeHtml(test.behavior_test)}</p>
          <small>${escapeHtml(test.defect_theme)}</small>
        </li>
      `
    )
    .join("");

  return `
    <div class="surface-head">
      <p class="eyebrow">${escapeHtml(item.release_decision)}</p>
      <h2>Governance and Release Gates</h2>
      <p>Release posture is tied to behavior-test evidence, residual risk, compliance complexity, and reviewer burden.</p>
    </div>
    <div class="gate-layout">
      <section class="block">
        <h3>Release Readiness</h3>
        <div class="readiness ${scoreClass(Number(item.release_readiness_score))}">
          <strong>${escapeHtml(item.release_readiness_score)}</strong>
          <span>${escapeHtml(item.release_decision)}</span>
        </div>
        ${scoreBar("Risk exposure", item.risk_exposure_score, true)}
        ${scoreBar("Compliance complexity", item.compliance_complexity_score, true)}
        ${scoreBar("Human review need", item.human_review_need_score, true)}
      </section>
      <section class="block">
        <h3>Agent Behavior Tests</h3>
        <ul class="test-list">${tests}</ul>
      </section>
    </div>
  `;
}

function renderAdoption(item) {
  const metrics = item.adoption;
  return `
    <div class="surface-head">
      <p class="eyebrow">Pilot OKR Tracker</p>
      <h2>Adoption, Outcomes, and Next Change</h2>
      <p>Change-management readiness is measured through AI Champion coverage, active usage, override behavior, trust, and cycle-time movement.</p>
    </div>
    <div class="okr-grid">
      <div class="metric large"><span>AI Champions</span><strong>${escapeHtml(metrics.ai_champions)}</strong></div>
      <div class="metric large"><span>Active users</span><strong>${escapeHtml(metrics.active_users)}</strong></div>
      <div class="metric large"><span>Automation rate</span><strong>${escapeHtml(metrics.automation_rate)}%</strong></div>
      <div class="metric large"><span>Trust score</span><strong>${escapeHtml(metrics.trust_score)}</strong></div>
    </div>
    <section class="block">
      <h3>Outcome Movement</h3>
      ${scoreBar("Human override rate", metrics.human_override_rate, true)}
      ${scoreBar("Cycle-time improvement", Math.abs(Number(metrics.cycle_time_delta_percent)))}
      ${scoreBar("Quality movement", Math.max(0, Number(metrics.quality_delta_percent) * 8))}
      <p class="next-change">${escapeHtml(metrics.next_change)}</p>
    </section>
  `;
}

function renderDetail() {
  const item = selectedUseCase();
  const renderers = {
    intake: renderIntake,
    prd: renderPrd,
    gates: renderGates,
    adoption: renderAdoption,
  };
  document.getElementById("detailSurface").innerHTML = renderers[state.activeTab](item);
}

function wireTabs() {
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      state.activeTab = tab.dataset.tab;
      document.querySelectorAll(".tab").forEach((item) => item.classList.toggle("active", item === tab));
      renderDetail();
    });
  });
}

async function init() {
  const response = await fetch("analysis/outputs/app_payload.json");
  state.payload = await response.json();
  state.selectedId = state.payload.use_cases[0].use_case_id;
  renderSummary();
  renderQueue();
  renderDetail();
  wireTabs();
}

init().catch((error) => {
  document.getElementById("detailSurface").innerHTML = `<p class="error">Unable to load operating packet: ${escapeHtml(error.message)}</p>`;
});
