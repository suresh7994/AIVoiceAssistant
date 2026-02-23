import os
import json
from openai import OpenAI
from typing import List, Dict, Optional, Callable
import logging
from windsurf_controller import WindsurfController, WINDSURF_TOOLS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentBrain:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = 20
        self.windsurf = WindsurfController()
        
        self.system_prompt = """You are Surya, a helpful, professional, and intelligent AI voice assistant with access to Windsurf IDE and VS Code.
You can help users with coding tasks, file operations, and IDE commands for both Windsurf and Visual Studio Code.
You provide clear, concise, and accurate responses. You are friendly but professional.
Keep your responses conversational and natural for voice interaction.
Avoid overly long responses - aim for clarity and brevity.

You have intelligent file and folder finding capabilities:
- When users ask to find or locate files/folders, use find_file or find_folder tools
- You can automatically identify and navigate to any folder or file
- You can get information about files and folders
- You can change directories and show current location

When users ask you to perform IDE operations, use the available tools to help them.
When users mention VS Code, Visual Studio Code, or code editor, use the VS Code tools.
When users mention Windsurf, use the Windsurf tools.
Your name is Surya and you respond when users say 'Hello Surya' or 'Hi Surya'."""
        
        self.conversation_history.append({
            "role": "system",
            "content": self.system_prompt
        })
    
    def _execute_tool(self, tool_name: str, arguments: Dict) -> Dict:
        """Execute a Windsurf or VS Code tool function"""
        try:
            if tool_name == "open_windsurf":
                return self.windsurf.open_windsurf(arguments.get("path"))
            elif tool_name == "open_vscode":
                return self.windsurf.open_vscode(arguments.get("path"))
            elif tool_name == "open_file_vscode":
                return self.windsurf.open_file_vscode(arguments["file_path"])
            elif tool_name == "open_file":
                return self.windsurf.open_file(arguments["file_path"])
            elif tool_name == "create_file":
                return self.windsurf.create_file(
                    arguments["file_path"],
                    arguments.get("content", "")
                )
            elif tool_name == "read_file":
                return self.windsurf.read_file(arguments["file_path"])
            elif tool_name == "write_file":
                return self.windsurf.write_file(
                    arguments["file_path"],
                    arguments["content"]
                )
            elif tool_name == "search_in_files":
                return self.windsurf.search_in_files(
                    arguments["search_term"],
                    arguments.get("directory", ".")
                )
            elif tool_name == "run_terminal_command":
                return self.windsurf.run_terminal_command(
                    arguments["command"],
                    arguments.get("cwd")
                )
            elif tool_name == "list_files":
                return self.windsurf.list_files(
                    arguments.get("directory", ".")
                )
            elif tool_name == "find_file":
                return self.windsurf.find_file(
                    arguments["filename"],
                    arguments.get("search_path", ".")
                )
            elif tool_name == "find_folder":
                return self.windsurf.find_folder(
                    arguments["foldername"],
                    arguments.get("search_path", ".")
                )
            elif tool_name == "get_current_directory":
                return self.windsurf.get_current_directory()
            elif tool_name == "change_directory":
                return self.windsurf.change_directory(arguments["path"])
            elif tool_name == "get_file_info":
                return self.windsurf.get_file_info(arguments["path"])
            else:
                return {"success": False, "error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def process_input(
        self, 
        user_input: str, 
        stream_callback: Optional[Callable[[str], None]] = None
    ) -> str:
        try:
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            if len(self.conversation_history) > self.max_history:
                self.conversation_history = [
                    self.conversation_history[0]
                ] + self.conversation_history[-(self.max_history-1):]
            
            # First API call with tools
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                tools=WINDSURF_TOOLS,
                temperature=0.7,
                max_tokens=500
            )
            
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            
            # If AI wants to use tools
            if tool_calls:
                self.conversation_history.append(response_message)
                
                # Execute each tool call
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    logger.info(f"Executing tool: {function_name} with args: {function_args}")
                    
                    # Execute the tool
                    tool_result = self._execute_tool(function_name, function_args)
                    
                    # Add tool result to conversation
                    self.conversation_history.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(tool_result)
                    })
                
                # Get final response after tool execution
                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history,
                    temperature=0.7,
                    max_tokens=500
                )
                
                response_text = final_response.choices[0].message.content
            else:
                # No tools needed, use direct response
                response_text = response_message.content
            
            if stream_callback:
                stream_callback(response_text)
            
            self.conversation_history.append({
                "role": "assistant",
                "content": response_text
            })
            
            return response_text
        
        except Exception as e:
            error_msg = f"Error processing request: {str(e)}"
            logger.error(error_msg)
            return "I apologize, but I encountered an error processing your request. Please try again."
    
    def clear_history(self):
        self.conversation_history = [{
            "role": "system",
            "content": self.system_prompt
        }]
    
    def set_system_prompt(self, prompt: str):
        self.system_prompt = prompt
        self.conversation_history[0] = {
            "role": "system",
            "content": prompt
        }
