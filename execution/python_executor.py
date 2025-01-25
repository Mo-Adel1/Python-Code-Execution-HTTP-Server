import io
import sys
import traceback
from multiprocessing import Process, Queue
from .monitor import limiter
from .cleaner import clean_traceback_paths

def run_user_code(code):
    result = {"stdout": "", "stderr": "", "error": ""}

    result_queue = Queue()

    process = Process(target=execute_code, args=(code, result_queue))
    process.start()

    limiter(process, result)

    if not result_queue.empty():
        result_data = result_queue.get()
        if "error" in result_data:
            result["error"] = result_data["error"]
        else:
            result["stdout"] = result_data["stdout"]
            result["stderr"] = result_data["stderr"]
    return result

def execute_code(code, result_queue):
    stdout = io.StringIO()
    sys.stdout = stdout
    
    try:
        exec(code, {})
        result_queue.put({"stdout": stdout.getvalue(), "stderr": ""})
    except Exception:
        stderr = clean_traceback_paths(traceback.format_exc())
        result_queue.put({"stdout": stdout.getvalue(), "stderr": stderr})
    finally:
        sys.stdout = sys.__stdout__