import io
import sys
import traceback
import psutil
import time
from .traceback import clean_traceback_paths
from multiprocessing import Process, Queue

TIME_LIMIT = 2
MEMORY_LIMIT_MB = 100

def execute_code(code):
    result = {"stdout": "", "stderr": "", "error": ""}

    result_queue = Queue()    
    process = Process(target=_execute_user_code, args=(code, result_queue))
    process.start()

    start_time = time.time()
    while process.is_alive():
        if _check_memory(process.pid):
            process.terminate()
            result["error"] = "Memory limit exceeded"
            break
        
        if _check_time(start_time):
            process.terminate()
            result["error"] = "Execution timeout"
            break

        time.sleep(0.1)

    if not result_queue.empty():
        result_data = result_queue.get()
        if "error" in result_data:
            result["error"] = result_data["error"]
        else:
            result["stdout"] = result_data["stdout"]
            result["stderr"] = result_data["stderr"]

    return result

def _check_memory(pid):
    memory_info = psutil.Process(pid).memory_info()
    return memory_info.rss > MEMORY_LIMIT_MB * 1024 * 1024  # If memory exceeds limit

def _check_time(start_time):
    return time.time() - start_time > TIME_LIMIT  # If execution time exceeds limit

def _execute_user_code(code, result_queue):
    stdout = io.StringIO()
    stderr = io.StringIO()
    sys.stdout = stdout
    sys.stderr = stderr

    try:
        exec(code, {})  # Execute the user code
        result_queue.put({"stdout": stdout.getvalue(), "stderr": stderr.getvalue()})
    except Exception as e:
        result_queue.put({"error": str(e)})
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

def handle_execution_error(stdout, stderr, error_message=None):
    raw_traceback = error_message or stderr
    clean_traceback = clean_traceback_paths(raw_traceback)
    return {"stdout": stdout, "stderr": clean_traceback, "error": error_message}
