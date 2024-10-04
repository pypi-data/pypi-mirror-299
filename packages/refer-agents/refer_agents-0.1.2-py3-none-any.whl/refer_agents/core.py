# refer/core.py
import asyncio
import json
import re
from tqdm import tqdm
import concurrent.futures
import time
from .models.openai_models import OpenAIModel
from .models.mistral_models import MistralModel
from .models.togetherai_models import TogetherAIModel
from .models.google_models import GoogleModel
from .models.groq_models import GroqModel
from .utils.logger import get_logger
from refer_agents.prompts.autoprompt_template import TEMPLATE
import logging
import os
from typing import List, Dict, Any, Optional, Tuple
from .models.openai_multimodal_models import OpenAIMultimodalModel
from .models.google_multimodal_models import GoogleMultimodalModel

class ReFeR:
    """
    ReFeR is a framework for evaluating and refining responses using a peer review mechanism.
    It allows for setting up multiple peer models and AC (Area Chair) models, with options to 
    set prompts, hyperparameters, and control over the number of peers and ACs.
    """
    def __init__(self, log_level: str = 'WARNING') -> None:
        self.api_keys = {}
        self.peers = []
        self.ac_models = []
        self.peer_prompt = ""
        self.peer_examples = []
        self.hyperparams = {}
        self.regex_pattern = None
        self.processing_function = None
        self.num_peers = 1
        self.num_acs = 1
        self.n_responses = 1
        self.ac_mode = 'Lite'  
        self.default_hyperparams = {
            'temperature': 1.0
        }
        self.max_threads = 2  # Default number of threads
        self.set_log_level(log_level)

    def set_log_level(self, level: str) -> None:
        """Set the logging level for the ReFeR instance.

        Args:
            level (str): The logging level to set. Choose from 'INFO', 'WARNING', or 'ERROR'.
        
        Raises:
            ValueError: If the provided level is not one of the allowed values.
        """
        level = level.upper()
        if level not in ['INFO', 'WARNING', 'ERROR']:
            raise ValueError("Invalid log level. Choose 'INFO', 'WARNING', or 'ERROR'.")
        
        log_level = getattr(logging, level)
        self.logger = get_logger(log_level)
        self.logger.setLevel(log_level)
        self.logger.info(f"Log level set to {level}")

    def set_api_key(self, platform: str, api_key: str) -> None:
        """Set the API key for a specific platform.

        Args:
            platform (str): The platform to set the API key for.
            api_key (str): The API key to set.
        """
        self.api_keys[platform.lower()] = api_key
        self.logger.info(f"API key set for {platform}")

    def add_peer(self, model_name: str, platform: str) -> None:
        """Add a peer model to the list of peers.

        Args:
            model_name (str): The name of the peer model according to the platform's API.
            platform (str): The platform of the peer model.
        """
        if len(self.peers) < self.num_peers:
            self.peers.append({'model_name': model_name, 'platform': platform.lower()})
            self.logger.info(f"Added peer model: {model_name} ({platform})")
        else:
            self.logger.error(f"Cannot add more peer models. Maximum number of peers ({self.num_peers}) reached.")
            raise ValueError(f"Cannot add more peer models. Maximum number of peers ({self.num_peers}) reached.")

    def set_num_peers(self, num_peers: int) -> None:
        """Set the number of peers.

        Args:
            num_peers (int): The number of peers to set.
        
        Raises:
            ValueError: If the provided number of peers is less than 1.
        """
        if num_peers >= 1:
            self.num_peers = num_peers
            self.peers = []  # Reset peers list
            self.logger.info(f"Number of peers set to {num_peers}")
        else:
            self.logger.error("Minimum number of peers is 1")
            raise ValueError("Minimum number of peers is 1")

    def set_num_acs(self, num_acs: int) -> None:
        """Set the number of ACs.

        Args:
            num_acs (int): The number of ACs to set.
        
        Raises:
            ValueError: If the provided number of ACs is less than 1.
        """
        if num_acs >= 1:
            self.num_acs = num_acs
            self.ac_models = []  # Reset AC models list
            self.logger.info(f"Number of ACs set to {num_acs}")
        else:
            self.logger.error("Minimum number of ACs is 1")
            raise ValueError("Minimum number of ACs is 1")

    def set_ac_mode(self, mode: str, n_responses: int = None) -> None:
        """Set the AC mode and number of responses for Turbo mode.

        Args:
            mode (str): The AC mode to set. Choose from 'Turbo' or 'Lite'.
            n_responses (int, optional): The number of responses to generate in Turbo mode. Default is 20 for Turbo mode, 1 for Lite mode.
        
        Raises:
            ValueError: If the provided AC mode is not one of the allowed values.
        """
        if mode in ['Turbo', 'Lite']:
            self.ac_mode = mode
            if mode == 'Turbo':
                self.n_responses = 20 if n_responses is None else n_responses
                self.logger.info(f"AC mode set to {mode} with {self.n_responses} responses")
            else:
                self.n_responses = 1
                self.logger.info(f"AC mode set to {mode}")
        else:
            self.logger.error("Invalid AC mode. Choose 'Turbo' or 'Lite'.")
            raise ValueError("Invalid AC mode. Choose 'Turbo' or 'Lite'.")

    def set_ac_model(self, model_name: str, platform: str) -> None:
        """Set the AC model.

        Args:
            model_name (str): The name of the AC model according to the platform's API.
            platform (str): The platform of the AC model.
        """
        if len(self.ac_models) < self.num_acs:
            self.ac_models.append({'model_name': model_name, 'platform': platform.lower()})
            self.logger.info(f"Set AC model: {model_name} ({platform})")
        else:
            self.logger.error(f"Cannot add more AC models. Maximum number of ACs ({self.num_acs}) reached.")
            raise ValueError(f"Cannot add more AC models. Maximum number of ACs ({self.num_acs}) reached.")

    def set_peer_prompt(self, prompt: str, examples: Optional[List[str]] = None) -> None:
        """Set the peer prompt.

        Args:
            prompt (str): The peer prompt to set.
            examples (Optional[List[str]]): The examples to set.
        """
        self.peer_prompt = prompt
        self.peer_examples = examples or []
        self.logger.info("Peer prompt set")

    def set_hyperparameters(self, **kwargs: Any) -> None:
        """Set the hyperparameters.

        Args:
            **kwargs (Any): The hyperparameters to set.
        """
        self.hyperparams.update(kwargs)
        self.logger.info("Hyperparameters updated")

    def set_regex_pattern(self, pattern: str) -> None:
        """Set the regex pattern.

        Args:
            pattern (str): The regex pattern to set.
        """
        if self.processing_function:
            self.logger.warning("Custom processing function is already set. Regex pattern will be ignored.")
        else:
            self.regex_pattern = pattern
            self.logger.info("Regex pattern set")

    def set_peer_response_processing_function(self, func: callable) -> None:
        """Set a custom function to process peer responses before passing to AC.

        Args:
            func (callable): The custom function to process peer responses.
        """
        if callable(func):
            self.processing_function = func
            self.regex_pattern = None  # Clear regex pattern if it was set
            self.logger.info("Custom processing function set. Regex pattern cleared if it was set.")
        else:
            self.logger.error("Invalid processing function. Must be callable.")
            raise ValueError("Invalid processing function. Must be callable.")

    def set_max_threads(self, max_threads: int) -> None:
        """Set the maximum number of threads to use for batch inference.

        Args:
            max_threads (int): The maximum number of threads to use.
        
        Raises:
            ValueError: If the provided maximum number of threads is less than 1.
        """
        if max_threads >= 1:
            self.max_threads = max_threads
            self.logger.info(f"Max threads set to {max_threads}")
        else:
            self.logger.error("Max threads must be at least 1")
            raise ValueError("Max threads must be at least 1")

    async def _call_model(self, model_info: Dict[str, str], prompt: str, n: int = 1) -> Tuple[List[str], Dict[str, int]]:
        """Call the specified model and return the responses.

        Args:
            model_info (Dict[str, str]): The model information containing platform and model name.
            prompt (str): The prompt to use for generating responses.
            n (int): The number of responses to generate (default is 1).
        
        Returns:
            List[str]: The generated responses.
        
        Raises:
            ValueError: If the platform is not supported.
        """
        platform = model_info['platform']
        model_name = model_info['model_name']
        api_key = self.api_keys.get(platform)
        if not api_key:
            raise ValueError(f"API key for {platform} is not set.")

        # Merge default hyperparameters with user-specified ones
        hyperparams = {**self.default_hyperparams, **self.hyperparams}

        if platform == 'openai':
            model = OpenAIModel(api_key, model_name, hyperparams)
        elif platform == 'mistral':
            model = MistralModel(api_key, model_name, hyperparams)
        elif platform == 'togetherai':
            model = TogetherAIModel(api_key, model_name, hyperparams)
        elif platform == 'google':
            model = GoogleModel(api_key, model_name, hyperparams)
        elif platform == 'groq':
            model = GroqModel(api_key, model_name, hyperparams)
        else:
            raise ValueError(f"Unsupported platform: {platform}")
        
        if platform == 'openai':
            responses, tokens = await model.generate(prompt, n)
        else:
            responses, tokens = await model.generate(prompt)

        return responses, tokens

    def _apply_regex(self, text: str) -> str:
        """Apply the regex pattern to the text.

        Args:
            text (str): The text to apply the regex pattern to.
        
        Returns:
            str: The processed text.
        """
        if self.regex_pattern:
            match = re.search(self.regex_pattern, text)
            if match:
                return match.group(0)
        return text

    def _process_response(self, response: str) -> str:
        """Apply either custom processing function or regex, whichever is available.

        Args:
            response (str): The response to process.
        
        Returns:
            str: The processed response.
        """
        if self.processing_function:
            try:
                return self.processing_function(response)
            except Exception as e:
                self.logger.error(f"Error applying custom processing function: {str(e)}. Using original response.")
                return response
        elif self.regex_pattern:
            return self._apply_regex(response)
        return response

    def generate_optimized_prompts(self) -> Tuple[str, str]:
        """Generate optimized prompts for peer and AC models.

        Returns:
            Tuple[str, str]: The optimized peer prompt and AC prompt.
        """
        self.logger.info("Generating optimized peer and AC prompts using Autoprompt")
        try:
            autoprompt_ac_model_info = self.ac_models[0]  # Use first AC model for autoprompt
        except IndexError:
            raise ValueError("AC models are not set. Please set AC models before generating optimized prompts, since we create the optimized prompt using the AC model.")

        # Load peer autoprompt template from file
        peer_autoprompt_template = TEMPLATE

        # Prepare peer autoprompt
        peer_autoprompt = peer_autoprompt_template.replace('{{user_prompt}}', self.peer_prompt)
        peer_autoprompt = peer_autoprompt.replace('{{examples}}', '\n'.join(self.peer_examples))

        # Generate optimized peer prompt using AC model
        optimized_peer_prompt_list, tokens_list = asyncio.run(self._call_model(autoprompt_ac_model_info, peer_autoprompt, n=1))
        optimized_peer_prompt = optimized_peer_prompt_list[0]

        # Ensure {{user_input}} placeholder is present in the peer prompt
        if '{{user_input}}' not in optimized_peer_prompt:
            optimized_peer_prompt += "\n\nInput: {{user_input}}"

        # Prepare AC prompt
        optimized_ac_prompt = f"""Alongside your evaluation, you will also receive initial evaluations from {len(self.peers)} large language models, referred to as the assistants' evaluations. Please read the instructions and criteria below carefully and use them as a guide in your evaluation, critically assessing the user input, and the assistants' inputs.\n\n"""
        optimized_ac_prompt += optimized_peer_prompt

        # Ensure {{user_input}} and {{peer_responses}} placeholders are present in the AC prompt
        if '{{user_input}}' not in optimized_ac_prompt:
            optimized_ac_prompt += "\n\nInput: {{user_input}}"
        if '{{peer_responses}}' not in optimized_ac_prompt:
            optimized_ac_prompt += "\n\nAssistant Responses:\n{{peer_responses}}"

        return optimized_peer_prompt, optimized_ac_prompt

    def batch_infer(self, user_inputs: List[str], optimized_peer_prompt: str, optimized_ac_prompt: str, use_threading: bool = False, sleep_time: float = 0, output_file: Optional[str] = None, max_workers: Optional[int] = None, max_retries: int = 3, retry_delay: float = 3, calculate_tokens: bool = False) -> Optional[List[Dict[str, Any]]]:
        """Batch infer using the optimized prompts.

        Args:
            user_inputs (List[str]): The list of user inputs to process.
            optimized_peer_prompt (str): The optimized peer prompt.
            optimized_ac_prompt (str): The optimized AC prompt.
            use_threading (bool): Whether to use threading for batch inference (default is False).
            sleep_time (float): The sleep time between inferences (default is 0).
            output_file (Optional[str]): The output file to save the results (default is None).
            max_workers (Optional[int]): The maximum number of threads to use for batch inference (default is None).
            max_retries (int): The maximum number of retries for inference (default is 3).
            retry_delay (float): The delay between retries in seconds (default is 3).
        
        Returns:
            Optional[List[Dict[str, Any]]]: The list of results.
        """
        results = []
        errors = 0
        max_errors = len(user_inputs) // 4  # Allow up to 25% of inputs to fail before suggesting non-threaded approach

        # Ensure output file is JSON
        if output_file:
            file_name, file_extension = os.path.splitext(output_file)
            if file_extension.lower() != '.json':
                output_file = f"{file_name}.json"
                self.logger.warning(f"Output file extension changed to .json. New output file: {output_file}")
        intermediate_file = output_file.replace('.json', '_intermediate.json')
        if use_threading:
            if max_workers is None:
                max_workers = self.max_threads
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(asyncio.run, self.infer(input, optimized_peer_prompt, optimized_ac_prompt, sleep_time=sleep_time, max_retries=max_retries, retry_delay=retry_delay, calculate_tokens=calculate_tokens)) 
                           for input in user_inputs]
                for f in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing inputs"):
                    try:
                        temp = f.result()
                        results.append(temp)
                        with open(intermediate_file, 'a') as f:
                            json.dump(temp, f, indent=4)
                    except Exception as e:
                        self.logger.error(f"Error processing input: {str(e)}")
                        errors += 1
                        if errors > max_errors:
                            self.logger.warning("Too many errors encountered. Suggesting to use batch_infer without threading or increase sleep time between instances.")
                            return None
        else:
            for input in tqdm(user_inputs, desc="Processing inputs"):
                try:
                    result = asyncio.run(self.infer(input, optimized_peer_prompt, optimized_ac_prompt, sleep_time=sleep_time, max_retries=max_retries, retry_delay=retry_delay, calculate_tokens=calculate_tokens))
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"Error processing input: {str(e)}")
                    errors += 1
                    if errors > max_errors:
                        self.logger.warning("Too many errors encountered. Batch processing stopped. Consider increasing sleep time between instances.")
                        break

        self.logger.info(f"Batch processing completed. Successful: {len(results)}, Failed: {errors}")
        if errors > 0:
            self.logger.warning(f"Some inputs failed to process. {errors} out of {len(user_inputs)} inputs failed.")

        if output_file:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=4)
            if os.path.exists(intermediate_file):
                os.remove(intermediate_file)

        return results

    async def infer(self, user_input: str, peer_prompt: Optional[str] = None, ac_prompt: Optional[str] = None, max_retries: int = 3, retry_delay: float = 3, sleep_time: float = 0, calculate_tokens: bool = False) -> Dict[str, Any]:
        """Perform inference using the provided or optimized prompts.

        Args:
            user_input (str): The user input to process.
            peer_prompt (Optional[str]): Direct peer prompt to use. If None, uses optimized prompt.
            ac_prompt (Optional[str]): Direct AC prompt to use. If None, uses optimized prompt.
            max_retries (int): The maximum number of retries for inference (default is 3).
            retry_delay (float): The delay between retries in seconds (default is 3).
            sleep_time (float): The sleep time between inferences (default is 0).
            calculate_tokens (bool): Whether to calculate and return token usage (default is False).
        
        Returns:
            Dict[str, Any]: The inference result.
        """
        self.logger.info("Starting inference")

        for attempt in range(max_retries):
            try:
                # Use provided prompts or generate optimized ones
                if peer_prompt is None or ac_prompt is None:
                    optimized_peer_prompt, optimized_ac_prompt = self.generate_optimized_prompts()
                    peer_prompt = peer_prompt or optimized_peer_prompt
                    ac_prompt = ac_prompt or optimized_ac_prompt

                # Check for required placeholders in prompts
                required_placeholders = ['{{user_input}}']
                for placeholder in required_placeholders:
                    if placeholder not in peer_prompt:
                        raise ValueError(f"Peer prompt is missing required placeholder: {placeholder}")
                    if placeholder not in ac_prompt:
                        raise ValueError(f"AC prompt is missing required placeholder: {placeholder}")

                if '{{peer_responses}}' not in ac_prompt:
                    raise ValueError("AC prompt is missing required placeholder: {{peer_responses}} or {{user_input}}")

                # Replace user input in peer prompt
                peer_prompt = peer_prompt.replace('{{user_input}}', user_input)

                # Asynchronously call peer models
                self.logger.info("Calling peer models asynchronously")
                if not self.peers:
                    self.logger.error("No peers given. Please add at least one peer model before inference.")
                    return None

                peer_tasks = {f"peer_model_{i+1}_{peer['model_name']}": self._call_model(peer, peer_prompt)
                              for i, peer in enumerate(self.peers)}

                peer_responses = {}
                peer_tokens = {}
                for model_name, task in peer_tasks.items():
                    response, tokens = await task
                    peer_responses[model_name] = response[0]  # Assuming single response per peer
                    if calculate_tokens:
                        peer_tokens[f"{model_name}_tokens"] = tokens

                # Apply processing (custom function or regex)
                processed_peer_responses = {model: self._process_response(resp)
                                            for model, resp in peer_responses.items()}
                processed_responses_lst = list(processed_peer_responses.values())

                # Prepare AC input
                peer_responses_formatted = []
                for i, response in enumerate(processed_responses_lst, start=1):
                    ordinal = self._ordinal_suffix(i).capitalize()
                    peer_responses_formatted.append(f"{ordinal} Assistant's Evaluation: {response}")
                
                ac_input = ac_prompt.replace('{{peer_responses}}', '\n'.join(peer_responses_formatted))
                ac_input = ac_input.replace('{{user_input}}', user_input)

                # Call AC models
                self.logger.info("Calling AC models")
                ac_responses = {}
                ac_tokens = {}
                for i, ac_model in enumerate(self.ac_models):
                    if self.ac_mode == 'Turbo' and ac_model['platform'].lower() != 'openai':
                        self.logger.warning(f"Turbo mode is only supported for OpenAI models. The current {ac_model['platform']} AC model will be used in Lite mode.")
                    
                    model_key = f"ac_model_{i+1}_{ac_model['model_name']}"
                    responses, tokens = await self._call_model(ac_model, ac_input, n=self.n_responses)
                    ac_responses[model_key] = responses
                    if calculate_tokens:
                        ac_tokens[f"{model_key}_tokens"] = tokens

                # Prepare the final output
                result = {
                    'user_input': user_input,
                    'peer_prompt': peer_prompt,
                    'ac_prompt': ac_input,
                }
                result.update(peer_responses)
                result.update(ac_responses)
                if calculate_tokens:
                    result.update(peer_tokens)
                    result.update(ac_tokens)

                await asyncio.sleep(sleep_time)  # Sleep after successful inference
                return result

            except ValueError as ve:
                # Catch and re-raise ValueError for missing placeholders
                self.logger.error(f"Prompt error: {str(ve)}")
                raise

            except Exception as e:
                if "rate limit" in str(e).lower() or "token limit" in str(e).lower():
                    if attempt < max_retries - 1:
                        self.logger.warning(f"Rate limit or token limit hit. Retrying in {retry_delay} seconds...")
                        await asyncio.sleep(retry_delay)
                    else:
                        self.logger.error(f"Max retries reached. Error: {str(e)}")
                        raise
                else:
                    self.logger.error(f"Unexpected error: {str(e)}")
                    raise

    def _ordinal_suffix(self, n: int) -> str:
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return f"{n}{suffix}"

    def _call_multimodal_model(self, model_info: Dict[str, str], prompt: str, image_path: str) -> Tuple[str, Dict[str, int]]:
        """Call the specified multimodal model and return the response.

        Args:
            model_info (Dict[str, str]): The model information containing platform and model name.
            prompt (str): The prompt to use for generating responses.
            image_path (str): The path to the image file.
        
        Returns:
            Tuple[str, Dict[str, int]]: The generated response and token usage.
        
        Raises:
            ValueError: If the platform is not supported.
        """
        platform = model_info['platform']
        model_name = model_info['model_name']
        api_key = self.api_keys.get(platform)
        if not api_key:
            raise ValueError(f"API key for {platform} is not set.")

        # Merge default hyperparameters with user-specified ones
        hyperparams = {**self.default_hyperparams, **self.hyperparams}

        if platform == 'openai':
            model = OpenAIMultimodalModel(api_key, model_name, hyperparams)
        elif platform == 'google':
            model = GoogleMultimodalModel(api_key, model_name, hyperparams)
        else:
            raise ValueError(f"Unsupported multimodal platform: {platform}")
        
        response, tokens = model.generate(prompt, image_path)
        return response, tokens

    def infer_multimodal(self, user_input: str, image_path: str, peer_prompt: Optional[str] = None, ac_prompt: Optional[str] = None, max_retries: int = 3, retry_delay: float = 3, sleep_time: float = 0, calculate_tokens: bool = False) -> Dict[str, Any]:
        """Perform multimodal inference using the provided or optimized prompts.

        Args:
            user_input (str): The user input to process.
            image_path (str): The path to the image file.
            peer_prompt (Optional[str]): Direct peer prompt to use. If None, uses optimized prompt.
            ac_prompt (Optional[str]): Direct AC prompt to use. If None, uses optimized prompt.
            max_retries (int): The maximum number of retries for inference (default is 3).
            retry_delay (float): The delay between retries in seconds (default is 3).
            sleep_time (float): The sleep time between inferences (default is 0).
            calculate_tokens (bool): Whether to calculate and return token usage (default is False).
        
        Returns:
            Dict[str, Any]: The inference result.
        """
        self.logger.info("Starting multimodal inference")

        for attempt in range(max_retries):
            try:
                # Use provided prompts or generate optimized ones
                if peer_prompt is None or ac_prompt is None:
                    optimized_peer_prompt, optimized_ac_prompt = self.generate_optimized_prompts()
                    peer_prompt = peer_prompt or optimized_peer_prompt
                    ac_prompt = ac_prompt or optimized_ac_prompt

                # Check for required placeholders in prompts
                required_placeholders = ['{{user_input}}']
                for placeholder in required_placeholders:
                    if placeholder not in peer_prompt:
                        raise ValueError(f"Peer prompt is missing required placeholder: {placeholder}")
                    if placeholder not in ac_prompt:
                        raise ValueError(f"AC prompt is missing required placeholder: {placeholder}")

                if '{{peer_responses}}' not in ac_prompt:
                    raise ValueError("AC prompt is missing required placeholder: {{peer_responses}}")

                # Replace user input in peer prompt
                peer_prompt = peer_prompt.replace('{{user_input}}', user_input)

                # Call peer models
                self.logger.info("Calling multimodal peer models")
                if not self.peers:
                    self.logger.error("No peers given. Please add at least one peer model before inference.")
                    return None

                peer_responses = {}
                peer_tokens = {}
                for i, peer in enumerate(self.peers):
                    model_name = f"peer_model_{i+1}_{peer['model_name']}"
                    response, tokens = self._call_multimodal_model(peer, peer_prompt, image_path)
                    peer_responses[model_name] = response
                    if calculate_tokens:
                        peer_tokens[f"{model_name}_tokens"] = tokens

                # Apply processing (custom function or regex)
                processed_peer_responses = {model: self._process_response(resp)
                                            for model, resp in peer_responses.items()}
                processed_responses_lst = list(processed_peer_responses.values())

                # Prepare AC input
                peer_responses_formatted = []
                for i, response in enumerate(processed_responses_lst, start=1):
                    ordinal = self._ordinal_suffix(i).capitalize()
                    peer_responses_formatted.append(f"{ordinal} Assistant's Evaluation: {response}")
                
                ac_input = ac_prompt.replace('{{peer_responses}}', '\n'.join(peer_responses_formatted))
                ac_input = ac_input.replace('{{user_input}}', user_input)

                # Call AC models
                self.logger.info("Calling AC models")
                ac_responses = {}
                ac_tokens = {}
                for i, ac_model in enumerate(self.ac_models):
                    model_key = f"ac_model_{i+1}_{ac_model['model_name']}"
                    response, tokens = self._call_multimodal_model(ac_model, ac_input, image_path)
                    ac_responses[model_key] = response
                    if calculate_tokens:
                        ac_tokens[f"{model_key}_tokens"] = tokens

                # Prepare the final output
                result = {
                    'user_input': user_input,
                    'image_path': image_path,
                    'peer_prompt': peer_prompt,
                    'ac_prompt': ac_input,
                }
                result.update(peer_responses)
                result.update(ac_responses)
                if calculate_tokens:
                    result.update(peer_tokens)
                    result.update(ac_tokens)

                time.sleep(sleep_time)  # Sleep after successful inference
                return result

            except Exception as e:
                if "rate limit" in str(e).lower() or "token limit" in str(e).lower():
                    if attempt < max_retries - 1:
                        self.logger.warning(f"Rate limit or token limit hit. Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                    else:
                        self.logger.error(f"Max retries reached. Error: {str(e)}")
                        raise
                else:
                    self.logger.error(f"Unexpected error: {str(e)}")
                    raise

    def batch_infer_multimodal(self, user_inputs: List[str], image_paths: List[str], optimized_peer_prompt: str, optimized_ac_prompt: str, sleep_time: float = 0, output_file: Optional[str] = None, max_retries: int = 3, retry_delay: float = 5, calculate_tokens: bool = False) -> Optional[List[Dict[str, Any]]]:
        """Batch infer using the optimized prompts for multimodal inputs.

        Args:
            user_inputs (List[str]): The list of user inputs to process.
            image_paths (List[str]): The list of image paths corresponding to user inputs.
            optimized_peer_prompt (str): The optimized peer prompt.
            optimized_ac_prompt (str): The optimized AC prompt.
            sleep_time (float): The sleep time between inferences (default is 0).
            output_file (Optional[str]): The output file to save the results (default is None).
            max_retries (int): The maximum number of retries for inference (default is 3).
            retry_delay (float): The delay between retries in seconds (default is 3).
            calculate_tokens (bool): Whether to calculate and return token usage (default is False).
        
        Returns:
            Optional[List[Dict[str, Any]]]: The list of results.
        """
        if len(user_inputs) != len(image_paths):
            raise ValueError("The number of user inputs must match the number of image paths.")

        results = []
        errors = 0
        max_errors = len(user_inputs) // 4  # Allow up to 25% of inputs to fail before stopping

        # Ensure output file is JSON
        if output_file:
            file_name, file_extension = os.path.splitext(output_file)
            if file_extension.lower() != '.json':
                output_file = f"{file_name}.json"
                self.logger.warning(f"Output file extension changed to .json. New output file: {output_file}")
        intermediate_file = output_file.replace('.json', '_intermediate.json') if output_file else None

        for input, image_path in tqdm(zip(user_inputs, image_paths), total=len(user_inputs), desc="Processing inputs"):
            try:
                result = self.infer_multimodal(input, image_path, optimized_peer_prompt, optimized_ac_prompt, sleep_time=sleep_time, max_retries=max_retries, retry_delay=retry_delay, calculate_tokens=calculate_tokens)
                results.append(result)
                if intermediate_file:
                    with open(intermediate_file, 'a') as f:
                        json.dump(result, f, indent=4)
                        f.write('\n')
            except Exception as e:
                self.logger.error(f"Error processing input: {str(e)}")
                errors += 1
                if errors > max_errors:
                    self.logger.warning("Too many errors encountered. Batch processing stopped.")
                    break

        self.logger.info(f"Batch processing completed. Successful: {len(results)}, Failed: {errors}")
        if errors > 0:
            self.logger.warning(f"Some inputs failed to process. {errors} out of {len(user_inputs)} inputs failed.")

        if output_file:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=4)
            if os.path.exists(intermediate_file):
                os.remove(intermediate_file)

        return results