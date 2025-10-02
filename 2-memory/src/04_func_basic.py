import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


def multiply(x: float, y: float) -> float:
    return x * y


multiply_definition = {
    "type": "function",
    "function": {
        "name": "multiply",
        "description": "Multiplies two numbers.",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {
                    "type": "number",
                    "description": "The first number to multiply.",
                },
                "y": {
                    "type": "number",
                    "description": "The second number to multiply.",
                },
            },
            "required": ["x", "y"],
        },
    },
}


def main():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "what is 12.34 * 56.78?"},
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        messages=messages,
        tools=[multiply_definition],
        tool_choice="auto",
    )
    answer = response.choices[0].message
    messages.append(answer)

    if answer.tool_calls:
        for tool in answer.tool_calls:
            function_name = tool.function.name
            function_args = json.loads(tool.function.arguments)

            if function_name == "multiply":
                x = function_args["x"]
                y = function_args["y"]
                result = multiply(x, y)
                messages.append(
                    {
                        "role": "tool",
                        "content": str(result),
                        "tool_call_id": tool.id,
                    }
                )

        response = client.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=messages,
            tools=[multiply_definition],
            tool_choice="auto",
        )
        answer = response.choices[0].message
        print(answer.content)


if __name__ == "__main__":
    main()
