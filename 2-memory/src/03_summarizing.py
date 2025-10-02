from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


def main():
    messages = []

    while True:
        user_input = input("User: ")

        # summarizing sliding window
        if len(messages) > 5:
            summary_messages = [
                {
                    "role": "system",
                    "content": "You are conversational summarizer, Please summarize this context and provide cncise summarize for future reference",
                },
                *messages,
                {
                    "role": "user",
                    "content": "Please summarize the above conversation in concise manner",
                },
            ]
            summary_response = client.chat.completions.create(
                model="gpt-4.1-nano-2025-04-14",
                messages=summary_messages,
            )
            summary = summary_response.choices[0].message
            messages = [
                {
                    "role": "system",
                    "content": f"You are a helpful assistant. Here is the summary of previous conversation: {summary.content}",
                }
            ] + messages[-5:]

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
