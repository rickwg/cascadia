import json
import random
from typing import Callable

from cascadia.openrouter_client import make_client


def call_add_two_numbers_tool(tool_call: dict) -> float:
    a = json.loads(tool_call["function"]["arguments"])["a"]
    b = json.loads(tool_call["function"]["arguments"])["b"]
    return a + b


def call_weather_forcast_tool(tool_call: dict):
    return {
        "forecast": "sunny" if random.choice([True, False]) else "cloudy",
        "temperature": "25°C" if random.choice([True, False]) else "15°C",
    }


def extract_tool_call_results(messages: list[dict]) -> list[dict]:
    output = list()
    for tool_call in messages[0].get("tool_calls", []):
        try:
            tool_function = TOOL_REGISTRY[tool_call["function"]["name"]]
            result = tool_function(tool_call)
        except Exception as e:
            result = {"error": f"Tool call failed: {str(e)}"}

        output.append(
            {
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.get("id"),
            }
        )
    return output


def next_message(agent_state: list[dict]) -> list[dict]:
    assistant_messages = [agent_state[-1]["choices"][0]["message"]]
    extraction_result = extract_tool_call_results(assistant_messages)
    return assistant_messages + extraction_result


def extract_last_message_content(all_responses: list[dict]) -> str:
    if not all_responses:
        return ""
    return all_responses[-1]["choices"][0]["message"]["content"]


def loop(input_params: dict) -> tuple[list[dict], str]:
    call_model = input_params["call_model"]
    model_name = input_params["model_name"]
    maximum_budget = input_params["maximum_budget"]
    messages = input_params["messages"]
    tools = input_params["tools"]

    budget = 0
    all_responses = list()
    result = "task completed because all budge was spent."
    while budget < maximum_budget:
        response = call_model(
            model=model_name,
            messages=messages,
            tools=tools,
        )
        budget += 1
        response_dict = response.model_dump()
        all_responses.append(response_dict)

        last_message = response_dict["choices"][0]["message"]
        messages += next_message(agent_state=all_responses)

        if not last_message.get("tool_calls"):
            result = last_message["content"]
            break

    return messages, result


def merge_user_messages(user_messages: list[dict]) -> dict:
    merged_content = " ".join([msg["content"] for msg in user_messages])
    return {"role": "user", "content": merged_content}


TOOL_REGISTRY = {
    "weather_forecast": call_weather_forcast_tool,
    "add_two_numbers": call_add_two_numbers_tool,
}

EXAMPLE_MESSAGES = [
    {
        "role": "user",
        "content": "What is the weather for Berlin today? "
        "You can use the weather forecast tool to get the information. "
        "In fact you should assume you can use the tool to get the information. "
        "If you got the temperature, only report the temperature and present the temperature in the format: Temperature: Number°C. ",
    },
    {
        "role": "user",
        "content": "Please add 5 and 10 using the add two numbers tool. "
        "You can use the add two numbers tool to get the information. "
        "In fact you should assume you can use the tool to get the information. "
        "If you got the result, only report the result and present the result in the format: Sum: Number. "
        "Example: Sum: 15. ",
    },
]


def main() -> None:
    maximum_budget = 10
    model_name = "apodex/apodex-1.1-mini:free"
    loop_input = {
        "call_model": None,
        "model_name": model_name,
        "maximum_budget": maximum_budget,
        "messages": [merge_user_messages(user_messages=EXAMPLE_MESSAGES)],
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "weather_forecast",
                    "description": "Get the weather forecast for a given location for today.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The location for which to get the weather forecast.",
                            }
                        },
                        "required": ["location"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "add_two_numbers",
                    "description": "Add two numbers together.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "a": {
                                "type": "number",
                                "description": "The first number to add.",
                            },
                            "b": {
                                "type": "number",
                                "description": "The second number to add.",
                            },
                        },
                        "required": ["a", "b"],
                    },
                },
            },
        ],
    }
    with make_client() as router:
        loop_input["call_model"] = router.chat.send
        responses, result = loop(input_params=loop_input)
    print(result)


if __name__ == "__main__":
    main()
