import random

from cascadia.openrouter_client import make_client


def call_weather_forcast_tool(tool_call):
    """Call the weather forecast tool with the given tool call."""
    # This is a placeholder implementation. Replace it with actual logic to call the tool.
    return {"forecast": "sunny" if random.choice([True, False]) else "cloudy",
            "temperature": "25°C" if random.choice([True, False]) else "15°C"}


def next_message(agent_state: list[dict]) -> list[dict]:
    """Return the next message to send to the model, given the agent's state."""
    assistant_messages = [agent_state[-1]["choices"][0]["message"]]
    for tool_call in assistant_messages[0].get("tool_calls", []):
        result = call_weather_forcast_tool(tool_call)
        assistant_messages.append({
            "role": "tool",
            "tool_call_id": tool_call["id"],
            "content": result,
        })

    return assistant_messages


def main():
    maximum_budget = 5
    budget = 0
    all_responses = list()
    messages = [{
        "role": "user",
        "content": "What is the weather today?",
    }]
    while budget < maximum_budget:
        with make_client() as router:
            response = router.chat.send(
                model="apodex/apodex-1.1-mini:free",
                messages=messages,
            )
            all_responses.append(response.model_dump())
            budget += 1
            messages += next_message(agent_state=all_responses)

    print(messages)


if __name__ == "__main__":
    main()
