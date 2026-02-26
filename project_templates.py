"""
Project Templates for Various Technologies
Provides scaffolding for different project types
"""

import os
from typing import Dict, Any


def create_python_project(project_path: str, project_name: str) -> Dict[str, Any]:
    """Create a basic Python project structure"""
    try:
        os.makedirs(project_path, exist_ok=True)
        
        # Create main.py
        with open(os.path.join(project_path, "main.py"), 'w') as f:
            f.write(f'''"""
{project_name} - Main Entry Point
"""

def main():
    print("Hello from {project_name}!")

if __name__ == "__main__":
    main()
''')
        
        # Create requirements.txt
        with open(os.path.join(project_path, "requirements.txt"), 'w') as f:
            f.write("# Add your dependencies here\n")
        
        # Create README.md
        with open(os.path.join(project_path, "README.md"), 'w') as f:
            f.write(f"# {project_name}\n\nA Python project.\n\n## Installation\n\n```bash\npip install -r requirements.txt\n```\n\n## Usage\n\n```bash\npython main.py\n```\n")
        
        return {"success": True, "message": f"Python project created at {project_path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_calculator_project(project_path: str, project_name: str) -> Dict[str, Any]:
    """Create a calculator project"""
    try:
        os.makedirs(project_path, exist_ok=True)
        
        with open(os.path.join(project_path, "calculator.py"), 'w') as f:
            f.write('''"""
Simple Calculator Application
"""

def add(x, y):
    """Add two numbers"""
    return x + y

def subtract(x, y):
    """Subtract two numbers"""
    return x - y

def multiply(x, y):
    """Multiply two numbers"""
    return x * y

def divide(x, y):
    """Divide two numbers"""
    if y == 0:
        return "Error! Division by zero."
    return x / y

def main():
    print("=" * 40)
    print("Simple Calculator")
    print("=" * 40)
    
    while True:
        print("\\nSelect operation:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Exit")
        
        choice = input("\\nEnter choice (1/2/3/4/5): ")
        
        if choice == '5':
            print("Thank you for using the calculator!")
            break
        
        if choice in ['1', '2', '3', '4']:
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                
                if choice == '1':
                    print(f"\\nResult: {num1} + {num2} = {add(num1, num2)}")
                elif choice == '2':
                    print(f"\\nResult: {num1} - {num2} = {subtract(num1, num2)}")
                elif choice == '3':
                    print(f"\\nResult: {num1} × {num2} = {multiply(num1, num2)}")
                elif choice == '4':
                    result = divide(num1, num2)
                    print(f"\\nResult: {num1} ÷ {num2} = {result}")
            except ValueError:
                print("\\nInvalid input! Please enter numbers only.")
        else:
            print("\\nInvalid choice! Please select 1-5.")

if __name__ == "__main__":
    main()
''')
        
        with open(os.path.join(project_path, "README.md"), 'w') as f:
            f.write(f"# {project_name}\n\nA simple calculator application.\n\n## Usage\n\n```bash\npython calculator.py\n```\n")
        
        return {"success": True, "message": f"Calculator project created at {project_path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_flask_project(project_path: str, project_name: str) -> Dict[str, Any]:
    """Create a Flask web application project"""
    try:
        os.makedirs(project_path, exist_ok=True)
        os.makedirs(os.path.join(project_path, "templates"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "static"), exist_ok=True)
        
        # Create app.py
        with open(os.path.join(project_path, "app.py"), 'w') as f:
            f.write('''from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/hello')
def hello():
    return {'message': 'Hello from Flask!'}

if __name__ == '__main__':
    app.run(debug=True)
''')
        
        # Create index.html
        with open(os.path.join(project_path, "templates", "index.html"), 'w') as f:
            f.write(f'''<!DOCTYPE html>
<html>
<head>
    <title>{project_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 50px; }}
        h1 {{ color: #333; }}
    </style>
</head>
<body>
    <h1>Welcome to {project_name}!</h1>
    <p>Your Flask application is running.</p>
</body>
</html>
''')
        
        # Create requirements.txt
        with open(os.path.join(project_path, "requirements.txt"), 'w') as f:
            f.write("Flask==3.0.0\n")
        
        # Create README.md
        with open(os.path.join(project_path, "README.md"), 'w') as f:
            f.write(f"# {project_name}\n\nA Flask web application.\n\n## Installation\n\n```bash\npip install -r requirements.txt\n```\n\n## Run\n\n```bash\npython app.py\n```\n")
        
        return {"success": True, "message": f"Flask project created at {project_path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_fastapi_project(project_path: str, project_name: str) -> Dict[str, Any]:
    """Create a FastAPI project"""
    try:
        os.makedirs(project_path, exist_ok=True)
        
        with open(os.path.join(project_path, "main.py"), 'w') as f:
            f.write('''from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}

@app.post("/items/")
def create_item(item: Item):
    return {"item": item, "message": "Item created successfully"}
''')
        
        with open(os.path.join(project_path, "requirements.txt"), 'w') as f:
            f.write("fastapi==0.104.1\nuvicorn[standard]==0.24.0\n")
        
        with open(os.path.join(project_path, "README.md"), 'w') as f:
            f.write(f"# {project_name}\n\nA FastAPI application.\n\n## Installation\n\n```bash\npip install -r requirements.txt\n```\n\n## Run\n\n```bash\nuvicorn main:app --reload\n```\n\nVisit http://localhost:8000/docs for API documentation.\n")
        
        return {"success": True, "message": f"FastAPI project created at {project_path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_react_project(project_path: str, project_name: str) -> Dict[str, Any]:
    """Create a React project structure"""
    try:
        os.makedirs(project_path, exist_ok=True)
        os.makedirs(os.path.join(project_path, "src"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "public"), exist_ok=True)
        
        # package.json
        with open(os.path.join(project_path, "package.json"), 'w') as f:
            f.write(f'''{{"name": "{project_name}",
  "version": "1.0.0",
  "private": true,
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  }},
  "scripts": {{
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }}
}}
''')
        
        # src/App.js
        with open(os.path.join(project_path, "src", "App.js"), 'w') as f:
            f.write(f'''import React from 'react';
import './App.css';

function App() {{
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to {project_name}</h1>
        <p>Edit src/App.js and save to reload.</p>
      </header>
    </div>
  );
}}

export default App;
''')
        
        # src/index.js
        with open(os.path.join(project_path, "src", "index.js"), 'w') as f:
            f.write('''import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
''')
        
        # public/index.html
        with open(os.path.join(project_path, "public", "index.html"), 'w') as f:
            f.write(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{project_name}</title>
</head>
<body>
    <div id="root"></div>
</body>
</html>
''')
        
        # README.md
        with open(os.path.join(project_path, "README.md"), 'w') as f:
            f.write(f"# {project_name}\n\nA React application.\n\n## Installation\n\n```bash\nnpm install\n```\n\n## Run\n\n```bash\nnpm start\n```\n")
        
        return {"success": True, "message": f"React project created at {project_path}. Run 'npm install' to install dependencies."}
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_html_project(project_path: str, project_name: str) -> Dict[str, Any]:
    """Create a basic HTML/CSS/JS project"""
    try:
        os.makedirs(project_path, exist_ok=True)
        os.makedirs(os.path.join(project_path, "css"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "js"), exist_ok=True)
        
        # index.html
        with open(os.path.join(project_path, "index.html"), 'w') as f:
            f.write(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container">
        <h1>Welcome to {project_name}</h1>
        <p>Your website is ready!</p>
        <button onclick="showMessage()">Click Me</button>
    </div>
    <script src="js/script.js"></script>
</body>
</html>
''')
        
        # css/style.css
        with open(os.path.join(project_path, "css", "style.css"), 'w') as f:
            f.write('''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.container {
    background: white;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    text-align: center;
}

h1 {
    color: #333;
    margin-bottom: 20px;
}

button {
    background: #667eea;
    color: white;
    border: none;
    padding: 12px 30px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    margin-top: 20px;
}

button:hover {
    background: #764ba2;
}
''')
        
        # js/script.js
        with open(os.path.join(project_path, "js", "script.js"), 'w') as f:
            f.write('''function showMessage() {
    alert('Hello! Your website is working perfectly!');
}

console.log('Website loaded successfully!');
''')
        
        # README.md
        with open(os.path.join(project_path, "README.md"), 'w') as f:
            f.write(f"# {project_name}\n\nA simple HTML/CSS/JavaScript website.\n\n## Usage\n\nOpen `index.html` in your browser.\n")
        
        return {"success": True, "message": f"HTML project created at {project_path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_node_project(project_path: str, project_name: str) -> Dict[str, Any]:
    """Create a Node.js project"""
    try:
        os.makedirs(project_path, exist_ok=True)
        
        # package.json
        with open(os.path.join(project_path, "package.json"), 'w') as f:
            f.write(f'''{{"name": "{project_name}",
  "version": "1.0.0",
  "description": "A Node.js application",
  "main": "index.js",
  "scripts": {{
    "start": "node index.js",
    "dev": "nodemon index.js"
  }},
  "dependencies": {{}}
}}
''')
        
        # index.js
        with open(os.path.join(project_path, "index.js"), 'w') as f:
            f.write(f'''console.log('Welcome to {project_name}!');

// Your Node.js code here
function greet(name) {{
    return `Hello, ${{name}}!`;
}}

console.log(greet('World'));
''')
        
        # README.md
        with open(os.path.join(project_path, "README.md"), 'w') as f:
            f.write(f"# {project_name}\n\nA Node.js application.\n\n## Installation\n\n```bash\nnpm install\n```\n\n## Run\n\n```bash\nnpm start\n```\n")
        
        return {"success": True, "message": f"Node.js project created at {project_path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_express_project(project_path: str, project_name: str) -> Dict[str, Any]:
    """Create an Express.js project"""
    try:
        os.makedirs(project_path, exist_ok=True)
        os.makedirs(os.path.join(project_path, "routes"), exist_ok=True)
        
        # package.json
        with open(os.path.join(project_path, "package.json"), 'w') as f:
            f.write(f'''{{"name": "{project_name}",
  "version": "1.0.0",
  "description": "An Express.js application",
  "main": "server.js",
  "scripts": {{
    "start": "node server.js",
    "dev": "nodemon server.js"
  }},
  "dependencies": {{
    "express": "^4.18.2"
  }}
}}
''')
        
        # server.js
        with open(os.path.join(project_path, "server.js"), 'w') as f:
            f.write('''const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
    res.json({ message: 'Welcome to Express API!' });
});

app.get('/api/hello', (req, res) => {
    res.json({ message: 'Hello from Express!' });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
''')
        
        # README.md
        with open(os.path.join(project_path, "README.md"), 'w') as f:
            f.write(f"# {project_name}\n\nAn Express.js application.\n\n## Installation\n\n```bash\nnpm install\n```\n\n## Run\n\n```bash\nnpm start\n```\n")
        
        return {"success": True, "message": f"Express.js project created at {project_path}. Run 'npm install' to install dependencies."}
    except Exception as e:
        return {"success": False, "error": str(e)}


# Export all template functions
PROJECT_TEMPLATES = {
    "python": create_python_project,
    "calculator": create_calculator_project,
    "flask": create_flask_project,
    "fastapi": create_fastapi_project,
    "react": create_react_project,
    "html": create_html_project,
    "node": create_node_project,
    "express": create_express_project,
}
