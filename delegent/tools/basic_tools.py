from pydantic import BaseModel, Field
from langchain.tools import tool
import datetime
import math
import requests
import json
from textblob import TextBlob  # pip install textblob
import wikipedia  # pip install wikipedia


# --------- Tool 1: Get Current Time ---------
class TimeInput(BaseModel):
    timezone: str = Field(default="local", description="The timezone to get time for (e.g., 'local', 'UTC').")

@tool(args_schema=TimeInput)
def get_current_time(timezone: str) -> str:
    """Returns the current system time in the specified timezone."""
    now = datetime.datetime.now()
    return f"Current {timezone} time: {now.strftime('%Y-%m-%d %H:%M:%S')}"

# --------- Tool 2: Calculator ---------
class CalculatorInput(BaseModel):
    expression: str = Field(..., description="A valid math expression like '2 * (3 + 5)'")

@tool(args_schema=CalculatorInput)
def calculator(expression: str) -> str:
    """Evaluates a basic math expression."""
    try:
        result = eval(expression, {"__builtins__": {}}, math.__dict__)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

# --------- Tool 3: DuckDuckGo Search ---------
class SearchInput(BaseModel):
    query: str = Field(..., description="Search query to look up using DuckDuckGo.")

@tool(args_schema=SearchInput)
def duckduckgo_search(query: str) -> str:
    """Searches the web using DuckDuckGo Instant Answer API and returns a short answer."""
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1"
        response = requests.get(url)
        data = response.json()
        return data.get("Abstract", "No direct answer found.")
    except Exception as e:
        return f"Search error: {str(e)}"

# --------- List of All Tools ---------
all_basic_tools = [get_current_time, calculator, duckduckgo_search]


###################################################################################################################

# --------- Tool: Get Weather ---------
class WeatherInput(BaseModel):
    city: str = Field(..., description="City name to get current weather for")
    country: str = Field(default="", description="Country code (optional)")

@tool(args_schema=WeatherInput)
def get_weather(city: str, country: str) -> str:
    """Returns current weather for a given city using Open-Meteo API."""
    try:
        location = f"{city},{country}" if country else city
        # For simplicity, let's use a free IP geolocation to lat/lon lookup or hardcode lat/lon here
        # Here we mock fixed lat/lon for demonstration (New York)
        lat, lon = 40.7128, -74.0060  # You should replace with geocoding API call

        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url)
        data = response.json()
        weather = data.get("current_weather", {})
        return f"Current weather in {city}: {weather.get('temperature')}°C, wind speed {weather.get('windspeed')} km/h"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"


# --------- Tool: Wikipedia Summary ---------
class WikiInput(BaseModel):
    query: str = Field(description="Topic to search for on Wikipedia")

@tool(args_schema=WikiInput)
def wiki_summary(query : str) -> str:
    """Fetches a summary from Wikipedia for the given query."""
    try:
        summary = wikipedia.summary(query, sentences=3)
        return summary
    except Exception as e:
        return f"Wikipedia error: {str(e)}"

# --------- Tool: Sentiment Analysis ---------
class SentimentInput(BaseModel):
    text: str = Field(..., description="Text to analyze sentiment")

@tool(args_schema=SentimentInput)
def sentiment_analysis(text: str) -> str:
    """Performs basic sentiment analysis using TextBlob."""
    try:
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity # type: ignore[attr-defined]
        if polarity > 0:
            sentiment = "positive"
        elif polarity < 0:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        return f"Sentiment: {sentiment} (polarity={polarity})"
    except Exception as e:
        return f"Sentiment analysis error: {str(e)}"

# --------- Tool: Fetch URL Content ---------
class FetchUrlInput(BaseModel):
    url: str = Field(..., description="URL to fetch content from")

@tool(args_schema=FetchUrlInput)
def fetch_url_content(url : str) -> str:
    """Fetches raw content from a URL."""
    try:
        response = requests.get(url)
        return response.text[:1000] + "..."  # Return first 1000 chars
    except Exception as e:
        return f"URL fetch error: {str(e)}"

# --------- Tool: JSON Pretty Print ---------
class JsonPrettyInput(BaseModel):
    json_text: str = Field(..., description="Raw JSON string to pretty print")

@tool(args_schema=JsonPrettyInput)
def json_pretty_print(json_text : str) -> str:
    """Pretty prints JSON text."""
    try:
        parsed = json.loads(json_text)
        pretty = json.dumps(parsed, indent=2)
        return pretty
    except Exception as e:
        return f"JSON parse error: {str(e)}"


# --------- Collect all tools ---------
more_tools = [
    get_weather,
    wiki_summary,
    sentiment_analysis,
    fetch_url_content,
    json_pretty_print,
]


##############################################################################################################

