import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class TaskPlanner:
    """
    A class to plan and manage tasks using AI-powered assistance.
    """

    def __init__(self, repo):
        """
        Initialize the TaskPlanner with necessary configurations.

        Args:
            directory_path (str): Path to the project directory.
            api_key (str): API key for authentication.
            endpoint (str): API endpoint URL.
            deployment_id (str): Deployment ID for the AI model.
            max_tokens (int): Maximum number of tokens for AI responses.
        """
        self.max_tokens = 4096
        self.repo = repo
        self.ai = AIGateway()

    async def get_task_plan(self, instruction, file_list):
        """
        Get a development plan based on the user's instruction using AI.

        Args:
            instruction (str): The user's instruction for task planning.
            crawl_logs: Logs from web crawling, if any.

        Returns:
            dict: Development plan or error reason.
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a principal engineer specializing in Pyramid architecture. Generate an ordered list of files necessary for implementing a system following Pyramid best practices based on the user's instruction and provided file list. Start with foundational components and progress to more complex files requiring greater context and integration.\n\n"
                    "Guidelines:\n"
                    "1. **File Selection:** Only include files from the provided `file_list`.\n"
                    "2. **Ordering:** Begin with foundational, context-rich files, then move to higher-level, more complex files, following Pyramid architecture principles.\n"
                    "3. **Content Scope:** List only essential files required for implementation.\n"
                    "4. **File Structure:** For each file, provide `file_name` (full path), `techStack`, `need_data`, and `prompt`.\n"
                    "5. **Integration:** Ensure each file integrates seamlessly with others for maintainability and scalability.\n"
                    "6. **Exclusions:** Omit configuration, dependencies, and non-essential files. Exclude all image files except `.svg` and all audio asset files.\n"
                    "7. **Assets:** Include only asset files with the `.svg` extension.\n"
                    "8. **Data Requirement:** Set `need_data` to True if the file requires data from the original instruction, False otherwise.\n"
                    "9. **Prompt:** Create a comprehensive prompt for each file, detailing the specific tasks, features, and integrations required based on the user's initial instruction.\n"
                    "10. **SVG Files:** For all SVG files, provide a detailed prompt including what to build, theme colors, purpose of use, and a comprehensive description to guide other agents in creating the image.\n"
                    "11. **UI Design:** For UI-related tasks, emphasize designing an elegant, professional, and intuitive user interface. Provide specific guidelines for layout, color scheme, and user experience. Ensure careful integration with other files and components.\n\n"
                    "Response Format:\n"
                    "Provide a JSON object in the following structure:\n"
                    "{\n"
                    '    "steps": [\n'
                    '        {\n'
                    '            "file_name": "/full/path/to/file",\n'
                    '            "techStack": "python",\n'
                    '            "need_data": true,\n'
                    '            "prompt": "Detailed description of tasks for this file"\n'
                    '        },\n'
                    '        {\n'
                    '            "file_name": "/full/path/to/another/file",\n'
                    '            "techStack": "java",\n'
                    '            "need_data": false,\n'
                    '            "prompt": "Comprehensive instructions for implementing this file"\n'
                    '        }\n'
                    '    ]\n'
                    "}\n\n"
                    "Important: Respond with only the specified JSON content. Do not include additional text, explanations, or Markdown formatting. Ensure files are correctly ordered according to Pyramid architecture best practices for optimal integration and maintainability. The `techStack` field should indicate the programming language or technology used in the file, such as 'python', 'java', 'javascript', etc. The `need_data` field should be true if the file requires data from the original instruction, false otherwise, following Python's valid boolean syntax. The `prompt` field should contain a detailed, comprehensive description of all tasks, features, and integrations required for the file, based on the user's initial instruction. For UI-related files, include specific guidelines for creating an elegant, professional, and intuitive interface, considering layout, color scheme, and user experience. For SVG files, include specific details about what to build, theme colors, purpose of use, and any other relevant information to guide the creation process.\n\n"
                    f"Current working project is {self.repo.get_repo_path()}\n\n"
                    "Return only valid JSON without Markdown symbols or invalid escapes."
                )
            },
            {
                "role": "user",
                "content": f"Create an ordered list of files to implement following Pyramid architecture best practices. Ensure foundational files are listed first, progressing to more complex files requiring greater context. Only select files from this list:\n{file_list}\n\nInclude the `file_name` (full path), `techStack`, `need_data`, and `prompt` for each file in the specified JSON format. Ensure that the `file_name` respects the root path and the correct relative path from the original instruction. Set `need_data` to true if the file requires data from the original instruction, false otherwise, using Python's valid boolean syntax. For the `prompt` field, provide a comprehensive description of all tasks, features, and integrations required for each file, based on the user's initial instruction. Be thorough and specific to avoid missing any crucial details. For UI-related files, emphasize designing an elegant, professional, and intuitive user interface with specific guidelines for layout, color scheme, and user experience. Ensure careful integration with other files and components. For SVG files, include detailed information about what to build, theme colors, purpose of use, and any other relevant details to guide the creation process. Here is the original instruction: {instruction}"
            }
        ]

        try:
            response = await self.ai.prompt(messages, self.max_tokens, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f"TaskPlanner failed to get task plan: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, instruction, file_lists):
        """
        Get development plans based on the user's instruction.

        Args:
            instruction (str): The user's instruction for task planning.

        Returns:
            dict: Development plan or error reason.
        """
        plan = await self.get_task_plan(instruction, file_lists)
        return plan
