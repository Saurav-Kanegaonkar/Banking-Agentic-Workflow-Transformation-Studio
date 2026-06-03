import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "analysis" / "outputs"


USE_CASES = [
    {
        "id": "AAI-101",
        "workflow": "Commercial covenant exception triage",
        "domain": "Corporate lending",
        "persona": "Relationship manager and credit analyst",
        "problem": "Covenant exceptions arrive through fragmented notes, spreadsheets, and inbox threads, which slows credit follow-up and makes escalation evidence inconsistent.",
        "agent": "Summarizes exceptions, retrieves covenant context, drafts follow-up questions, and routes unresolved items to credit review.",
        "value": 91,
        "readiness": 76,
        "quality": 81,
        "risk": 82,
        "compliance": 78,
        "review": 86,
        "adoption": 42,
        "volume": 640,
        "minutes_saved": 18,
        "current_hours": 32,
        "target_hours": 18,
        "owner": "Credit product operations",
        "status": "Pilot candidate",
    },
    {
        "id": "AAI-102",
        "workflow": "Treasury payment investigation assistant",
        "domain": "Treasury and payments",
        "persona": "Payment operations specialist",
        "problem": "Investigators need to reconcile payment status, client notes, exception codes, and policy constraints before they can resolve delayed payments.",
        "agent": "Assembles the investigation timeline, flags missing data, recommends the next operational step, and requests human approval for client-facing updates.",
        "value": 94,
        "readiness": 82,
        "quality": 86,
        "risk": 74,
        "compliance": 71,
        "review": 79,
        "adoption": 35,
        "volume": 1180,
        "minutes_saved": 12,
        "current_hours": 14,
        "target_hours": 7,
        "owner": "Payments platform",
        "status": "Discovery complete",
    },
    {
        "id": "AAI-103",
        "workflow": "KYC refresh evidence collector",
        "domain": "Client onboarding and due diligence",
        "persona": "Onboarding analyst and compliance reviewer",
        "problem": "Refresh packets require repeated document checks, ownership questions, and policy evidence before a reviewer can approve the case.",
        "agent": "Prepares an evidence checklist, extracts document signals, drafts reviewer notes, and blocks completion when critical evidence is absent.",
        "value": 88,
        "readiness": 69,
        "quality": 74,
        "risk": 89,
        "compliance": 92,
        "review": 94,
        "adoption": 51,
        "volume": 420,
        "minutes_saved": 24,
        "current_hours": 72,
        "target_hours": 48,
        "owner": "Financial crimes operations",
        "status": "Governance review",
    },
    {
        "id": "AAI-104",
        "workflow": "Institutional client service request router",
        "domain": "Institutional client service",
        "persona": "Client service associate",
        "problem": "Service requests move across custody, trust, liquidity, and reporting teams without a consistent routing rationale or client-ready status summary.",
        "agent": "Classifies request intent, selects the next service queue, drafts internal context, and keeps the client-service owner in control.",
        "value": 83,
        "readiness": 84,
        "quality": 88,
        "risk": 63,
        "compliance": 66,
        "review": 70,
        "adoption": 32,
        "volume": 1540,
        "minutes_saved": 9,
        "current_hours": 20,
        "target_hours": 12,
        "owner": "Institutional servicing",
        "status": "Pilot ready",
    },
    {
        "id": "AAI-105",
        "workflow": "Wealth onboarding packet reviewer",
        "domain": "Wealth management",
        "persona": "Advisor support specialist",
        "problem": "New client packets often need follow-up because forms, identity evidence, risk preferences, and account-opening notes are reviewed in separate systems.",
        "agent": "Checks packet completeness, highlights missing evidence, drafts advisor follow-up language, and sends exceptions to human review.",
        "value": 79,
        "readiness": 73,
        "quality": 79,
        "risk": 76,
        "compliance": 83,
        "review": 88,
        "adoption": 45,
        "volume": 510,
        "minutes_saved": 15,
        "current_hours": 48,
        "target_hours": 30,
        "owner": "Wealth digital product",
        "status": "Intake scoring",
    },
    {
        "id": "AAI-106",
        "workflow": "Capital markets document intake summarizer",
        "domain": "Capital markets operations",
        "persona": "Operations analyst and legal reviewer",
        "problem": "Deal documents and amendments require quick summarization, obligation tracking, and review routing without weakening legal control.",
        "agent": "Creates structured summaries, extracts obligations, links source passages, and routes low-confidence clauses to legal review.",
        "value": 86,
        "readiness": 61,
        "quality": 68,
        "risk": 91,
        "compliance": 90,
        "review": 96,
        "adoption": 58,
        "volume": 260,
        "minutes_saved": 31,
        "current_hours": 96,
        "target_hours": 60,
        "owner": "Markets product operations",
        "status": "Control design",
    },
    {
        "id": "AAI-107",
        "workflow": "Commercial card dispute packet assembler",
        "domain": "Commercial card",
        "persona": "Dispute operations specialist",
        "problem": "Case packets require transaction context, merchant evidence, customer notes, and policy checks before a specialist can act.",
        "agent": "Builds a dispute packet, flags contradictory evidence, suggests the next case action, and requires specialist approval before submission.",
        "value": 81,
        "readiness": 79,
        "quality": 83,
        "risk": 72,
        "compliance": 74,
        "review": 80,
        "adoption": 39,
        "volume": 890,
        "minutes_saved": 11,
        "current_hours": 28,
        "target_hours": 17,
        "owner": "Card operations product",
        "status": "Backlog refinement",
    },
    {
        "id": "AAI-108",
        "workflow": "Relationship manager next-best-action brief",
        "domain": "Corporate relationship management",
        "persona": "Relationship manager",
        "problem": "Relationship managers need a concise account context brief before client outreach, but signals are spread across service, credit, treasury, and pipeline systems.",
        "agent": "Synthesizes account signals, highlights open risks, recommends next questions, and blocks unsupported product recommendations.",
        "value": 78,
        "readiness": 66,
        "quality": 70,
        "risk": 84,
        "compliance": 81,
        "review": 85,
        "adoption": 62,
        "volume": 730,
        "minutes_saved": 14,
        "current_hours": 40,
        "target_hours": 26,
        "owner": "Relationship platform",
        "status": "Discovery in progress",
    },
]


def priority_score(item):
    upside = item["value"] * 0.34 + item["readiness"] * 0.19 + item["quality"] * 0.14
    control_drag = item["risk"] * 0.13 + item["compliance"] * 0.09 + item["review"] * 0.05 + item["adoption"] * 0.04
    scale_bonus = min(item["volume"] / 40, 32) * 0.07
    return round(upside - control_drag + scale_bonus + 38, 1)


def release_readiness(item):
    evidence = item["readiness"] * 0.25 + item["quality"] * 0.2 + (100 - item["risk"]) * 0.15
    governance = (100 - item["compliance"]) * 0.15 + (100 - item["review"]) * 0.1
    adoption = (100 - item["adoption"]) * 0.1 + item["value"] * 0.05
    return round(evidence + governance + adoption, 1)


def release_decision(readiness):
    if readiness >= 63:
        return "Release to controlled pilot"
    if readiness >= 58:
        return "Hold for control evidence"
    return "Keep in discovery"


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_use_case_rows():
    rows = []
    for item in USE_CASES:
        score = priority_score(item)
        readiness = release_readiness(item)
        rows.append(
            {
                "use_case_id": item["id"],
                "workflow": item["workflow"],
                "banking_domain": item["domain"],
                "primary_persona": item["persona"],
                "problem_statement": item["problem"],
                "agent_role": item["agent"],
                "business_value_score": item["value"],
                "implementation_readiness_score": item["readiness"],
                "data_quality_score": item["quality"],
                "risk_exposure_score": item["risk"],
                "compliance_complexity_score": item["compliance"],
                "human_review_need_score": item["review"],
                "adoption_friction_score": item["adoption"],
                "weekly_case_volume": item["volume"],
                "estimated_minutes_saved_per_case": item["minutes_saved"],
                "current_cycle_time_hours": item["current_hours"],
                "target_cycle_time_hours": item["target_hours"],
                "product_owner": item["owner"],
                "current_status": item["status"],
                "priority_score": score,
                "release_readiness_score": readiness,
                "release_decision": release_decision(readiness),
            }
        )
    return sorted(rows, key=lambda row: row["priority_score"], reverse=True)


def build_journey_rows():
    steps = [
        (
            "Intake",
            "Business user submits workflow pain point and expected outcome.",
            "Checks intake completeness and maps the workflow to known systems.",
            "Reject intake if the target user, decision point, or source data owner is missing.",
            "Missing owner, missing decision point, or unclear regulated action.",
            "Intake form, source-system inventory, target user group.",
        ),
        (
            "Agent draft",
            "Agent prepares a summary, recommendation, or packet for review.",
            "Retrieves source context, drafts the work product, and cites evidence fields.",
            "Require source links, confidence score, and blocked-action labels.",
            "Low confidence, unsupported recommendation, client-facing wording.",
            "Prompt version, source fields, confidence threshold, generated output.",
        ),
        (
            "Human review",
            "Business reviewer accepts, edits, or rejects the agent output.",
            "Captures edits and routes rejected outputs to test backlog.",
            "No autonomous completion for regulated decisions or client commitments.",
            "Reviewer override, adverse action, legal language, policy exception.",
            "Reviewer decision, edit log, exception reason.",
        ),
        (
            "Escalation",
            "Risk, Compliance, Legal, or Technology reviews blocked cases.",
            "Packages the evidence trail and suggested remediation path.",
            "Escalate before release when defects repeat or evidence is incomplete.",
            "Repeat defect, missing audit trail, sensitive data concern.",
            "Escalation ticket, control owner signoff, remediation note.",
        ),
    ]
    rows = []
    for item in USE_CASES:
        for index, step in enumerate(steps, start=1):
            rows.append(
                {
                    "use_case_id": item["id"],
                    "step_order": index,
                    "journey_step": step[0],
                    "human_role": item["persona"],
                    "user_action": step[1],
                    "agent_action": step[2],
                    "control": step[3],
                    "escalation_trigger": step[4],
                    "evidence_required": step[5],
                }
            )
    return rows


def build_test_rows():
    tests = [
        ("HITL-01", "Blocks autonomous completion for regulated decisions", 96, "Critical", "No bypass attempt passed."),
        ("EVID-02", "Cites required source evidence in generated summary", 91, "High", "Weak citation coverage on older document packets."),
        ("SAFE-03", "Avoids unsupported client-facing recommendation", 94, "Critical", "One output needed product-eligibility clarification."),
        ("ROUTE-04", "Routes low-confidence cases to the correct escalation queue", 88, "Medium", "Routing labels need cleaner operational taxonomy."),
        ("AUDIT-05", "Preserves prompt, reviewer, and source-field audit trail", 93, "High", "Audit export needs a release-owner field."),
    ]
    rows = []
    for item in USE_CASES:
        modifier = (item["quality"] - item["risk"]) / 12
        for test_id, test, base, severity, defect in tests:
            pass_rate = max(70, min(99, round(base + modifier - item["compliance"] / 45, 1)))
            rows.append(
                {
                    "use_case_id": item["id"],
                    "test_id": test_id,
                    "behavior_test": test,
                    "pass_rate": pass_rate,
                    "sample_size": 120,
                    "severity": severity,
                    "review_partner": "Technology and Risk",
                    "defect_theme": defect,
                }
            )
    return rows


def build_backlog_rows():
    rows = []
    for item in USE_CASES:
        rows.extend(
            [
                {
                    "use_case_id": item["id"],
                    "epic": "Workflow intake and PRD evidence",
                    "story": f"As a product manager, I need a validated intake packet for {item['workflow']} so the team can refine scope with business, technology, and control partners.",
                    "acceptance_criteria": "Includes target user, source systems, decision point, control owner, success metric, and blocked autonomous actions.",
                    "sprint": "Sprint 1",
                    "effort_points": 5,
                    "dependency": "Business process owner",
                    "status": "Ready",
                },
                {
                    "use_case_id": item["id"],
                    "epic": "Human review and escalation",
                    "story": f"As a {item['persona'].split(' and ')[0].lower()}, I need every agent output for {item['workflow']} to show why it can be accepted, edited, or escalated.",
                    "acceptance_criteria": "Shows evidence links, confidence threshold, reviewer action, escalation reason, and immutable audit event.",
                    "sprint": "Sprint 2",
                    "effort_points": 8,
                    "dependency": "Risk and Compliance signoff",
                    "status": "In refinement",
                },
                {
                    "use_case_id": item["id"],
                    "epic": "Pilot measurement",
                    "story": f"As an AI Champion, I need adoption and outcome metrics for {item['workflow']} so pilot feedback can drive the next backlog decision.",
                    "acceptance_criteria": "Tracks active users, automation rate, override rate, cycle-time movement, quality movement, trust score, and feedback theme.",
                    "sprint": "Sprint 3",
                    "effort_points": 5,
                    "dependency": "Analytics instrumentation",
                    "status": "Planned",
                },
            ]
        )
    return rows


def build_adoption_rows():
    rows = []
    for item in USE_CASES:
        trained = 45 + int(item["readiness"] / 2)
        active = round(trained * (0.52 + (100 - item["adoption"]) / 260))
        automation_rate = round((item["readiness"] + item["quality"] - item["risk"] * 0.35) / 2.2, 1)
        override_rate = round((item["review"] + item["risk"]) / 4.8, 1)
        rows.append(
            {
                "use_case_id": item["id"],
                "pilot_group": item["owner"],
                "ai_champions": 3 + int(item["volume"] / 500),
                "trained_users": trained,
                "active_users": active,
                "automation_rate": automation_rate,
                "human_override_rate": override_rate,
                "trust_score": round(8.4 - item["adoption"] / 25 + item["quality"] / 100, 1),
                "cycle_time_delta_percent": round(((item["target_hours"] - item["current_hours"]) / item["current_hours"]) * 100, 1),
                "quality_delta_percent": round((item["quality"] - 72) / 2.4, 1),
                "next_change": "Tighten control labels" if item["risk"] > 82 else "Expand pilot cohort",
            }
        )
    return rows


def build_payload(use_cases, journeys, tests, backlog, adoption):
    journey_by_case = {}
    for row in journeys:
        journey_by_case.setdefault(row["use_case_id"], []).append(row)
    tests_by_case = {}
    for row in tests:
        tests_by_case.setdefault(row["use_case_id"], []).append(row)
    backlog_by_case = {}
    for row in backlog:
        backlog_by_case.setdefault(row["use_case_id"], []).append(row)
    adoption_by_case = {row["use_case_id"]: row for row in adoption}

    enriched = []
    for row in use_cases:
        use_case_id = row["use_case_id"]
        enriched.append(
            {
                **row,
                "journey": journey_by_case[use_case_id],
                "tests": tests_by_case[use_case_id],
                "backlog": backlog_by_case[use_case_id],
                "adoption": adoption_by_case[use_case_id],
            }
        )

    avg_priority = round(sum(float(row["priority_score"]) for row in use_cases) / len(use_cases), 1)
    avg_readiness = round(sum(float(row["release_readiness_score"]) for row in use_cases) / len(use_cases), 1)
    pilot_ready = sum(1 for row in use_cases if row["release_decision"] == "Release to controlled pilot")
    controlled = sum(1 for row in use_cases if "Hold" in row["release_decision"])

    return {
        "summary": {
            "use_cases": len(use_cases),
            "avg_priority": avg_priority,
            "avg_readiness": avg_readiness,
            "pilot_ready": pilot_ready,
            "control_hold": controlled,
            "highest_priority": use_cases[0]["workflow"],
            "total_weekly_volume": sum(int(row["weekly_case_volume"]) for row in use_cases),
            "estimated_weekly_hours_saved": round(
                sum(int(row["weekly_case_volume"]) * int(row["estimated_minutes_saved_per_case"]) for row in use_cases) / 60,
                1,
            ),
        },
        "use_cases": enriched,
    }


def write_markdown(use_cases, payload):
    top = use_cases[0]
    findings = [
        "# Executive Findings",
        "",
        "## What I Analyzed",
        "",
        "I evaluated eight synthetic agentic AI use cases across a regulated wealth, corporate, commercial, and institutional banking operating model. The scoring connects business value, implementation readiness, data quality, risk exposure, human review need, compliance complexity, and adoption friction.",
        "",
        "## Findings",
        "",
        f"- The highest-priority workflow is {top['workflow']} with a priority score of {top['priority_score']}.",
        f"- The portfolio contains {payload['summary']['pilot_ready']} controlled pilot candidates and {payload['summary']['control_hold']} use cases that should pause for stronger control evidence.",
        f"- The modeled portfolio has {payload['summary']['total_weekly_volume']:,} weekly cases and an estimated {payload['summary']['estimated_weekly_hours_saved']:,} weekly hours of staff capacity that could shift from manual packet assembly to review and exception handling.",
        "- Human-in-the-loop design is not a late-stage governance task. It is part of the product requirement because all high-risk workflows need reviewer decision capture, escalation routing, and audit evidence before pilot release.",
        "",
        "## Recommendation",
        "",
        "Start with the payment investigation and institutional service routing use cases because they combine high volume, strong data readiness, and a practical review pattern. Keep KYC refresh and capital markets document intake in control design until evidence citation, audit export, and escalation behavior meet release thresholds.",
    ]
    (ROOT / "analysis" / "executive_findings.md").write_text("\n".join(findings) + "\n")

    plan = [
        "# Analysis Plan",
        "",
        "1. Build a synthetic intake inventory of banking workflow automation opportunities.",
        "2. Score each use case for value, readiness, data quality, risk, compliance complexity, human review need, and adoption friction.",
        "3. Translate the ranked opportunities into PRD-ready stories, acceptance criteria, controls, and validation tests.",
        "4. Connect release decisions to behavior test results and adoption metrics.",
        "5. Use the output as a portfolio artifact for product discovery, backlog refinement, governance review, and pilot planning.",
    ]
    (ROOT / "analysis" / "analysis_plan.md").write_text("\n".join(plan) + "\n")

    methodology = [
        "# Methodology",
        "",
        "The data is deterministic synthetic data. It is modeled on common regulated banking workflow patterns, including payment investigations, commercial lending exceptions, KYC refresh, wealth onboarding, institutional service routing, commercial card disputes, capital markets document review, and relationship-manager account preparation.",
        "",
        "Priority score weights business value, implementation readiness, data quality, control effort, human review need, adoption friction, and scale. Release readiness weights evidence quality, source-data readiness, residual risk, compliance complexity, human review burden, adoption friction, and expected value. The scores are intentionally rules-based so a product manager can explain and challenge them with Risk, Compliance, Technology, Operations, and business stakeholders.",
    ]
    (ROOT / "analysis" / "methodology.md").write_text("\n".join(methodology) + "\n")


def write_sql_checks():
    sql = """-- SQL checks mirror the synthetic CSV outputs in this public portfolio artifact.
-- Table names assume the CSVs have been loaded into similarly named warehouse tables.

select
  count(*) as use_case_count,
  round(avg(priority_score), 1) as avg_priority_score,
  round(avg(release_readiness_score), 1) as avg_release_readiness
from use_cases;

select
  use_case_id,
  workflow,
  priority_score,
  release_decision
from use_cases
where risk_exposure_score >= 85
  and release_decision = 'Release to controlled pilot';

select
  use_case_id,
  count(*) as control_steps
from journey_controls
group by use_case_id
having count(*) < 4;

select
  use_case_id,
  min(pass_rate) as weakest_behavior_test
from agent_tests
group by use_case_id
having min(pass_rate) < 85;

select
  use_case_id,
  automation_rate,
  human_override_rate,
  trust_score
from adoption_metrics
where human_override_rate > 35
   or trust_score < 7.0;
"""
    (ROOT / "analysis" / "sql_checks.sql").write_text(sql)


def write_data_readme():
    content = """# Data Sources

All datasets are deterministic synthetic data for a public portfolio artifact. They do not represent real customer, employee, client, payment, lending, wealth, compliance, model-risk, or production AI data.

The data is modeled on common structures in regulated wealth, corporate, commercial, and institutional banking workflows:

- `use_cases.csv`: Agentic AI workflow opportunities with value, readiness, risk, compliance, human-review, adoption, volume, and release-readiness fields.
- `journey_controls.csv`: Workflow steps, user actions, agent actions, human-in-the-loop controls, escalation triggers, and audit evidence.
- `agent_tests.csv`: Behavior-validation tests for evidence citation, safe recommendations, escalation routing, and audit trail completeness.
- `backlog_items.csv`: PRD-style epics, user stories, acceptance criteria, sprint placement, dependencies, and status.
- `adoption_metrics.csv`: Pilot readiness, AI Champion coverage, active users, automation rate, override rate, trust score, cycle-time movement, and next change.

The scores are rules-based so the artifact can be defended in an interview without claiming access to private banking systems.
"""
    (DATA_DIR / "README.md").write_text(content)


def write_dictionary():
    content = """# Data Dictionary

## use_cases.csv

- `priority_score`: Rules-based product priority score using value, readiness, quality, risk, compliance complexity, human-review need, adoption friction, and scale.
- `release_readiness_score`: Rules-based score for whether the use case has enough evidence, control design, and adoption readiness for a pilot.
- `release_decision`: Suggested release posture, either controlled pilot, hold for control evidence, or discovery.

## journey_controls.csv

- `control`: Product control that must be designed into the workflow.
- `escalation_trigger`: Condition that moves work to Risk, Compliance, Legal, Technology, or another accountable human owner.
- `evidence_required`: Audit evidence expected before release or reviewer approval.

## agent_tests.csv

- `behavior_test`: Agent behavior that must be validated before pilot release.
- `pass_rate`: Synthetic test pass rate across a 120-case sample.
- `defect_theme`: Main defect pattern to feed into backlog refinement.

## backlog_items.csv

- `story`: User-story wording that connects the use case to delivery work.
- `acceptance_criteria`: Testable product criteria for Agile planning and release coordination.

## adoption_metrics.csv

- `automation_rate`: Modeled share of cases where the agent can prepare useful work without rework before human approval.
- `human_override_rate`: Modeled share of cases where the reviewer edits or rejects the agent output.
- `trust_score`: Synthetic user trust score from pilot feedback.
"""
    (ROOT / "data_dictionary.md").write_text(content)


def main():
    DATA_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    use_cases = build_use_case_rows()
    journeys = build_journey_rows()
    tests = build_test_rows()
    backlog = build_backlog_rows()
    adoption = build_adoption_rows()
    payload = build_payload(use_cases, journeys, tests, backlog, adoption)

    write_csv(DATA_DIR / "use_cases.csv", use_cases, list(use_cases[0].keys()))
    write_csv(
        DATA_DIR / "journey_controls.csv",
        journeys,
        ["use_case_id", "step_order", "journey_step", "human_role", "user_action", "agent_action", "control", "escalation_trigger", "evidence_required"],
    )
    write_csv(
        DATA_DIR / "agent_tests.csv",
        tests,
        ["use_case_id", "test_id", "behavior_test", "pass_rate", "sample_size", "severity", "review_partner", "defect_theme"],
    )
    write_csv(
        DATA_DIR / "backlog_items.csv",
        backlog,
        ["use_case_id", "epic", "story", "acceptance_criteria", "sprint", "effort_points", "dependency", "status"],
    )
    write_csv(
        DATA_DIR / "adoption_metrics.csv",
        adoption,
        ["use_case_id", "pilot_group", "ai_champions", "trained_users", "active_users", "automation_rate", "human_override_rate", "trust_score", "cycle_time_delta_percent", "quality_delta_percent", "next_change"],
    )

    write_csv(OUTPUT_DIR / "priority_queue.csv", use_cases, list(use_cases[0].keys()))
    write_csv(
        OUTPUT_DIR / "release_gate_matrix.csv",
        [
            {
                "use_case_id": row["use_case_id"],
                "workflow": row["workflow"],
                "release_readiness_score": row["release_readiness_score"],
                "release_decision": row["release_decision"],
                "risk_exposure_score": row["risk_exposure_score"],
                "compliance_complexity_score": row["compliance_complexity_score"],
                "human_review_need_score": row["human_review_need_score"],
            }
            for row in use_cases
        ],
        ["use_case_id", "workflow", "release_readiness_score", "release_decision", "risk_exposure_score", "compliance_complexity_score", "human_review_need_score"],
    )
    write_csv(OUTPUT_DIR / "prd_story_cards.csv", backlog, ["use_case_id", "epic", "story", "acceptance_criteria", "sprint", "effort_points", "dependency", "status"])
    write_csv(OUTPUT_DIR / "adoption_okr_tracker.csv", adoption, ["use_case_id", "pilot_group", "ai_champions", "trained_users", "active_users", "automation_rate", "human_override_rate", "trust_score", "cycle_time_delta_percent", "quality_delta_percent", "next_change"])

    (OUTPUT_DIR / "app_payload.json").write_text(json.dumps(payload, indent=2))
    (OUTPUT_DIR / "summary.json").write_text(json.dumps(payload["summary"], indent=2))

    write_markdown(use_cases, payload)
    write_sql_checks()
    write_data_readme()
    write_dictionary()

    print(f"Generated {len(use_cases)} use cases and {len(backlog)} PRD story cards.")
    print(f"Top priority: {use_cases[0]['workflow']} ({use_cases[0]['priority_score']})")


if __name__ == "__main__":
    main()
