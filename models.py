from pydantic import BaseModel


class JudgeScore(BaseModel):
    passed: bool
    reason: str
