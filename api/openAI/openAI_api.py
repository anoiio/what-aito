import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class OpenAIClient:
    def __init__(self, api_key=None):
        # Use the provided API key or fall back to the environment variable
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def get_response(self, instructions, input_text, model='gpt-4o-mini', max_output_tokens=300):
        return self.client.responses.create(
            model=model,
            instructions=instructions,
            input=input_text,
            max_output_tokens=max_output_tokens
        )