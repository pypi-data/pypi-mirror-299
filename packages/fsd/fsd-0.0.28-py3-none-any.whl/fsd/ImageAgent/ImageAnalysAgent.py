import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class ImageAnalysAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway('bedrock')
        self.project_path = self.repo.get_repo_path()

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def remove_latest_conversation(self):
        """Remove the latest conversation from the history."""
        if self.conversation_history:
            self.conversation_history.pop()

    def initial_setup(self, dependency_files):
        """
        Initialize the conversation with a system prompt and user context.
        """

        all_file_contents = ""
        tree_contents = self.repo.print_tree()

        dependency_files_path = dependency_files

        if dependency_files_path:
            for file_path in dependency_files_path:
                file_content = self.read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}:\n{file_content}"
        else:
            all_file_contents = "No dependency files found."

        system_prompt = (
            f"You're a UI/UX designer for image generation and style analysis. Analyze project files for style elements and plan image generation matching the theme. STRICTLY FOLLOW:\n\n"
            f"1. ALWAYS start with: cd {self.project_path}\n"
            "2. Analyze ALL style-related files (CSS, SCSS, JSON themes).\n"
            "3. Extract theme info: colors, typography, layout, design elements.\n"
            "4. Determine image sizes from layout requirements.\n"
            "5. Identify background colors/patterns.\n"
            "6. Analyze existing images for consistency.\n"
            "7. If no style files, state this and recommend basic style guide.\n"
            "8. Provide clear image generation guidelines matching project style.\n"
            "9. Suggest suitable image generation techniques/tools.\n"
            "10. Adapt specific image requests to fit theme and sizes ('1024x1024', '1792x1024', '1024x1792').\n"
            f"11. ALWAYS suggest saving images in appropriate directory within {self.project_path}, mention the FULL PATH for each new generated image.\n\n"
            "FOCUS SOLELY on style analysis and image generation. NO code modification or implementation steps.\n\n"
            "CRITICAL: Limit to style analysis and image generation recommendations. Any deviation is a critical error.\n\n"
            "IMPORTANT: Use EXACT file names/paths mentioned by user. Follow specific requirements strictly."
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
        self.conversation_history.append({"role": "user", "content":  f"Here are the current dependency files: {all_file_contents}\n\nProject structure: {tree_contents}\n"})
        self.conversation_history.append({"role": "assistant", "content": "Got it! Give me user prompt so i can support them."})

    def read_file_content(self, file_path):
        """
        Read and return the content of any type of file, including special files like Podfile.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Content of the file or empty string if file doesn't exist.
        """
        if not os.path.exists(file_path):
            logger.info(f"\n ### The `ImageAnalysAgent` reports: File does not exist\n File path: {file_path}")
            return ""

        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.info(f"\n ### The `ImageAnalysAgent` encountered an issue while reading a file\n File: {file_path}\n Encoding: {encoding}\n Error: {e}")

        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.info(f"\n ### The `ImageAnalysAgent` failed to read a file in binary mode\n File: {file_path}\n Error: {e}")

        return ""

    async def get_idea_plan(self, user_prompt):
        prompt = (
             f"Follow the user prompt strictly and provide a no code response:\n{user_prompt}\n\n"
        )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            logger.info("\n ### The `ImageAnalysAgent` is initiating the AI prompt for idea generation")
            response = await self.ai.prompt(self.conversation_history, self.max_tokens, 0, 0)
            logger.info("\n ### The `ImageAnalysAgent` has successfully received the AI response")
            return response.choices[0].message.content
        except Exception as e:
            logger.info(f"\n ### The `ImageAnalysAgent` encountered an error during idea generation\n Error: {e}")
            return {
                "reason": str(e)
            }


    async def get_idea_plans(self, user_prompt):
        logger.info("\n ### The `ImageAnalysAgent` is beginning the process of generating idea plans")
        plan = await self.get_idea_plan(user_prompt)
        logger.info("\n ### The `ImageAnalysAgent` has completed generating idea plans")
        return plan
