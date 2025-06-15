from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List, Optional
import random

class SensorToolInput(BaseModel):
    """Input for the SensorAPIClientTool."""
    sensor_names: List[str] = Field(..., description="A list of sensor names to query.")
    date: Optional[str] = Field(default=None, description="Optional: a date for historical data, e.g., 'yesterday'.")

class SensorAPIClientTool(BaseTool):
    name: str = "Sensor API Client"
    description: str = "A tool to query real-time or historical values from building sensors. For historical data, provide a date."
    args_schema: Type[BaseModel] = SensorToolInput

    def _run(self, sensor_names: List[str], date: Optional[str] = None) -> dict:
        """
        Simulates querying an API for sensor values.
        This is a dummy tool and will return plausible random values for recognized sensor types.
        If a specific sensor type is not recognized, it will default to providing a temperature reading.
        """
        results = {}
        for name in sensor_names:
            lower_name = name.lower()
            is_historical = date is not None

            if "conductivity" in lower_name:
                base_value = random.uniform(1500, 2500)
                value = base_value * (0.95 if is_historical else 1)
                results[name] = {"value": round(value, 2), "unit": "µS/cm"}
            elif "temp" in lower_name: # Using a shorter keyword for better matching
                base_value = random.uniform(20, 23)
                value = base_value * (1.05 if is_historical else 1)
                results[name] = {"value": round(value, 1), "unit": "°C"}
            elif "humid" in lower_name: # Using a shorter keyword for better matching
                base_value = random.uniform(45, 55)
                value = base_value * (0.90 if is_historical else 1)
                results[name] = {"value": round(value, 1), "unit": "%"}
            elif "air" in lower_name and "flow" in lower_name:
                base_value = random.uniform(0.1, 0.5)
                value = base_value * (1.1 if is_historical else 1)
                results[name] = {"value": round(value, 2), "unit": "m/s"}
            else:
                # Default case: If no other keyword matches, return a temperature reading.
                # This makes the tool more robust to unexpected agent inputs.
                base_value = random.uniform(20, 23)
                value = base_value * (1.05 if is_historical else 1)
                results[name] = {
                    "value": round(value, 1), 
                    "unit": "°C", 
                    "note": f"Sensor '{name}' not specifically recognized, providing default temperature."
                }
        
        return results

# Example of how to use the tool:
if __name__ == '__main__':
    tool = SensorAPIClientTool()
    # Query current data
    current_metrics = tool.run(sensor_names=["Room 101 Temperature", "Room 101 Air Flow"])
    print(f"Current Metrics: {current_metrics}")

    # Query historical data
    historical_metrics = tool.run(sensor_names=["Room 101 Temperature", "Room 101 Air Flow"], date="yesterday")
    print(f"Yesterday's Metrics: {historical_metrics}") 