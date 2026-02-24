from openai import OpenAI
from pydantic import BaseModel

import environ as env


def main():
    print("Hello from prompt chatgpt's API!")
    
    # a pathlib.Lab variable
    cwd = env.CURRENT_WORKING_DIRECTORY
    
# setup and test access
    client = OpenAI(api_key= env.OPENAI_API_KEY)
    print("OpenAI client created successfully!")
    print(f"Using API key: {client.api_key[:8]}...")
    print()
    
# send a basic text prompt
    text_response = client.responses.create(
        model="gpt-5",
        input="Tell me a joke about Python programming"
    )
    print(f"Joke:\n{text_response.output_text}")
    print()
    
# Control Behavior With Role-Based Messages
    user_input = input("How can I help you? ")
    # when this appears, ask a question for GPT to answer
    # e.g. how many key words does python have?

    code_response = client.responses.create(
        model="gpt-5",
        input=[
            {
                "role": "developer",
                "content": (
                    "You are a Python coding assistant. "
                    "Only accept Python-related questions."
                ),
            },
            {
                "role": "user",
                "content": f"{user_input}",
            },
        ],
    )
    print(f"\n{code_response.output_text}")
    print()
    
# Get Structured Outputs With Pydantic Models
    # Define a Pydantic Output Model
    class CodeOutput(BaseModel):
        function_name: str
        code: str
        explanation: str
        example_usage: str

    code_response = client.responses.parse(
        model="gpt-5",
        input=[
            {
                "role": "developer",
                "content": ("You are a coding assistant. Generate clean,"
                            "well-documented Python code."
                        )
            },
            {
                "role": "user",
                "content": "Write a simple Python function to add two numbers."
            }
        ],
        text_format=CodeOutput,
    )

    code_result = code_response.output_parsed

    print(f"Function Name: {code_result.function_name}")
    print("\nCode:")
    print(code_result.code)
    print(f"\nExplanation: {code_result.explanation}")
    print(f"\nExample Usage:\n{code_result.example_usage}")
    print()


if __name__ == "__main__":
    main()
