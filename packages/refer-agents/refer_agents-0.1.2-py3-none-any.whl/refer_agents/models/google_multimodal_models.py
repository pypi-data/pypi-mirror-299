import google.generativeai as genai
import os
from PIL import Image

class GoogleMultimodalModel:
    def __init__(self, api_key, model_name, hyperparams=None):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.hyperparams = {
            'temperature': 1.0
        }
        if hyperparams:
            self.hyperparams.update(hyperparams)

    def generate(self, prompt, image_path):
        response = self._create_completion(prompt, image_path)
        tokens_dict = {
            'input_tokens': len(prompt) // 4,
            'output_tokens': len(response.text) // 4
        }
        return [response.text], tokens_dict

    def _create_completion(self, prompt, image_path):
        if not self._is_valid_image(image_path):
            raise ValueError(f"The file at {image_path} is not a valid image.")
        
        image = genai.upload_file(path=image_path)
        # No hyperparams are accepted here as Gemini sometimes behaves weirdly with hyperparams
        return self.model.generate_content(
            [image, prompt]
        )

    def _is_valid_image(self, image_path):
        if not os.path.exists(image_path):
            return False
        try:
            with Image.open(image_path) as img:
                img.verify()
            return True
        except Exception:
            return False
