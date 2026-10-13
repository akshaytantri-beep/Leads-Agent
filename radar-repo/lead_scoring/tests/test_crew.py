"""Smoke tests: the crew builds and its config is wired correctly. No API calls."""
import os

os.environ.setdefault("OPENAI_API_KEY", "test-key")

from radar_lead_scoring.crew import RadarLeadScoringCrew


def test_crew_builds_with_three_agents_and_tasks():
    crew = RadarLeadScoringCrew().crew()
    assert [a.role for a in crew.agents] == [
        "Lead Data Analyst",
        "RADAR Lead Scoring Specialist",
        "Sales Intelligence Reporter",
    ]
    assert len(crew.tasks) == 3


def test_scorer_is_deterministic():
    crew = RadarLeadScoringCrew().crew()
    assert crew.agents[1].llm.temperature == 0.0


def test_recipients_default_from_environment(monkeypatch):
    monkeypatch.setenv("REPORT_RECIPIENTS", "team@example.com")
    crew = RadarLeadScoringCrew().crew()
    inputs = None
    for callback in crew.before_kickoff_callbacks:
        inputs = callback(inputs or {})
    crew._interpolate_inputs(inputs)
    assert "team@example.com" in crew.tasks[2].description
    assert "{report_recipients}" not in crew.tasks[2].description
