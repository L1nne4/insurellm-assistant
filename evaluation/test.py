import json
from pathlib import Path
from pydantic import BaseModel, Field

TEST_FILE = str(Path(__file__).parent / "tests.jsonl")


class TestQuestion(BaseModel):
    """A test question with expected keywords and reference answer."""

    question: str = Field(description="The question to ask the RAG system")
    keywords: list[str] = Field(description="Keywords that must appear in retrieved context")
    reference_answer: str = Field(description="The reference answer for this question")
    category: str = Field(description="Question category (e.g., direct_fact, spanning, temporal)")


def load_tests(test_file: str | None = None) -> list[TestQuestion]:
    """Load test questions from JSONL. A relative name is resolved next to this module."""
    path = Path(test_file) if test_file else Path(TEST_FILE)
    if not path.is_file():
        path = Path(__file__).parent / Path(test_file or "tests.jsonl").name
    tests = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            tests.append(TestQuestion(**data))
    return tests
