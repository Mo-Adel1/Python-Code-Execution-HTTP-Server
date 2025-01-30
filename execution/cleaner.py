import re

def clean_traceback_paths(traceback_str):
    """Clean the traceback paths to make them more readable."""
    if "PermissionError" in traceback_str:
        correct_line_number, error_message = extract_permission_error_details(traceback_str)
        if correct_line_number:
            return format_permission_error_traceback(correct_line_number, error_message)
    else:
        line_number = extract_normal_traceback_line_number(traceback_str)
        if line_number:
            return format_normal_traceback(traceback_str, line_number)
    
    return traceback_str

def extract_permission_error_details(traceback_str):
    """Extract the line number and error message from a PermissionError traceback."""
    match = re.search(r"Permission denied: (.*?) at line (\d+)", traceback_str)
    if match:
        correct_line_number = match.group(2)
        error_message = match.group(1)
        return correct_line_number, error_message
    return None, None

def format_permission_error_traceback(line_number, error_message):
    """Format the PermissionError traceback to make it more readable."""
    return (
        f"Traceback (most recent call last):\n"
        f" File \"<stdin>\", line {line_number}, in <module>\n"
        f"PermissionError: [Errno 13] Permission denied: {error_message}\n"
    )

def extract_normal_traceback_line_number(traceback_str):
    """Extract the line number from a normal traceback."""
    match = re.findall(r'line (\d+)', traceback_str)
    if len(match) < 2:
        return None
    return match[1]

def format_normal_traceback(traceback_str, line_number):
    """Format a normal traceback to make it more readable."""
    lines = traceback_str.splitlines()
    line1 = lines[0]
    line2 = f'File "<stdin>", line {line_number}, in <module>'
    line3 = lines[-1]
    return "\n".join([line1, line2, line3])
