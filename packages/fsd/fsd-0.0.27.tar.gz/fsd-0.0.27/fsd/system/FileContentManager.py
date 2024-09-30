import re
import aiofiles
import os
from typing import List, Tuple
from log.logger_config import get_logger
logger = get_logger(__name__)

class FileContentManager:
    @staticmethod
    async def read_file(file_path: str) -> str:
        """Read the content of the file asynchronously."""
        try:
            async with aiofiles.open(file_path, 'r') as file:
                content = await file.read()
            logger.info(f"FileContentManager successfully read file {file_path}")
            return content
        except FileNotFoundError:
            logger.warning(f"FileContentManager: File {file_path} not found. Returning empty string.")
            return ""
        except Exception as e:
            logger.error(f"FileContentManager encountered an error reading file {file_path}. Error: {e}")
            return ""

    @staticmethod
    async def write_file(file_path: str, content: str):
        """Write content to the file asynchronously."""
        try:
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
                logger.info(f"FileContentManager created directory {directory} for new file {file_path}")
            
            async with aiofiles.open(file_path, 'w') as file:
                await file.write(content)
            
            if not os.path.exists(file_path):
                logger.info(f"FileContentManager created new file {file_path}")
            else:
                logger.info(f"FileContentManager has successfully updated file {file_path}")
        except Exception as e:
            logger.error(f"FileContentManager encountered an error writing to file {file_path}. Error: {e}")

    @staticmethod
    def parse_search_replace_blocks(response: str) -> List[Tuple[str, str]]:
        """
        Parses a response string for single or multiple SEARCH/REPLACE blocks,
        returning search and replace content as tuples. Handles both cases correctly.
        """
        # Regular expression pattern to capture multiple SEARCH/REPLACE blocks
        pattern = r'<<<<< SEARCH\n(.*?)=======\n(.*?)>>>>>>> REPLACE'

        # Find all matches in the response
        matches = re.findall(pattern, response, re.DOTALL)

        # Raise an error if no blocks are found
        if not matches:
            raise ValueError("No valid SEARCH/REPLACE blocks found in the input.")

        blocks = []
        for search, replace in matches:
            # Strip any extra spaces or newlines for cleanliness
            search = search.strip()
            replace = replace.strip()

            # Append the search and replace blocks as a tuple
            blocks.append((search, replace))

        return blocks


    @classmethod
    async def apply_changes(cls, file_path: str, blocks: List[Tuple[str, str]]) -> str:
        """Apply the changes from SEARCH/REPLACE blocks to the file content."""
        content = await cls.read_file(file_path)
        for search, replace in blocks:
            if search:
                content = content.replace(search, replace)
            else:
                content += f"\n\n{replace}"
        logger.info(f"FileContentManager successfully applied changes to content of {file_path}")
        return content

    @classmethod
    async def process_coding_agent_response(cls, file_path: str, coding_agent_response: str):
        """Process the coding agent response and automatically apply changes to the file."""
        blocks = cls.parse_search_replace_blocks(coding_agent_response)
        if not blocks:
            logger.warning(f"FileContentManager found no valid SEARCH/REPLACE blocks in the coding agent response for {file_path}")
            return

        new_content = await cls.apply_changes(file_path, blocks)
        await cls.write_file(file_path, new_content)
        logger.info(f"FileContentManager has automatically applied changes to {file_path}")

    @classmethod
    async def handle_coding_agent_response(cls, file_path: str, coding_agent_response: str):
        """Main method to handle coding agent responses and automatically manage code changes for a single file."""
        try:
            await cls.process_coding_agent_response(file_path, coding_agent_response)
            logger.info(f"FileContentManager successfully handled coding agent response for {file_path}")
        except Exception as e:
            logger.error(f"FileContentManager encountered an error processing coding agent response for {file_path}: {e}")
