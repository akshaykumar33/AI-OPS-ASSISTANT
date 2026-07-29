"""
Phase 3: Multi-agent (agentic AI) system - hand-rolled (no framework yet,
same reasoning as Phase 2: see the handoffs before LangGraph abstracts them).

Pipeline: Researcher -> Writer -> Reviewer -> (approved | revise -> Writer again)

- Researcher: uses the Phase 2 tool-calling agent to gather findings on the task
- Writer: drafts an answer from the findings alone (not from its own knowledge,
  so the reviewer can actually check claims against a fixed source)
- Reviewer: checks the draft against the findings, approves or sends feedback

Not started until Phase 2 (single agent) is fully working and tested.
"""
from src.agents.single_agent import run_agent
from src.llm_client import ask

MAX_REVISIONS = 2

RESEARCHER_TASK_TEMPLATE = (
    "Research the following topic thoroughly. Use the available tools "
    "(document search, calculator) whenever they could help. Report your "
    "findings as clear, factual bullet points - do not draft a final answer, "
    "just gather and list what you find.\n\nTopic: {task}"
)

WRITER_SYSTEM_PROMPT = (
    "You are a writer. Draft a clear, well-organized answer using ONLY the "
    "findings provided below - do not add facts that aren't in the findings. "
    "If the findings don't fully cover the question, say so in the draft "
    "rather than filling the gap yourself."
)

REVIEWER_SYSTEM_PROMPT = (
    "You are a reviewer. Compare the draft against the findings it's supposed "
    "to be based on. If the draft is accurate, well-supported by the findings, "
    "and clearly written, respond with exactly: APPROVED\n"
    "If it needs changes, respond with: REVISE: <specific feedback on what to fix>\n"
    "Do not write a new draft yourself - only approve or give feedback."
)


def researcher(task: str) -> str:
    """Gather findings on the task using the Phase 2 tool-calling agent."""
    return run_agent(RESEARCHER_TASK_TEMPLATE.format(task=task))


def writer(task: str, findings: str, feedback: str | None = None) -> str:
    """Draft an answer from the findings. If feedback is given, revise based on it."""
    prompt = f"Original question: {task}\n\nFindings:\n{findings}"
    if feedback:
        prompt += f"\n\nA reviewer gave this feedback on your last draft - revise accordingly:\n{feedback}"
    return ask(prompt, system=WRITER_SYSTEM_PROMPT)


def reviewer(task: str, findings: str, draft: str) -> tuple[bool, str]:
    """Review the draft against the findings.

    Returns (approved, feedback) - feedback is empty when approved.
    """
    prompt = (
        f"Original question: {task}\n\nFindings:\n{findings}\n\nDraft to review:\n{draft}"
    )
    response = ask(prompt, system=REVIEWER_SYSTEM_PROMPT).strip()

    if response.upper().startswith("APPROVED"):
        return True, ""
    # Strip the "REVISE:" prefix if present, keep the rest as feedback either way
    feedback = response.split(":", 1)[1].strip() if ":" in response else response
    return False, feedback


def run_pipeline(task: str, max_revisions: int = MAX_REVISIONS) -> str:
    """Run the full researcher -> writer -> reviewer pipeline on a task.

    Revises the draft up to max_revisions times if the reviewer requests
    changes. Returns the last draft produced even if never approved, so
    the pipeline always returns something instead of raising.
    """
    findings = researcher(task)
    draft = writer(task, findings)

    for _ in range(max_revisions):
        approved, feedback = reviewer(task, findings, draft)
        if approved:
            return draft
        draft = writer(task, findings, feedback=feedback)

    return draft


if __name__ == "__main__":
    user_task = input("Give the pipeline a task: ")
    print(run_pipeline(user_task))
