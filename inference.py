"""
EmailTriagePro — Baseline Inference Script
Runs all 3 tasks against the environment and produces reproducible scores.
Uses OpenAI client as required by hackathon spec.
"""

import os
import json
import time
import httpx
from openai import OpenAI

# ── Config from environment variables ─────────────────────────────────────────
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME   = os.environ.get("MODEL_NAME",   "gpt-4o-mini")
HF_TOKEN     = os.environ.get("HF_TOKEN",     "")
ENV_URL      = os.environ.get("ENV_URL",      "http://localhost:7860")

client = OpenAI(
    api_key=HF_TOKEN if HF_TOKEN else os.environ.get("OPENAI_API_KEY", "sk-dummy"),
    base_url=API_BASE_URL
)

CATEGORIES = ["Spam", "Urgent", "Technical", "HR", "Billing", "Support", "General"]
PRIORITIES  = ["High", "Medium", "Low"]
ACTIONS     = ["auto_reply", "escalate", "archive", "forward_to_dev", "forward_to_billing", "ignore"]


def classify_email(subject: str, body: str, sender: str, task_id: str) -> dict:
    """Call LLM to classify the email. Returns dict with category, priority, action."""
    
    system_prompt = """You are an expert email triage AI. Classify the given email.
Respond ONLY with a valid JSON object with these exact keys:
{
  "category": "<one of: Spam, Urgent, Technical, HR, Billing, Support, General>",
  "priority": "<one of: High, Medium, Low>",
  "action": "<one of: auto_reply, escalate, archive, forward_to_dev, forward_to_billing, ignore>",
  "reasoning": "<one short sentence>"
}

Category rules:
- Spam: unsolicited promotional, scam, phishing, fake prizes
- Urgent: system down, breach, critical failures needing immediate attention
- Technical: bugs, APIs, code, infrastructure, SSL, performance issues
- HR: leave, salary, performance reviews, HR policies
- Billing: invoices, payments, refunds, subscription issues
- Support: customer complaints, refund requests, help requests
- General: meetings, general announcements

Priority rules:
- High: requires same-day action, system down, security, overdue payments
- Medium: needs action within 2–3 days
- Low: informational, not time-sensitive

Action rules:
- Spam → archive
- Urgent → escalate
- Technical → forward_to_dev
- HR → auto_reply
- Billing → forward_to_billing
- Support → escalate
- General → auto_reply"""

    user_prompt = f"""Email to classify:
From: {sender}
Subject: {subject}
Body: {body}"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt}
            ],
            temperature=0.0,
            max_tokens=200
        )
        raw = response.choices[0].message.content.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except Exception as e:
        print(f"    [LLM ERROR] {e} — using fallback heuristic")
        return _heuristic_fallback(subject, body)


def _heuristic_fallback(subject: str, body: str) -> dict:
    """Rule-based fallback when LLM is unavailable."""
    text = (subject + " " + body).lower()
    if any(w in text for w in ["free", "win", "prize", "lottery", "gift card", "click here", "no prescription", "cheap meds"]):
        return {"category": "Spam",      "priority": "Low",    "action": "archive",            "reasoning": "Spam keywords detected"}
    if any(w in text for w in ["urgent", "server down", "503", "breach", "critical", "site down", "production"]):
        return {"category": "Urgent",    "priority": "High",   "action": "escalate",           "reasoning": "Urgency keywords found"}
    if any(w in text for w in ["api", "bug", "crash", "ssl", "database", "memory leak", "sdk", "migration", "node.js"]):
        return {"category": "Technical", "priority": "Medium", "action": "forward_to_dev",     "reasoning": "Technical keywords found"}
    if any(w in text for w in ["leave", "salary", "hr", "performance review", "appraisal"]):
        return {"category": "HR",        "priority": "Medium", "action": "auto_reply",          "reasoning": "HR keywords found"}
    if any(w in text for w in ["invoice", "payment", "billing", "overdue", "subscription", "charged", "refund", "duplicate"]):
        return {"category": "Billing",   "priority": "High",   "action": "forward_to_billing", "reasoning": "Billing keywords found"}
    if any(w in text for w in ["refund", "complaint", "support", "order", "not received", "rude"]):
        return {"category": "Support",   "priority": "High",   "action": "escalate",           "reasoning": "Support request"}
    return {"category": "General", "priority": "Low", "action": "auto_reply", "reasoning": "No specific pattern matched"}


def run_task(task_id: str) -> float:
    """Run a full episode for one task. Returns final average score."""
    
    print(f"\n{'='*60}")
    print(f"[START] task_id={task_id}")
    print(f"{'='*60}")

    # Reset environment
    try:
        res = httpx.post(f"{ENV_URL}/reset?task_id={task_id}", timeout=15.0)
        res.raise_for_status()
        obs = res.json()
    except Exception as e:
        print(f"[ERROR] Could not reset environment: {e}")
        print(f"[END] task_id={task_id} score=0.0")
        return 0.0

    episode_rewards = []
    step_num = 0
    done = False

    while not done:
        email_id  = obs.get("email_id", "unknown")
        subject   = obs.get("subject",  "")
        body      = obs.get("content",  "")
        sender    = obs.get("sender",   "")

        if email_id in ("done", "") or not subject:
            break

        step_num += 1
        print(f"\n  [STEP {step_num}] Processing email: {email_id}")
        print(f"    Subject : {subject[:60]}...")
        print(f"    Sender  : {sender}")

        # LLM classification
        result = classify_email(subject, body, sender, task_id)
        cat    = result.get("category", "General")
        pri    = result.get("priority", "Low")
        act    = result.get("action",   "auto_reply")
        reason = result.get("reasoning", "")

        print(f"    Prediction → Category: {cat} | Priority: {pri} | Action: {act}")
        print(f"    Reasoning  : {reason}")

        # Submit to environment
        action_value = f"{cat}|{pri}|{act}"
        payload = {"action_type": "full_triage", "value": action_value}

        try:
            step_res = httpx.post(f"{ENV_URL}/step", json=payload, timeout=15.0)
            step_res.raise_for_status()
            step_data = step_res.json()
        except Exception as e:
            print(f"    [ERROR] Step failed: {e}")
            break

        reward  = step_data.get("reward", 0.0)
        done    = step_data.get("done",   True)
        info    = step_data.get("info",   {})
        obs     = step_data.get("observation", {})

        episode_rewards.append(reward)

        # Breakdown
        bd = info.get("breakdown", {})
        actual_cat = info.get("email_category", "?")
        actual_pri = info.get("email_priority", "?")

        print(f"    → Reward   : {reward:.4f}")
        if bd:
            for field, details in bd.items():
                if isinstance(details, dict):
                    status = "✓ CORRECT" if details.get("score", 0) > 0 else f"✗ WRONG (actual: {details.get('actual','?')})"
                    print(f"       {field}: {details.get('predicted','?')} {status}")

        # MANDATORY [STEP] log line
        print(f"[STEP] task_id={task_id} step={step_num} email_id={email_id} action={action_value} reward={reward:.4f} done={done}")

        time.sleep(0.3)  # Rate limit protection

    # Final score
    final_score = sum(episode_rewards) / len(episode_rewards) if episode_rewards else 0.0

    print(f"\n{'─'*60}")
    print(f"  Task Summary: {task_id}")
    print(f"  Emails processed : {len(episode_rewards)}")
    print(f"  Rewards          : {[round(r,3) for r in episode_rewards]}")
    print(f"  Average score    : {final_score:.4f}")
    
    # MANDATORY [END] log line
    print(f"[END] task_id={task_id} score={final_score:.4f}")
    print(f"{'='*60}")

    return final_score


def main():
    print("\n" + "█"*60)
    print("  EmailTriagePro — Baseline Inference")
    print(f"  Model    : {MODEL_NAME}")
    print(f"  Base URL : {API_BASE_URL}")
    print(f"  Env URL  : {ENV_URL}")
    print("█"*60)

    tasks = ["task_1_easy", "task_2_medium", "task_3_hard"]
    all_scores = {}

    for task_id in tasks:
        score = run_task(task_id)
        all_scores[task_id] = score
        time.sleep(1)

    # Final summary table
    print("\n" + "█"*60)
    print("  FINAL RESULTS")
    print("█"*60)
    print(f"  {'Task':<25} {'Score':>8}  {'%':>6}  {'Status':>10}")
    print(f"  {'─'*55}")
    
    overall = 0.0
    for task_id, score in all_scores.items():
        pct = score * 100
        status = "PASS ✓" if score >= 0.5 else "FAIL ✗"
        print(f"  {task_id:<25} {score:>8.4f}  {pct:>5.1f}%  {status:>10}")
        overall += score
    
    overall_avg = overall / len(all_scores)
    print(f"  {'─'*55}")
    print(f"  {'OVERALL AVERAGE':<25} {overall_avg:>8.4f}  {overall_avg*100:>5.1f}%")
    print("█"*60 + "\n")
    
    return all_scores


if __name__ == "__main__":
    main()
