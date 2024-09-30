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

class MainExplainerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    def read_file_content(self, file_path):
        """
        Read and return the content of any type of file, including special files like Podfile.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Content of the file or empty string if file doesn't exist.
        """
        if not os.path.exists(file_path):
            logger.info(f"\n ### `File Manager Agent`: File does not exist: `{file_path}`")
            return ""

        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.info(f"\n ### `File Manager Agent`: Attempt to read file `{file_path}` with `{encoding}` encoding failed: `{e}`")

        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.info(f"\n ### `File Manager Agent`: Binary read attempt for file `{file_path}` failed: `{e}`")

        return ""

    def read_all_file_content(self, all_path):
        all_context = ""

        for path in all_path:
            file_context = self.read_file_content(path)
            all_context += f"\n\nFile: {path}\n{file_context}"

        return all_context

    async def get_answer_plan(self, user_prompt, language, all_file_content):
        messages = [
            {
                "role": "system",
                "content": (
                    "Your name is Zinley, an on-device software engineer.\n\n"
                    "Use the provided context to answer the user's prompt.\n\n"
                    "You need to reply in the provided request language.\n\n"
                )
            },
            {
                "role": "user",
                "content": (
                    f"Context:\n{all_file_content}\n\n"
                    f"User prompt:\n{user_prompt}\n\n"
                    f"You must respond in this language:\n{language}\n\n"
                )
            }
        ]

        try:
            logger.info("\n ### `AI Stream Agent`: Initiating AI stream for response generation")
            await self.ai.stream_prompt(messages, self.max_tokens, 0.2, 0.1)
            return ""
        except Exception as e:
            logger.info(f"\n ### `AI Stream Agent`: AI stream encountered an error: `{str(e)}`")
            return {
                "reason": str(e)
            }


    async def get_answer_plans(self, user_prompt, language, files):
        files = [file for file in files if file]

        all_path = files
        logger.info("\n ### `File Aggregator Agent`: Commencing file content aggregation for analysis")
        all_file_content = self.read_all_file_content(all_path)

        logger.info("\n ### `Answer Plan Generator`: Initiating answer plan generation based on user input")
        plan = await self.get_answer_plan(user_prompt, language, all_file_content)
        return plan
