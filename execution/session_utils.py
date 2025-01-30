import uuid
from threading import Lock
from multiprocessing import Manager
from .executer import go

sessions = {}
sessions_lock = Lock()

def get_session(session_id):
    """Retrieve an existing session using the session_id."""
    with sessions_lock:
        return sessions.get(session_id)

def create_session(session_id=None):
    """Create a new session and add it to the sessions dictionary."""
    if session_id is not None and not isinstance(session_id, (str, uuid.UUID)):
        raise ValueError(f"Session ID must be a string or UUID, got {type(session_id)} instead")

    with sessions_lock:
        new_id = str(uuid.uuid4()) if session_id is None else session_id
        sessions[new_id] = {"id": new_id, "vars": Manager().dict()}  # Use Manager for shared dict
        return sessions[new_id]


def handler(code, session, result_queue):
    """Task to execute code in a separate process."""
    result = {"stdout": "", "stderr": "", "error": ""}


    # Directly use the shared dictionary from Manager
    session_copy = session  # session already holds a reference to the shared dict

    try:
        # Execute code within the session environment (execute function)
        result_data = go(code, session_copy)
        result_queue.put(result_data)
    except Exception as e:
        result["error"] = str(e)
        result_queue.put(result)
    finally:
        # Save the updated session back to the global sessions dictionary
        with sessions_lock:
            sessions[session_copy["id"]] = session_copy  # Explicitly update the global sessions dict
