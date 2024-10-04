import openai
import base64
import requests

class OpenAIMultimodalModel:
    def __init__(self, api_key, model_name, hyperparams=None):
        self.api_key = api_key
        self.model_name = model_name
        self.hyperparams = {
            'temperature': 1,
            'top_p': 1,
            'frequency_penalty': 0,
            'presence_penalty': 0
        }
        if hyperparams:
            self.hyperparams.update(hyperparams)

    def generate(self, prompt, image_path, n=1):
        response = self._create_completion(prompt, image_path, n)
        all_responses = [response['choices'][i]['message']['content'] for i in range(len(response['choices']))]
        tokens_dict = {
            'input_tokens': response['usage']['prompt_tokens'],
            'output_tokens': response['usage']['completion_tokens']
        }
        return all_responses, tokens_dict

    def _create_completion(self, prompt, image_path, n=1):
        base64_image = self._encode_image(image_path)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "n": n,
            **self.hyperparams
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        return response.json()

    def _encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
