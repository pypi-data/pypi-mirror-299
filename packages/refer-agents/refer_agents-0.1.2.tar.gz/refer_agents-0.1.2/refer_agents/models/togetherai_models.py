# refer/models/togetherai_model.py
from together import Together
import asyncio

class TogetherAIModel:
    def __init__(self, api_key, model_name, hyperparams=None):
        self.client = Together(api_key=api_key)
        self.model_name = model_name
        self.hyperparams = {
            'temperature': 1.0,
            'top_p': 1.0,
            'stop': None
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
        return [choice.message.content for choice in response.choices], tokens_dict

    def _create_completion(self, prompt):
        return self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            **self.hyperparams
        )