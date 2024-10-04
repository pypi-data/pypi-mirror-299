TEMPLATE = """
You are tasked with creating a clear and concise prompt for a task based on the provided instructions and examples. The prompt should be written in such a way that it can be easilyunderstood and followed by another LLM or human user performing the task. 
Your prompt should include the following:

• A brief overview of the task.
• Clear instructions for how to approach the task.
• A mention of any evaluation/task criteria.
• Example format or structure for completing the task. (Create a placeholder for user input like {{user_input}}.)
and give a response format in which the model should respond(Just give the format, NO placeholders needed for what is to be given in the response. Example Response Format can be like: Analysis: Give the analysis for your response and then on next line give the score for the task starting with "Score: " and just give the score)
Do not give any of the example or example format again, except for the output format needed.

Task Instructions:

{{user_prompt}}

Examples for Task:

{{examples}}

"""