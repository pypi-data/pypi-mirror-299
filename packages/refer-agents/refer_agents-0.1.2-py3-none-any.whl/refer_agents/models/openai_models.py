# refer/models/openai_model.py
import openai
import asyncio

class OpenAIModel:
    def __init__(self, api_key, model_name, hyperparams=None):
        self.client = openai.OpenAI(api_key=api_key)
        self.model_name = model_name
        self.hyperparams = {
            'temperature': 1,
            'top_p': 1,
            'frequency_penalty': 0,
            'presence_penalty': 0,
            'stop': None
        }
        if hyperparams:
            self.hyperparams.update(hyperparams)

    async def generate(self, prompt, n=1):
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, self._create_completion, prompt, n)
        all_responses = [response.choices[i].message.content for i in range(len(response.choices))]
        tokens_dict = {
            'input_tokens': response.usage.prompt_tokens,
            'output_tokens': response.usage.completion_tokens
        }
        return all_responses, tokens_dict

    def _create_completion(self, prompt, n=1):
        return self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            n=n,
            **self.hyperparams
        )