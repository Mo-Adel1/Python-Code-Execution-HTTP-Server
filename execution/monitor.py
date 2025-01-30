import psutil
import time

TIME_LIMIT = 2
MEMORY_LIMIT_MB = 100
INTERVAL = 0.01


def limiter(process, result, result_queue):
    """Limit the execution time and memory usage of the process."""
    start_time = time.time()
    while process.is_alive():
        if check_memory(process.pid):
            process.terminate()  # Force terminate the process
            result["error"] = "Memory limit exceeded"
            result_queue.put(result)
            break

        if check_time(start_time):
            process.terminate()  # Force terminate the process
            result["error"] = "Execution timeout"
            result_queue.put(result)
            break

        time.sleep(0.01)  # Small sleep to prevent 100% CPU usage while monitoring

def check_memory(pid):
    """Check if the process exceeds the memory limit."""
    try:
        memory_info = psutil.Process(pid).memory_info()
        return memory_info.rss > MEMORY_LIMIT_MB * 1024 * 1024
    except psutil.NoSuchProcess:
        return False

def check_time(start_time):
    """Check if the process exceeds the time limit."""
    return time.time() - start_time > TIME_LIMIT
