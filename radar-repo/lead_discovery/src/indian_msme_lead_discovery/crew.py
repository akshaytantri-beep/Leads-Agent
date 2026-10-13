import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	SerperDevTool,
	ScrapeWebsiteTool
)

@CrewBase
class IndianMsmeLeadDiscoveryCrew:
    """IndianMsmeLeadDiscovery crew"""

    @agent
    def b2b_prospect_discovery_specialist(self) -> Agent:
        
        return Agent(
            config=self.agents_config["b2b_prospect_discovery_specialist"],
            
            tools=[				SerperDevTool(),
				ScrapeWebsiteTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            apps=[
                    "microsoft_onedrive/upload_file",
                    ],
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
            ),
        )
    

    @task
    def discover_indian_companies_with_buying_signals(self) -> Task:
        return Task(
            config=self.tasks_config["discover_indian_companies_with_buying_signals"],
            markdown=False,
            
        )
    @task
    def research_indian_decision_makers_and_company_intelligence(self) -> Task:
        return Task(
            config=self.tasks_config["research_indian_decision_makers_and_company_intelligence"],
            markdown=False,
            
        )
    @task
    def generate_indian_leads_csv_report(self) -> Task:
        return Task(
            config=self.tasks_config["generate_indian_leads_csv_report"],
            markdown=False,
            
        )
    @task
    def save_indian_leads_to_onedrive_as_leads_csv(self) -> Task:
        return Task(
            config=self.tasks_config["save_indian_leads_to_onedrive_as_leads_csv"],
            markdown=False,
            
        )

    @crew
    def crew(self) -> Crew:
        """Creates the IndianMsmeLeadDiscovery crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,

            chat_llm=LLM(model="openai/gpt-4o"),
        )

