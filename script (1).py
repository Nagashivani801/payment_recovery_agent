import pandas as pd
import google.generativeai as genai
import time
import os

df = pd.read_csv("payments.csv")
df.columns = df.columns.str.strip()

key = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-3.6-flash")

def build_prompt(name, amount, reason, days):
    p = "You are a payment recovery specialist for a fintech company.\n\n"
    p += "Here is a failed payment record:\n"
    p += "Name: " + str(name) + "\n"
    p += "Amount: " + str(amount) + "\n"
    p += "Failure Reason: " + str(reason) + "\n"
    p += "Days Since Failure: " + str(days) + "\n\n"
    p += "Based on this, recommend ONE recovery action from this list:\n"
    p += "- Send a reminder email\n"
    p += "- Offer a small discount (5-10%)\n"
    p += "- Send a payment retry link\n"
    p += "- Escalate to human follow-up call\n\n"
    p += "Then give a one-line reason for your choice, and rate your confidence (High/Medium/Low) that this recovery will succeed.\n\n"
    p += "Respond in this exact format:\n"
    p += "Action: [action]\n"
    p += "Reason: [one line]\n"
    p += "Confidence: [High/Medium/Low]"
    return p

def get_recovery_action(name, amount, reason, days, retries=3):
    prompt = build_prompt(name, amount, reason, days)
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print("  retrying after error:", str(e)[:80])
            time.sleep(5)
    return "Action: Send a reminder email\nReason: fallback after repeated errors\nConfidence: Low"

actions = []
reasons = []
confidences = []

for idx, row in df.iterrows():
    result = get_recovery_action(row["Name"], row["Amount"], row["Failure Reason"], row["Days Since Failure"])
    lines = [l for l in result.strip().split("\n") if l.strip()]
    action = lines[0].replace("Action:", "").strip() if len(lines) > 0 else "Unknown"
    reason = lines[1].replace("Reason:", "").strip() if len(lines) > 1 else "Unknown"
    confidence = lines[2].replace("Confidence:", "").strip() if len(lines) > 2 else "Low"
    actions.append(action)
    reasons.append(reason)
    confidences.append(confidence)
    print("Row", idx+1, "/", len(df), "done:", row["Name"], "->", action)
    time.sleep(3)

df["Recommended Action"] = actions
df["Reason"] = reasons
df["Confidence"] = confidences
df.to_csv("payments_with_recovery_actions.csv", index=False)
print("Done!")
