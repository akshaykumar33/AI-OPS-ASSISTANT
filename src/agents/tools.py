"""
Phase 2: Tools available to the agent.

Each tool is a plain Python function with type hints and a docstring -
the google-genai SDK reads these to build the schema the model sees.
Keep docstrings clear and specific; the model decides when to call a
tool based on its name and description, so vague docstrings mean the
model guesses wrong more often.
"""
import ast
import operator


def search_documents(query: str) -> str:
    """Search the user's ingested documents and return relevant excerpts.

    Use this whenever the task asks about information that might be in
    the user's own documents (uploaded PDFs/notes), rather than general
    knowledge.

    Args:
        query: The question or topic to search for in the documents.

    Returns:
        Relevant excerpts joined together, or a message saying nothing was found.
    """
    from src.rag.retrieve import retrieve_chunks

    chunks = retrieve_chunks(query)
    if not chunks:
        return "No relevant documents found for this query."
    return "\n---\n".join(chunks)


# Only these operators are supported - deliberately NOT using eval(),
# which would let the model run arbitrary code via a crafted expression.
_SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _safe_eval(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _SAFE_OPERATORS:
        return _SAFE_OPERATORS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _SAFE_OPERATORS:
        return _SAFE_OPERATORS[type(node.op)](_safe_eval(node.operand))
    raise ValueError(f"Unsupported expression element: {ast.dump(node)}")


def calculate(expression: str) -> str:
    """Evaluate a basic arithmetic expression and return the numeric result.

    Use this for any math the task requires instead of computing it yourself,
    since language models are unreliable at exact arithmetic.

    Args:
        expression: A math expression using +, -, *, /, ** and parentheses.
            Example: "47 * 89" or "(12 + 3) / 5".

    Returns:
        The numeric result as a string, or an error message if the expression is invalid.
    """
    try:
        tree = ast.parse(expression, mode="eval")
        result = _safe_eval(tree.body)
        return str(result)
    except Exception as e:  # noqa: BLE001
        return f"Error evaluating '{expression}': {e}"


# Dispatch table used by the agent loop to call a tool by name.
TOOL_FUNCTIONS = {
    "search_documents": search_documents,
    "calculate": calculate,
}


def execute_tool(name: str, args: dict) -> str:
    """Run the named tool with the given arguments, catching and reporting any error
    rather than letting it crash the agent loop."""
    fn = TOOL_FUNCTIONS.get(name)
    if fn is None:
        return f"Error: unknown tool '{name}'"
    try:
        return fn(**args)
    except Exception as e:  # noqa: BLE001
        return f"Error running tool '{name}': {e}"

