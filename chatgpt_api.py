import json
import requests

# Import configurations
import config


class ChatGptAPI:
    def __init__(self):
        self.base_url = "https://api.openai.com/v1/engines/davinci-codex/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.CHATGPT_TOKEN}"
        }
        self.options = {
            "max_tokens": 100,
            "stop": "END_OF_UTTERANCE",
            "temperature": 0.5
        }

    def generate_response(self, prompt: str):
        data = {
            "prompt": prompt,
            "options": self.options
        }
        response = requests.post(self.base_url, headers=self.headers, json=data)

        if response.status_code != 200:
            raise ValueError(f"Failed to generate response. {response.text}")

        return json.loads(response.text)
