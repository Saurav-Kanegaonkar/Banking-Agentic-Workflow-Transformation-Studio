-- SQL checks mirror the synthetic CSV outputs in this public portfolio artifact.
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
