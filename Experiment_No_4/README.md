# Experiment 4: ReAct Agent Implementation for Network Diagnostics

## Aim

To implement a ReAct (Reasoning and Acting) agent using a Large Language Model (LLM) that performs network diagnostics by following the Thought → Action → Observation → Final Answer cycle.

## Overview

The ReAct framework combines reasoning and tool-based actions. Instead of directly generating an answer, the agent analyses the given problem, selects an appropriate tool, observes its output, and uses that information to decide its next action.

In this experiment, a network diagnostics agent is implemented using the Groq API and the `openai/gpt-oss-120b` model.

The agent investigates simulated network conditions, identifies possible issues, and performs a corrective action when required.

## Technologies Used

- Python
- Groq API
- OpenAI-compatible Groq model: `openai/gpt-oss-120b`
- python-dotenv
- Regular Expressions

## ReAct Architecture

The agent follows this execution cycle:

1. **Thought:** Analyses the network problem and decides what information is required.
2. **Action:** Selects and executes an available diagnostic tool.
3. **Observation:** Receives the actual output returned by the Python tool.
4. **Reasoning:** Uses the observation to decide the next step.
5. **Final Answer:** Summarises the identified issue and the actions performed.

## Available Diagnostic Tools

The experiment implements four simulated network diagnostic tools.

| Tool | Description |
|---|---|
| `ping_server(server_id)` | Checks the simulated ping latency of a server. |
| `check_service_status(service_name)` | Checks the status of a network service. |
| `inspect_cpu_load(server_id)` | Checks the CPU utilisation of a server. |
| `restart_daemon(service_name)` | Restarts the specified service and updates the simulated network state. |

## Simulated Network Environment

The experiment uses a predefined Python dictionary to represent the network environment.

Initial network conditions:

| Component | Initial State |
|---|---|
| US East Edge | Degraded |
| US East Ping | 312 ms |
| US East CPU Load | 94.2% |
| US West Edge | Nominal |
| US West Ping | 28 ms |
| Routing Daemon | Hung |

The `restart_daemon()` function simulates recovery by updating the routing daemon status and normalising the US East network metrics.

## Project Structure

```text
Experiment_No_4/
│
├── exp4.py
├── requirements.txt
├── README.md
├── report.md
│
└── outputs/
    ├── code.png
    └── output.png
```

The `.env` file is maintained in the project root directory, one level above the experiment folder.

## Installation and Setup

### 1. Install Dependencies

Open the terminal in the project root directory and run:

```bash
pip install -r Experiment_No_4/requirements.txt
```

### 2. Configure the API Key

Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=your_actual_groq_api_key
```

Replace the placeholder with your actual Groq API key.

Do not upload or share your API key.

### 3. Run the Experiment

From the project root directory, execute:

```bash
python Experiment_No_4/exp4.py
```

Alternatively, navigate to the experiment folder and run:

```bash
python exp4.py
```

## Execution Results

The agent successfully performed seven actual tool executions during the latest run.

| Step | Tool Executed | Observation |
|---|---|---|
| 1 | `ping_server(us-west-edge)` | 28 ms |
| 2 | `check_service_status(routing_daemon)` | Hung, memory usage 142 MB |
| 3 | `ping_server(us-east-edge)` | 312 ms |
| 4 | `inspect_cpu_load(us-east-edge)` | 94.2% |
| 5 | `restart_daemon(routing_daemon)` | Restart successful |
| 6 | `ping_server(us-east-edge)` | 32 ms |
| 7 | `ping_server(us-west-edge)` | 28 ms |

After the restart, the US East ping latency decreased from 312 ms to 32 ms, while the US West ping remained at 28 ms.

## Conclusion

The ReAct agent successfully demonstrated how an LLM can reason about a network problem, select appropriate diagnostic tools, interpret their observations, and perform a corrective action.

The simulated routing daemon was identified as hung. Restarting it resulted in improved US East network latency.

This experiment demonstrates the practical application of the ReAct framework for automated network diagnostics and troubleshooting.