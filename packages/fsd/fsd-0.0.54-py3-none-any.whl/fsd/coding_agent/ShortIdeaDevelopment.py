import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class ShortIdeaDevelopment:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def remove_latest_conversation(self):
        """Remove the latest conversation from the history."""
        if self.conversation_history:
            self.conversation_history.pop()

    def initial_setup(self, role, crawl_logs):
        """
        Initialize the conversation with a system prompt and user context.
        """
        logger.debug("Initializing conversation with system prompt and user context")

        all_file_contents = self.repo.print_summarize_with_tree()

        system_prompt = (
            f"As a senior {role}, analyze project files and develop a concise plan:\n\n"
            "1. What: Step-by-step actions to implement the request.\n"
            "2. Why: Brief reasoning for each step.\n"
            "3. Workflow: If applicable, describe process sequence.\n"
            "4. New files/images: Specify full paths. Use SVG for most, PNG/JPEG for large, high-quality images.\n"
            "5. Quick tree: Brief project structure if necessary.\n\n"
            "No Yapping"
            "Format: Concise, focused response. Use h4 headings and bullet points. Avoid unnecessary details."
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
        self.conversation_history.append({"role": "user", "content":  f"Here are the current project structure and files summary:\n{all_file_contents}\n"})
        self.conversation_history.append({"role": "assistant", "content": "Got it! Give me user prompt so i can support them."})

        if crawl_logs:
            crawl_logs_prompt = f"Use this existing crawl data for planning: {crawl_logs}"
            self.conversation_history.append({"role": "user", "content": crawl_logs_prompt})
            self.conversation_history.append({"role": "assistant", "content": "Understood. Using provided data only."})
            
            utilization_prompt = (
                "Specify which file(s) should access this crawl data. "
                "Do not provide steps for crawling or API calls. "
                "The data is already available. "
                "Follow the original development plan guidelines strictly, "
                "ensuring adherence to all specified requirements and best practices."
            )
            self.conversation_history.append({"role": "user", "content": utilization_prompt})
            self.conversation_history.append({"role": "assistant", "content": "Will specify files for data access, following original development plan guidelines strictly. No additional crawling or API calls needed."})


    def read_file_content(self, file_path):
        """
        Read and return the content of any type of file, including special files like Podfile.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Content of the file or empty string if file doesn't exist.
        """
        if not os.path.exists(file_path):
            logger.debug(f"File does not exist: `{file_path}`")
            return ""

        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.debug(f"`IdeaDevelopment` agent encountered an error while reading file `{file_path}` with `{encoding}` encoding: {e}")

        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.debug(f"`IdeaDevelopment` agent failed to read file `{file_path}` in binary mode: {e}")

        return ""

    async def get_idea_plan(self, user_prompt, original_prompt_language):
        logger.debug("Generating idea plan based on user prompt")
        
        prompt = (
            f"Follow the user prompt strictly and provide a clear no-code plan. "
            f"Do not include any code in your response. Focus on high-level concepts, strategies, and approaches. "
            f"Here's the user prompt:\n\n{user_prompt}\n\n"
            f"Return a nicely formatted response. Spacing wisely, ensure the text is clear and easy to read, not crowded together. Use clear headings (no larger than h4). "
            f"Remember, your response should be a comprehensive plan without any code snippets. "
            f"Importantly, provide your response in the original prompt language: {original_prompt_language}."
        )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            logger.info("ShortIdeaDevelopment")
            response = await self.ai.stream_prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
            return response
        except Exception as e:
            logger.debug(f"`IdeaDevelopment` agent encountered an error: {e}")
            return {
                "reason": str(e)
            }

    async def get_idea_plans(self, user_prompt, original_prompt_language):
        logger.debug("Initiating idea plan generation process")
        return await self.get_idea_plan(user_prompt, original_prompt_language)
