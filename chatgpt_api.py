import json
import requests

# Import configurations
import config


class ChatGptAPI:
    def __init__(self):
        engine = "davinci"
        self.base_url = f"https://api.openai.com/v1/engines/{engine}/completions"
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
        try:
            response = requests.post(self.base_url, headers=self.headers, json=data)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if response.status_code == 401:
                raise ValueError("Failed to generate response. Invalid or expired token.")
            else:
                raise ValueError(f"Failed to generate response. {err}")
        except requests.exceptions.RequestException as err:
            raise ValueError(f"Failed to generate response. {err}")

        return json.loads(response.text)
