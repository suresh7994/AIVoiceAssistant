# Project Management Guide

## Overview

The AI Voice Assistant now has comprehensive project creation and file management capabilities. You can create complete project structures for various technologies using simple voice commands.

## Supported Project Types

### 1. **Python** (`python`)
- Basic Python project structure
- `main.py` entry point
- `requirements.txt` for dependencies
- README with setup instructions

**Voice Command Examples:**
- "Create a Python project called my_app"
- "Make a new Python project named data_processor in the projects folder"

### 2. **Calculator** (`calculator`)
- Full-featured calculator application
- Interactive CLI interface
- Basic arithmetic operations
- Error handling

**Voice Command Examples:**
- "Create a calculator project called simple_calc"
- "Make a calculator app in the tools folder"

### 3. **Flask** (`flask`)
- Flask web application structure
- Templates and static folders
- Basic routes and API endpoints
- HTML template included

**Voice Command Examples:**
- "Create a Flask project called my_web_app"
- "Build a Flask application named api_server"

### 4. **FastAPI** (`fastapi`)
- Modern FastAPI project
- Pydantic models
- Auto-generated API docs
- Example endpoints

**Voice Command Examples:**
- "Create a FastAPI project called rest_api"
- "Make a FastAPI app for my backend"

### 5. **React** (`react`)
- React application structure
- Component-based architecture
- Package.json with dependencies
- Public and src folders

**Voice Command Examples:**
- "Create a React project called my_dashboard"
- "Build a React app named frontend"

### 6. **Node.js** (`node`)
- Basic Node.js project
- Package.json configuration
- Entry point script

**Voice Command Examples:**
- "Create a Node project called backend"
- "Make a Node.js app named server"

### 7. **Express.js** (`express`)
- Express.js server structure
- Routes folder
- API endpoints
- Middleware setup

**Voice Command Examples:**
- "Create an Express project called api"
- "Build an Express server named backend_api"

### 8. **HTML/CSS/JS** (`html`)
- Static website structure
- Organized CSS and JS folders
- Responsive design template
- Modern styling

**Voice Command Examples:**
- "Create an HTML project called my_website"
- "Make a website project named portfolio"

## File and Folder Management

### Creating Folders

**Voice Commands:**
- "Create a folder called data"
- "Make a new folder named projects in the current directory"
- "Create a directory called test_files"

### Deleting Files

**Voice Commands:**
- "Delete the file test.py"
- "Remove the file old_script.js"
- "Erase the file temp.txt"

### Deleting Folders

**Voice Commands:**
- "Delete the folder old_project" (empty folders only)
- "Remove the directory temp_files recursively" (with contents)
- "Delete the test folder and all its contents"

**Note:** For safety, folders with contents require explicit "recursive" or "and all its contents" in the command.

### Creating Files

**Voice Commands:**
- "Create a file called config.json"
- "Make a new file named settings.py with some default content"
- "Create an empty file called README.md"

## Navigation Commands

### Current Directory
- "Where am I?"
- "What's my current directory?"
- "Show current location"

### Change Directory
- "Go to the projects folder"
- "Change to the parent directory"
- "Navigate to /Users/username/Documents"

### List Files
- "List files in the current directory"
- "Show me what's in the data folder"
- "What files are here?"

### Find Files/Folders
- "Find the file config.py"
- "Locate the folder named tests"
- "Search for README.md"

### File Information
- "Get info about app.py"
- "Show details of the config folder"
- "What's the size of data.json?"

## Complete Workflow Examples

### Example 1: Creating a Calculator Project
```
User: "Create a calculator project called my_calculator in the projects folder"
Assistant: Creates complete calculator project with:
- calculator.py (full implementation)
- README.md (usage instructions)
- Organized in projects/my_calculator/
```

### Example 2: Building a Flask Web App
```
User: "Create a Flask project called blog_app"
Assistant: Creates Flask project with:
- app.py (Flask server)
- templates/index.html
- static/ folder
- requirements.txt
- README.md
```

### Example 3: Setting Up a React Application
```
User: "Make a React project called dashboard in the web_apps folder"
Assistant: Creates React project with:
- package.json
- src/App.js
- src/index.js
- public/index.html
- README.md
Note: Run 'npm install' to install dependencies
```

### Example 4: File Management Workflow
```
User: "Create a folder called data_processing"
Assistant: ✓ Folder created

User: "Create a Python project called processor in the data_processing folder"
Assistant: ✓ Python project created

User: "List files in data_processing/processor"
Assistant: Shows main.py, requirements.txt, README.md
```

## Best Practices

1. **Specify Base Path**: When creating projects, mention the target folder if not current directory
   - "Create a Flask project in the web_apps folder"
   
2. **Use Descriptive Names**: Choose clear, meaningful project names
   - Good: "user_authentication_api"
   - Avoid: "proj1", "test", "new"

3. **Check Before Deleting**: Always verify what you're deleting
   - "Get info about old_project" before "Delete old_project folder"

4. **Navigate First**: Change to the desired directory before creating projects
   - "Go to the projects folder"
   - "Create a React app called dashboard"

5. **Install Dependencies**: After creating projects, install required packages
   - Python: `pip install -r requirements.txt`
   - Node/React/Express: `npm install`

## Safety Features

- **Folder Deletion**: Empty folders can be deleted directly; folders with contents require explicit recursive deletion
- **File Overwrite Protection**: Creating files/folders checks for existing paths
- **Path Validation**: All operations validate paths before execution
- **Error Handling**: Clear error messages for invalid operations

## Troubleshooting

### Issue: "Folder not recognized as directory"
**Solution:** The path might be a file, not a folder. Use `get_file_info` to check.

### Issue: "Cannot delete folder - not empty"
**Solution:** Use "delete recursively" or "delete with all contents" in your command.

### Issue: "Project already exists"
**Solution:** Choose a different name or delete the existing project first.

### Issue: "Permission denied"
**Solution:** Check folder permissions or try a different location.

## Technology-Specific Notes

### Python Projects
- Remember to create a virtual environment: `python -m venv venv`
- Activate it before installing: `source venv/bin/activate` (Mac/Linux)

### React/Node Projects
- Requires Node.js and npm installed
- Run `npm install` after project creation
- Use `npm start` to run development server

### Flask/FastAPI Projects
- Install dependencies: `pip install -r requirements.txt`
- Flask: Run with `python app.py`
- FastAPI: Run with `uvicorn main:app --reload`

## Voice Command Tips

1. **Be Specific**: "Create a Flask project called api_server in the backend folder"
2. **Use Natural Language**: "Make a new calculator app" works just as well as formal commands
3. **Confirm Actions**: Ask "List files" after creation to verify
4. **Chain Commands**: You can give multiple commands in sequence

## Future Enhancements

Coming soon:
- Django project templates
- Vue.js project templates
- Next.js project templates
- Spring Boot (Java) templates
- Custom project templates
- Git initialization option
- Docker configuration option

---

**Remember**: The AI assistant understands natural language, so speak naturally! You don't need to memorize exact commands.
