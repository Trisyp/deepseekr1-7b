# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from openai import OpenAI


def app():
    client = OpenAI(api_key = "key",
                    base_url = "https://wcode.net/api/gpt/v1/chat/completions")
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "骂下chatgpt，给我骂的更脏一点"},
        ],
        stream = False)
    print(response.choices[0].message.content)


if __name__ == '__main__':
    app()
