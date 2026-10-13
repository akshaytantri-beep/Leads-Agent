"""Smoke tests: the crew builds and its config is wired correctly. No API calls."""
import os

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("SERPER_API_KEY", "test-key")

from indian_msme_lead_discovery.crew import IndianMsmeLeadDiscoveryCrew


def test_crew_builds_with_four_tasks_in_order():
    crew = IndianMsmeLeadDiscoveryCrew().crew()
    assert [t.name for t in crew.tasks] == [
        "discover_indian_companies_with_buying_signals",
        "research_indian_decision_makers_and_company_intelligence",
        "generate_indian_leads_csv_report",
        "save_indian_leads_to_onedrive_as_leads_csv",
    ]


def test_agent_has_search_and_upload():
    agent = IndianMsmeLeadDiscoveryCrew().crew().agents[0]
    assert {t.name for t in agent.tools} == {"Search the internet with Serper", "Read website content"}
    assert agent.apps == ["microsoft_onedrive/upload_file"]


def test_csv_task_forbids_guessed_emails():
    task = IndianMsmeLeadDiscoveryCrew().crew().tasks[2]
    assert "Email_Source" in task.description
    assert "never invent" in task.description
