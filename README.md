# AI Testing Portfolio: Mock Bank

Testing a fictional UK bank's AI customer-support assistant for **accuracy, safety and reliability**, the same way I'd test a real fintech's AI features before they reach customers.

Built with Python, the Claude API and (from week 3) pytest. This repo is a work in progress: the roadmap below shows what's done and what's next.

## Findings so far

| # | Finding | Why it matters | Status |
|---|---|---|---|
| 1 | When the policy has no answer (e.g. Mock Saver interest rate), the bot says so but still reports `confident: true` | Any system that trusts the confidence flag would treat a non-answer as reliable | Open |
| 2 | Out-of-scope answers (savings rate, cheque clearing, joint accounts) don't refer the customer to the bank | The customer is left with no next step | Open |

**Latest run (week 1, 10 questions):** 7/7 in-scope answers matched the policy; 3/3 out-of-scope questions were correctly declined without guessing.

## Roadmap

- [ ] **Week 1: FAQ answer script**
  - [x] Generate a one-page policy for Mock Bank (`policy.md`)
  - [x] `ask.py`: answers questions from the policy with structured JSON output
  - [x] Run 10 test questions with expected answers (`test_questions.json` → `test_run.json`)
  - [ ] Fix findings 1 and 2 in the system prompt and re-run
- [ ] **Week 2: Mock Bank support bot** (multi-file policy, keyword retrieval, chat loop)
- [ ] **Week 3: First test suite** (50-question golden dataset, pytest, pass rates, GitHub Actions)
- [ ] **Week 4: DeepEval suite** (faithfulness, relevancy, custom rubric, CI quality gate)
- [ ] **Week 5: Red-team report** (Promptfoo: prompt injection, data leakage, financial-advice probes)
- [ ] **Week 6: Agent tests** (tool calls: right tool, right arguments, right order)
- [ ] **Week 7: Load test and monitoring** (latency, cost, consistency, Langfuse tracing)
- [ ] **Week 8: Package it** (findings write-up, demo video)

## How to run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install anthropic python-dotenv
```

Create a `.env` file with your API key:

```
ANTHROPIC_API_KEY=your-key-here
```

Then run the test questions:

```bash
python ask.py
```

Results are written to `test_run.json`.

## Files

| File | What it is |
|---|---|
| `policy.md` | The fictional Mock Bank customer account policy the bot answers from |
| `ask.py` | Sends questions to Claude with the policy as context and records the answers |
| `test_questions.json` | Test questions with expected answers, including out-of-scope ones |
| `test_run.json` | Output of the latest run: question, expected answer, actual answer, source, confidence |
