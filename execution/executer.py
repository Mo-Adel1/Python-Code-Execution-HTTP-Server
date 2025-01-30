import ast
import io
import sys
import traceback
from .cleaner import clean_traceback_paths
from .sandbox import RestrictUnsafeCode, restricted_builtins

def go(code, session):
    """Execute the code and capture stdout and stderr."""
    exec_env = dict(session["vars"])  # Convert DictProxy to a standard dict
    stdout = io.StringIO()
    sys.stdout = stdout  # Redirect stdout to capture print output

    try:
        # Parse the code into an AST
        tree = ast.parse(code)
        
        # Transform the AST (remove or block unsafe constructs)
        transformed_tree = RestrictUnsafeCode().visit(tree)
        
        # Compile the transformed AST into a code object
        compiled_code = compile(transformed_tree, "<string>", "exec")
        
        # Create a restricted environment for execution
        restricted_globals = {
            '__builtins__': restricted_builtins(),  # Allow only safe builtins
            'os': None,  # Disable filesystem access
            'socket': None,  # Disable networking
            'requests': None,  # Disable HTTP requests
            'multiprocessing': None  # Disable multiprocessing
        }
        
        exec(compiled_code, restricted_globals, exec_env)  # Use the restricted environment for execution
        session["vars"].update(exec_env)  # Save updates back to the shared DictProxy
        return {"stdout": stdout.getvalue(), "stderr": ""}
    except PermissionError as e:
        # stderr = traceback.format_exc()
        stderr = clean_traceback_paths(traceback.format_exc())
        return {"stdout": stdout.getvalue(), "stderr": stderr}
    except Exception:
        stderr = clean_traceback_paths(traceback.format_exc())
        return {"stdout": stdout.getvalue(), "stderr": stderr}
    finally:
        sys.stdout = sys.__stdout__

