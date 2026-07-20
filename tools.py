import ast, operator
from pathlib import Path
import subprocess
PROJECT_ROOT = Path(r"D:\proj\cli_chatbot").resolve()

ALLOWED_COMMANDS = {"pytest", "git status", "git diff", "ls", "dir"}

def run_command(command: str) -> str:
    """Run a whitelisted shell command and return its output.
    Only a fixed set of safe, read-only commands are permitted.

    Args:
        command: The command to run, e.g. 'pytest' or 'git status'.
    """
    if command not in ALLOWED_COMMANDS:
        return (f"error: '{command}' is not in the allowed command list "
                f"({sorted(ALLOWED_COMMANDS)}), refused")

    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        return f"error: '{command}' timed out after 30s"

    output = result.stdout + result.stderr
    return output[:2000] if output else "(no output)"

def read_file(file_path: str) -> str:
    """Read the contents of a file.

    Args:
        file_path: The path to the file to read.

    """
    target = (PROJECT_ROOT / file_path).resolve()
    
    # Scope chcek: target must stay inside PROJECT_ROOT
    if not target.is_relative_to(PROJECT_ROOT):
        raise ValueError(f"File path {file_path} is outside of the project root.")
    
    if not target.exists():
        raise FileNotFoundError(f"File {file_path} does not exist.")
    
    if not target.is_file():
        raise ValueError(f"Path {file_path} is not a file.")
    
    try:
        return target.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return f"error: '{file_path}' is not a text file (binary content)"

def write_file(file_path: str, content: str) -> None:
    """Write content to a file.

    Args:
        file_path: The path to the file to write.
        content: The content to write to the file.

    """
    target = (PROJECT_ROOT / file_path).resolve()
    
    # Scope check: target must stay inside PROJECT_ROOT
    if not target.is_relative_to(PROJECT_ROOT):
        return f"error: '{file_path}' is outside the project directory, refused"
    
    if target.exists():
        return f"error: '{file_path}' already exists — refused to overwrite. Use overwrite_file if this is intentional."
    
    # Ensure the parent directory exists
    target.parent.mkdir(parents=True, exist_ok=True)
    
    target.write_text(content, encoding='utf-8')

    return f"wrote {len(content)} chars to '{file_path}'"



def get_weather(city: str) -> str:
    """Get the current weather for a given city.

    Args:
        city: The name of the city to get the weather for.

    """

    fake_db = {"Basel": "12°C, light rain", 
               "Tokyo": "24°C, clear"}
    return fake_db.get(city, "no data for that city")


def calculate(expression: str) -> str:
    """Calculate a simple arithmetic expression.

    Args:
        expression: A string containing an arithmetic expression, e.g. "2 + 2".

    """
    print(f"calculating: {expression}")
    ops = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
           ast.Div: operator.truediv, ast.USub: operator.neg}
    
    def ev(node):
        if isinstance(node, ast.Constant): return node.value
        if isinstance(node, ast.BinOp): return ops[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp):        return ops[type(node.op)](ev(node.operand))
        raise ValueError("unsupported expression")
    
    return str(ev(ast.parse(expression, mode='eval').body))


ALL_TOOLS = [get_weather, calculate, read_file, write_file, run_command]                               # We hand this to the model
BY_NAME = {tool.__name__: tool for tool in ALL_TOOLS}   # How we dispatch a call to the real code


