import threading
from multiprocessing import Process, Queue
from .monitor import limiter
from .session_utils import get_session, create_session, handler


def run(code, session_id):
    """Execute code in a separate process and return the result."""
    result = {"id":"", "stdout": "", "stderr": "", "error": ""}

    session = get_session(session_id)
    if not session:
        session = create_session(session_id)
    
    # Create a queue to capture the results from the execution process
    result_queue = Queue()

    # Create the process to run the code execution task
    process = Process(target=handler, args=(code, session, result_queue))
    process.start()

    # Start a thread to monitor the process with limits for time and memory
    limiter_thread = threading.Thread(target=limiter, args=(process, result, result_queue))
    limiter_thread.start()

    # Wait for the process to finish and retrieve the result
    process.join()

    # Stop the limiter thread once the process has finished
    limiter_thread.join()

    # Retrieve the result from the queue
    result_data = result_queue.get()
    result["id"] = session["id"]
    result["stdout"] = result_data.get("stdout", "")
    result["stderr"] = result_data.get("stderr", "")
    result["error"] = result_data.get("error", "")
    return result
