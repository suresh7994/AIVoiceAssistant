import subprocess
import json
import logging
from typing import Optional, Dict, Any
from project_templates import PROJECT_TEMPLATES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WindsurfController:
    """Controller for executing Windsurf IDE and VS Code operations via CLI"""
    
    def __init__(self):
        self.windsurf_cli = "windsurf"
        self.windsurf_app_name = "Windsurf"
        self.vscode_cli = "code"
        self.vscode_app_name = "Visual Studio Code"
    
    def execute_command(self, command: str, args: Optional[list] = None) -> Dict[str, Any]:
        """Execute a Windsurf CLI command"""
        try:
            cmd = [self.windsurf_cli, command]
            if args:
                cmd.extend(args)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timeout"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def open_file(self, file_path: str) -> Dict[str, Any]:
        """Open a file in Windsurf"""
        return self.execute_command("open", [file_path])
    
    def create_file(self, file_path: str, content: str = "") -> Dict[str, Any]:
        """Create a new file"""
        try:
            import os
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(content)
            return {"success": True, "message": f"File created: {file_path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_folder(self, folder_path: str) -> Dict[str, Any]:
        """Create a new folder/directory"""
        try:
            import os
            os.makedirs(folder_path, exist_ok=True)
            return {"success": True, "message": f"Folder created: {folder_path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete_file(self, file_path: str) -> Dict[str, Any]:
        """Delete a file"""
        try:
            import os
            if not os.path.exists(file_path):
                return {"success": False, "error": f"File does not exist: {file_path}"}
            if os.path.isdir(file_path):
                return {"success": False, "error": f"Path is a directory, not a file: {file_path}"}
            os.remove(file_path)
            return {"success": True, "message": f"File deleted: {file_path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete_folder(self, folder_path: str, recursive: bool = False) -> Dict[str, Any]:
        """Delete a folder/directory"""
        try:
            import os
            import shutil
            if not os.path.exists(folder_path):
                return {"success": False, "error": f"Folder does not exist: {folder_path}"}
            if not os.path.isdir(folder_path):
                return {"success": False, "error": f"Path is not a directory: {folder_path}"}
            
            if recursive:
                shutil.rmtree(folder_path)
                return {"success": True, "message": f"Folder and contents deleted: {folder_path}"}
            else:
                os.rmdir(folder_path)
                return {"success": True, "message": f"Empty folder deleted: {folder_path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_project(self, project_name: str, project_type: str, base_path: str = ".") -> Dict[str, Any]:
        """Create a complete project structure based on technology type"""
        try:
            import os
            project_path = os.path.join(base_path, project_name)
            
            project_type_lower = project_type.lower()
            if project_type_lower not in PROJECT_TEMPLATES:
                return {
                    "success": False,
                    "error": f"Unknown project type: {project_type}. Supported: {', '.join(PROJECT_TEMPLATES.keys())}"
                }
            
            # Create project using template
            result = PROJECT_TEMPLATES[project_type_lower](project_path, project_name)
            return result
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def read_file(self, file_path: str) -> Dict[str, Any]:
        """Read file contents"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            return {"success": True, "content": content}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def write_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Write content to a file"""
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            return {"success": True, "message": f"File updated: {file_path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def search_in_files(self, search_term: str, directory: str = ".") -> Dict[str, Any]:
        """Search for text in files"""
        try:
            result = subprocess.run(
                ["grep", "-r", search_term, directory],
                capture_output=True,
                text=True,
                timeout=10
            )
            return {
                "success": True,
                "results": result.stdout
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run_terminal_command(self, command: str, cwd: Optional[str] = None) -> Dict[str, Any]:
        """Run a terminal command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=30
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timeout"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_files(self, directory: str = ".") -> Dict[str, Any]:
        """List files and directories"""
        try:
            import os
            items = os.listdir(directory)
            return {
                "success": True,
                "files": [f for f in items if os.path.isfile(os.path.join(directory, f))],
                "directories": [d for d in items if os.path.isdir(os.path.join(directory, d))]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_file(self, filename: str, search_path: str = ".") -> Dict[str, Any]:
        """Find a file by name in the given path and subdirectories"""
        try:
            import os
            matches = []
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if filename.lower() in file.lower():
                        full_path = os.path.join(root, file)
                        matches.append(full_path)
            
            if matches:
                return {
                    "success": True,
                    "message": f"Found {len(matches)} file(s)",
                    "files": matches
                }
            else:
                return {
                    "success": False,
                    "message": f"No files found matching '{filename}'"
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_folder(self, foldername: str, search_path: str = ".") -> Dict[str, Any]:
        """Find a folder by name in the given path and subdirectories"""
        try:
            import os
            matches = []
            for root, dirs, files in os.walk(search_path):
                for dir_name in dirs:
                    if foldername.lower() in dir_name.lower():
                        full_path = os.path.join(root, dir_name)
                        matches.append(full_path)
            
            if matches:
                return {
                    "success": True,
                    "message": f"Found {len(matches)} folder(s)",
                    "folders": matches
                }
            else:
                return {
                    "success": False,
                    "message": f"No folders found matching '{foldername}'"
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_current_directory(self) -> Dict[str, Any]:
        """Get the current working directory"""
        try:
            import os
            cwd = os.getcwd()
            return {
                "success": True,
                "directory": cwd,
                "message": f"Current directory: {cwd}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def change_directory(self, path: str) -> Dict[str, Any]:
        """Change the current working directory"""
        try:
            import os
            os.chdir(path)
            new_cwd = os.getcwd()
            return {
                "success": True,
                "directory": new_cwd,
                "message": f"Changed to directory: {new_cwd}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_file_info(self, path: str) -> Dict[str, Any]:
        """Get information about a file or folder"""
        try:
            import os
            from datetime import datetime
            
            if not os.path.exists(path):
                return {"success": False, "error": f"Path does not exist: {path}"}
            
            stat_info = os.stat(path)
            is_file = os.path.isfile(path)
            is_dir = os.path.isdir(path)
            
            info = {
                "success": True,
                "path": path,
                "type": "file" if is_file else "directory",
                "size": stat_info.st_size if is_file else None,
                "modified": datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                "created": datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            if is_dir:
                items = os.listdir(path)
                info["item_count"] = len(items)
            
            return info
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def is_windsurf_running(self) -> bool:
        """Check if Windsurf IDE is currently running"""
        try:
            result = subprocess.run(
                ["pgrep", "-f", "Windsurf"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0 and bool(result.stdout.strip())
        except Exception as e:
            logger.error(f"Error checking if Windsurf is running: {e}")
            return False
    
    def open_windsurf(self, path: Optional[str] = None) -> Dict[str, Any]:
        """Open Windsurf IDE, optionally with a specific path"""
        try:
            if self.is_windsurf_running():
                message = "Windsurf IDE is already running"
                logger.info(message)
                
                # If path provided, try to open it
                if path:
                    result = subprocess.run(
                        ["open", "-a", self.windsurf_app_name, path],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if result.returncode == 0:
                        return {"success": True, "message": f"Opened {path} in Windsurf"}
                    else:
                        return {"success": False, "error": result.stderr}
                else:
                    # Just bring Windsurf to front
                    subprocess.run(
                        ["open", "-a", self.windsurf_app_name],
                        capture_output=True,
                        timeout=5
                    )
                    return {"success": True, "message": message}
            else:
                # Launch Windsurf
                logger.info("Launching Windsurf IDE...")
                if path:
                    result = subprocess.run(
                        ["open", "-a", self.windsurf_app_name, path],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                else:
                    result = subprocess.run(
                        ["open", "-a", self.windsurf_app_name],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                
                if result.returncode == 0:
                    return {"success": True, "message": "Windsurf IDE launched successfully"}
                else:
                    return {"success": False, "error": result.stderr or "Failed to launch Windsurf"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def is_vscode_running(self) -> bool:
        """Check if VS Code is currently running"""
        try:
            result = subprocess.run(
                ["pgrep", "-f", "Visual Studio Code"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0 and bool(result.stdout.strip())
        except Exception as e:
            logger.error(f"Error checking if VS Code is running: {e}")
            return False
    
    def open_vscode(self, path: Optional[str] = None) -> Dict[str, Any]:
        """Open VS Code, optionally with a specific path"""
        try:
            if self.is_vscode_running():
                message = "VS Code is already running"
                logger.info(message)
                
                # If path provided, try to open it
                if path:
                    result = subprocess.run(
                        ["open", "-a", self.vscode_app_name, path],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if result.returncode == 0:
                        return {"success": True, "message": f"Opened {path} in VS Code"}
                    else:
                        return {"success": False, "error": result.stderr}
                else:
                    # Just bring VS Code to front
                    subprocess.run(
                        ["open", "-a", self.vscode_app_name],
                        capture_output=True,
                        timeout=5
                    )
                    return {"success": True, "message": message}
            else:
                # Launch VS Code
                logger.info("Launching VS Code...")
                if path:
                    result = subprocess.run(
                        ["open", "-a", self.vscode_app_name, path],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                else:
                    result = subprocess.run(
                        ["open", "-a", self.vscode_app_name],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                
                if result.returncode == 0:
                    return {"success": True, "message": "VS Code launched successfully"}
                else:
                    return {"success": False, "error": result.stderr or "Failed to launch VS Code"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def open_file_vscode(self, file_path: str) -> Dict[str, Any]:
        """Open a file in VS Code using the code CLI"""
        try:
            result = subprocess.run(
                [self.vscode_cli, file_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return {"success": True, "message": f"Opened {file_path} in VS Code"}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def quick_open_windsurf(self):
        """Open quick file picker in Windsurf using Cmd+P"""
        try:
            script = '''
            tell application "System Events"
                tell process "Windsurf"
                    keystroke "p" using command down
                end tell
            end tell
            '''
            subprocess.run(["osascript", "-e", script], check=True)
            return {"success": True, "message": "Quick file picker opened in Windsurf"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def execute_in_vscode_terminal(self, command: str, cwd: Optional[str] = None):
        """Execute a command in VS Code's integrated terminal"""
        try:
            import time
            
            # Simple and reliable approach - just open terminal and type
            script = f'''
            tell application "Visual Studio Code" to activate
            delay 0.6
            tell application "System Events"
                tell process "Code"
                    -- Open/focus terminal with Ctrl+`
                    keystroke "`" using control down
                    delay 0.7
                    -- Type the command directly
                    keystroke "{command}"
                    delay 0.2
                    -- Execute the command
                    key code 36
                end tell
            end tell
            '''
            subprocess.run(["osascript", "-e", script], check=True)
            return {"success": True, "message": f"Command executed in VS Code terminal: {command}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def execute_in_windsurf_terminal(self, command: str, cwd: Optional[str] = None):
        """Execute a command in Windsurf's integrated terminal"""
        try:
            import time
            
            # Simple and reliable approach - just open terminal and type
            script = f'''
            tell application "Windsurf" to activate
            delay 0.6
            tell application "System Events"
                tell process "Windsurf"
                    -- Open/focus terminal with Ctrl+`
                    keystroke "`" using control down
                    delay 0.7
                    -- Type the command directly
                    keystroke "{command}"
                    delay 0.2
                    -- Execute the command
                    key code 36
                end tell
            end tell
            '''
            subprocess.run(["osascript", "-e", script], check=True)
            return {"success": True, "message": f"Command executed in Windsurf terminal: {command}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_vscode_terminal_content(self):
        """Get the content from VS Code terminal by selecting and copying it"""
        try:
            import time
            import pyperboard
            
            # Save current clipboard
            old_clipboard = pyperboard.paste()
            
            # Select all terminal content using Cmd+A
            script = '''
            tell application "System Events"
                tell process "Code"
                    keystroke "a" using command down
                    delay 0.2
                    keystroke "c" using command down
                    delay 0.2
                end tell
            end tell
            '''
            subprocess.run(["osascript", "-e", script], check=True)
            time.sleep(0.3)
            
            # Get terminal content from clipboard
            terminal_content = pyperboard.paste()
            
            # Restore old clipboard
            pyperboard.copy(old_clipboard)
            
            return {"success": True, "content": terminal_content}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_windsurf_terminal_content(self):
        """Get the content from Windsurf terminal by selecting and copying it"""
        try:
            import time
            import pyperboard
            
            # Save current clipboard
            old_clipboard = pyperboard.paste()
            
            # Select all terminal content using Cmd+A
            script = '''
            tell application "System Events"
                tell process "Windsurf"
                    keystroke "a" using command down
                    delay 0.2
                    keystroke "c" using command down
                    delay 0.2
                end tell
            end tell
            '''
            subprocess.run(["osascript", "-e", script], check=True)
            time.sleep(0.3)
            
            # Get terminal content from clipboard
            terminal_content = pyperboard.paste()
            
            # Restore old clipboard
            pyperboard.copy(old_clipboard)
            
            return {"success": True, "content": terminal_content}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def analyze_terminal_errors(self, terminal_content: str) -> Dict[str, Any]:
        """Analyze terminal output for errors and provide fix suggestions"""
        try:
            import re
            from openai import OpenAI
            import os
            
            # Common error patterns
            error_patterns = {
                "npm_not_found": r"npm: command not found|npm is not recognized",
                "module_not_found": r"ModuleNotFoundError|Cannot find module|Module not found",
                "syntax_error": r"SyntaxError|syntax error",
                "permission_denied": r"Permission denied|EACCES",
                "port_in_use": r"EADDRINUSE|port.*already in use",
                "package_not_found": r"Package.*not found|No package.*found",
                "git_error": r"fatal:|error:|Git command failed",
                "python_error": r"Traceback \(most recent call last\)",
                "compilation_error": r"error:|compilation failed",
                "dependency_error": r"dependency|dependencies|peer dependency"
            }
            
            detected_errors = []
            for error_type, pattern in error_patterns.items():
                if re.search(pattern, terminal_content, re.IGNORECASE):
                    detected_errors.append(error_type)
            
            if not detected_errors:
                return {
                    "success": True,
                    "has_errors": False,
                    "message": "No errors detected in terminal output"
                }
            
            # Use OpenAI to analyze and suggest fixes
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            analysis_prompt = f"""Analyze this terminal output and provide:
1. What error(s) occurred
2. Root cause of the error(s)
3. Step-by-step fix instructions
4. Exact commands to run to fix the issue

Terminal Output:
{terminal_content[-2000:]}  # Last 2000 chars to avoid token limits

Detected Error Types: {', '.join(detected_errors)}

Provide a clear, actionable response."""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert developer who analyzes terminal errors and provides clear, actionable fixes."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.3
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "success": True,
                "has_errors": True,
                "detected_errors": detected_errors,
                "analysis": analysis,
                "terminal_output": terminal_content[-1000:]  # Include last 1000 chars for context
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def auto_fix_terminal_error(self, terminal_content: str, ide: str = "vscode") -> Dict[str, Any]:
        """Automatically attempt to fix errors found in terminal output"""
        try:
            # First analyze the error
            analysis_result = self.analyze_terminal_errors(terminal_content)
            
            if not analysis_result.get("success"):
                return analysis_result
            
            if not analysis_result.get("has_errors"):
                return {
                    "success": True,
                    "message": "No errors to fix",
                    "action_taken": None
                }
            
            # Extract fix commands from analysis using OpenAI
            from openai import OpenAI
            import os
            
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            fix_prompt = f"""Based on this error analysis, extract ONLY the exact terminal commands needed to fix the issue.
Return them as a JSON array of commands in order.

Analysis:
{analysis_result['analysis']}

Return format: {{"commands": ["command1", "command2", ...]}}
Only include commands that are safe to auto-execute (no rm -rf, no sudo without confirmation, etc.)"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You extract fix commands from error analysis. Return only valid JSON."},
                    {"role": "user", "content": fix_prompt}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            import json
            fix_commands = json.loads(response.choices[0].message.content)
            commands = fix_commands.get("commands", [])
            
            if not commands:
                return {
                    "success": True,
                    "message": "Error detected but no safe auto-fix available",
                    "analysis": analysis_result["analysis"],
                    "requires_manual_fix": True
                }
            
            # Execute fix commands in the appropriate IDE terminal
            executed_commands = []
            for cmd in commands:
                if ide.lower() == "vscode":
                    result = self.execute_in_vscode_terminal(cmd)
                else:
                    result = self.execute_in_windsurf_terminal(cmd)
                
                executed_commands.append({
                    "command": cmd,
                    "result": result
                })
                
                # Wait between commands
                import time
                time.sleep(1)
            
            return {
                "success": True,
                "message": "Auto-fix attempted",
                "analysis": analysis_result["analysis"],
                "executed_commands": executed_commands,
                "detected_errors": analysis_result["detected_errors"]
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def open_terminal_vscode(self, cwd: Optional[str] = None) -> Dict[str, Any]:
        """Open integrated terminal in VS Code"""
        try:
            # Use AppleScript to open terminal in VS Code
            applescript = '''
            tell application "Visual Studio Code"
                activate
            end tell
            
            tell application "System Events"
                keystroke "`" using {control down}
            end tell
            '''
            
            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return {"success": True, "message": "Opened terminal in VS Code"}
            else:
                return {"success": False, "error": result.stderr or "Failed to open terminal"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def open_terminal_windsurf(self, cwd: Optional[str] = None) -> Dict[str, Any]:
        """Open integrated terminal in Windsurf"""
        try:
            # Use AppleScript to open terminal in Windsurf
            applescript = '''
            tell application "Windsurf"
                activate
            end tell
            
            tell application "System Events"
                keystroke "`" using {control down}
            end tell
            '''
            
            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return {"success": True, "message": "Opened terminal in Windsurf"}
            else:
                return {"success": False, "error": result.stderr or "Failed to open terminal"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def close_file_vscode(self, file_path: Optional[str] = None) -> Dict[str, Any]:
        """Close current file or specific file in VS Code"""
        try:
            applescript = '''
            tell application "Visual Studio Code"
                activate
            end tell
            
            tell application "System Events"
                keystroke "w" using {command down}
            end tell
            '''
            
            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return {"success": True, "message": "Closed file in VS Code"}
            else:
                return {"success": False, "error": result.stderr or "Failed to close file"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def close_file_windsurf(self, file_path: Optional[str] = None) -> Dict[str, Any]:
        """Close current file or specific file in Windsurf"""
        try:
            applescript = '''
            tell application "Windsurf"
                activate
            end tell
            
            tell application "System Events"
                keystroke "w" using {command down}
            end tell
            '''
            
            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return {"success": True, "message": "Closed file in Windsurf"}
            else:
                return {"success": False, "error": result.stderr or "Failed to close file"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def split_editor_vscode(self, direction: str = "right") -> Dict[str, Any]:
        """Split editor in VS Code (right, down)"""
        try:
            # Cmd+\ for split right, Cmd+K then Cmd+\ for split down
            if direction.lower() == "down":
                applescript = '''
                tell application "Visual Studio Code"
                    activate
                end tell
                
                tell application "System Events"
                    keystroke "k" using {command down}
                    delay 0.2
                    keystroke "\\" using {command down}
                end tell
                '''
            else:  # right
                applescript = '''
                tell application "Visual Studio Code"
                    activate
                end tell
                
                tell application "System Events"
                    keystroke "\\" using {command down}
                end tell
                '''
            
            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return {"success": True, "message": f"Split editor {direction} in VS Code"}
            else:
                return {"success": False, "error": result.stderr or "Failed to split editor"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def split_editor_windsurf(self, direction: str = "right") -> Dict[str, Any]:
        """Split editor in Windsurf (right, down)"""
        try:
            if direction.lower() == "down":
                applescript = '''
                tell application "Windsurf"
                    activate
                end tell
                
                tell application "System Events"
                    keystroke "k" using {command down}
                    delay 0.2
                    keystroke "\\" using {command down}
                end tell
                '''
            else:  # right
                applescript = '''
                tell application "Windsurf"
                    activate
                end tell
                
                tell application "System Events"
                    keystroke "\\" using {command down}
                end tell
                '''
            
            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return {"success": True, "message": f"Split editor {direction} in Windsurf"}
            else:
                return {"success": False, "error": result.stderr or "Failed to split editor"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def toggle_sidebar_vscode(self) -> Dict[str, Any]:
        """Toggle sidebar visibility in VS Code"""
        try:
            applescript = '''
            tell application "Visual Studio Code"
                activate
            end tell
            
            tell application "System Events"
                keystroke "b" using {command down}
            end tell
            '''
            
            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return {"success": True, "message": "Toggled sidebar in VS Code"}
            else:
                return {"success": False, "error": result.stderr or "Failed to toggle sidebar"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def toggle_sidebar_windsurf(self) -> Dict[str, Any]:
        """Toggle sidebar visibility in Windsurf"""
        try:
            applescript = '''
            tell application "Windsurf"
                activate
            end tell
            
            tell application "System Events"
                keystroke "b" using {command down}
            end tell
            '''
            
            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return {"success": True, "message": "Toggled sidebar in Windsurf"}
            else:
                return {"success": False, "error": result.stderr or "Failed to toggle sidebar"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def open_command_palette_vscode(self) -> Dict[str, Any]:
        """Open command palette in VS Code"""
        try:
            applescript = '''
            tell application "Visual Studio Code"
                activate
            end tell
            
            tell application "System Events"
                keystroke "p" using {command down, shift down}
            end tell
            '''
            
            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return {"success": True, "message": "Opened command palette in VS Code"}
            else:
                return {"success": False, "error": result.stderr or "Failed to open command palette"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def open_command_palette_windsurf(self) -> Dict[str, Any]:
        """Open command palette in Windsurf"""
        try:
            applescript = '''
            tell application "Windsurf"
                activate
            end tell
            
            tell application "System Events"
                keystroke "p" using {command down, shift down}
            end tell
            '''
            
            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return {"success": True, "message": "Opened command palette in Windsurf"}
            else:
                return {"success": False, "error": result.stderr or "Failed to open command palette"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def quick_open_vscode(self) -> Dict[str, Any]:
        """Open quick file picker in VS Code"""
        try:
            applescript = '''
            tell application "Visual Studio Code"
                activate
            end tell
            
            tell application "System Events"
                keystroke "p" using {command down}
            end tell
            '''
            
            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return {"success": True, "message": "Opened quick file picker in VS Code"}
            else:
                return {"success": False, "error": result.stderr or "Failed to open quick picker"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def quick_open_windsurf(self) -> Dict[str, Any]:
        """Open quick file picker in Windsurf"""
        try:
            applescript = '''
            tell application "Windsurf"
                activate
            end tell
            
            tell application "System Events"
                keystroke "p" using {command down}
            end tell
            '''
            
            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return {"success": True, "message": "Opened quick file picker in Windsurf"}
            else:
                return {"success": False, "error": result.stderr or "Failed to open quick picker"}
        except Exception as e:
            return {"success": False, "error": str(e)}


# Tool definitions for OpenAI function calling
WINDSURF_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "open_windsurf",
            "description": "Open or launch Windsurf IDE. Use this when user wants to open Windsurf, open a new window, or launch the IDE.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Optional path to open in Windsurf (file or directory)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_vscode",
            "description": "Open or launch VS Code (Visual Studio Code). Use this when user wants to open VS Code, Visual Studio Code, or code editor.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Optional path to open in VS Code (file or directory)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_file_vscode",
            "description": "Open a specific file in VS Code using the code CLI",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to open in VS Code"
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_file",
            "description": "Open a file in Windsurf IDE",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to open"
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_file",
            "description": "Create a new file with optional content",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path where the file should be created"
                    },
                    "content": {
                        "type": "string",
                        "description": "The initial content of the file"
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to read"
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write or update content in a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to write"
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file"
                    }
                },
                "required": ["file_path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_in_files",
            "description": "Search for text in files within a directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_term": {
                        "type": "string",
                        "description": "The text to search for"
                    },
                    "directory": {
                        "type": "string",
                        "description": "The directory to search in (default: current directory)"
                    }
                },
                "required": ["search_term"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_terminal_command",
            "description": "Execute a terminal command",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The terminal command to execute"
                    },
                    "cwd": {
                        "type": "string",
                        "description": "The working directory for the command"
                    }
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files and directories in a given path",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "The directory to list (default: current directory)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_file",
            "description": "Find a file by name in the current directory and subdirectories. Use this when user asks to find, locate, or search for a specific file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name or partial name of the file to find"
                    },
                    "search_path": {
                        "type": "string",
                        "description": "The path to start searching from (default: current directory)"
                    }
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_folder",
            "description": "Find a folder/directory by name in the current directory and subdirectories. Use this when user asks to find, locate, or search for a specific folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "foldername": {
                        "type": "string",
                        "description": "The name or partial name of the folder to find"
                    },
                    "search_path": {
                        "type": "string",
                        "description": "The path to start searching from (default: current directory)"
                    }
                },
                "required": ["foldername"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_directory",
            "description": "Get the current working directory path. Use this when user asks where they are or what the current folder is.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "change_directory",
            "description": "Change the current working directory. Use this when user wants to navigate to a different folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path to change to"
                    }
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_file_info",
            "description": "Get detailed information about a file or folder (size, type, modification date, etc.). Use this when user asks about file/folder details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path to the file or folder"
                    }
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_folder",
            "description": "Create a new folder/directory. Use this when user wants to create, make, or add a new folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder_path": {
                        "type": "string",
                        "description": "The path where the folder should be created"
                    }
                },
                "required": ["folder_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Delete a file. Use this when user wants to delete, remove, or erase a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to delete"
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_folder",
            "description": "Delete a folder/directory. Use this when user wants to delete, remove, or erase a folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder_path": {
                        "type": "string",
                        "description": "The path to the folder to delete"
                    },
                    "recursive": {
                        "type": "boolean",
                        "description": "Whether to delete folder contents recursively (default: false for safety)"
                    }
                },
                "required": ["folder_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_project",
            "description": "Create a complete project structure with files and folders for a specific technology stack. Use this when user wants to create a new project, app, or application in Python, React, Flask, Node.js, Express, FastAPI, HTML, or Calculator.",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "The name of the project"
                    },
                    "project_type": {
                        "type": "string",
                        "description": "The type/technology of the project",
                        "enum": ["python", "react", "node", "flask", "fastapi", "html", "express", "calculator"]
                    },
                    "base_path": {
                        "type": "string",
                        "description": "The base directory where the project should be created (default: current directory)"
                    }
                },
                "required": ["project_name", "project_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_terminal_vscode",
            "description": "Open integrated terminal in VS Code. Use this when user wants to open terminal, console, or command line in VS Code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cwd": {
                        "type": "string",
                        "description": "Optional working directory for the terminal"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_terminal_windsurf",
            "description": "Open integrated terminal in Windsurf. Use this when user wants to open terminal, console, or command line in Windsurf.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cwd": {
                        "type": "string",
                        "description": "Optional working directory for the terminal"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "close_file_vscode",
            "description": "Close the current file in VS Code. Use this when user wants to close a file or tab in VS Code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Optional specific file path to close"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "close_file_windsurf",
            "description": "Close the current file in Windsurf. Use this when user wants to close a file or tab in Windsurf.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Optional specific file path to close"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "split_editor_vscode",
            "description": "Split the editor view in VS Code. Use this when user wants to split editor, view files side by side, or create split panes in VS Code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "direction": {
                        "type": "string",
                        "description": "Direction to split: 'right' (default) or 'down'",
                        "enum": ["right", "down"]
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "split_editor_windsurf",
            "description": "Split the editor view in Windsurf. Use this when user wants to split editor, view files side by side, or create split panes in Windsurf.",
            "parameters": {
                "type": "object",
                "properties": {
                    "direction": {
                        "type": "string",
                        "description": "Direction to split: 'right' (default) or 'down'",
                        "enum": ["right", "down"]
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "toggle_sidebar_vscode",
            "description": "Toggle sidebar visibility in VS Code. Use this when user wants to show/hide sidebar, toggle explorer, or toggle file tree in VS Code.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "toggle_sidebar_windsurf",
            "description": "Toggle sidebar visibility in Windsurf. Use this when user wants to show/hide sidebar, toggle explorer, or toggle file tree in Windsurf.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_command_palette_vscode",
            "description": "Open command palette in VS Code. Use this when user wants to open command palette, run commands, or access VS Code features.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_command_palette_windsurf",
            "description": "Open command palette in Windsurf. Use this when user wants to open command palette, run commands, or access Windsurf features.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "quick_open_vscode",
            "description": "Open quick file picker in VS Code. Use this when user wants to quickly open a file, search files, or use Go to File in VS Code.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "quick_open_windsurf",
            "description": "Open quick file picker in Windsurf. Use this when user wants to quickly open a file, search files, or use Go to File in Windsurf.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_in_vscode_terminal",
            "description": "Execute a command directly in VS Code's integrated terminal. Use this when user wants to run npm, git, python, or any terminal command in VS Code. This types the command into the actual IDE terminal.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to execute in the terminal"
                    },
                    "cwd": {
                        "type": "string",
                        "description": "Optional working directory for the command"
                    }
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_in_windsurf_terminal",
            "description": "Execute a command directly in Windsurf's integrated terminal. Use this when user wants to run npm, git, python, or any terminal command in Windsurf. This types the command into the actual IDE terminal.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to execute in the terminal"
                    },
                    "cwd": {
                        "type": "string",
                        "description": "Optional working directory for the command"
                    }
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_vscode_terminal_content",
            "description": "Read and retrieve the terminal output/logs from VS Code. Use this when user asks to check terminal, read logs, see output, or analyze what happened in VS Code terminal.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_windsurf_terminal_content",
            "description": "Read and retrieve the terminal output/logs from Windsurf. Use this when user asks to check terminal, read logs, see output, or analyze what happened in Windsurf terminal.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_terminal_errors",
            "description": "Analyze terminal output for errors and provide detailed fix suggestions. Use this when user asks to check for errors, analyze terminal output, or understand what went wrong.",
            "parameters": {
                "type": "object",
                "properties": {
                    "terminal_content": {
                        "type": "string",
                        "description": "The terminal output/logs to analyze"
                    }
                },
                "required": ["terminal_content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "auto_fix_terminal_error",
            "description": "Automatically detect and fix errors found in terminal output. Use this when user asks to fix terminal errors, resolve issues automatically, or when errors are detected. This will analyze the error and execute fix commands.",
            "parameters": {
                "type": "object",
                "properties": {
                    "terminal_content": {
                        "type": "string",
                        "description": "The terminal output/logs containing errors"
                    },
                    "ide": {
                        "type": "string",
                        "description": "Which IDE to execute fixes in: 'vscode' or 'windsurf'",
                        "enum": ["vscode", "windsurf"]
                    }
                },
                "required": ["terminal_content", "ide"]
            }
        }
    }
]
