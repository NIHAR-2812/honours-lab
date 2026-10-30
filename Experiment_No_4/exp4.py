
"""
Experiment 04: ReAct Agent Implementation for Network Diagnostics

Framework:
Dynamic Thought-Action-Observation loop with simulated tools.
"""

import os
import re
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# ---------------------------------------------------------
# 1. Environment Configuration
# ---------------------------------------------------------

# Load .env from the AIDS Honours root directory.
ROOT_ENV = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ROOT_ENV)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY missing. Check the .env file "
        "in the AIDS Honours root directory."
    )

client = Groq(api_key=api_key)

MODEL_NAME = "openai/gpt-oss-120b"


# ---------------------------------------------------------
# 2. Simulated Infrastructure Environment
# ---------------------------------------------------------

SYSTEM_STATE = {
    "us-east-edge": {
        "status": "degraded",
        "ping_ms": 312,
        "cpu_load": 94.2
    },
    "us-west-edge": {
        "status": "nominal",
        "ping_ms": 28,
        "cpu_load": 18.5
    },
    "routing_daemon": "hung"
}


# ---------------------------------------------------------
# 3. Tool Definitions
# ---------------------------------------------------------

def ping_server(server_id: str) -> str:
    """Measure simulated network latency."""

    server_id = server_id.strip().lower()

    if server_id in SYSTEM_STATE and isinstance(
        SYSTEM_STATE[server_id], dict
    ):
        latency = SYSTEM_STATE[server_id]["ping_ms"]

        return (
            f"Ping to {server_id}: SUCCESS | "
            f"Latency: {latency}ms"
        )

    return (
        f"Ping to {server_id}: ERROR | "
        "Host not reachable or unknown."
    )


def check_service_status(service_name: str) -> str:
    """Check simulated infrastructure service status."""

    service_name = service_name.strip().lower()

    if service_name == "routing_daemon":
        status = SYSTEM_STATE["routing_daemon"]

        return (
            f"Service {service_name}: "
            f"State={status}, Memory=142MB"
        )

    return f"Service {service_name}: NOT_FOUND"


def inspect_cpu_load(server_id: str) -> str:
    """Inspect simulated CPU utilization."""

    server_id = server_id.strip().lower()

    if server_id in SYSTEM_STATE and isinstance(
        SYSTEM_STATE[server_id], dict
    ):
        cpu = SYSTEM_STATE[server_id]["cpu_load"]

        return (
            f"{server_id} CPU Utilization: {cpu}%"
        )

    return f"{server_id}: Metrics unavailable."


def restart_daemon(service_name: str) -> str:
    """Simulate restarting a failed infrastructure service."""

    service_name = service_name.strip().lower()

    if service_name == "routing_daemon":

        SYSTEM_STATE["routing_daemon"] = "running"

        SYSTEM_STATE["us-east-edge"]["cpu_load"] = 21.0
        SYSTEM_STATE["us-east-edge"]["ping_ms"] = 32
        SYSTEM_STATE["us-east-edge"]["status"] = "nominal"

        return (
            f"SUCCESS: {service_name} restarted. "
            "Edge cluster metrics normalized."
        )

    return f"FAILURE: Unable to restart {service_name}."


# Tool registry
TOOLS = {
    "ping_server": ping_server,
    "check_service_status": check_service_status,
    "inspect_cpu_load": inspect_cpu_load,
    "restart_daemon": restart_daemon
}


# ---------------------------------------------------------
# 4. ReAct Prompt Specification
# ---------------------------------------------------------

REACT_PROMPT = """
You are an automated Site Reliability Engineer assistant.

Investigate the technical problem using the ReAct
(Reasoning + Acting) architecture.

Your task is to diagnose the network incident, identify
the root cause, perform the required remediation, and
verify recovery.

AVAILABLE TOOLS:

1. ping_server[server_id]
   Measures network latency to a server.

2. check_service_status[service_name]
   Checks the status of an infrastructure service.

3. inspect_cpu_load[server_id]
   Returns CPU utilization percentage.

4. restart_daemon[service_name]
   Restarts a simulated infrastructure service.

STRICT INSTRUCTIONS:

- Use only the available tools.
- Do not invent tool observations or telemetry values.
- Investigate both us-east-edge and us-west-edge.
- Inspect CPU utilization when necessary.
- Check routing_daemon status before restarting it.
- Restart the daemon only when observations justify it.
- After remediation, verify network recovery.
- Use the actual tool observations in your diagnosis.
- Generate only one tool action at a time.
- Do not generate your own Observation.
- Do not repeat completed tool calls unnecessarily.
- Keep thoughts concise.

REQUIRED RESPONSE FORMAT:

Thought: Briefly explain the next diagnostic step.

Action: One of:
ping_server
check_service_status
inspect_cpu_load
restart_daemon

Action Input: The required argument.

The Python environment will execute the action and
return an Observation.

Continue the Thought-Action-Observation cycle.

When the investigation and verification are complete,
respond using:

Thought: The diagnosis and verification are complete.

Final Answer: Provide a consolidated diagnostic report
including:
- Initial problem
- Evidence collected
- Root cause
- Remediation performed
- Verification results

Do not output an Observation yourself.

Maximum tool executions: 7.

Question:
{question}
"""


# ---------------------------------------------------------
# 5. Action Parser
# ---------------------------------------------------------

def extract_action_and_input(model_output: str):
    """Extract tool name and argument from model response."""

    action_match = re.search(
        r"(?im)^\s*Action:\s*([A-Za-z_]\w*)\s*$",
        model_output
    )

    input_match = re.search(
        r"(?im)^\s*Action Input:\s*(.+?)\s*$",
        model_output
    )

    action = (
        action_match.group(1).strip()
        if action_match else None
    )

    action_input = (
        input_match.group(1).strip()
        if input_match else ""
    )

    return action, action_input


# ---------------------------------------------------------
# 6. ReAct Agent Execution Loop
# ---------------------------------------------------------


def run_react_agent(task: str, max_tool_calls: int = 9):

    prompt_history = REACT_PROMPT.format(question=task)

    tool_calls = 0
    model_cycles = 0
    max_model_cycles = max_tool_calls + 3

    print("\n" + "=" * 65)
    print("INITIALIZING REACT AGENT LOOP")
    print("=" * 65)

    while model_cycles < max_model_cycles:

        model_cycles += 1

        print(f"\n--- Cycle {model_cycles} ---")

        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": prompt_history
                    }
                ],
                temperature=0.0,
                max_tokens=700
            )

            generated_step = (
                response.choices[0].message.content or ""
            ).strip()

            if not generated_step:
                print("Empty response received.")
                print(
                    "Finish reason:",
                    response.choices[0].finish_reason
                )
                return

        except Exception as error:
            print(f"API Error: {error}")
            return

        print(generated_step)

        # Extract the first action from the model response.
        action, action_input = extract_action_and_input(
            generated_step
        )

        # If an action exists, execute ONLY that action.
        # Ignore any additional actions or observations
        # generated in the same model response.

        if action and action_input:

            if action not in TOOLS:
                observation = (
                    f"ERROR: Unknown tool '{action}'. "
                    f"Available tools: {', '.join(TOOLS.keys())}"
                )

            elif tool_calls >= max_tool_calls:
                print("Maximum tool execution limit reached.")
                return

            else:
                tool_calls += 1

                try:
                    observation = TOOLS[action](action_input)

                except Exception as error:
                    observation = f"Tool execution error: {error}"

            # Keep only the model's response up to the
            # first Action Input line in the conversation.
            input_match = re.search(
                r"(?im)^\s*Action Input:\s*.+$",
                generated_step
            )

            if input_match:
                accepted_step = generated_step[
                    :input_match.end()
                ]
            else:
                accepted_step = generated_step

            prompt_history += "\n" + accepted_step + "\n"

            obs_str = f"Observation: {observation}"

            print(obs_str)

            # Append the real Python tool observation.
            prompt_history += obs_str + "\n"

            continue

        # Accept a final answer only when the model
        # has not requested another tool action.
        if re.search(
            r"(?im)^\s*Final Answer:",
            generated_step
        ):
            prompt_history += "\n" + generated_step

            print("\nExecution terminated: Final Answer reached.")
            print("Total actual tool executions:", tool_calls)
            return

        # No valid action or final answer.
        observation = (
            "ERROR: No valid tool action or Final Answer found. "
            "Provide exactly one valid action or a final answer."
        )

        prompt_history += (
            "\n" + generated_step +
            "\nObservation: " + observation + "\n"
        )

    print("\nMaximum model cycle limit reached.")
    print("Total actual tool executions:", tool_calls)


# ---------------------------------------------------------
# 7. Main Program
# ---------------------------------------------------------

if __name__ == "__main__":

    incident_query = (
        "Server alert: Critical network latency reported "
        "on cluster edge nodes. Investigate us-east-edge "
        "and us-west-edge, diagnose the underlying root "
        "cause, perform the necessary remediation, and "
        "verify full recovery."
    )

    run_react_agent(incident_query)
