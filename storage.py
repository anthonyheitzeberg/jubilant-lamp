import json

from datetime import datetime


# logging results to disk
def log_result(result: dict, filepath: str) -> None:
    record = {**result, "timestamp": datetime.utcnow().isoformat()}
    with open(filepath, "a") as f:
        f.write(json.dumps(record) + "\n")


def summarize(filepath: str) -> dict:
    with open(filepath) as f:
        results = [json.loads(line) for line in f]
    passed = sum(1 for r in results if r["passed"])
    return {"total": len(results), "passed": passed, "pass_rate": passed / len(results)}
