import openai
import json

import config


class ChatGptAPI:
    def __init__(self):
        self.model = "text-davinci-003"
        #self.model = "text-curie-001"
        self.token = config.CHATGPT_TOKEN
        self.options = {
            "max_tokens": 100,
            "temperature": 0.7
        }
        openai.api_key = self.token

    def generate_response(self, prompt: str):
        try:
            response = openai.Completion.create(
                model=self.model,
                prompt=prompt,
                temperature=self.options["temperature"],
                max_tokens=self.options["max_tokens"]
            )
        except Exception as e:
            raise ValueError(f"Failed to generate response. {e}")
        return response.choices[0].text
