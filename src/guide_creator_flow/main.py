#!/usr/bin/env python
import json
import os
import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from crewai import LLM
from crewai.flow.flow import Flow, listen, start
from guide_creator_flow.crews.facility_assistant_crew.facility_assistant_crew import FacilityAssistantCrew
from guide_creator_flow.tools.sensor_api_tool import SensorAPIClientTool
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Define our models for structured data
class QueryAnalysis(BaseModel):
    user_name: Optional[str] = Field(description="The user's name, if mentioned.")
    user_location: Optional[str] = Field(description="The user's location, like a room number, if mentioned.")
    intent: str = Field(description="The user's primary intent, e.g., 'get_status', 'ask_knowledge_base', 'compare_data', 'general_query'.")
    required_sensors: List[str] = Field(description="A list of sensor names needed to answer the query, if any.")
    knowledge_query: Optional[str] = Field(description="A concise query for the knowledge base, if needed.")
    date_qualifier: Optional[str] = Field(description="The date or time period for comparison, e.g., 'yesterday'.")

# Define our flow state
class BuildingAssistantState(BaseModel):
    user_query: str = ""
    analysis: Optional[QueryAnalysis] = None
    final_response: str = ""
    chat_history: List[Dict[str, str]] = []

class BuildingAssistantFlow(Flow[BuildingAssistantState]):
    """A conversational AI flow for building management."""

    def __init__(self):
        super().__init__()
        # Instantiate tools to be used within the flow logic
        self.sensor_tool = SensorAPIClientTool()

    @start()
    def get_initial_state(self):
        """This method is the entry point of the flow."""
        return self.state

    @listen(get_initial_state)
    def analyze_query(self, state):
        """Analyze the user's query to extract entities and determine intent."""
        print("Analyzing user query...")
        llm = LLM(model="gemini/gemini-2.0-flash", response_format=QueryAnalysis)
        
        history_context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in state.chat_history])

        messages = [
            {"role": "system", "content": "You are a helpful assistant designed to analyze user queries and output JSON. You can use the chat history for context."},
            {"role": "user", "content": f"""
            Analyze the following user query based on the conversation history and extract the required information.
            Conversation History:
            {history_context}
            Current User Query: "{state.user_query}"
            - If the user mentions their name, extract it.
            - If they mention a location (e.g., room, floor), extract it.
            - Determine the intent:
                - 'get_status' if they ask for a sensor value (e.g., temperature, conductivity).
                - 'ask_knowledge_base' if they ask a 'why' or 'what is' question that requires a lookup.
                - 'compare_data' if they ask to compare data with a previous time (e.g., "yesterday").
                - 'general_query' for anything else.
            - If the intent is 'get_status' or 'compare_data', list the sensors they are asking about.
            - If the intent is 'compare_data', extract the date qualifier (e.g., 'yesterday', 'last week').
            - If the intent requires looking up information, formulate a concise search query for a knowledge base.
            """}
        ]
        
        response = llm.call(messages=messages)
        self.state.analysis = QueryAnalysis(**json.loads(response))

        print(f"Intent identified: {self.state.analysis.intent}")
        return self.state

    @listen(analyze_query)
    def run_facility_crew(self, state):
        """Run the facility assistant crew to synthesize a response."""
        print("Running Facility Assistant Crew...")

        mdx_path = r"C:\PersonalSpace\sd_emsd\data\cooling_tower_practice.md"
        
        today = datetime.date.today()
        current_date_str = today.strftime("%B %d, %Y")
        comparison_date_str = ""
        if state.analysis.date_qualifier:
            yesterday = today - datetime.timedelta(days=1)
            comparison_date_str = yesterday.strftime("%B %d, %Y")

        inputs = {
            "user_query": state.user_query,
            "user_name": state.analysis.user_name,
            "user_location": state.analysis.user_location,
            "required_sensors": state.analysis.required_sensors,
            "knowledge_query": state.analysis.knowledge_query or "No specific information was looked up.",
            "mdx_path": mdx_path,
            "date_qualifier": state.analysis.date_qualifier,
            "current_date": current_date_str,
            "comparison_date": comparison_date_str
        }
        
        crew_result = FacilityAssistantCrew().crew().kickoff(inputs=inputs)
        self.state.final_response = crew_result.raw
        return self.state

    @listen(run_facility_crew)
    def package_response(self, state):
        """Packages the final state to be returned to the UI."""
        self.state.chat_history.append({"role": "user", "content": state.user_query})
        self.state.chat_history.append({"role": "assistant", "content": state.final_response})
        return self.state

def kickoff():
    """Run the building assistant flow."""
    BuildingAssistantFlow().kickoff()
    print("\n=== Flow Complete ===")

if __name__ == "__main__":
    kickoff()