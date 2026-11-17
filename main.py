import asyncio
import json
import litellm
import litellm

from datetime import datetime
from pydantic import BaseModel

class JudgeScore(BaseModel):
    passed: bool
    reason: str

# scoring the output with a judge layer
async def llm_judge(result: dict, judge_model: str) ->  dict:
    prompt = f"Input: {result['input']}\nResponse: {result['raw_output']}\nCriteria: {result['expected_concept']}\nDid the response meet the criteria? Reply as JSON."
    response = await litellm.acompletion(
        model=judge_model,
        messages=[{"role": "user", "content": prompt}],
        response_format=JudgeScore
    )
    score = JudgeScore.model_validate_json(response.choices[0].message.content)
    return {**result, "passed": score.passed, "reason": score.reason, "judge": "llm"}

def deterministic_judge(result: dict) -> dict:
    output = result["raw_output"].lower()
    concept = result["expected_concept"].lower()
    passed = concept in output
    return {**result, "passed": passed, "judge": "deterministic"}

async def run_case(case: dict, model: str) -> dict:
    response = await litellm.acompletion(
        model=model,
        messages=[{"role": "user", "content": case["input"]}],
        num_retries=3,
        timeout=30
    )
    raw = response.choices[0].message.content
    return {**case, "raw_output": raw}

# logging results to disk
def log_result(result: dict, filepath: str) -> None:
    record = {**result, "timestamp": datetime.utcnow().isoformat()}
    with open(filepath, "a") as f:
        f.write(json.dumps(record) + "\n")

def summarize(filepath: str) -> dict:
    results = [json.loads(l) for l in open(filepath)]
    passed = sum(1 for r in results if r["passed"])
    return{"total": len(results), "passed": passed, "pass_rate": passed / len(results)}