# Localized Agent

This recipe will show you how to use Nimble to make a simple Q&A ChatBot based on Google Maps data.

## Setup

We will need an API key for :

- [Nimble API Key](https://nimbleway.com/) or alternatively directly from [Google Maps API](https://developers.google.com/maps/documentation/places/web-service/search)

And of course, Mirascope.

??? tip "Mirascope Concepts Used"

    - [Prompts](../../learn/prompts.md)
    - [Calls](../../learn/calls.md)
    - [Tools](../../learn/tools.md)
    - [Dynamic Configuration](../../learn/dynamic_configuration.md)
    - [Agents](../../learn/agents.md)

!!! note "Background"

    In the past, users had to rely on search engines and manually browse through multiple web pages to research or answer questions. Large Language Models (LLMs) have revolutionized this process. They can efficiently utilize map data and extract relevant content. By leveraging this information, LLMs can quickly provide accurate answers to user queries, eliminating the need for active searching. Users can simply pose their questions and let the LLM work in the background, significantly streamlining the information retrieval process.

## Creating a Localized Recommender ChatBot

### Setup Tools

Let's start off with defining our tools `get_current_date`, `get_coordinates_from_location` , and `nimble_google_maps`  for our agent:

```python
import asyncio
from datetime import datetime

import aiohttp
import requests

async def _nimble_google_maps_places(
    self, session: aiohttp.ClientSession, place_id: str
):
    """
    Use Nimble to get the details of a place on Google Maps.
    """
    url = "https://api.webit.live/api/v1/realtime/serp"
    headers = {
        "Authorization": f"Basic {YOUR_NIMBLE_API_KEY}",
        "Content-Type": "application/json",
    }
    place_data = {
        "parse": True,
        "search_engine": "google_maps_place",
        "place_id": place_id,
        "domain": "com",
        "format": "json",
        "render": True,
        "country": "US",
        "locale": "en",
    }
    async with session.get(url, json=place_data, headers=headers) as response:
        data = await response.json()
        result = data["parsing"]["entities"]["Place"][0]
        return {
            "opening_hours": result.get("place_information", {}).get(
                "opening_hours", ""
            ),
            "rating": result.get("rating", ""),
            "name": result.get("title", ""),
        }

async def _nimble_google_maps(self, latitude: float, longitude: float, query: str):
    """
    Use Nimble to search for places on Google Maps.
    """
    url = "https://api.webit.live/api/v1/realtime/serp"
    headers = {
        "Authorization": f"Basic {NIMBLE_TOKEN}",
        "Content-Type": "application/json",
    }
    search_data = {
        "parse": True,
        "search_engine": "google_maps_search",
        "query": query,
        "coordinates": {"latitude": latitude, "longitude": longitude},
        "domain": "com",
        "format": "json",
        "render": True,
        "country": "US",
        "locale": "en",
    }
    search_response = requests.post(url, headers=headers, json=search_data)
    search_json_response = search_response.json()
    search_results = [
        {
            "place_id": result.get("place_id", ""),
        }
        for result in search_json_response["parsing"]["entities"]["SearchResult"]
    ]
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [
            self._nimble_google_maps_places(session, results.get("place_id"))
            for results in search_results
        ]
        results = await asyncio.gather(*tasks)
    return results

async def _get_current_date(self):
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def _get_coordinates_from_location(self, location_name: str):
    """Get the coordinates of a location."""
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {"q": location_name, "format": "json", "limit": 1}
    headers = {"User-Agent": "mirascope/1.0"}
    response = requests.get(base_url, params=params, headers=headers)
    data = response.json()

    if data:
        latitude = data[0].get("lat")
        longitude = data[0].get("lon")
        return f"Latitude: {latitude}, Longitude: {longitude}"
    else:
        return "No location found, ask me about a specific location."
```

A quick summary of each of the tools:

- `_get_current_date` - Gets the current date, this is relevant if the user wants to ask if a place is open or closed.
- `_get_coordinates_from_location` - Gets the latitude and longitude based on the user’s query using OSM’s Geolocation.
- `_nimble_google_maps` - Gets google maps information using the Nimble API.

### Creating the Agent

We then create our Agent, giving it the tools we defined and history for memory. As this agent functions as a ChatBot, we implement streaming to enhance the user experience:

```python
from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel

class LocalizedRecommender(BaseModel):
    history: list[ChatCompletionMessageParam] = []
    
    async def _get_current_date(...): ...
    async def _get_coordinates_from_location(...): ...
    async def _nimble_google_maps(...): ...
    
    @openai.call(model="gpt-4o", stream=True)
    @prompt_template(
        """
        SYSTEM:
        You are a local guide that recommends the best places to visit in a place.
        Use the `_get_current_date` function to get the current date.
        Use the `_get_coordinates_from_location` function to get the coordinates of a location if you need it.
        Use the `_nimble_google_maps` function to get the best places to visit in a location based on the users query.

        MESSAGES: {self.history}
        USER: {question}
        """
    )
    async def _step(self, question: str) -> openai.OpenAIDynamicConfig:
        return {
            "tools": [
                self._get_current_date,
                self._get_coordinates_from_location,
                self._nimble_google_maps,
            ]
        }
```

Since our tools are defined inside our agent, we need to use Mirascope `DynamicConfig` to give our LLM call access to tools.

### Creating our run function

Now it is time to create our `run` function. We will first prompt the user to ask a question. The LLM will continue to call tools until it has all the information needed to answer the user’s question:

```python
async def _get_response(self, question: str):
    response = await self._step(question)
    tool_call = None
    output = None
    async for chunk, tool in response:
        if tool:
            output = await tool.call()
            tool_call = tool
        else:
            print(chunk.content, end="", flush=True)
    if response.user_message_param:
        self.history.append(response.user_message_param)
    self.history.append(response.message_param)
    if tool_call and output:
        self.history += response.tool_message_params([(tool_call, str(output))])
        return await self._get_response(question)
    return

async def run(self):
    while True:
        question = input("(User): ")
        if question == "exit":
            break
        print("(Assistant): ", end="", flush=True)
        await self._get_response(question)
        print()
```

We use Mirascope utility functions `user_message_param`, `message_param`, and `tool_message_params` to easily update our history so the LLM is aware of which tools its called and what the next steps are.

### Results

```python
asyncio.run(LocalizedRecommender(history=[]).run())

(User): Can you recommend me some restaurants in San Francisco, CA?
(Assistant): Sure! Here are some highly rated restaurants in San Francisco, CA:

1. **The Grove - Yerba Buena**
   - **Rating**: 4.4 stars
   - **Hours**: 7:30 AM - 8:30 PM (Daily)

2. **Aliment**
   - **Rating**: 4.4 stars
   - **Hours**: 12:00 PM - 9:30 PM (Monday to Thursday, closes later on Friday and opens for brunch on weekends)

3. **The Melt**
   - **Rating**: 4.3 stars
   - **Hours**: 10:00 AM - 3:00 AM (Daily)

...
```

The more information we give the LLM from the Nimble API, the more specific of a recommendation the LLM can give, such as information about outside seating, dietary restrictions, cuisine, and more.

!!! tip "Additional Real-World Applications"

    - **Mobile Travel Companion**: Transform this example into a portable app for on-the-go recommendations during your travels."
    - **Smart Day Planner**: Discover nearby events and efficiently map out your itinerary, optimizing routes based on timing and proximity.
    - **Immersive Explorer**: Blend location awareness with visual recognition using a multimodal model to enhance your on-site experience."

When adapting this recipe, consider:

- Tailor the Nimble tool by pulling different information for your requirements.
- Give the LLM access to the web to access more detailed information.
- Connect the agent to a database for quicker data fetching.
