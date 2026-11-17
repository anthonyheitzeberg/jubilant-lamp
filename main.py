import asyncio
import os

from dotenv import load_dotenv

from judges import deterministic_judge, llm_judge
from runner import run_case
from storage import log_result, summarize

load_dotenv()

MODEL = os.getenv("EVAL_MODEL", "ollama/llama3.2")
JUDGE_MODEL = os.getenv("JUDGE_MODEL", MODEL)
RESULTS_FILE = os.getenv("RESULTS_FILE", "results.jsonl")

CASES = [
    {"input": "What is the capital of France?", "expected_concept": "Paris"},
    {"input": "What is 12 multiplied by 12?", "expected_concept": "144"},
    {"input": "Which planet is known as the Red Planet?", "expected_concept": "Mars"},
    {"input": "Who wrote the play Romeo and Juliet?", "expected_concept": "Shakespeare"},
]


async def evaluate(case: dict) -> list[dict]:
    result = await run_case(case, MODEL)
    return [deterministic_judge(result), await llm_judge(result, JUDGE_MODEL)]


async def main() -> None:
    open(RESULTS_FILE, "w").close()
    print(f"model={MODEL} judge={JUDGE_MODEL}")
    for case in CASES:
        for scored in await evaluate(case):
            log_result(scored, RESULTS_FILE)
            status = "PASS" if scored["passed"] else "FAIL"
            print(f"[{status}] ({scored['judge']}) {case['input']}")
    print(summarize(RESULTS_FILE))


if __name__ == "__main__":
    asyncio.run(main())
