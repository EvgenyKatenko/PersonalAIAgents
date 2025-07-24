from agents import Agent, Runner
from dotenv import load_dotenv
import json


def search_weather(location: str) -> str:
    """
    Simulated weather search tool that returns weather information for a given location.
    In a real implementation, this would call a weather API.
    """
    weather_data = {
        "Moscow": {
            "temperature": "-5°C",
            "condition": "Snowy",
            "humidity": "85%",
            "wind": "15 km/h NE"
        }
    }
    
    if location in weather_data:
        data = weather_data[location]
        return f"Weather in {location}: {data['temperature']}, {data['condition']}, Humidity: {data['humidity']}, Wind: {data['wind']}"
    else:
        return f"Weather data not available for {location}"


def create_hello_world_with_weather(weather_info: str) -> str:
    """
    Tool to create a hello world file with weather information.
    """
    content = f"""Hello World!

Today's Weather Report:
{weather_info}

This file was created by an AI agent with weather search capabilities.
Have a great day!
"""
    
    with open("hello_world_weather.txt", "w") as f:
        f.write(content)
    
    return "Successfully created hello_world_weather.txt with weather information"


def main():
    agent = Agent(
        name="WeatherAgent",
        instructions="You are a helpful assistant that can search for weather information and create files. When asked to create a hello world file with weather, first search for the weather and then create the file with that information.",
        tools=[search_weather, create_hello_world_with_weather]
    )
    
    result = Runner.run_sync(
        agent, 
        "Search for the weather in Moscow and create a hello world file that includes this weather information"
    )
    
    print(result.final_output)


if __name__ == "__main__":
    load_dotenv(override=True)
    main()