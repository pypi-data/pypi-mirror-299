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

class CodingAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway('bedrock')

    def get_current_time_formatted(self):
        """Return the current time formatted as mm/dd/yy."""
        current_time = datetime.now()
        formatted_time = current_time.strftime("%m/%d/%y")
        return formatted_time

    def initial_setup(self, context_files, instructions, context, role):
        """Initialize the setup with the provided instructions and context."""

        logger.info("\n ### The `CodingAgent` is initializing setup with provided instructions and context")

        prompt = f"""You are a senior software engineer working as a coding agent. You will receive detailed instructions to work on. Follow these guidelines strictly:
                **Response Guidelines:**
                1. For ALL code changes, additions, or deletions, you MUST ALWAYS use the following *SEARCH/REPLACE block* format:

                   <<<<<<< SEARCH
                   [Existing code to be replaced, if any]
                   =======
                   [New or modified code]
                   >>>>>>> REPLACE

                2. For new code additions, use an empty SEARCH section:

                   <<<<<<< SEARCH
                   =======
                   [New code to be added]
                   >>>>>>> REPLACE

                3. Ensure that the SEARCH section exactly matches the existing code, including whitespace and comments.

                4. For large files, focus on the relevant sections. Use comments to indicate skipped portions:
                   // ... existing code ...

                5. For complex changes or large files, break them into multiple SEARCH/REPLACE blocks.

                6. CRITICAL: NEVER provide code snippets, suggestions, or examples outside of the SEARCH/REPLACE block format. ALL code must be within these blocks.

                7. Do not provide explanations, ask questions, or engage in discussions. Only return SEARCH/REPLACE blocks.

                8. If a user's request cannot be addressed solely through SEARCH/REPLACE blocks, do not respond.

                Remember, your responses should ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed.
        """

        self.conversation_history = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"These are your instructions: {instructions}"},
            {"role": "assistant", "content": "Got it! I'll proceed with the given instructions."},
            {"role": "user", "content": f"Current context: {context}"},
            {"role": "assistant", "content": "Understood. I'm ready to receive instructions."},
            {"role": "user", "content": f"This is latest tree: {self.repo.print_tree()}"},
            {"role": "assistant", "content": "Got it"},
        ]

        
        if context_files:
            all_file_contents = ""

            for file_path in context_files:
                file_content = self.read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}\n{file_content}"

            self.conversation_history.append({"role": "user", "content": f"These are all the supported files to provide enough context for this task: {all_file_contents}"})
            self.conversation_history.append({"role": "assistant", "content": "Got it!"})

        additional_guideline = """
            **Code Guidelines:**
            0. Implement comprehensive unit tests for all new functionality to ensure code reliability and maintainability.
            1. Write clear and concise documentation for all functions and classes.
            2. Follow consistent naming conventions throughout the codebase.
            3. Implement proper exception handling and provide informative error messages.
            4. Optimize database queries and use indexing where appropriate.
            5. Implement caching mechanisms to improve performance where applicable.
            6. Use dependency injection to improve code modularity and testability.
            7. Implement logging throughout the application for easier debugging and monitoring.
            8. Use code linting tools to maintain consistent code style and quality.
            9. Implement continuous integration and continuous deployment (CI/CD) pipelines.
            10. Regularly update and patch dependencies to address security vulnerabilities.
            11. Use design patterns appropriately to solve common software design problems.
            12. Implement proper authentication and authorization mechanisms.
            13. Use version control best practices, including meaningful commit messages and branching strategies.
            14. Conduct regular code reviews to maintain code quality and share knowledge among team members.
            15. Follow SOLID principles to create more maintainable and scalable code.
            16. Implement proper error handling and logging for better debugging and monitoring.
            17. Use asynchronous programming techniques where appropriate to improve performance.
            18. Implement proper security measures, including input validation and sanitization.
            19. Optimize code for performance, considering time and space complexity.
            20. Write self-documenting code with meaningful variable and function names.
        """
        self.conversation_history.append({"role": "user", "content": additional_guideline})
        self.conversation_history.append({"role": "assistant", "content": "Understood. I will adhere to these guidelines to produce high-quality code as a senior developer, ensuring reliability, maintainability, and best practices throughout the development process."})


    def read_file_content(self, file_path):
        """
        Read and return the content of any type of file, including special files like Podfile.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Content of the file or empty string if file doesn't exist.
        """
        if not os.path.exists(file_path):
            logger.info(f"\n ### The `CodingAgent` encountered a non-existent file: {file_path}")
            return ""

        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.info(f"\n ### The `CodingAgent` failed to read file {file_path} with {encoding} encoding: {e}")

        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.info(f"\n ### The `CodingAgent` failed to read file {file_path} in binary mode: {e}")

        return ""

        # Start of Selection

    async def get_coding_request(self, is_first, file, techStack, crawl_logs, prompt):
        """
        Get coding response for the given instruction and context from Azure OpenAI.

        Args:
            is_first (bool): Flag to indicate if it's the first request.
            file (str): Name of the file to work on.
            techStack (str): The technology stack for which the code should be written.
            crawl_logs (str): Additional data needed for the file.

        Returns:
            str: The code response.
        """
        file_name = os.path.basename(file)
        relative_path = os.path.relpath(file, self.repo.get_repo_path())
        file_info = os.path.join(os.path.dirname(relative_path), file_name)

        if crawl_logs:
            logger.info(f"\n ### The `CodingAgent` is processing crawl logs for {file_info}")
            crawl_logs_prompt = f"This is data you need to work for {file_info}: {crawl_logs}"
            self.conversation_history.append({"role": "user", "content": crawl_logs_prompt})
            self.conversation_history.append({"role": "assistant", "content": "Understood, I'll use this data for the task."})

        user_prompt = (
            f"{'Begin' if is_first else 'Continue'} implementing the following task on {file_info}:\n"
            f"{prompt}\n\n"
            f"Adhere to {techStack} best practices and write idiomatic code.\n"
            "Provide complete, production-ready code with full logic and integration, polished UI, no placeholders allowed.\n"
            "Your responses must ONLY contain SEARCH/REPLACE blocks for code changes. No other content is permitted.\n"
        )

        if self.conversation_history and self.conversation_history[-1]["role"] == "user":
            self.conversation_history.append({"role": "assistant", "content": ""})

        self.conversation_history.append({"role": "user", "content": user_prompt})

        try:
            response = await self.ai.prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
            self.conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"\n ### The `CodingAgent` encountered an error while getting coding request: {e}")
            raise


    async def get_coding_requests(self, is_first, file, techStack, crawl_logs, prompt):
        """
        Get coding responses for a list of files from Azure OpenAI based on user instruction.

        Args:
            is_first (bool): Flag to indicate if it's the first request.
            prompt (str): The coding task prompt.
            file (str): Name of the file to work on.
            techStack (str): The technology stack for which the code should be written.

        Returns:
            dict: The code response or error reason.
        """
        return await self.get_coding_request(is_first, file, techStack, crawl_logs, prompt)

    def clear_conversation_history(self):
        """Clear the conversation history."""
        logger.info("\n ### The `CodingAgent` is clearing conversation history")
        self.conversation_history = []
