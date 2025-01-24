import re

def clean_traceback_paths(traceback_str):
    line1 = traceback_str.splitlines()[0]

    match = re.findall(r'line (\d+)', traceback_str)
    
    if len(match) < 2:
        return traceback_str
    
    line_number = match[1]
    line2 = f'File "<stdin>", line {line_number}, in <module>'

    line3 = traceback_str.splitlines()[-1]

    return "\n".join([line1, line2, line3])
