import pandas as pd
import random

random.seed(42)

df = pd.read_csv("payments_with_recovery_actions.csv")

def simulate_outcome(action, confidence):
    base_rates = {
        "Send a payment retry link": 0.65,
        "Offer a small discount (5-10%)": 0.55,
        "Send a reminder email": 0.35,
        "Escalate to human follow-up call": 0.45
    }
    rate = base_rates.get(action.strip(), 0.4)
    if "High" in confidence:
        rate += 0.15
    elif "Low" in confidence:
        rate -= 0.15
    rate = max(0.1, min(0.9, rate))
    return "Recovered" if random.random() < rate else "Not Recovered"

df["Outcome"] = df.apply(lambda row: simulate_outcome(row["Recommended Action"], row["Confidence"]), axis=1)

recovered_count = (df["Outcome"] == "Recovered").sum()
total = len(df)
recovery_rate = round((recovered_count / total) * 100, 1)

df.to_csv("payments_final_with_outcomes.csv", index=False)

print("Recovered:", recovered_count, "/", total)
print("Recovery Rate:", recovery_rate, "%")
