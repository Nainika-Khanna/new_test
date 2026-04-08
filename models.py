from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Observation(BaseModel):
    email_id: str
    subject: str
    content: str
    sender: str
    current_status: str
    possible_actions: List[str]
    task_name: str = ""
    emails_remaining: int = 0
    step_count: int = 0

class Action(BaseModel):
    action_type: str   # "categorize" | "set_priority" | "decide_action" | "full_triage"
    value: str         # e.g. "Spam" | "High" | "escalate" | "Spam|High|escalate"

class Reward(BaseModel):
    score: float       # 0.0 to 1.0
    comment: str
    breakdown: Dict[str, Any] = {}
