import os
import sys
import asyncio
from datetime import datetime
import aiohttp
import json
import re
from json_repair import repair_json

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class ConfigAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway('bedrock')

    def get_current_time_formatted(self):
        """Return the current time formatted as mm/dd/yy."""
        current_time = datetime.now()
        formatted_time = current_time.strftime("%m/%d/%y")
        return formatted_time

    def read_file_content(self, file_path):
        """
        Read and return the content of any type of file, including special files like Podfile.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Content of the file.
        """
        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.info(f"Failed to read file {file_path} with {encoding} encoding: {e}")

        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.context(f"Failed to read file {file_path} in binary mode: {e}")

        return None

    async def get_config_request(self, instruction, main_path):
        """
        Get coding response for the given instruction and context from AI.

        Args:
            instruction (str): The instruction for the config change.
            main_path (str): Path to the file to work on.

        Returns:
            str: The config response or error reason.
        """
        if main_path:
            context = self.read_file_content(main_path)
        else:
            context = "Empty File context"

        system_prompt = """You are an ELITE DevOps engineering specialist working as a dependency config agent. You will receive detailed instructions to work on. Follow these guidelines strictly:
                1. For ALL config changes, additions, or deletions, you MUST ALWAYS use the following *SEARCH/REPLACE block* format:

                   <<<<<<< SEARCH
                   [Existing config to be replaced, if any]
                   =======
                   [New or modified config]
                   >>>>>>> REPLACE

                2. For new config additions, use an empty SEARCH section:

                   <<<<<<< SEARCH
                   =======
                   [New config to be added]
                   >>>>>>> REPLACE

                3. Ensure that the SEARCH section exactly matches the existing config, including whitespace and comments.

                4. For large files, focus on the relevant sections. Use comments to indicate skipped portions:
                   // ... existing config ...

                5. For complex changes or large files, break them into multiple SEARCH/REPLACE blocks.

                6. CRITICAL: NEVER provide config snippets, suggestions, or examples outside of the SEARCH/REPLACE block format. ALL config must be within these blocks.

                7. Do not provide explanations, ask questions, or engage in discussions. Only return SEARCH/REPLACE blocks.

                8. If a user's request cannot be addressed solely through SEARCH/REPLACE blocks, do not respond.

                Remember, your responses should ONLY contain SEARCH/REPLACE blocks for config changes. Nothing else is allowed."""

        user_prompt = (
            f"File context: {context}. "
            f"Your config must be well-organized, with a senior-level design approach.\n"
            "Remember, your responses should ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed.\n\n"
            f"Instruction: {instruction}"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        try:
            response = await self.ai.prompt(messages, self.max_tokens, 0, 0)
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Failed to get config request: {e}")
            return str(e)

    async def get_config_requests(self, instruction, main_path):
        """
        Get config response for the given file and instruction.

        Args:
            file_name (str): Name of the file to work on.
            instruction (str): The instruction for the config change.

        Returns:
            str: The config response or error reason.
        """
        return await self.get_config_request(instruction, main_path)
