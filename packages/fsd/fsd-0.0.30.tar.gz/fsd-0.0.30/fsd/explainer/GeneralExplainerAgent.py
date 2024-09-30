import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class GeneralExplainerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_normal_answer_plan(self, user_prompt, language):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            user_prompt (str): The user's prompt.
            language (str): The language in which the response should be given.

        Returns:
            dict: The development plan or error reason.
        """
        logger.info("\n ### The `GeneralExplainerAgent` is preparing to generate a response plan")
        messages = [
            {
                "role": "system",
                "content": (
                    "Your name is Zinley, an on-device software engineer.\n\n"
                    "You need to reply to the user prompt and respond in the provided request language.\n\n"
                )
            },
            {
                "role": "user",
                "content": (
                    f"User prompt:\n{user_prompt}\n\n"
                    f"You must respond in this language:\n{language}\n\n"
                )
            }
        ]

        try:
            logger.info("\n ### The `GeneralExplainerAgent` is initiating AI stream prompt for response generation")
            response = await self.ai.stream_prompt(messages, self.max_tokens, 0.2, 0.1)
            logger.info("\n ### The `GeneralExplainerAgent` has successfully received AI response")
            return ""
        except Exception as e:
            logger.info(f"\n ### The `GeneralExplainerAgent` encountered an error during response generation: `{str(e)}`")
            return {
                "reason": str(e)
            }


    async def get_normal_answer_plans(self, user_prompt, language):
        logger.info("\n ### The `GeneralExplainerAgent` is commencing the process of obtaining normal answer plans")
        plan = await self.get_normal_answer_plan(user_prompt, language)
        logger.info("\n ### The `GeneralExplainerAgent` has successfully retrieved the normal answer plan")
        return plan
