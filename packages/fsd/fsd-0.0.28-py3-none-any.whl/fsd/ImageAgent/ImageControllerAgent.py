import os
import sys
import json
import subprocess
import asyncio
import re

from .ImagePrePromptAgent import CompilePrePromptAgent
from .ImageTaskPlanner import ImageTaskPlanner
from .ImageFileFinderAgent import ImageFileFinderAgent
from .ImageAnalysAgent import ImageAnalysAgent
from .ImageGenAgent import ImageGenAgent

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.coding_agent.LanguageAgent import LanguageAgent
from fsd.util import utils
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class ImageControllerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.preprompt = CompilePrePromptAgent(repo)
        self.lang = LanguageAgent(repo)
        self.fileFinder = ImageFileFinderAgent(repo)
        self.analysAgent = ImageAnalysAgent(repo)
        self.taskPlanner = ImageTaskPlanner(repo)
        self.imageGenAgent = ImageGenAgent(repo)

    def read_file_content(self, file_path):
        """
        Read and return the content of any type of file, including special files like Podfile.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Content of the file or empty string if file doesn't exist.
        """
        if not os.path.exists(file_path):
            logger.info(f"\n ### File does not exist: `{file_path}`")
            return ""

        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.info(f"\n ### Attempt to read file `{file_path}` with `{encoding}` encoding failed: `{e}`")

        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.info(f"\n ### Binary read attempt for file `{file_path}` failed: `{e}`")

        return ""

    async def get_prePrompt(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.preprompt.get_prePrompt_plans(user_prompt)


    async def start_image_process(self, instruction):

        logger.info(f"\n ### Image generation process initiated with instruction: `{instruction}`")
        logger.info(f"\n ### User input required: Press 'a' or 'Approve' to execute this step, or press Enter to skip")
        user_permission = input()
        if user_permission != 's':
            logger.info("\n ### Image Generation process has been skipped")
            return
        
        file_result = await self.fileFinder.get_style_file_plannings()

        style_files = file_result.get('style_files', [])

        self.analysAgent.initial_setup(style_files)

        logger.info("\n ### Image Analysis Agent is preparing an initial image plan for clarification")

        idea_plan = await self.analysAgent.get_idea_plans(instruction)

        logger.info(f"\n ### Initial image plan generated: `{idea_plan}`")

        while True:
            logger.info(
                "\n ### User feedback required: Are you satisfied with this image plan? Enter \"yes\" if satisfied, or provide feedback for modifications")

            user_prompt_json = input()
            user_prompt, _ = self.parse_payload(user_prompt_json)
            user_prompt = user_prompt.lower()

            if user_prompt == "" or user_prompt == "yes" or user_prompt == "y":
                break
            else:
                logger.info(f"\n ### Image Analysis Agent is updating the image plan based on user feedback")
                eng_prompt = await self.lang.get_language_plans(user_prompt, "DevOps engineer")
                instruction = instruction + " " + eng_prompt
                self.analysAgent.remove_latest_conversation()
                idea_plan = await self.analysAgent.get_idea_plans(instruction)
                logger.info(f"\n ### Updated image plan: `{idea_plan}`")

        self.analysAgent.clear_conversation_history()

        logger.info("\n ### Task Planner is organizing and preparing the task")
        task = await self.taskPlanner.get_task_plan(idea_plan)
        await self.imageGenAgent.generate_images(task)
        logger.info(f"\n ### Image generation process completed for instruction: `{instruction}`")


    async def process_creation(self, data):
        """Process the creation of new files based on provided data."""
        if data.get('Is_creating'):
            processes = data.get('Adding_new_files', [])
            await self.project.execute_files_creation(processes)


    def parse_payload(self, user_prompt_json):
        try:
            file_path = None
            data = json.loads(user_prompt_json)
            user_prompt = data.get("prompt", "")
            file_path = data.get("file_path", None)
        except json.JSONDecodeError:
            # If input is not valid JSON, treat it as plain text
            user_prompt = user_prompt_json
            logger.info(f"\n ### Received Plain Text Prompt: `{user_prompt}`")
        return user_prompt, file_path


    async def get_started(self, user_prompt):
        """Start the processing of the user prompt."""
        
        logger.info("\n ### Image generation agent initialized and ready to process image requests")

        prePrompt = await self.get_prePrompt(user_prompt)
        pipeline = prePrompt['pipeline']

        if pipeline == "0":
            print(user_prompt)
        elif pipeline == "1":
            finalPrompt = prePrompt['processed_prompt']
            await self.start_image_process(finalPrompt)

        logger.info(f"\n ### Image generation process completed for prompt: `{user_prompt}`")
