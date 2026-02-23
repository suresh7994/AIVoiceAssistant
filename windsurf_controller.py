import subprocess
import json
import logging
from typing import Optional, Dict, Any

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
            with open(file_path, 'w') as f:
                f.write(content)
            return {"success": True, "message": f"File created: {file_path}"}
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
        """List files in a directory"""
        try:
            result = subprocess.run(
                ["ls", "-la", directory],
                capture_output=True,
                text=True,
                timeout=10
            )
            return {
                "success": True,
                "files": result.stdout
            }
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
        """Open a file in VS Code using CLI"""
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
                return {"success": False, "error": result.stderr or "Failed to open file"}
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
    }
]
