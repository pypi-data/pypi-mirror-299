import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class IdeaDevelopment:
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


        all_file_contents = self.repo.print_summarize_with_tree()

            # Start of Selection
        system_prompt = (
                    f"You are a senior {role}. Analyze the project files and develop a comprehensive development plan. Follow these guidelines meticulously:\n\n"

                    "**Guidelines:**\n"
                    "- **Enterprise Standards:** Ensure scalability, performance, and security are top priorities.\n"
                    "- **External Resources:** Assume external data from Zinley crawler agent will be provided later. Guide coders to integrate it properly without including data directly. Specify which files will need to read the crawled data when another agent works on them.\n"
                    "- **No Source Code:** Focus on technical and architectural planning; exclude source code.\n"
                    "- **File Integrity:** Modify existing files without renaming. Create new files if necessary, detailing updates and integrations.\n"
                    "- **Image Assets:** Follow strict specifications:\n"
                    "    - Use `.svg` for icons, logos, illustrations, simple graphics, and interactive graphics.\n"
                    "    - Use `.png` or `.jpg` for product representations and large images that require high quality.\n"
                    "    - **File Sizes:** Icons/logos: 24x24px-512x512px; Illustrations: ≤1024x1024px; Product images: ≤2048x2048px.\n"
                    "    - **Directories:** `assets/icons/`, `assets/illustrations/`, `assets/products/`.\n"
                    "    - **Naming:** Use descriptive names (e.g., `latte.svg`).\n"
                    "    - **Plan Submission:** Include detailed plans for all new files and images with dimensions.\n"
                    "- **README:** Mention inclusion or update of README without detailing it. Focus on technical and structural planning.\n"
                    "- **Structure & Naming:** Propose clear, logical file and folder structures for scalability and expansion. Describe directory structure and navigation.\n"
                    "- **UI Design:** Ensure well-designed UI for web/app, tailored for each platform.\n\n"

                    "**2. Strict Guidelines:**\n"
                    "**2.0 Ultimate Goal:**\n"
                    "- State the project's goal, final product's purpose, target users, and how it meets their needs. Concisely summarize objectives and deliverables.\n\n"

                    "**2.1 Existing Files (mention if need for this task only):**\n"
                    "- **Detailed Implementations:** Provide thorough descriptions of implementations in existing files, specifying the purpose and functionality of each.\n"
                    "- **Algorithms & Dependencies:** Suggest necessary algorithms, dependencies, functions, or classes for each existing file.\n"
                    "- **Interdependencies:** Identify dependencies or relationships with other files and their impact on the system architecture.\n"
                    "- **Asset Usage:** Describe the use of image, video, or audio assets in each existing file, specifying filenames and their placement. Use `.svg` formats when applicable.\n"
                    "- **Modification Guidelines:** Specify what modifications are needed in each existing file to align with the new development plan.\n"
                    
                    "**2.2 New Files:**\n"
                    
                     "**File Organization:**\n"
                    "- **Enterprise Setup:** Organize all files deeply following enterprise setup standards. Ensure that the file hierarchy is logical, scalable, and maintainable.\n"
                    "- **Final Tree Structure:** The final file tree must mirror the proposed structure, ensuring consistency between planning and implementation.\n"
                    "- **Documentation:** Provide a detailed description of the file and folder structure, explaining the purpose of each directory and how they interrelate.\n\n"

                    "- **Enterprise-Level Structure:** Ensure that new files are structured according to enterprise-level standards, avoiding unrelated functionalities within single files.\n"
                    "- **Detailed Implementations:** Provide comprehensive details for implementations in each new file, including the purpose and functionality.\n"
                    "- **Necessary Components:** Suggest required algorithms, dependencies, functions, or classes for each new file.\n"
                    "- **System Integration:** Explain how each new file will integrate with existing systems, including data flow, API calls, or interactions.\n"
                    "- **Asset Integration:** Describe the usage of image, video, or audio assets in new files, specifying filenames and their placement. Prefer `.svg` formats for new images.\n"
                    "- **Image Specifications:** Provide detailed descriptions of new images, including content, style, colors, dimensions, and purpose. Specify exact dimensions per guidelines (e.g., Create `latte.svg` (128x128px), `cappuccino.svg` (128x128px)).\n"
                    "- **Image Paths:** For all new generated images, include the full path for each image (e.g., `assets/icons/latte.svg`, `assets/products/cappuccino.png`).\n"
                    "- **Directory Structure:** Define the expected new tree structure after implementation, ensuring it aligns with enterprise setup standards.\n"
                    f"- **Project Paths:** Mention the main new project folder for all new files and the current project root path: {self.repo.get_repo_path()}.\n"
                    "- **Project Setup:** Ensure all necessary setup files are included, such as `index.js` for React projects, `package.json` for Node.js projects, or any other crucial configuration files. Do not use ellipsis (...) or 'etc.' when listing files; be explicit and comprehensive.\n"
                    "- **Critical File Check:** Carefully review and ensure that all critical files are included in the plan. For JavaScript projects, must check for and include `index.js` in both client and server directories if applicable. For other project types, ensure all essential setup and configuration files are accounted for.\n"

                    "**2.3 Existing Context Files (Must follow, mention if need for this task only):**\n"
                    "- Provide a list of relevant existing context files necessary for understanding and completing the task, such as configuration files, environment settings, or other critical resources. Explain their importance and how they will be used.\n"
                    "- Exclude non-essential files like assets, development environment configurations, and IDE-specific files. Clarify why these files are not included.\n"
                    "- Ensure there is no overlap with Existing Files (2.1) and New Files (2.2). Clearly differentiate their roles and usage. Provide explanations to avoid confusion.\n"
                    "- Existing Context Files will be used for RAG purposes, so please list relevant files needed for these tasks if any.\n"
                    "- If no relevant context files are found, mention this briefly, confirming that all necessary files have been accounted for. Clearly state that all essential files are included and identified.\n"

                    
                    "**2.4 Dependencies:**\n"
                    "- **Dependency Listing:** Enumerate all dependencies essential needed for the task, indicating whether they are already installed or need to be installed. Include their roles and relevance to the project.\n"
                    "- **Version Management:** Use the latest versions of dependencies; specify version numbers only if explicitly requested.\n"
                    "- **CLI-Installable:** Include only dependencies that can be installed via the command line interface (CLI), specifying the installation method (e.g., npm, pip).\n"
                    "- **Installation Commands:** Provide exact CLI commands for installing dependencies without including version numbers unless specified.\n"
                    "- **Exclusions:** Exclude dependencies that require IDE manipulation or cannot be installed via CLI.\n"
                    "- **Compatibility Assurance:** Ensure compatibility among all dependencies and with the existing system architecture.\n\n"

                    "**2.5 APIs:**\n"
                    "- **API Usage:** Clearly mention any APIs that need to be used in the project. Provide details on their purpose, endpoints, and integration points. Include the full API call links, not just domains (e.g., 'https://api.example.com/v1/users' instead of just 'api.example.com').\n"
                    "- **Authentication:** If applicable, specify the authentication methods required for each API (e.g., API keys, OAuth). Include the full authentication endpoint URLs where relevant.\n"
                    "- **Data Flow:** Describe how data will flow between the application and the APIs, including any data transformations or processing required. Specify the exact API endpoints involved in each data flow.\n"
                    "- **Error Handling:** Outline strategies for handling API errors and rate limiting. Include specific error endpoint URLs if applicable.\n"
                    "- **Documentation:** Provide full links to the API documentation for further details, ensuring they lead directly to the relevant sections.\n\n"

                    "**(No additional information needed):**\n"

                    "**No Yapping:** Provide concise, focused responses without unnecessary elaboration or repetition. Stick strictly to the requested information and guidelines."

                    "**2.6 Crawl Data Integration:**\n"
                    "- If crawl data is provided, specify which file(s) should access this data.\n"
                    "- Explain how the crawl data should be integrated into the project structure.\n"
                    "- Provide clear instructions on how to use the crawl data within the specified files.\n"
                    "- If no crawl data is provided, state that no integration is needed at this time.\n"
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
            logger.info(f"File does not exist: {file_path}")
            return ""

        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.info(f"IdeaDevelopment agent failed to read file {file_path} with {encoding} encoding: {e}")

        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.info(f"IdeaDevelopment agent failed to read file {file_path} in binary mode: {e}")

        return ""

    async def get_idea_plan(self, user_prompt):
        
        prompt = (
            f"Follow the user prompt strictly and provide a detailed, step-by-step no-code plan. "
            f"Do not include any code in your response. Focus on high-level concepts, strategies, and approaches. "
            f"Here's the user prompt:\n\n{user_prompt}\n\n"
            f"Remember, your response should be a comprehensive plan without any code snippets."
        )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            response = await self.ai.stream_prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
            return response
        except Exception as e:
            logger.info(f"IdeaDevelopment agent failed: {e}")
            return {
                "reason": str(e)
            }

    async def get_idea_plans(self, user_prompt):
        return await self.get_idea_plan(user_prompt)
