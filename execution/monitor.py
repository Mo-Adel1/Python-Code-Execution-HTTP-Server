import psutil
import time

TIME_LIMIT = 2
MEMORY_LIMIT_MB = 100
INTERVAL = 0.01

def limiter(process, result):
    start_time = time.time()
    while process.is_alive():
        if check_memory(process.pid):
            process.terminate()
            result["error"] = "Memory limit exceeded"
            break
        
        if check_time(start_time):
            process.terminate()
            result["error"] = "Execution timeout"
            break

        time.sleep(INTERVAL)

def check_memory(pid):
    try:
        memory_info = psutil.Process(pid).memory_info()
        return memory_info.rss > MEMORY_LIMIT_MB * 1024 * 1024
    except psutil.NoSuchProcess:
        return False

def check_time(start_time):
    return time.time() - start_time > TIME_LIMIT 