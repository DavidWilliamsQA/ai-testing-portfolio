# AI Testing Portfolio: Mock Bank

Testing a fictional UK bank's AI customer-support assistant for **accuracy, safety and reliability**, the same way I'd test a real fintech's AI features before they reach customers.

Built with Python, the Claude API and (from week 3) pytest. This repo is a work in progress: the roadmap below shows what's done and what's next.

## Findings so far

| # | Finding | Why it matters | Status |
|---|---|---|---|
| 1 | When the policy had no answer (e.g. Mock Saver interest rate), the bot said so but still reported `confident: true` | Any system that trusts the confidence flag would treat a non-answer as reliable | Fixed |
| 2 | Out-of-scope answers (savings rate, cheque clearing, joint accounts) didn't refer the customer to the bank | The customer was left with no next step | Fixed |
| 3 | The first fix pointed customers to 0800 000 0000, which is the lost/stolen card and fraud line | A prompt fix introduced a new bug: general enquiries routed to the fraud line | Fixed |
| 4 | With no general contact number in the policy, the bot filled the gap with other numbers it could find (fraud line, complaints line) | The bot invents contact details when the source document has gaps | Fixed |
| 5 | The overdraft answer claimed unarranged overdrafts aren't allowed on Saver accounts; the policy only covers Everyday and Premier | Small over-generalisation beyond the source (low severity) | Fixed |

**How they were fixed:**

- Added rules above the policy in the system prompt: answer only from the policy; if it has no answer, say so, set `confident: false`, and direct the customer to telephone banking or live chat; never guess.
- Added a telephone banking number (0800 000 0002) to the policy, so the bot has a correct number to give, and named it in the prompt.

**Before:** 7/10 fully correct (all 3 out-of-scope answers failed the expected behaviour). **After (latest run):** 10/10. The first run is kept in `test_run_before.json` for comparison.

## Roadmap

- [x] **Week 1: FAQ answer script**
  - [x] Generate a one-page policy for Mock Bank (`policy.md`)
  - [x] `ask.py`: answers questions from the policy with structured JSON output
  - [x] Run 10 test questions with expected answers (`test_questions.json` → `test_run.json`)
  - [x] Fix findings 1–5 and re-run (10/10)
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
| `test_run.json` | Output of the latest run: question, expected answer, actual answer, source, confidence (overwritten each run) |
| `test_run_before.json` | The first run, before the fixes, kept for comparison |
