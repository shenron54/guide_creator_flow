import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from guide_creator_flow.tools.sensor_api_tool import SensorAPIClientTool
from crewai_tools import MDXSearchTool

# Uncomment the following line to use an example of a custom tool
# from facility_assistant_crew.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class FacilityAssistantCrew():
	"""FacilityAssistantCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def building_systems_analyst(self) -> Agent:
		# Configure the MDXSearchTool
		mdx_tool = MDXSearchTool(
			config=dict(
				llm=dict(
					provider="google",
					config=dict(
						model="gemini-pro",
					),
				),
				embedder=dict(
					provider="google",
					config=dict(
						model="models/embedding-001",
						task_type="retrieval_document",
					),
				),
			)
		)
		return Agent(
			config=self.agents_config['building_systems_analyst'],
			tools=[SensorAPIClientTool(), mdx_tool],
			verbose=True
		)

	@agent
	def helpful_assistant(self) -> Agent:
		return Agent(
			config=self.agents_config['helpful_assistant'],
			verbose=True
		)

	@task
	def analyze_data_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_data_task'],
		)

	@task
	def generate_response_task(self) -> Task:
		return Task(
			config=self.tasks_config['generate_response_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the FacilityAssistantCrew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
