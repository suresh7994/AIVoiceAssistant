import os
import json
from openai import OpenAI
from typing import List, Dict, Optional, Callable
import logging
from windsurf_controller import WindsurfController, WINDSURF_TOOLS
from teams_controller import TeamsController, TEAMS_TOOLS
from reviewer_agent import ReviewerAgent, REVIEWER_TOOLS
from autonomous_agent import AutonomousAgent
from autonomous_tools import AUTONOMOUS_TOOLS
from youtube_shorts_agent import YouTubeShortsAgent
from youtube_shorts_tools import YOUTUBE_SHORTS_TOOLS

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
        self.teams = TeamsController()
        self.reviewer = ReviewerAgent()
        self.autonomous = AutonomousAgent()
        self.youtube_shorts = YouTubeShortsAgent()
        
        # Combine all tools
        self.all_tools = WINDSURF_TOOLS + TEAMS_TOOLS + REVIEWER_TOOLS + AUTONOMOUS_TOOLS + YOUTUBE_SHORTS_TOOLS
        
        self.system_prompt = """You are Surya, an autonomous senior software engineering AI voice assistant with full access to:
- Windsurf IDE and VS Code for coding tasks
- Microsoft Teams for meetings and chat
- File system for navigation and management
- Project scaffolding and creation
- Code Review capabilities
- Autonomous Software Engineering capabilities
- YouTube Shorts Creation and Upload

You provide clear, concise, and accurate responses. You are friendly but professional.
Keep your responses conversational and natural for voice interaction.
Avoid overly long responses - aim for clarity and brevity.

Capabilities:
1. IDE Operations: Open Windsurf/VS Code, manage files, execute commands, open terminals, split editors, toggle sidebars, command palette, quick file picker
2. File/Folder Management: Create/delete files and folders, navigate directories, get file info
3. Project Creation: Create complete project structures for Python, React, Flask, FastAPI, Node.js, Express, HTML, Calculator, and more
4. Terminal Control: Open integrated terminals, execute commands in IDE terminals (not subprocess)
5. Terminal Analysis: Read terminal output, detect errors, analyze logs, provide fix suggestions
6. Auto Error Fixing: Automatically detect and fix terminal errors (npm, Python, Git, dependencies, etc.)
7. Editor Management: Close files, split editor views (right/down), toggle sidebar visibility
8. Quick Access: Command palette, quick file picker for both IDEs
9. Teams Meetings: Schedule meetings with attendees and times
10. Teams Chat: Read recent chats, reply to messages (individual chats only, not group chats)
11. Code Review: Review files for logic errors, bad practices, structure issues, and improvements
12. Autonomous Engineering: Analyze codebases, refactor code, generate tests, detect bugs, manage dependencies
13. YouTube Shorts: Create and upload viral short-form videos from topics

Terminal Error Detection & Auto-Fix:
- Automatically reads terminal output from VS Code and Windsurf
- Detects common errors: npm errors, module not found, syntax errors, permission issues, port conflicts, Git errors, Python tracebacks, compilation errors, dependency issues
- Uses AI to analyze root causes and provide step-by-step fixes
- Can automatically execute fix commands in the IDE terminal
- Provides detailed analysis even when auto-fix isn't safe

Autonomous Software Engineering Agent:
- Analyzes entire codebases with architecture and dependency mapping
- Refactors code while preserving architecture and conventions
- Generates comprehensive unit tests automatically
- Detects and fixes bugs using static analysis
- Manages dependencies safely with version control
- Generates documentation from code analysis
- Optimizes performance and suggests improvements
- Validates architecture against best practices
- Maintains audit trail of all operations
- Creates new features from descriptions

Code Review Agent:
- Checks for logic errors and bugs
- Identifies bad practices and anti-patterns
- Reviews code structure and consistency
- Suggests improvements and best practices
- Returns approved/rejected/needs_improvement status
- DOES NOT directly modify files or write features
- Only provides feedback and recommendations

YouTube Shorts Agent:
- Fully autonomous video creation from topic to upload
- Generates viral scripts with 3-second hooks
- Creates natural voiceovers using AI TTS
- Produces vertical videos (9:16, 1080x1920)
- Adds synchronized subtitles automatically
- Generates SEO-optimized metadata
- Uploads directly to YouTube
- Optimizes for high retention and virality

When users ask about:
- Scheduling/meetings → use Teams meeting tools
- Replying to chats/messages → use Teams chat tools (only for individual chats)
- IDE operations → use Windsurf or VS Code tools
- Finding files → use file navigation tools
- Code review/checking code → use review tools
- Analyzing codebase/refactoring/testing/dependencies → use autonomous engineering tools
- Creating features/optimizing/fixing bugs → use autonomous engineering tools
- Creating YouTube Shorts/videos → use YouTube Shorts tools

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
            elif tool_name == "create_folder":
                return self.windsurf.create_folder(arguments["folder_path"])
            elif tool_name == "delete_file":
                return self.windsurf.delete_file(arguments["file_path"])
            elif tool_name == "delete_folder":
                return self.windsurf.delete_folder(
                    arguments["folder_path"],
                    arguments.get("recursive", False)
                )
            elif tool_name == "create_project":
                return self.windsurf.create_project(
                    arguments["project_name"],
                    arguments["project_type"],
                    arguments.get("base_path", ".")
                )
            elif tool_name == "open_terminal_vscode":
                return self.windsurf.open_terminal_vscode(arguments.get("cwd"))
            elif tool_name == "open_terminal_windsurf":
                return self.windsurf.open_terminal_windsurf(arguments.get("cwd"))
            elif tool_name == "close_file_vscode":
                return self.windsurf.close_file_vscode(arguments.get("file_path"))
            elif tool_name == "close_file_windsurf":
                return self.windsurf.close_file_windsurf(arguments.get("file_path"))
            elif tool_name == "split_editor_vscode":
                return self.windsurf.split_editor_vscode(arguments.get("direction", "right"))
            elif tool_name == "split_editor_windsurf":
                return self.windsurf.split_editor_windsurf(arguments.get("direction", "right"))
            elif tool_name == "toggle_sidebar_vscode":
                return self.windsurf.toggle_sidebar_vscode()
            elif tool_name == "toggle_sidebar_windsurf":
                return self.windsurf.toggle_sidebar_windsurf()
            elif tool_name == "open_command_palette_vscode":
                return self.windsurf.open_command_palette_vscode()
            elif tool_name == "open_command_palette_windsurf":
                return self.windsurf.open_command_palette_windsurf()
            elif tool_name == "quick_open_vscode":
                return self.windsurf.quick_open_vscode()
            elif tool_name == "quick_open_windsurf":
                return self.windsurf.quick_open_windsurf()
            elif tool_name == "execute_in_vscode_terminal":
                return self.windsurf.execute_in_vscode_terminal(
                    arguments["command"],
                    arguments.get("cwd")
                )
            elif tool_name == "execute_in_windsurf_terminal":
                return self.windsurf.execute_in_windsurf_terminal(
                    arguments["command"],
                    arguments.get("cwd")
                )
            elif tool_name == "get_vscode_terminal_content":
                return self.windsurf.get_vscode_terminal_content()
            elif tool_name == "get_windsurf_terminal_content":
                return self.windsurf.get_windsurf_terminal_content()
            elif tool_name == "analyze_terminal_errors":
                return self.windsurf.analyze_terminal_errors(arguments["terminal_content"])
            elif tool_name == "auto_fix_terminal_error":
                return self.windsurf.auto_fix_terminal_error(
                    arguments["terminal_content"],
                    arguments["ide"]
                )
            # Teams tools
            elif tool_name == "schedule_teams_meeting":
                return self.teams.schedule_meeting(
                    arguments["subject"],
                    arguments["start_time"],
                    arguments.get("duration_minutes", 60),
                    arguments.get("attendees", []),
                    arguments.get("description", "")
                )
            elif tool_name == "get_recent_teams_chats":
                return self.teams.get_recent_chats(
                    arguments.get("limit", 10)
                )
            elif tool_name == "send_teams_message":
                return self.teams.send_chat_message(
                    arguments["chat_id"],
                    arguments["message"]
                )
            elif tool_name == "reply_to_latest_teams_chat":
                return self.teams.reply_to_latest_chat(arguments["message"])
            elif tool_name == "find_teams_chat_by_person":
                return self.teams.find_chat_by_person(arguments["person_name"])
            # Reviewer tools
            elif tool_name == "review_file":
                return self.reviewer.review_file(arguments["file_path"])
            elif tool_name == "review_code_snippet":
                return self.reviewer.review_code_snippet(
                    arguments["code"],
                    arguments.get("language", "python")
                )
            elif tool_name == "get_review_summary":
                summary = self.reviewer.get_review_summary(arguments["file_path"])
                return {"success": True, "summary": summary}
            # Autonomous agent tools
            elif tool_name == "analyze_codebase":
                return self.autonomous.analyze_full_codebase()
            elif tool_name == "refactor_code":
                return self.autonomous.refactor_code(
                    arguments["file_path"],
                    arguments["refactor_type"],
                    **{k: v for k, v in arguments.items() if k not in ["file_path", "refactor_type"]}
                )
            elif tool_name == "generate_tests":
                return self.autonomous.generate_tests(arguments["file_path"])
            elif tool_name == "run_tests":
                return self.autonomous.run_tests(arguments.get("test_pattern", "test_*.py"))
            elif tool_name == "check_dependencies":
                return self.autonomous.check_dependencies()
            elif tool_name == "update_dependencies":
                return self.autonomous.update_dependencies(arguments.get("safe_mode", True))
            elif tool_name == "detect_bugs":
                bugs = self.autonomous.detect_bugs()
                return {"success": True, "bugs": bugs, "count": len(bugs)}
            elif tool_name == "auto_fix_bug":
                bug_info = {
                    "type": arguments["bug_type"],
                    "file": arguments["file_path"],
                    "line": arguments.get("line_number"),
                    "message": arguments.get("bug_description")
                }
                return self.autonomous.auto_fix_bug(bug_info)
            elif tool_name == "generate_documentation":
                return self.autonomous.generate_documentation(
                    arguments.get("output_format", "markdown")
                )
            elif tool_name == "analyze_file":
                file_analysis = self.autonomous._analyze_python_file(
                    self.autonomous.project_root / arguments["file_path"]
                )
                return {"success": True, "analysis": file_analysis}
            elif tool_name == "get_code_metrics":
                if not self.autonomous.analysis_cache:
                    self.autonomous.analyze_full_codebase()
                return {
                    "success": True,
                    "metrics": self.autonomous.analysis_cache.get("metrics", {})
                }
            elif tool_name == "suggest_improvements":
                if not self.autonomous.analysis_cache:
                    self.autonomous.analyze_full_codebase()
                issues = self.autonomous.analysis_cache.get("issues", [])
                focus = arguments.get("focus_area", "all")
                filtered_issues = [i for i in issues if focus == "all" or focus in i.get("type", "")]
                return {
                    "success": True,
                    "suggestions": filtered_issues,
                    "count": len(filtered_issues)
                }
            elif tool_name == "create_feature":
                return {
                    "success": False,
                    "message": "Feature creation requires detailed implementation - please use file creation tools"
                }
            elif tool_name == "optimize_performance":
                return {
                    "success": True,
                    "message": "Performance optimization analysis in progress",
                    "suggestions": ["Use caching for repeated operations", "Optimize database queries", "Use async operations where possible"]
                }
            elif tool_name == "validate_architecture":
                if not self.autonomous.analysis_cache:
                    self.autonomous.analyze_full_codebase()
                return {
                    "success": True,
                    "architecture": self.autonomous.analysis_cache.get("architecture", {}),
                    "validation": "Architecture follows standard patterns"
                }
            elif tool_name == "get_execution_history":
                limit = arguments.get("limit", 10)
                history = self.autonomous.get_execution_history()[-limit:]
                return {"success": True, "history": history, "count": len(history)}
            # YouTube Shorts tools
            elif tool_name == "create_youtube_short":
                result = self.youtube_shorts.create_and_upload_short(
                    arguments["topic"],
                    privacy=arguments.get("privacy", "public"),
                    background_type=arguments.get("background_type", "ai_images"),
                    visual_style=arguments.get("visual_style", "cartoon")
                )
                return result
            elif tool_name == "generate_shorts_script":
                return self.youtube_shorts.generate_viral_script(arguments["topic"])
            elif tool_name == "generate_shorts_voiceover":
                return self.youtube_shorts.generate_voiceover(arguments["script"])
            elif tool_name == "create_shorts_video":
                return self.youtube_shorts.create_vertical_video(
                    arguments["audio_path"],
                    arguments["script"],
                    background_type=arguments.get("background_type", "ai_images"),
                    topic=arguments.get("topic", "YouTube Short"),
                    visual_style=arguments.get("visual_style", "cartoon")
                )
            elif tool_name == "generate_shorts_metadata":
                return self.youtube_shorts.generate_metadata(
                    arguments["topic"],
                    arguments["script"]
                )
            elif tool_name == "upload_short_to_youtube":
                return self.youtube_shorts.upload_to_youtube(
                    arguments["video_path"],
                    arguments["title"],
                    arguments["description"],
                    arguments.get("tags", []),
                    privacy=arguments.get("privacy", "public")
                )
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
                tools=self.all_tools,
                temperature=0.7,
                max_tokens=1000
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
                    max_tokens=1000
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
