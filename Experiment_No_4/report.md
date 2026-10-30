# Experiment 4: ReAct Agent Implementation for Network Diagnostics

## 1. Aim

To implement a ReAct (Reasoning and Acting) agent using a Large Language Model (LLM) for network diagnostics, enabling it to analyse network conditions, execute diagnostic tools, observe results, and perform corrective actions.

## 2. Objectives

- To understand the ReAct prompting framework.
- To implement the Thought → Action → Observation → Final Answer cycle.
- To integrate an LLM using the Groq API.
- To develop simulated network diagnostic tools using Python.
- To enable the agent to identify network issues based on tool observations.
- To perform corrective actions and analyse the resulting network conditions.

## 3. Theory

### ReAct Framework

ReAct stands for Reasoning and Acting. It is an approach in which a Large Language Model combines reasoning with external tool execution to solve a problem.

Instead of generating an answer directly, the model interacts with its environment through a sequence of actions and observations.

The main components are:

**1. Thought**

The agent analyses the current problem and determines what information is required.

**2. Action**

The agent selects an appropriate tool and provides the required input.

**3. Observation**

The selected Python function executes and returns an actual result to the agent.

**4. Reasoning**

The agent uses the observation to decide its next diagnostic step.

**5. Final Answer**

After gathering sufficient information and performing the required actions, the agent generates a final response.

### ReAct Execution Flow

```text
       User Query
            |
            v
     LLM Reasoning
            |
            v
         Thought
            |
            v
          Action
            |
            v
     Execute Python Tool
            |
            v
       Observation
            |
            v
      LLM Reasoning
            |
            |
       More Actions?
         /       \
       Yes        No
        |          |
        v          v
    Next Tool   Final Answer
```

The cycle continues until the agent has sufficient information to provide its final answer or reaches its execution limit.

## 4. Software and Libraries Required

- Python
- Groq API
- `groq` Python package
- `python-dotenv` package
- Regular Expression (`re`) module
- `pathlib` module

**LLM Model:** `openai/gpt-oss-120b`

## 5. Implementation

The experiment implements a simulated network environment using Python.

### A. Initial Network State

The network state is represented using a Python dictionary.

| Component | Initial Value |
|---|---|
| US East Edge Status | Degraded |
| US East Ping | 312 ms |
| US East CPU Load | 94.2% |
| US West Edge Status | Nominal |
| US West Ping | 28 ms |
| Routing Daemon | Hung |
| Routing Daemon Memory | 142 MB |

### B. Diagnostic Tools

Four Python functions are implemented as tools for the ReAct agent.

| Function | Purpose |
|---|---|
| `ping_server()` | Checks network latency for a specified server. |
| `check_service_status()` | Checks the status of the routing daemon. |
| `inspect_cpu_load()` | Checks CPU utilisation of a specified server. |
| `restart_daemon()` | Simulates restarting the routing daemon and updates the network state. |

### C. LLM Integration

The Groq API is used to connect the Python application with the `openai/gpt-oss-120b` model.

The API key is stored in a `.env` file and loaded using `python-dotenv`.

The model receives the diagnostic task and available tool descriptions. It selects the required tool based on the problem and the observations received from previous executions.

### D. Action Execution

The model response is processed using regular expressions to identify the requested action and its input.

The corresponding Python function is executed, and its actual return value is appended to the conversation as an observation.

The agent processes one tool action at a time, preventing additional tool calls generated in the same model response from being executed without a new cycle.

The agent also uses an execution limit to prevent an unlimited loop.

## 6. Problem Statement

The agent is assigned the following network troubleshooting task:

Investigate the US East and US West edge servers, identify any abnormal network conditions, inspect the routing daemon, and restart it if required. After the corrective action, verify the network latency of both edge servers.

## 7. Execution and Observations

The following observations were obtained during the successful execution of the experiment.

| Cycle | Action Performed | Actual Observation |
|---|---|---|
| 1 | Ping US West Edge | Latency: 28 ms |
| 2 | Check Routing Daemon | Status: Hung; Memory: 142 MB |
| 3 | Ping US East Edge | Latency: 312 ms |
| 4 | Inspect US East CPU | CPU Load: 94.2% |
| 5 | Restart Routing Daemon | Restart successful; simulated metrics normalised |
| 6 | Ping US East Edge | Latency: 32 ms |
| 7 | Ping US West Edge | Latency: 28 ms |

### Initial Network Condition

The US East Edge server showed degraded performance with a ping latency of 312 ms and CPU utilisation of 94.2%.

The routing daemon was also found to be hung, indicating a service-level issue in the simulated environment.

The US West Edge server was operating normally with a ping latency of 28 ms.

### Corrective Action

Based on the observations, the agent selected the `restart_daemon()` function to restart the routing daemon.

The tool returned the following observation:

```text
SUCCESS: routing_daemon restarted.
Edge cluster metrics normalized.
```

The simulated restart function updated the routing daemon state to running and normalised the US East server metrics.

### Post-Restart Verification

The agent performed additional ping checks after restarting the daemon.

| Server | Initial Ping | Post-Restart Ping |
|---|---:|---:|
| US East Edge | 312 ms | 32 ms |
| US West Edge | 28 ms | 28 ms |

The US East latency decreased significantly, while the US West latency remained unchanged.

Note: Post-restart ping values were independently checked using the diagnostic tool. The updated CPU load and routing daemon state were set by the simulated restart function but were not independently queried again after the restart.

## 8. Result Analysis

The experiment successfully demonstrated the ReAct agent's ability to:

1. Analyse a network troubleshooting task.
2. Select appropriate diagnostic tools.
3. Retrieve network latency and CPU utilisation.
4. Identify the hung routing daemon.
5. Execute a corrective action.
6. Verify network latency after the corrective action.
7. Generate a final diagnostic summary.

The US East Edge latency improved from 312 ms to 32 ms after the simulated routing daemon restart.

The US West Edge remained stable at 28 ms throughout the experiment.

## 9. Advantages of ReAct

- Combines reasoning with external tool execution.
- Allows the agent to use real tool observations instead of relying only on generated responses.
- Supports multi-step problem-solving.
- Can perform corrective actions based on diagnostic findings.
- Makes the troubleshooting process more structured and explainable.

## 10. Limitations

- The network environment is simulated using predefined Python values.
- The experiment does not connect to actual network servers.
- The diagnostic tools return predefined simulated observations.
- The LLM may generate incorrect or unnecessary actions, so tool execution must be controlled and validated.
- The results demonstrate the ReAct workflow rather than production-level network monitoring.

## 11. Conclusion

The ReAct agent was successfully implemented using Python and the Groq API.

The agent followed the Thought → Action → Observation → Final Answer approach to investigate simulated network conditions.

It identified a hung routing daemon, observed high CPU utilisation and increased latency on the US East Edge server, and performed a simulated restart.

After the corrective action, the US East ping latency improved from 312 ms to 32 ms, while the US West server maintained a stable latency of 28 ms.

Thus, the experiment demonstrates how a ReAct-based AI agent can combine LLM reasoning and Python tools to perform automated, multi-step network diagnostics and troubleshooting.