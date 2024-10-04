import google.generativeai as genai
import asyncio

class GoogleModel:
    def __init__(self, api_key, model_name, hyperparams=None):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.hyperparams = {
            'temperature': 1.0
        }
        if hyperparams:
            self.hyperparams.update(hyperparams)

    async def generate(self, prompt):
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, self._create_completion, prompt)
        tokens_dict = {
            'input_tokens': len(prompt) // 4,
            'output_tokens': len(response.text) // 4
        }
        return [response.text], tokens_dict

    def _create_completion(self, prompt):
        return self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(**self.hyperparams)
        )
