from openrouter.components import ChatResult

from cascadia.main import loop


def chat_result_with_message(message: dict) -> ChatResult:
    finish_reason = "tool_calls" if message.get("tool_calls") else "stop"
    return ChatResult.model_validate(
        {
            "id": "scripted",
            "object": "chat.completion",
            "created": 0,
            "model": "scripted-model",
            "system_fingerprint": None,
            "choices": [
                {"index": 0, "finish_reason": finish_reason, "message": message}
            ],
        }
    )


def make_scripted_model(scripted_replies: list[dict]):
    received_calls = list()
    remaining_replies = iter(scripted_replies)

    def call_model(*, model, messages, tools):
        received_calls.append(
            {
                "model": model,
                "messages": messages,
                "tools": tools,
            }
        )
        return next(remaining_replies)

    return call_model, received_calls


def test_loop_one_round_without_tools():
    scripted_replies = [
        chat_result_with_message(
            {"role": "assistant", "content": "Hello, how can I assist you?"}
        )
    ]
    call_model, received_calls = make_scripted_model(scripted_replies=scripted_replies)

    input_params = {
        "call_model": call_model,
        "model_name": "test-model",
        "maximum_budget": 5,
        "messages": [
            {"role": "user", "content": "Hi! How is it going today?"},
        ],
        "tools": [],
    }

    messages, result = loop(input_params)

    assert len(messages) == 2
    assert result == "Hello, how can I assist you?"
    assert len(received_calls) == 1
