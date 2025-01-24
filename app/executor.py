import io
import sys
import traceback
from traceback_utils import clean_traceback_paths

def execute_user_code(code):
    """Executes the user's code and captures stdout/stderr."""
    stdout = io.StringIO()
    stderr = io.StringIO()

    sys.stdout = stdout
    sys.stderr = stderr

    try:
        exec(code, {})
        return {"stdout": stdout.getvalue(), "stderr": ""}
    except Exception:
        return handle_execution_error(stdout, stderr)

def handle_execution_error(stdout, stderr):
    """Handles errors that occur during code execution."""
    raw_traceback = traceback.format_exc()
    clean_traceback = clean_traceback_paths(raw_traceback)
    return {"stdout": stdout.getvalue(), "stderr": clean_traceback}
