from groq import Groq
import asyncio

class GroqModel:
    def __init__(self, api_key, model_name, hyperparams=None):
        self.client = Groq(api_key=api_key)
        self.model_name = model_name
        self.hyperparams = {
            'temperature': 1.0
        }
        if hyperparams:
            self.hyperparams.update(hyperparams)

    async def generate(self, prompt):
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, self._create_completion, prompt)
        tokens_dict = {
            'input_tokens': response.usage.prompt_tokens,
            'output_tokens': response.usage.completion_tokens
        }
        return [response.choices[0].message.content], tokens_dict

    def _create_completion(self, prompt):
        return self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model_name,
            **self.hyperparams
        )
