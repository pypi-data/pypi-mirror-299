import os
import sys
import json
import subprocess
import asyncio
import re

from .DependencyPrePromptAgent import DependencyPrePromptAgent
from .DependencyProjectAnalysAgent import DependencyProjectAnalysAgent
from .DependencyFileFinderAgent import DependencyFileFinderAgent
from .DependencyGuiderAgent import DependencyGuiderAgent
from .DependencyTaskPlanner import DependencyTaskPlanner
from .DependencyCheckAgent import DependencyCheckAgent
from .DependencyCheckCLIAgent import DependencyCheckCLIAgent


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.MainOperation.ProjectManager import ProjectManager
from fsd.coding_agent.LanguageAgent import LanguageAgent
from fsd.system.CommandRunner import CommandRunner
from fsd.system.OSEnvironmentDetector import OSEnvironmentDetector
from fsd.util import utils
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

HOME_DIRECTORY = os.path.expanduser('~')
HIDDEN_ZINLEY_FOLDER = '.zinley'

class DependencyControllerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.analysAgent = DependencyProjectAnalysAgent(repo)
        self.preprompt = DependencyPrePromptAgent(repo)
        self.project = ProjectManager(repo)
        self.fileFinder = DependencyFileFinderAgent(repo)
        self.guider = DependencyGuiderAgent(repo)
        self.lang = LanguageAgent(repo)
        self.taskPlanner = DependencyTaskPlanner(repo)
        self.command = CommandRunner(repo)
        self.detector = OSEnvironmentDetector()
        self.CLI = DependencyCheckCLIAgent(repo)
        self.checker = DependencyCheckAgent(repo)
        self.directory_path = self.repo.get_repo_path()


    async def get_prePrompt(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.preprompt.get_prePrompt_plans(user_prompt)


    async def guider_pipeline(self, user_prompt):
        """Pipeline for regular coding tasks."""
        logger.info("\n ### The `DependencyControllerAgent` is initiating the guider pipeline")

        while True:
            user_prompt_json = input("Do you need more help with dependency?: ")
            guide = await self.guider.get_guider_plans(user_prompt_json)
            finalPrompt = guide['processed_prompt']
            pipeline = guide['pipeline']
            explainer = guide['explainer']

            if pipeline == "0":
                break
            elif pipeline == "1":
                print(explainer)
            elif pipeline == "2":
                print(guide)
                await self.start_dependency_installation_process(user_prompt)
                break


    async def start_dependency_installation_process(self, instruction):
        logger.info("\n ### The `DependencyControllerAgent` is commencing the dependency installation process")
        os_architecture = self.detector
        file_result = await self.fileFinder.get_dependency_file_plannings()

        dependency_files = file_result.get('dependency_files', [])

        self.analysAgent.initial_setup(dependency_files, os_architecture)

        logger.info("\n ### The `DependencyControllerAgent` is creating an initial dependency plan for clarification")

        idea_plan = await self.analysAgentCoding.get_idea_plans(instruction)

        while True:
            logger.info("\n ### The `DependencyControllerAgent` is requesting feedback on the dependency plan")
            logger.info("Are you satisfied with this dependency plan? Enter \"yes\" if satisfied, or provide feedback for modifications: ")

            user_prompt_json = input()
            user_prompt, _ = self.parse_payload(user_prompt_json)
            user_prompt = user_prompt.lower()

            if user_prompt == "" or user_prompt == "yes" or user_prompt == "y":
                break
            else:
                logger.info("\n ### The `DependencyControllerAgent` is updating the dependency plan based on feedback")
                eng_prompt = await self.lang.get_language_plans(user_prompt, "DevOps engineer")
                instruction = instruction + " " + eng_prompt
                self.analysAgent.remove_latest_conversation()
                idea_plan = await self.analysAgent.get_idea_plans(instruction)

        self.analysAgent.clear_conversation_history()
        logger.info("\n ### The `DependencyControllerAgent` is preparing to execute the finalized dependency plan")
        task = await self.taskPlanner.get_task_plan(idea_plan, os_architecture)
        await self.command.execute_steps(task)
        logger.info("\n ### The `DependencyControllerAgent` has completed the dependency installation process")


    async def start_dependency_installation_process_coding_pipeline(self, instruction):
        logger.info("\n ### The `DependencyControllerAgent` is initiating the dependency installation process for the coding pipeline")
        logger.info(instruction)
        logger.info("Press a or approve to proceed with dependency installation, or s or skip to skip: ")
        user_permission = input()
        if user_permission == "s" or user_permission == "skip":
            logger.info("\n ### The `DependencyControllerAgent` has skipped the dependency installation as per user request")
            return
        if user_permission == "a" or user_permission == "approve":
            os_architecture = self.detector
            file_result = await self.fileFinder.get_dependency_file_plannings()
            dependency_files = file_result.get('dependency_files', [])
            self.analysAgentCoding.initial_setup(dependency_files, os_architecture)
            idea_plan = await self.analysAgentCoding.get_idea_plans(instruction)
            should_process_install_dependency = idea_plan.get('should_process_install_dependency')
            if should_process_install_dependency:
                logger.info(f"\n ### The `DependencyControllerAgent` has generated an initial dependency plan: {idea_plan.get('plan')}")

                while True:
                    logger.info("\n ### The `DependencyControllerAgent` is requesting feedback on the dependency plan")
                    logger.info("Are you satisfied with this dependency plan? Enter \"yes\" if satisfied, or provide feedback for modifications: ")

                    user_prompt_json = input()
                    user_prompt, _ = self.parse_payload(user_prompt_json)
                    user_prompt = user_prompt.lower()

                    if user_prompt == "" or user_prompt == "yes" or user_prompt == "y":
                        break
                    else:
                        logger.info("\n ### The `DependencyControllerAgent` is updating the dependency plan based on feedback")
                        eng_prompt = await self.lang.get_language_plans(user_prompt, "DevOps engineer")
                        instruction = instruction + " " + eng_prompt
                        self.analysAgentCoding.remove_latest_conversation()
                        idea_plan = await self.analysAgentCoding.get_idea_plans(instruction)
                        should_process_install_dependency = idea_plan.get('should_process_install_dependency')

                        if should_process_install_dependency:
                            logger.info(f"\n ### The `DependencyControllerAgent` has updated the dependency plan: {idea_plan.get('plan')}")
                        else:
                            logger.info(f"\n ### The `DependencyControllerAgent` reports: {idea_plan.get('reason')}")
                            return

                self.analysAgentCoding.clear_conversation_history()
                logger.info("\n ### The `DependencyControllerAgent` is preparing to execute the finalized dependency plan")
                task = await self.taskPlanner.get_task_plan(idea_plan, os_architecture)
                await self.command.execute_steps(task, dependency_files)
                logger.info(f"\n ### The `DependencyControllerAgent` has completed the task: {instruction}")
            else:
                logger.info(f"\n ### The `DependencyControllerAgent` reports: {idea_plan.get('reason')}")



    def parse_payload(self, user_prompt_json):
        try:
            file_path = None
            data = json.loads(user_prompt_json)
            user_prompt = data.get("prompt", "")
            file_path = data.get("file_path", None)
        except json.JSONDecodeError:
            # If input is not valid JSON, treat it as plain text
            user_prompt = user_prompt_json
            logger.info(f"\n ### The `DependencyControllerAgent` received a plain text prompt: {user_prompt}")
        return user_prompt, file_path


    async def get_started(self, user_prompt):
        """Start the processing of the user prompt."""
        logger.info("\n ### The `DependencyControllerAgent` is beginning to process the user request")

        prePrompt = await self.get_prePrompt(user_prompt)
        pipeline = prePrompt['pipeline']


        if pipeline == "0":
            explainer = prePrompt['explainer']
            print(explainer)
        elif pipeline == "1":
            explainer = prePrompt['explainer']
            print(explainer)
            self.guider.initial_setup(user_prompt)
            self.guider.conversation_history.append({"role": "assistant", "content": f"{prePrompt}"})
            await self.guider_pipeline(user_prompt)
        elif pipeline == "2":
            install_plan = prePrompt['install_plan']
            await self.start_dependency_installation_process(install_plan)

        logger.info(f"\n ### The `DependencyControllerAgent` has completed processing the request: `{user_prompt}`")


    async def get_started_coding_pipeline(self, user_prompt):
        logger.info("\n ### The `DependencyControllerAgent` is initiating the coding pipeline")
        """Start the processing of the user prompt."""

        check_result = await self.checker.get_dependency_check_plans(user_prompt)
        result = check_result.get('result')
        if result == "0":
            logger.info("\n ### The `DependencyControllerAgent` has determined that no dependencies are needed for this task")
            return
        elif result == "1":
            prePrompt = await self.get_prePrompt(user_prompt)
            pipeline = prePrompt['pipeline']

            if pipeline == "0":
                explainer = prePrompt['explainer']
                print(explainer)
            elif pipeline == "2":
                install_plan = prePrompt['install_plan']
                await self.start_dependency_installation_process_coding_pipeline(install_plan)

            logger.info("\n ### The `DependencyControllerAgent` has completed the dependency installation process for the coding pipeline")
