import os

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()  # loads WEATHER_API_KEY from the .env file

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get the current weather for a given city"""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": location, "appid": WEATHER_API_KEY, "units": "metric"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    if response.status_code != 200:
        return f"Could not get weather for {location}: {response.text}"

    data = response.json()
    description = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]

    return f"{location}: {description}, {temp}°C, humidity {humidity}%"

if __name__ == "__main__":
    mcp.run(transport="streamable-http") # Streamable http exposes an api for this particular service
