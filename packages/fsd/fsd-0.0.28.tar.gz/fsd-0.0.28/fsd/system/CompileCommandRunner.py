import subprocess
import os
import sys
import requests
import json
import threading
import time
import re
import signal
from log.logger_config import get_logger
from .FileContentManager import FileContentManager
from .OSEnvironmentDetector import OSEnvironmentDetector
from .ConfigAgent import ConfigAgent
from .TaskErrorPlanner import TaskErrorPlanner
from .ErrorDetection import ErrorDetection

logger = get_logger(__name__)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.coding_agent.BugExplainer import BugExplainer
from fsd.coding_agent.SelfHealingAgent import SelfHealingAgent
from fsd.MainOperation.ProjectManager import ProjectManager
from fsd.coding_agent.FileManagerAgent import FileManagerAgent


class CompileCommandRunner:
    def __init__(self, repo):
        """
        Initializes the CommandRunner.
        """
        self.repo = repo
        self.config = ConfigAgent(repo)
        self.errorDetection = ErrorDetection(repo)
        self.errorPlanner = TaskErrorPlanner(repo)
        self.self_healing = SelfHealingAgent(repo)
        self.bugExplainer = BugExplainer(repo)
        self.project = ProjectManager(repo)
        self.fileManager = FileManagerAgent(repo)
        self.config_manager = FileContentManager()  # Initialize CodeManager in the constructor
        self.detector = OSEnvironmentDetector()
        self.directory_path = repo.get_repo_path()
        self.max_retry_attempts = 3  # Set a maximum number of retry attempts

    async def get_config_requests(self, instructions, file_name):
        """Generate coding requests based on instructions and context."""

        main_path = file_name
        logger.info(f"\n ### `ConfigAgent` is processing file: {file_name} in {main_path}")
        logger.info(f"\n ### `ConfigAgent` task: {instructions}")
        result = await self.config.get_config_requests(instructions, main_path)
        if main_path:
            await self.config_manager.handle_coding_agent_response(main_path, result)
            logger.info(f"\n ### `ConfigAgent` has completed its work on {file_name}")
        else:
            logger.warning(f"\n ### `ConfigAgent` was unable to locate the file: {file_name}")

    async def get_error_planner_requests(self, error, config_context, os_architecture, compile_files):
        """Generate coding requests based on instructions and context."""
        result = await self.errorPlanner.get_task_plans(error, config_context, os_architecture, compile_files)
        return result

    def run_command(self, command, method='bash'):
        """
        Runs a given command using the specified method.
        Shows real-time output during execution.
        Returns a tuple of (return_code, all_output).
        """
        try:
            # Use bash for all commands
            shell = True
            executable = '/bin/bash'

            # Check if the first part of the command is 'cd'
            if command.startswith('cd '):
                # Change the working directory
                new_dir = command[3:].strip()
                os.chdir(new_dir)
                logger.info(f"\n ### `CommandRunner` has changed the directory to: {new_dir}")
                return 0, [f"Changed directory to: {new_dir}"]

            # Log the current working directory
            current_path = os.getcwd()
            logger.info(f"\n ### `CommandRunner` is executing the command: {command} in: {current_path}")

            # Start the process and capture output
            process = subprocess.Popen(
                command,
                shell=shell,
                executable=executable,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
                cwd=current_path,  # Explicitly set the working directory
                preexec_fn=os.setsid  # Start the process in a new session
            )

            output = []
            error_occurred = False

            def read_output(pipe, is_stdout=True):
                nonlocal output, error_occurred
                try:
                    for line in iter(pipe.readline, ''):
                        if not line:
                            break
                        line = line.strip()
                        if is_stdout:
                            logger.info(line)
                            print(f"line: {line}")
                        else:
                            logger.error(line)
                            print(f"line: {line}")
                            error_occurred = True
                        output.append(line)
                except Exception as e:
                    # Pipe was closed
                    pass

            # Start threads to read stdout and stderr
            stdout_thread = threading.Thread(target=read_output, args=(process.stdout, True))
            stderr_thread = threading.Thread(target=read_output, args=(process.stderr, False))
            stdout_thread.start()
            stderr_thread.start()

            # Wait for the process to terminate
            process.wait()

            # Close the pipes to ensure threads exit
            process.stdout.close()
            process.stderr.close()

            # Wait for threads to finish
            stdout_thread.join()
            stderr_thread.join()

            return_code = process.returncode

            return return_code, output

        except Exception as e:
            logger.error(f"\n ### `CommandRunner` encountered an error while executing the command: {str(e)}")
            return -1, [f"Command execution failed: {str(e)}"]

    def update_file(self, file_name, content):
        """
        Updates the content of a file.
        """
        try:
            with open(file_name, 'a') as file:
                file.write(content + '\n')
            logger.info(f"\n ### `FileUpdater` has successfully updated {file_name}")
            return f"Successfully updated {file_name}"
        except Exception as e:
            logger.error(f"\n ### `FileUpdater` failed to update {file_name}: {str(e)}")
            return f"Failed to update {file_name}: {str(e)}"

    async def print_code_error(self, error_message, code_files, role="Elite software engineer", max_retries=50):
        """
        Prints the code syntax error details.
        """
        totalfile = set()
        fixing_related_files = set()

        retries = 0

        while retries < max_retries:
            self.self_healing.clear_conversation_history()
            self.bugExplainer.clear_conversation_history()

            self.bugExplainer.initial_setup(role)
            self.self_healing.initial_setup(role)

            try:
                logger.info("\n ### `ErrorHandler` has detected an issue and will commence work on the fix immediately")
                overview = ""

                if code_files:
                    overview = self.repo.print_tree()
                else:
                    overview = self.repo.print_summarize_with_tree()

                # Ensure basename list is updated without duplicates
                fixing_related_files.update(list(code_files))
                fixing_related_files.update(list(totalfile))

                logger.info("\n ### `BugExplainer` is initiating the examination of bugs and creation of a fixing plan")
                fix_plans = await self.bugExplainer.get_bugFixed_suggest_requests(
                    error_message, list(fixing_related_files), overview)
                print(f"fix_plans: {fix_plans}")
                logger.info("\n ### `BugExplainer` has completed the examination of bugs and creation of a fixing plan")

                logger.info("\n ### `FileProcessor` is beginning work on file processing")
                file_result = await self.get_file_planning(fix_plans)
                await self.process_creation(file_result)
                logger.info("\n ### `FileProcessor` has completed processing files")

                logger.info(f"\n ### `FixingAgent` is attempting to fix for the {retries + 1} time")
                steps = fix_plans.get('steps', [])

                for step in steps:
                    file_name = step['file_name']
                    totalfile.add(file_name)

                await self.self_healing.get_fixing_requests(steps)

                # If we reach this point without exceptions, we assume the fix was successful
                logger.info("\n ### `FixingAgent` has successfully applied the fix")
                return list(totalfile)

            except requests.exceptions.HTTPError as http_error:
                if http_error.response.status_code == 429:
                    wait_time = 2 ** retries
                    logger.info(f"\n ### `RateLimitHandler` has detected that the rate limit has been exceeded, retrying in {wait_time} seconds...")
                    time.sleep(wait_time)  # Exponential backoff
                else:
                    logger.error(f"\n ### `HTTPErrorHandler` encountered an HTTP error: {http_error}")
                    raise
            except Exception as e:
                logger.error(f"\n ### `ErrorHandler` encountered an error during the fixing process: {str(e)}")

            retries += 1

        self.self_healing.clear_conversation_history()
        self.bugExplainer.clear_conversation_history()
        logger.info("\n ### `BuildManager` reports that the build has failed after maximum retries")

    async def execute_steps(self, steps_json, compile_files, code_files):
        """
        Executes a series of steps provided in JSON format.
        Asks for user permission before executing each step.
        Waits for each command to complete before moving to the next step.
        """
        self.errorDetection.initial_setup()
        steps = steps_json['steps']

        for step in steps:
            if step['method'] == 'bash':
                logger.info(f"\n ### `StepExecutor`: {step['prompt']} - {step['command']}")
            elif step['method'] == 'update':
                logger.info(f"\n ### `StepExecutor`: {step['prompt']} - {step['prompt']}")
            else:
                logger.info(f"\n ### `StepExecutor`: {step['prompt']}")

            logger.info(f"\n ### Press a or Approve to execute this step, or Enter to skip: ")
            user_permission = input()

            if user_permission == 'exit':
                logger.info("\n ### `UserInteractionHandler`: User has chosen to exit. Stopping execution.")
                return "Execution stopped by user"
            elif user_permission != 'a':
                logger.info("\n ### `UserInteractionHandler`: Step skipped by user.")
                continue

            logger.info(f"\n ### `StepExecutor`: Executing step: {step['prompt']}")

            retry_count = 0
            while retry_count < self.max_retry_attempts:
                if step['method'] == 'bash':
                    # Run the command and get the return code and output
                    return_code, command_output = self.run_command(step['command'])

                    # Check for errors based on the return code
                    if return_code != 0:
                        error_message = ','.join(command_output)
                        logger.error(f"\n ### `CommandExecutor` failed with return code {return_code}: {error_message}")

                        error_check = await self.errorDetection.get_task_plan(error_message)
                        error_type = error_check.get('error_type', 1)
                        AI_error_message = error_check.get('error_message', "")

                        if error_type == 1:
                            await self.print_code_error(AI_error_message, code_files)
                            retry_count += 1
                            continue  # Re-run the command after fixing the code error

                        # Check if the error suggests an alternative command
                        if "Did you mean" in error_message:
                            suggested_command = error_message.split("Did you mean")[1].strip().strip('"?')
                            logger.info(f"\n ### `SystemSuggestionHandler` has found an alternative command: {suggested_command}")
                            logger.info(f"\n ### Press a or Approve to execute this step, or Enter to skip: ")
                            user_choice = input()
                            
                            if user_choice == 'a':
                                logger.info(f"\n ### `UserInteractionHandler`: Executing suggested command: {suggested_command}")
                                return_code, command_output = self.run_command(suggested_command)
                                if return_code == 0:
                                    break  # Command executed successfully
                                else:
                                    # Update error_message with new command output
                                    error_message = ','.join(command_output)
                                    logger.error(
                                        f"\n ### `CommandExecutor`: Suggested command also failed with return code {return_code}: {error_message}")
                            elif user_choice == 'exit':
                                logger.info("\n ### `UserInteractionHandler`: User has chosen to exit. Stopping execution.")
                                return "Execution stopped by user"
                            else:
                                logger.info("\n ### `UserInteractionHandler`: User chose not to run the suggested command.")

                        # Proceed to handle the error
                        fixing_steps = await self.get_error_planner_requests(
                            error_message, step['prompt'], self.detector, compile_files)
                        fixing_result = await self.execute_fixing_steps(fixing_steps, compile_files, code_files)
                        if fixing_result == "Execution stopped by user":
                            logger.info("\n ### `UserInteractionHandler`: User chose to exit during fixing steps. Skipping current step.")
                            break
                        retry_count += 1
                    else:
                        break  # Command executed successfully without errors
                elif step['method'] == 'update':
                    file_name = step.get('file_name', '')
                    if file_name != 'N/A':
                        await self.get_config_requests(step['prompt'], file_name)
                        logger.info(f"\n ### `FileUpdater` has successfully updated {file_name}")
                    else:
                        logger.warning("\n ### `FileUpdater`: Update method specified but no file name provided.")
                    break
                else:
                    logger.error(f"\n ### `StepExecutor` encountered an unknown method: {step['method']}")
                    break

            if retry_count == self.max_retry_attempts:
                logger.error(f"\n ### `StepExecutor`: Step failed after {self.max_retry_attempts} attempts: {step['prompt']}")
                error_message = f"Step failed after {self.max_retry_attempts} attempts: {step['prompt']}"
                fixing_steps = await self.get_error_planner_requests(
                    error_message, step['prompt'], self.detector, compile_files)
                fixing_result = await self.execute_fixing_steps(fixing_steps, compile_files, code_files)
                if fixing_result == "Execution stopped by user":
                    logger.info("\n ### `UserInteractionHandler`: User chose to exit during fixing steps. Skipping current step.")
                    continue
                return f"Step failed after {self.max_retry_attempts} attempts: {step['prompt']}"

            logger.info("\n ### `StepExecutor`: Step completed. Proceeding to the next step.")

        logger.info("\n ### `StepExecutor`: All steps have been completed successfully")
        return "All steps completed successfully"

    async def execute_fixing_steps(self, steps_json, compile_files, code_files):
        """
        Executes a series of steps provided in JSON format to fix dependency issues.
        Asks for user permission before executing each step.
        Waits for each command to complete before moving to the next step.
        """
        steps = steps_json['steps']

        for step in steps:

            if step['method'] == 'bash':
                logger.info(f"\n ### `FixingStepExecutor`: {step['error_resolution']} - {step['command']}")
            else:
                logger.info(f"\n ### `FixingStepExecutor`: {step['error_resolution']}")

            logger.info(f"\n ### Press a or Approve to execute this step, or Enter to skip: ")
            user_permission = input()

            if user_permission == 'exit':
                logger.info("\n ### `UserInteractionHandler`: User has chosen to exit. Stopping execution.")
                return "Execution stopped by user"
            elif user_permission != 's':
                logger.info("\n ### `UserInteractionHandler`: Step skipped by user.")
                continue

            logger.info(f"\n ### `FixingStepExecutor`: Executing step: {step['error_resolution']}")

            retry_count = 0
            while retry_count < self.max_retry_attempts:
                if step['method'] == 'bash':
                    # Run the command and get the return code and output
                    return_code, command_output = self.run_command(step['command'])

                    # Check for errors based on the return code
                    if return_code != 0:
                        error_message = ','.join(command_output)
                        logger.error(f"\n ### `CommandExecutor` failed with return code {return_code}: {error_message}")

                        error_check = await self.errorDetection.get_task_plan(error_message)
                        error_type = error_check.get('error_type', 1)
                        AI_error_message = error_check.get('error_message', "")

                        if error_type == 1:
                            await self.print_code_error(AI_error_message, code_files)
                            retry_count += 1
                            continue  # Re-run the command after fixing the code error

                        # Proceed to handle the error
                        fixing_steps = await self.get_error_planner_requests(
                            error_message, step['error_resolution'], self.detector, compile_files)
                        fixing_result = await self.execute_fixing_steps(fixing_steps, compile_files, code_files)
                        if fixing_result == "Execution stopped by user":
                            return "Execution stopped by user"
                        retry_count += 1
                    else:
                        break  # Command executed successfully without errors
                elif step['method'] == 'update':
                    file_name = step.get('file_name', '')
                    if file_name != 'N/A':
                        await self.get_config_requests(step['error_resolution'], file_name)
                        logger.info(f"\n ### `FileUpdater` has successfully updated {file_name}")
                    else:
                        logger.warning("\n ### `FileUpdater`: Update method specified but no file name provided.")
                    break
                else:
                    logger.error(f"\n ### `FixingStepExecutor` encountered an unknown method: {step['method']}")
                    break

            if retry_count == self.max_retry_attempts:
                logger.error(f"\n ### `FixingStepExecutor`: Step failed after {self.max_retry_attempts} attempts: {step['error_resolution']}")
                error_message = f"Step failed after {self.max_retry_attempts} attempts: {step['error_resolution']}"
                fixing_steps = await self.get_error_planner_requests(
                    error_message, step['error_resolution'], self.detector, compile_files)
                fixing_result = await self.execute_fixing_steps(fixing_steps, compile_files, code_files)
                if fixing_result == "Execution stopped by user":
                    return "Execution stopped by user"
                return f"Step failed after {self.max_retry_attempts} attempts: {step['error_resolution']}"

            logger.info("\n ### `FixingStepExecutor`: Step completed. Proceeding to the next step.")

        logger.info("\n ### `FixingStepExecutor`: All fixing steps have been completed successfully")
        return "All fixing steps completed successfully"

    async def get_file_planning(self, idea_plan):
        """Generate idea plans based on user prompt and available files."""
        return await self.fileManager.get_file_plannings(idea_plan)

    async def process_creation(self, data):
        # Check if 'Is_creating' is True
        if data.get('Is_creating'):
            # Extract the processes array
            processes = data.get('Adding_new_files', [])
            # Create a list of process details
            await self.project.execute_files_creation(processes)
        else:
            logger.info("\n ### `FileCreationManager`: No new files need to be added at this time.")
