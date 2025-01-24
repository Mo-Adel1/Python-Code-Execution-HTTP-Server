import io
import sys
import threading
import traceback
from .traceback import clean_traceback_paths

TIME_LIMIT = 2 
MEMORY_LIMIT_MB = 100


def execute_code(code):
    stdout = io.StringIO()
    stderr = io.StringIO()
    sys.stdout = stdout
    sys.stderr = stderr

    result = {"stdout": "", "stderr": "", "error": ""}

    def execute():
        try:
            exec_globals = {}
            exec_locals = {}
            exec(code, exec_globals, exec_locals)

            total_memory = sum(
                sys.getsizeof(obj) for obj in exec_locals.values()
            ) / (1024 * 1024)

            if total_memory > MEMORY_LIMIT_MB:
                result["error"] = "Memory limit exceeded"
        except Exception:
            result["stderr"] = traceback.format_exc()

    thread = threading.Thread(target=execute)
    thread.daemon = True
    thread.start()

    thread.join(TIME_LIMIT)

    if thread.is_alive():
        result["error"] = "execution timeout"

    if result["error"]:
        return handle_execution_error(stdout, stderr, result["error"])

    return {"stdout": stdout.getvalue(), "stderr": ""}


def handle_execution_error(stdout, stderr, error_message=None):
    raw_traceback = error_message or stderr.getvalue()
    clean_traceback = clean_traceback_paths(raw_traceback)
    return {"stdout": stdout.getvalue(), "stderr": clean_traceback, "error": error_message}
