import ast, operator

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


ALL_TOOLS = [get_weather, calculate]                               # We hand this to the model
BY_NAME = {tool.__name__: tool for tool in ALL_TOOLS}   # How we dispatch a call to the real code


