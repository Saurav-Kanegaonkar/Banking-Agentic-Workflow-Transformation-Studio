# Data Dictionary

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
