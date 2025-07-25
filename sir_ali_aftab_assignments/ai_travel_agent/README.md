# AI Travel Designer Agent

## Overview

This project uses the OpenAI Agent SDK with a modular multi-agent design to help users plan a travel experience based on their mood or interests.

### Agents

- **DestinationAgent**: Suggests places to travel based on input.
- **BookingAgent**: Simulates travel booking using tools like flight/hotel suggestion.
- **ExploreAgent**: Recommends attractions and local foods.

### Tools

- **TravelInfoGenerator**: Provides mock flight suggestions.
- **HotelPicker**: Provides mock hotel suggestions.

### Flow

1. User gives mood/interests.
2. DestinationAgent suggests a place.
3. BookingAgent books a mock flight/hotel using tools.
4. ExploreAgent recommends attractions/food.

### Tech

- Chainlit UI
- OpenAI Agent SDK + Runner
- Gemini API key (configured in `.env`)
