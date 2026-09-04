Payment Recovery Agent

An AI-powered payment recovery prototype that analyzes failed payments and recommends a recovery strategy based on the reason for failure, payment amount, and how recently the payment failed.

The goal is to explore whether an AI agent can make payment recovery more personalized than using the same generic follow-up for every failed payment.

What It Does

The system takes a list of failed payments containing:

- Customer name
- Payment amount
- Failure reason
- Number of days since the failure

Each payment is sent to the Gemini API, which analyzes the details and recommends one of four recovery actions:

1. Send a reminder email
2. Offer a small discount
3. Send a payment retry link
4. Escalate to a human call

For each payment, the model also provides:

- Recommended action
- Reason for the recommendation
- Confidence score

How It Works

Failed Payments
       ↓
Payment Details
       ↓
Gemini API
       ↓
Recovery Recommendation
       ↓
Simulated Recovery Outcome
       ↓
Recovery Rate / Results

I also built a second script that simulates what would happen if the recommended actions were actually taken.

For example, a direct payment retry link is assumed to have a higher recovery probability than a passive reminder. These assumptions are used only to demonstrate how the system could be evaluated.

Results

Across 30 synthetic test cases, the simulation produced a:

63.3% simulated recovery rate

This number is not a real-world recovery rate. It comes from simulated outcomes based on predefined assumptions and is intended to demonstrate how the system could measure the effectiveness of different recovery strategies.

Reliability & Error Handling

While testing the Gemini API, I started encountering "429" rate-limit errors after making several requests in quick succession.

Instead of allowing the entire pipeline to fail, I added retry logic:

- Retry failed API calls up to 3 times
- Wait between retries
- Fall back to a safe default action if all retries fail

This allows the pipeline to complete even when the API temporarily hits a rate limit or becomes unavailable.

Tech Stack

- Python
- Google Gemini API
- Pandas
- Environment variables for API key management

How to Run

1. Install dependencies

pip install pandas google-generativeai

2. Set your Gemini API key

Set an environment variable named:

GEMINI_API_KEY

3. Run the agent

python script.py

4. Run the simulation

python simulate.py

Dataset

The dataset used in this project is synthetic. It was created specifically to test the recommendation logic because I do not have access to real payment data.

The recovery outcomes are also simulated using predefined assumptions about the effectiveness of each recommended action.

Therefore, the results should not be interpreted as evidence of real-world payment recovery performance.

Limitations & Future Improvements

This is a prototype rather than a production payment recovery system.

Possible improvements include:

- Testing on real, anonymized payment data
- Learning recovery probabilities from historical outcomes
- Comparing AI recommendations against a fixed recovery strategy
- A/B testing different recovery messages
- Adding more payment failure categories
- Tracking actual recovery outcomes over time
- Adding monitoring for API errors, latency, and cost

Project Goal

The main purpose of this project is to demonstrate an end-to-end AI workflow:

Input data → LLM reasoning → actionable recommendation → simulated outcome → measurable evaluation

It focuses not only on getting an AI-generated answer, but also on handling API failures and creating a framework for measuring whether the recommendations would actually be useful.
