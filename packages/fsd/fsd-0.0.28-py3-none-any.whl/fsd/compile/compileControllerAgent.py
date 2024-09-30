import os
import sys
import json
import subprocess
import asyncio
import re

from .CompilePrePromptAgent import CompilePrePromptAgent
from .CompileProjectAnalysAgent import CompileProjectAnalysAgent
from .CompileFileFinderAgent import CompileFileFinderAgent
from .CompileGuiderAgent import CompileGuiderAgent
from .CompileTaskPlanner import CompileTaskPlanner


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.coding_agent.LanguageAgent import LanguageAgent
from fsd.system.CompileCommandRunner import CompileCommandRunner
from fsd.system.OSEnvironmentDetector import OSEnvironmentDetector
from fsd.util import utils
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class CompileControllerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.analysAgent = CompileProjectAnalysAgent(repo)
        self.preprompt = CompilePrePromptAgent(repo)
        self.fileFinder = CompileFileFinderAgent(repo)
        self.guider = CompileGuiderAgent(repo)
        self.lang = LanguageAgent(repo)
        self.taskPlanner = CompileTaskPlanner(repo)
        self.command = CompileCommandRunner(repo)
        self.detector = OSEnvironmentDetector()

    async def get_prePrompt(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.preprompt.get_prePrompt_plans(user_prompt)

    async def start_CLI_compile_process(self, instruction, code_files):

        user_permission = input("Press Tab to proceed with run/compile process, or Enter to skip: ")
        if user_permission != '\t':
            logger.info("\n ### The `CompileControllerAgent` has detected that the run/compile process has been skipped")
            return
    
        os_architecture = self.detector

        file_result = await self.fileFinder.get_compile_file_plannings(instruction)

        compile_files = file_result.get('crucial_files', [])

        logger.info(f"\n ### The `CompileControllerAgent` has identified the following compile-related files: {compile_files}")

        self.analysAgent.initial_setup(compile_files, os_architecture)

        logger.info("\n ### The `CompileProjectAnalysAgent` is initiating the creation of an initial compile plan for clarification")

        idea_plan = await self.analysAgent.get_idea_plans(instruction)

        logger.info(f"\n ### The `CompileProjectAnalysAgent` has generated the following initial compile plan: {idea_plan}")

        while True:
            logger.info("\n ### The `CompileControllerAgent` is requesting user feedback on the compile plan. Please enter \"yes\" if satisfied, or provide feedback for modifications")

            user_prompt_json = input()
            user_prompt, _ = self.parse_payload(user_prompt_json)
            user_prompt = user_prompt.lower()

            if user_prompt == "" or user_prompt == "yes" or user_prompt == "y":
                break
            else:
                logger.info("\n ### The `CompileProjectAnalysAgent` is preparing to update the compile plan based on user feedback")
                eng_prompt = await self.lang.get_language_plans(user_prompt, "DevOps engineer")
                instruction = instruction + " " + eng_prompt
                self.analysAgent.remove_latest_conversation()
                idea_plan = await self.analysAgent.get_idea_plans(instruction)
                logger.info(f"\n ### The `CompileProjectAnalysAgent` has generated an updated compile plan: {idea_plan}")

        self.analysAgent.clear_conversation_history()
        logger.info("\n ### The `CompileTaskPlanner` is now organizing and preparing the task for execution")
        task = await self.taskPlanner.get_task_plan(idea_plan, os_architecture)
        await self.command.execute_steps(task, compile_files, code_files)
        logger.info("\n ### The `CompileControllerAgent` has successfully completed the compilation process")


    def parse_payload(self, user_prompt_json):
        try:
            file_path = None
            data = json.loads(user_prompt_json)
            user_prompt = data.get("prompt", "")
            file_path = data.get("file_path", None)
        except json.JSONDecodeError:
            # If input is not valid JSON, treat it as plain text
            user_prompt = user_prompt_json
            logger.info(f"\n ### The `CompileControllerAgent` has received a Plain Text Prompt: {user_prompt}")
        return user_prompt, file_path


    async def get_started(self, user_prompt):
        """Start the processing of the user prompt."""
        logger.info("\n ### The `CompileControllerAgent` is initiating the compilation request process")

        prePrompt = await self.get_prePrompt(user_prompt)
        finalPrompt = prePrompt['compile_plan']
        pipeline = prePrompt['pipeline']

        if pipeline == "0":
            logger.info("\n ### The `CompileControllerAgent` has determined that no compilation is needed")
        elif pipeline == "1":
            await self.start_CLI_compile_process(finalPrompt)

        logger.info(f"\n ### The `CompileControllerAgent` has completed processing the user prompt: {user_prompt}")
