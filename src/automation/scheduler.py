"""
Phase 5: Automation - scheduled and event-triggered runs, driven by n8n.

n8n workflow design:
- Schedule Trigger node -> Execute Command node running:
    python -m src.automation.scheduler daily
- Local File Trigger node (watches data/docs/) -> Execute Command node running:
    python -m src.automation.scheduler on_new_file "<filename>"

State (which files have already been ingested) is tracked in
data/automation_state.json so repeated daily runs don't re-embed
documents that haven't changed.
"""
import json
import sys
from pathlib import Path

from src.llm_client import ask
from src.rag.embed import embed_and_store
from src.rag.ingest import chunk_text, load_documents

STATE_FILE = Path("data/automation_state.json")
DOCS_DIR = Path("data/docs")
SUPPORTED_EXTENSIONS = (".pdf", ".txt")


def _load_state() -> set[str]:
    """Return the set of filenames already ingested, per the state file."""
    if not STATE_FILE.exists():
        return set()
    return set(json.loads(STATE_FILE.read_text()))


def _save_state(ingested_filenames: set[str]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(sorted(ingested_filenames)))


def find_new_files() -> list[str]:
    """Return filenames in data/docs/ that haven't been ingested yet, per the state file."""
    if not DOCS_DIR.exists():
        return []
    already_ingested = _load_state()
    current_files = {f.name for f in DOCS_DIR.iterdir() if f.suffix.lower() in SUPPORTED_EXTENSIONS}
    return sorted(current_files - already_ingested)


def ingest_new_files(filenames: list[str]) -> int:
    """Ingest + chunk + embed only the given filenames, then record them as
    ingested. Returns the number of chunks stored."""
    if not filenames:
        return 0

    docs = load_documents(str(DOCS_DIR), filenames=filenames)
    chunks = [c for doc in docs for c in chunk_text(doc)]
    stored = embed_and_store(chunks)

    state = _load_state()
    state.update(filenames)
    _save_state(state)

    return stored


def daily_briefing() -> str:
    """Scheduled job: ingest anything new since last run, return a short
    notification summarizing what happened.

    Called by n8n's Schedule Trigger via:
        python -m src.automation.scheduler daily
    """
    new_files = find_new_files()

    if not new_files:
        return "Daily briefing: no new documents since last run."

    stored = ingest_new_files(new_files)
    summary_prompt = (
        f"{len(new_files)} new document(s) were just added and ingested: "
        f"{', '.join(new_files)}. {stored} chunks were stored in the knowledge base. "
        "Write a short, friendly 2-sentence notification about this for the user."
    )
    return ask(summary_prompt)


def on_new_file(filename: str) -> str:
    """Event-triggered run: ingest one newly-added file immediately.

    Called by n8n's Local File Trigger via:
        python -m src.automation.scheduler on_new_file "<filename>"
    """
    stored = ingest_new_files([filename])
    if stored == 0:
        return f"'{filename}' was already ingested or produced no chunks - nothing to do."
    return f"Ingested '{filename}': {stored} chunks stored and ready to search."


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m src.automation.scheduler [daily|on_new_file <filename>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "daily":
        print(daily_briefing())
    elif command == "on_new_file":
        if len(sys.argv) < 3:
            print("Usage: python -m src.automation.scheduler on_new_file <filename>")
            sys.exit(1)
        print(on_new_file(sys.argv[2]))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
