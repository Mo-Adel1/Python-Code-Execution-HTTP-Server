import sys
import threading
import subprocess
import psutil
from .traceback import clean_traceback_paths


TIME_LIMIT = 2 
MEMORY_LIMIT_MB = 100


def execute_code(code):
    result = {"stdout": "", "stderr": "", "error": ""}

    try:
        process = _start_subprocess(code)
        memory_thread = _start_memory_monitor(process.pid, MEMORY_LIMIT_MB, result)

        try:
            result["stdout"], result["stderr"] = process.communicate(timeout=TIME_LIMIT)
        except subprocess.TimeoutExpired:
            _handle_timeout(process, result)

        memory_thread.join()  # Ensure memory thread completes

    except Exception as e:
        result["error"] = str(e)

    return result


def _start_subprocess(code):
    return subprocess.Popen(
        [sys.executable, "-c", code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )


def _start_memory_monitor(pid, memory_limit_mb, result):
    memory_thread = threading.Thread(target=_monitor_memory, args=(pid, memory_limit_mb, result))
    memory_thread.daemon = True
    memory_thread.start()
    return memory_thread


def _monitor_memory(pid, memory_limit_mb, result):
    memory_limit_bytes = memory_limit_mb * 1024 * 1024
    try:
        process = psutil.Process(pid)
        while process.is_running():
            if process.memory_info().rss > memory_limit_bytes:
                process.terminate()
                result["error"] = "Memory limit exceeded"
                break
    except psutil.NoSuchProcess:
        pass


def _handle_timeout(process, result):
    process.kill()
    result["error"] = "Execution timeout"


def handle_execution_error(stdout, stderr, error_message=None):
    raw_traceback = error_message or stderr
    clean_traceback = clean_traceback_paths(raw_traceback)
    return {"stdout": stdout, "stderr": clean_traceback, "error": error_message}
