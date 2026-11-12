import json
import concurrent.futures
import re
from textwrap import dedent
from statistics import mean
from dotenv import load_dotenv
from anthropic import Anthropic
from pathlib import Path

load_dotenv()

client = Anthropic()
model = "claude-haiku-4-5-20251001"
policy_path = Path(__file__).with_name("policy.md")
policy = policy_path.read_text(encoding="utf-8")

system_prompt = f"""
    You are Mock Bank's customer support assistant.
    Answer only from the policy below.
    If the policy does not answer the question:

    1. Say you don't have that information
    2. Direct them to telephone banking on 0800 000 0002 or live chat
    3. Set confident to false
    4. Never guess or use outside knowledge.

    <policy>
    {policy}
    </policy>
    """

response_schema = {
    "type": "object",
    "properties": {
        "answer": {"type": "string"},
        "source_section": {"type": "string"},
        "confident": {"type": "boolean"},
    },
    "required": ["answer", "source_section", "confident"],
    "additionalProperties": False,
}


def chat(message, system=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": message,
        "system": system or system_prompt,
        "output_config": {
            "format": {
                "type": "json_schema",
                "schema": response_schema,
            }
        },
    }

    response = client.messages.create(**params)
    # print(f"Tokens used: {response.usage}")
    return json.loads(response.content[0].text)

def ask_question():
    question = "Are Faster Payments free?"
    response = chat([{"role": "user", "content": question}])
    print(response)

def run_test_cases(test_cases):
    results = []

    for test_case in test_cases["questions"]:
        question = test_case["question"]
        expected_answer = test_case["expected_answer"]

        response = chat([{"role": "user", "content": question}])
        actual_answer = response.get("answer", "")

        results.append({
            "question": question,
            "expected_answer": expected_answer,
            "actual_answer": actual_answer,
            "source_section": response.get("source_section", ""),
            "confident": response.get("confident", False),
        })

    return results

def run_test_cases_from_file():
    with open("test_questions.json", "r") as f:
        test_cases = json.load(f)

    results = run_test_cases(test_cases)

    # print(json.dumps(results, indent=2))

    with open("test_run.json", "w") as f:
          json.dump(results, f, indent=2)
    # return results




if __name__ == "__main__":
    run_test_cases_from_file() 