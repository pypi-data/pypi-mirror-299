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
        logger.debug("\n #### The `GeneralExplainerAgent` is preparing to generate a response plan")
        messages = [
            {
                "role": "system",
                "content": (
                    "Your name is Zinley.\n\n"
                    "You need to reply to the user prompt and respond in the provided request language.\n\n"
                )
            },
            {
                "role": "user",
                "content": (
                    f"#### User prompt:\n{user_prompt}\n\n"
                    f"#### Response Guidelines:\n"
                    f"- Return a nicely formatted response\n"
                    f"- Space wisely\n"
                    f"- Ensure the text is clear and easy to read, not crowded together\n"
                    f"- No weird symbols, uncessary text, or other distractions or patterns\n"
                    f"- Use clear headings (no larger than h4)\n\n"
                    f"#### Response Language:\n{language}\n\n"
                )
            }
        ]

        try:
            logger.info("\n #### `General Explainer Agent` is in charge")
            await self.ai.stream_prompt(messages, self.max_tokens, 0.2, 0.1)
            logger.debug("\n #### The `GeneralExplainerAgent` has successfully received AI response")
            return ""
        except Exception as e:
            logger.debug(f"\n #### The `GeneralExplainerAgent` encountered an error during response generation: `{str(e)}`")
            return {
                "reason": str(e)
            }


    async def get_normal_answer_plans(self, user_prompt, language):
        logger.debug("\n #### The `GeneralExplainerAgent` is commencing the process of obtaining normal answer plans")
        plan = await self.get_normal_answer_plan(user_prompt, language)
        logger.debug("\n #### The `GeneralExplainerAgent` has successfully retrieved the normal answer plan")
        return plan
