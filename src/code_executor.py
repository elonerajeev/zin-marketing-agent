#!/usr/bin/env python3
"""
Code executor for running Python scripts as automations
"""
import importlib.util
import sys
from pathlib import Path

class CodeExecutor:
    def __init__(self, scripts_dir="automations"):
        self.scripts_dir = Path(scripts_dir)
        self.scripts_dir.mkdir(exist_ok=True)
    
    def execute_script(self, script_name, user_input, parameters):
        """Execute a Python script as automation"""
        script_path = self.scripts_dir / f"{script_name}.py"
        
        if not script_path.exists():
            return {
                "status": "error",
                "message": f"Script not found: {script_path}"
            }
        
        try:
            # Load the script as a module
            spec = importlib.util.spec_from_file_location(script_name, script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Check if script has a 'run' function
            if not hasattr(module, 'run'):
                return {
                    "status": "error",
                    "message": f"Script must have a 'run' function"
                }
            
            # Execute the run function
            result = module.run(user_input=user_input, parameters=parameters)
            
            return {
                "status": "success",
                "data": result
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "traceback": str(e.__traceback__)
            }
    
    def execute_function(self, module_path, function_name, user_input, parameters):
        """Execute a specific function from a module"""
        try:
            # Import the module
            module = importlib.import_module(module_path)
            
            # Get the function
            if not hasattr(module, function_name):
                return {
                    "status": "error",
                    "message": f"Function '{function_name}' not found in {module_path}"
                }
            
            func = getattr(module, function_name)
            
            # Execute
            result = func(user_input=user_input, parameters=parameters)
            
            return {
                "status": "success",
                "data": result
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
