import os
import aiohttp
import asyncio
import json
import sys

from json_repair import repair_json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class CompilePrePromptAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_prePrompt_plan(self, user_prompt):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        logger.info("\n ### The `CompilePrePromptAgent` is initiating the process to generate a pre-prompt plan")
        all_file_contents = self.repo.print_tree()
        messages = [
            {
                "role": "system",
                "content": (
                    "You're an expert in project compilation and local development. Analyze the files and prompt, then respond in JSON format:\n\n"
                    "compile_plan: Refine the user's prompt, focusing on local setup and execution. Translate if needed. Enhance with project-specific insights. NO YAPPING OR UNNECESSARY EXPLANATIONS.\n"
                    "pipeline: Choose the best action (0, 1, or 2):\n"
                    "0. No setup needed (empty project or no executable code)\n"
                    "1. CLI setup possible (e.g., npm start, python manage.py runserver)\n"
                    "Respond in this JSON structure:\n"
                    "{\n"
                    '    "compile_plan": "Enhanced directive focusing on local setup",\n'
                    '    "pipeline": "0, 1"\n'
                    "}\n"
                    "Provide only valid JSON, no extra text. Prioritize local development unless deployment is explicitly requested. STRICTLY ENFORCE no yapping in the response."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Project structure:\n{all_file_contents}\n\n"
                    f"User directive:\n{user_prompt}\n"
                )
            }
        ]

        try:
            logger.info("\n ### The `CompilePrePromptAgent` is sending a request to the AI for plan generation")
            response = await self.ai.prompt(messages, self.max_tokens, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            logger.info("\n ### The `CompilePrePromptAgent` has successfully received and parsed the AI response")
            return res
        except json.JSONDecodeError:
            logger.info("\n ### The `CompilePrePromptAgent` encountered a JSON decoding error and is attempting to repair the response")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.info("\n ### The `CompilePrePromptAgent` has successfully repaired and parsed the JSON response")
            return plan_json
        except Exception as e:
            logger.info(f"\n ### The `CompilePrePromptAgent` encountered an error during plan generation: {e}")
            return {
                "reason": str(e)
            }

    async def get_prePrompt_plans(self, user_prompt):
        logger.info("\n ### The `CompilePrePromptAgent` is beginning the process to retrieve pre-prompt plans")
        plan = await self.get_prePrompt_plan(user_prompt)
        logger.info("\n ### The `CompilePrePromptAgent` has successfully completed retrieving pre-prompt plans")
        return plan
