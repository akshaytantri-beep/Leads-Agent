import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, before_kickoff, crew, task

@CrewBase
class RadarLeadScoringCrew:
    """RadarLeadScoring crew"""

    @before_kickoff
    def default_inputs(self, inputs):
        """Fill report_recipients from the environment when the run passes none."""
        inputs = dict(inputs or {})
        inputs.setdefault("report_recipients", os.environ.get("REPORT_RECIPIENTS", "sales@example.com"))
        return inputs

    @agent
    def lead_data_analyst(self) -> Agent:
        
        return Agent(
            config=self.agents_config["lead_data_analyst"],
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            apps=[
                    "microsoft_onedrive/download_file_by_path",
                    "microsoft_onedrive/get_file_by_path",
                    ],
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.0,
            ),
        )
    
    @agent
    def radar_lead_scoring_specialist(self) -> Agent:
        
        return Agent(
            config=self.agents_config["radar_lead_scoring_specialist"],
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.0,
            ),
        )
    
    @agent
    def sales_intelligence_reporter(self) -> Agent:
        
        return Agent(
            config=self.agents_config["sales_intelligence_reporter"],
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            apps=[
                    "google_gmail/send_email",
                    "google_sheets/create_spreadsheet",
                    "google_sheets/update_values",
                    "google_drive/share_file",
                    ],
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.0,
            ),
        )
    

    @task
    def process_lead_data_from_onedrive(self) -> Task:
        return Task(
            config=self.tasks_config["process_lead_data_from_onedrive"],
            markdown=False,
            
        )
    @task
    def apply_radar_scoring(self) -> Task:
        return Task(
            config=self.tasks_config["apply_radar_scoring"],
            markdown=False,
            
        )
    @task
    def generate_reports_and_send_alerts(self) -> Task:
        return Task(
            config=self.tasks_config["generate_reports_and_send_alerts"],
            markdown=False,
            
        )

    @crew
    def crew(self) -> Crew:
        """Creates the RadarLeadScoring crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,

            chat_llm=LLM(model="openai/gpt-4o"),
        )

