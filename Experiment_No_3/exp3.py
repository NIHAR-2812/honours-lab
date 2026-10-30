
"""
Experiment No. 03
Few-Shot and Chain-of-Thought Prompting
for Mathematical Reasoning

Course: Foundations of Artificial Intelligence Lab
CO2, LO3
Model: Groq Cloud through OpenAI-compatible SDK
"""

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

# Load the private API key from .env
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("[ERROR] GROQ_API_KEY not found.")
    print("Create a .env file and add your Groq API key.")
    sys.exit(1)

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
)

MODEL_NAME = "openai/gpt-oss-120b"

TARGET_PROBLEM = (
    "A bakery produces 48 artisan sourdough loaves every "
    "morning. It sells 3/8 of the total loaves to a local "
    "restaurant before noon. In the afternoon, it sells "
    "80% of the remaining loaves to retail customers. If "
    "each unsold loaf is donated at a loss of $1.75 each, "
    "calculate the total monetary loss incurred by the "
    "bakery from unsold loaves."
)


def execute_prompt(system_prompt, user_prompt):
    """Send a prompt to Groq and return the model response."""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
        max_tokens=1024,
    )

    content = response.choices[0].message.content
    return content.strip() if content else "[Empty response]"


# Strategy 1: Zero-Shot Direct
zero_shot_sys = (
    "You are an automated calculation system. "
    "Provide only the final numerical answer."
)

zero_shot_usr = f"Problem: {TARGET_PROBLEM}\nAnswer:"


# Strategy 2: Few-Shot Direct
few_shot_direct_sys = (
    "You are an automated math assistant. "
    "Follow the answer format shown in the examples. "
    "Output only the final answer."
)

few_shot_direct_usr = f"""
Problem: Janet has 16 eggs. She uses 1/4 to bake cookies
and sells half of the remaining eggs. How many eggs are left?

Answer: 6

Problem: Mark earns $120. He allocates 40% to rent and
1/3 of the remaining amount to groceries. How much does
he have left?

Answer: 48

Problem: {TARGET_PROBLEM}

Answer:
"""


# Strategy 3: Zero-Shot Chain-of-Thought
zero_shot_cot_sys = (
    "You are an expert mathematician. "
    "Explain the calculations in clear, concise steps "
    "and give the final answer."
)

zero_shot_cot_usr = (
    f"Problem: {TARGET_PROBLEM}\n"
    "Let's think step by step."
)


# Strategy 4: Few-Shot Chain-of-Thought
few_shot_cot_sys = (
    "You are a mathematical reasoning assistant. "
    "Follow the demonstrated solution format, show the "
    "necessary calculation steps, and state the final answer."
)

few_shot_cot_usr = f"""
Problem: Janet has 16 eggs. She uses 1/4 to bake cookies
and sells half of the remaining eggs. How many eggs are left?

Reasoning:
1. Starting eggs = 16.
2. Eggs used = 16 * (1/4) = 4.
3. Eggs remaining = 16 - 4 = 12.
4. Eggs sold = 12 * (1/2) = 6.
5. Final eggs = 12 - 6 = 6.

Answer: 6

Problem: Mark earns $120. He allocates 40% to rent and
1/3 of the remaining amount to groceries. How much does
he have left?

Reasoning:
1. Initial amount = $120.
2. Rent = 0.40 * 120 = $48.
3. Remaining amount = 120 - 48 = $72.
4. Groceries = 72 / 3 = $24.
5. Final amount = 72 - 24 = $48.

Answer: 48

Problem: {TARGET_PROBLEM}

Reasoning:
"""


def main():
    strategies = [
        (
            "1. ZERO-SHOT DIRECT",
            zero_shot_sys,
            zero_shot_usr,
        ),
        (
            "2. FEW-SHOT DIRECT",
            few_shot_direct_sys,
            few_shot_direct_usr,
        ),
        (
            "3. ZERO-SHOT CHAIN-OF-THOUGHT",
            zero_shot_cot_sys,
            zero_shot_cot_usr,
        ),
        (
            "4. FEW-SHOT CHAIN-OF-THOUGHT",
            few_shot_cot_sys,
            few_shot_cot_usr,
        ),
    ]

    print("=" * 72)
    print("EXPERIMENT 03: PROMPTING FOR MATHEMATICAL REASONING")
    print(f"Model: {MODEL_NAME}")
    print("=" * 72)
    print("\nTARGET PROBLEM")
    print(TARGET_PROBLEM)

    for title, system_prompt, user_prompt in strategies:
        print("\n" + "=" * 72)
        print(title)
        print("=" * 72)

        try:
            result = execute_prompt(system_prompt, user_prompt)
            print(result)
        except Exception as error:
            print(f"[ERROR] {type(error).__name__}: {error}")
            print("Check your API key, internet connection, "
                  "model availability, and Groq usage limits.")

    print("\n" + "=" * 72)
    print("EXPERIMENT EXECUTION FINISHED")
    print("=" * 72)


if __name__ == "__main__":
    main()
