import ast

class RestrictUnsafeCode(ast.NodeTransformer):
    """Transform the AST to remove unsafe code constructs."""
    
    def visit_Call(self, node):
        """Block function calls like os.remove(), open(), socket.socket(), etc."""
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in ["remove", "system", "unlink", "rmdir", "mkdir", "makedirs", "rename", "replace"]:
                if isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    raise PermissionError(13, f"Permission denied: '{node.args[0].s}' at line {node.lineno}")
                else:
                    raise PermissionError(13, f"Permission denied: unknown file or action at line {node.lineno}")
            elif node.func.attr in ["socket", "create_connection", "connect", "bind", "listen", "accept"]:
                raise PermissionError(13, f"Permission denied: network access is not allowed at line {node.lineno}")
        elif isinstance(node.func, ast.Name):
            if node.func.id in ["open"]:
                if isinstance(node.args[0], ast.Str):
                    raise PermissionError(13, f"Permission denied: '{node.args[0].s}' at line {node.lineno}")
                else:
                    raise PermissionError(13, f"Permission denied: unknown file or action at line {node.lineno}")
        return self.generic_visit(node)



def restricted_builtins():
    """Define a set of safe builtins that can be used in the execution environment."""
    safe_builtins = {
        'print': print,
        'len': len,
        'range': range,
        'str': str,
        'int': int,
        'float': float,
        'list': list,
        'dict': dict,
        'set': set
    }
    return safe_builtins
