import models
import random

# 20 real sample emails with full metadata
SAMPLE_EMAILS = [
    {
        "id": "e001", "subject": "WIN a FREE iPhone 15 Pro - Claim Now!!!",
        "body": "Congratulations! You've been selected to receive a FREE iPhone 15 Pro. Click here to claim your gift card worth $1000. Limited time offer - act NOW!",
        "sender": "promo@win-free-gifts.xyz",
        "category": "Spam", "priority": "Low",
        "keywords": ["free", "win", "gift card", "claim", "limited time"]
    },
    {
        "id": "e002", "subject": "URGENT: Server Down - Production at Risk",
        "body": "Our main production server is down. Users cannot access the platform. We need immediate action. Please respond within 10 minutes or escalate to on-call team.",
        "sender": "alerts@company.com",
        "category": "Urgent", "priority": "High",
        "keywords": ["urgent", "server down", "production", "immediate", "escalate"]
    },
    {
        "id": "e003", "subject": "API Rate Limit Issue in v2.3 SDK",
        "body": "Hi team, we are seeing 429 errors when calling the /users endpoint beyond 100 requests/minute. The retry logic in our SDK doesn't seem to be handling exponential backoff correctly.",
        "sender": "dev@partner.io",
        "category": "Technical", "priority": "Medium",
        "keywords": ["api", "rate limit", "sdk", "error", "retry", "endpoint"]
    },
    {
        "id": "e004", "subject": "Leave Application - Sick Leave 3 Days",
        "body": "Dear HR, I am writing to apply for 3 days of sick leave from Monday to Wednesday. I have a medical certificate attached. Please approve at your earliest convenience.",
        "sender": "employee@company.com",
        "category": "HR", "priority": "Medium",
        "keywords": ["leave", "sick", "hr", "apply", "medical", "approve"]
    },
    {
        "id": "e005", "subject": "Invoice #INV-2024-441 Payment Overdue",
        "body": "This is a reminder that invoice #INV-2024-441 for $4,200 is now 15 days overdue. Please process payment immediately to avoid service interruption.",
        "sender": "billing@vendor.com",
        "category": "Billing", "priority": "High",
        "keywords": ["invoice", "payment", "overdue", "billing", "service interruption"]
    },
    {
        "id": "e006", "subject": "You have won $10,000 lottery - Verify now",
        "body": "Dear Winner, Your email was randomly selected in our annual lottery. You have won $10,000. Please verify your bank details to receive your prize money.",
        "sender": "lottery@claim-prize.net",
        "category": "Spam", "priority": "Low",
        "keywords": ["won", "lottery", "prize", "verify", "bank details"]
    },
    {
        "id": "e007", "subject": "Critical Bug - App crashes on login for iOS users",
        "body": "We have identified a critical crash on the login screen for iOS 17+ users. Crash rate is at 34%. The issue is in the OAuth token refresh flow. Needs hotfix before EOD.",
        "sender": "qa@company.com",
        "category": "Technical", "priority": "High",
        "keywords": ["critical", "bug", "crash", "ios", "oauth", "hotfix"]
    },
    {
        "id": "e008", "subject": "Meeting postponed to next Friday",
        "body": "Hi all, the weekly sync originally scheduled for Thursday 3pm has been moved to Friday 10am due to a conflict. Please update your calendars accordingly.",
        "sender": "manager@company.com",
        "category": "General", "priority": "Low",
        "keywords": ["meeting", "postponed", "schedule", "calendar"]
    },
    {
        "id": "e009", "subject": "Refund Request - Order #ORD-78234",
        "body": "Hello, I placed an order on March 5th but still haven't received my package. It has been 12 days. I would like a full refund of $89.99. Please process this immediately.",
        "sender": "customer@gmail.com",
        "category": "Support", "priority": "High",
        "keywords": ["refund", "order", "package", "not received", "full refund"]
    },
    {
        "id": "e010", "subject": "Database migration plan review needed",
        "body": "Team, I've drafted the PostgreSQL to Aurora migration plan. Need a technical review of the schema changes and rollback procedure before we proceed next sprint.",
        "sender": "dba@company.com",
        "category": "Technical", "priority": "Medium",
        "keywords": ["database", "migration", "postgresql", "aurora", "schema", "review"]
    },
    {
        "id": "e011", "subject": "Salary revision letter for FY 2024-25",
        "body": "Dear Employee, Please find attached your salary revision letter for FY 2024-25 effective from April 1st. Kindly sign and return the acknowledgement copy to HR by March 31st.",
        "sender": "hr@company.com",
        "category": "HR", "priority": "Medium",
        "keywords": ["salary", "revision", "hr", "letter", "fy", "acknowledgement"]
    },
    {
        "id": "e012", "subject": "URGENT: Data Breach - Immediate Response Required",
        "body": "Our security team has detected unauthorized access to customer data. An estimated 2,000 user records may be compromised. Legal, InfoSec, and leadership must convene within 1 hour.",
        "sender": "security@company.com",
        "category": "Urgent", "priority": "High",
        "keywords": ["urgent", "data breach", "security", "unauthorized", "compromised", "immediate"]
    },
    {
        "id": "e013", "subject": "Cheap Meds Online - No Prescription Needed",
        "body": "Buy Viagra, Xanax, Ambien online at 90% discount. No prescription required. Discreet shipping worldwide. Order now using promo code: CHEAP2024",
        "sender": "pharma@nodoctorneeded.ru",
        "category": "Spam", "priority": "Low",
        "keywords": ["cheap", "meds", "no prescription", "discount", "promo code"]
    },
    {
        "id": "e014", "subject": "Subscription renewal failed - Action required",
        "body": "Your Premium subscription renewal for $99/year failed. Your card ending in 4242 was declined. Please update your payment method within 48 hours to avoid service interruption.",
        "sender": "noreply@saas-platform.com",
        "category": "Billing", "priority": "High",
        "keywords": ["subscription", "renewal", "failed", "card declined", "payment method"]
    },
    {
        "id": "e015", "subject": "Memory leak in Node.js worker threads",
        "body": "After profiling our worker pool, I found a significant memory leak in the thread recycling logic. RSS memory grows by 50MB every 10 minutes. Here is a heap snapshot for review.",
        "sender": "senior-dev@company.com",
        "category": "Technical", "priority": "Medium",
        "keywords": ["memory leak", "node.js", "worker threads", "heap", "profiling"]
    },
    {
        "id": "e016", "subject": "Quarterly performance review scheduled",
        "body": "This is a reminder that your Q1 performance review is scheduled for April 15th at 2pm with your manager. Please prepare your self-assessment form before the meeting.",
        "sender": "hr@company.com",
        "category": "HR", "priority": "Low",
        "keywords": ["performance review", "quarterly", "self-assessment", "manager"]
    },
    {
        "id": "e017", "subject": "Site down - 503 errors for all users",
        "body": "100% of our users are getting 503 Service Unavailable. Load balancer health checks are failing. This has been ongoing for 8 minutes. Need DevOps on a call NOW.",
        "sender": "monitoring@company.com",
        "category": "Urgent", "priority": "High",
        "keywords": ["site down", "503", "load balancer", "devops", "health check", "failing"]
    },
    {
        "id": "e018", "subject": "Duplicate charge on my account",
        "body": "Hi, I was charged $149 twice on March 12th for my monthly subscription. Transaction IDs: TXN-9921 and TXN-9922. Please refund the duplicate charge as soon as possible.",
        "sender": "user123@gmail.com",
        "category": "Billing", "priority": "Medium",
        "keywords": ["duplicate charge", "charged twice", "subscription", "refund", "transaction"]
    },
    {
        "id": "e019", "subject": "Customer complaint - Rude support agent",
        "body": "I am writing to formally complain about the support I received yesterday. The agent was dismissive and unhelpful. I expect a response and corrective action from your team.",
        "sender": "angry.customer@email.com",
        "category": "Support", "priority": "High",
        "keywords": ["complaint", "rude", "support agent", "formal complaint", "corrective action"]
    },
    {
        "id": "e020", "subject": "SSL certificate expiry warning - 7 days left",
        "body": "Warning: The SSL certificate for api.yourcompany.com will expire in 7 days on April 15th. Please renew it immediately to avoid HTTPS failures and security warnings for users.",
        "sender": "ssl-monitor@company.com",
        "category": "Technical", "priority": "High",
        "keywords": ["ssl", "certificate", "expiry", "renew", "https", "security"]
    }
]

# Task definitions
TASKS = {
    "task_1_easy": {
        "name": "Basic Spam Detection",
        "description": "Identify whether emails are Spam or Not Spam. Binary classification.",
        "email_ids": ["e001", "e006", "e013"],
        "actions_required": ["categorize"],
        "scoring": {"category_match": 1.0}
    },
    "task_2_medium": {
        "name": "Email Category & Priority",
        "description": "Classify emails into categories (Spam/Urgent/Technical/HR/Billing/Support/General) AND set correct priority (High/Medium/Low).",
        "email_ids": ["e002", "e005", "e007", "e009", "e011"],
        "actions_required": ["categorize", "set_priority"],
        "scoring": {"category_match": 0.6, "priority_match": 0.4}
    },
    "task_3_hard": {
        "name": "Full Email Triage with Action",
        "description": "Classify category, set priority, AND decide the correct action (auto_reply/escalate/archive/forward_to_billing/forward_to_dev).",
        "email_ids": ["e003", "e012", "e014", "e017", "e019", "e020"],
        "actions_required": ["categorize", "set_priority", "decide_action"],
        "scoring": {"category_match": 0.4, "priority_match": 0.3, "action_match": 0.3}
    }
}

ACTION_MAP = {
    "Spam": "archive",
    "Urgent": "escalate",
    "Technical": "forward_to_dev",
    "HR": "auto_reply",
    "Billing": "forward_to_billing",
    "Support": "escalate",
    "General": "auto_reply"
}

EMAIL_INDEX = {e["id"]: e for e in SAMPLE_EMAILS}


class EmailEnv:
    def __init__(self):
        self.current_task = None
        self.task_config = None
        self.email_queue = []
        self.current_email_idx = 0
        self.steps = 0
        self.episode_scores = []
        self.action_history = []
        self.max_steps = 20

    def reset(self, task_id: str = "task_1_easy"):
        self.current_task = task_id
        self.task_config = TASKS[task_id]
        self.email_queue = [EMAIL_INDEX[eid] for eid in self.task_config["email_ids"]]
        self.current_email_idx = 0
        self.steps = 0
        self.episode_scores = []
        self.action_history = []

        current_email = self.email_queue[0]
        return models.Observation(
            email_id=current_email["id"],
            subject=current_email["subject"],
            content=current_email["body"],
            sender=current_email["sender"],
            current_status="Unread",
            possible_actions=self.task_config["actions_required"],
            task_name=self.task_config["name"],
            emails_remaining=len(self.email_queue),
            step_count=0
        )

    def _compute_reward(self, email: dict, action: models.Action) -> tuple:
        scoring = self.task_config["scoring"]
        score = 0.0
        breakdown = {}

        if action.action_type == "categorize":
            match = action.value.strip().lower() == email["category"].lower()
            cat_score = scoring.get("category_match", 0.6) if match else 0.0
            score += cat_score
            breakdown["category"] = {"predicted": action.value, "actual": email["category"], "score": cat_score}

        elif action.action_type == "set_priority":
            match = action.value.strip().lower() == email["priority"].lower()
            pri_score = scoring.get("priority_match", 0.4) if match else 0.0
            score += pri_score
            breakdown["priority"] = {"predicted": action.value, "actual": email["priority"], "score": pri_score}

        elif action.action_type == "decide_action":
            expected_action = ACTION_MAP.get(email["category"], "auto_reply")
            match = action.value.strip().lower() == expected_action.lower()
            act_score = scoring.get("action_match", 0.3) if match else 0.0
            score += act_score
            breakdown["action"] = {"predicted": action.value, "actual": expected_action, "score": act_score}

        elif action.action_type == "full_triage":
            # Combined action: value = "category|priority|action"
            parts = action.value.split("|")
            if len(parts) == 3:
                cat, pri, act = parts[0].strip(), parts[1].strip(), parts[2].strip()
                expected_act = ACTION_MAP.get(email["category"], "auto_reply")

                cat_match = cat.lower() == email["category"].lower()
                pri_match = pri.lower() == email["priority"].lower()
                act_match = act.lower() == expected_act.lower()

                cs = scoring.get("category_match", 0.4) if cat_match else 0.0
                ps = scoring.get("priority_match", 0.3) if pri_match else 0.0
                as_ = scoring.get("action_match", 0.3) if act_match else 0.0
                score = cs + ps + as_

                breakdown = {
                    "category": {"predicted": cat, "actual": email["category"], "score": cs},
                    "priority": {"predicted": pri, "actual": email["priority"], "score": ps},
                    "action": {"predicted": act, "actual": expected_act, "score": as_}
                }

        # Penalty for too many steps
        if self.steps > self.max_steps:
            score = max(0.0, score - 0.1)
            breakdown["penalty"] = "excessive_steps"

        return round(min(1.0, max(0.0, score)), 4), breakdown

    def step(self, action: models.Action):
        self.steps += 1

        if self.current_email_idx >= len(self.email_queue):
            return models.Observation(
                email_id="done", subject="All emails processed", content="Episode complete",
                sender="system", current_status="Done", possible_actions=[],
                task_name=self.task_config["name"], emails_remaining=0, step_count=self.steps
            ), 0.0, True, {"message": "Episode already complete"}

        current_email = self.email_queue[self.current_email_idx]
        reward, breakdown = self._compute_reward(current_email, action)
        self.episode_scores.append(reward)
        self.action_history.append({
            "email_id": current_email["id"],
            "action": action.dict(),
            "reward": reward,
            "breakdown": breakdown
        })

        # Move to next email if this is the final action for current email
        final_actions = {"categorize", "full_triage", "decide_action"}
        if action.action_type in final_actions or action.action_type == self.task_config["actions_required"][-1]:
            self.current_email_idx += 1

        done = self.current_email_idx >= len(self.email_queue)
        avg_score = sum(self.episode_scores) / len(self.episode_scores) if self.episode_scores else 0.0

        if done:
            next_obs = models.Observation(
                email_id="done", subject="All Done", content="All emails have been triaged.",
                sender="system", current_status="Complete", possible_actions=[],
                task_name=self.task_config["name"], emails_remaining=0, step_count=self.steps
            )
        else:
            next_email = self.email_queue[self.current_email_idx]
            next_obs = models.Observation(
                email_id=next_email["id"],
                subject=next_email["subject"],
                content=next_email["body"],
                sender=next_email["sender"],
                current_status="Unread",
                possible_actions=self.task_config["actions_required"],
                task_name=self.task_config["name"],
                emails_remaining=len(self.email_queue) - self.current_email_idx,
                step_count=self.steps
            )

        return next_obs, reward, done, {
            "breakdown": breakdown,
            "email_category": current_email["category"],
            "email_priority": current_email["priority"],
            "episode_avg_score": round(avg_score, 4),
            "steps": self.steps,
            "history": self.action_history
        }

    def state(self):
        return {
            "current_task": self.current_task,
            "steps": self.steps,
            "emails_processed": self.current_email_idx,
            "emails_remaining": len(self.email_queue) - self.current_email_idx if self.email_queue else 0,
            "episode_scores": self.episode_scores,
            "avg_score": round(sum(self.episode_scores) / len(self.episode_scores), 4) if self.episode_scores else 0.0
        }

    def get_all_emails(self):
        return SAMPLE_EMAILS

    def get_tasks(self):
        return TASKS
