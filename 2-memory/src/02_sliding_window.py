from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


def main():
    messages = []

    while True:
        user_input = input("User: ")

        # sliding window
        if len(messages) > 5:
            messages = messages[-5:]  # keep last 5 messages

        messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=messages,
        )
        answer = response.choices[0].message
        messages.append(answer)
        print(answer.content)

        print("----" * 20)
        print(messages)
        print("----" * 20)


if __name__ == "__main__":
    main()
