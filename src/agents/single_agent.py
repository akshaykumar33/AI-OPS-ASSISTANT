"""
Phase 2: Single agent with tool calling.

Hand-rolled agent loop (no framework yet) so the plan -> act -> observe
cycle is visible instead of hidden inside LangGraph. Once this is solid,
Phase 3 can move to a framework knowing what it's abstracting over.

Loop:
1. Send the task (+ conversation so far) to Gemini with tools available
2. If the model returns a final text answer -> done
3. If the model requests one or more tool calls -> run them, feed results back
4. Repeat until a final answer or max_steps is hit (safety limit against loops)
"""
from google.genai import types

from src.agents.tools import TOOL_FUNCTIONS, execute_tool
from src.llm_client import MODEL_NAME, get_client

MAX_STEPS = 6

TOOLS = list(TOOL_FUNCTIONS.values())


def run_agent(task: str, max_steps: int = MAX_STEPS) -> str:
    """Run the single-agent loop on a given task and return the final text result.

    If the model never stops calling tools within max_steps, returns a
    message saying so rather than looping forever or raising.
    """
    client = get_client()
    contents = [types.Content(role="user", parts=[types.Part(text=task)])]
    config = types.GenerateContentConfig(
        tools=TOOLS,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    for _ in range(max_steps):
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=config,
        )

        # Keep the model's own turn in the conversation so it has memory
        # of what it already decided/called on the next loop iteration.
        contents.append(response.candidates[0].content)

        function_calls = response.function_calls
        if not function_calls:
            return response.text

        result_parts = []
        for call in function_calls:
            result = execute_tool(call.name, dict(call.args))
            result_parts.append(
                types.Part.from_function_response(
                    name=call.name,
                    response={"result": result},
                )
            )
        contents.append(types.Content(role="tool", parts=result_parts))

    return f"Agent stopped after {max_steps} steps without a final answer."


if __name__ == "__main__":
    user_task = input("Give the agent a task: ")
    print(run_agent(user_task))
