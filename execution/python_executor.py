import io
import sys
import traceback
from .traceback import clean_traceback_paths

def execute_code(code):
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
    raw_traceback = traceback.format_exc()
    clean_traceback = clean_traceback_paths(raw_traceback)
    return {"stdout": stdout.getvalue(), "stderr": clean_traceback}