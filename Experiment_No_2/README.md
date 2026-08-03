# Experiment No. 2

## Title

Structured JSON Extraction from Unstructured Engineering Logs using Large Language Models

---

## Objective

This experiment demonstrates how a Large Language Model (LLM) can transform unstructured engineering fault logs into structured JSON data using Prompt Engineering. The generated JSON is then validated using Python to ensure it can be safely integrated into software engineering applications.

---

## Technologies Used

- Python 3.x
- Visual Studio Code
- Groq API
- OpenAI Python SDK
- python-dotenv
- JSON Module

---

## Project Structure

```
Experiment_No_2/
│
├── outputs/
│   ├── code.png
│   └── output.png
│
├── exp2.py
├── report.md
└── README.md
```

---

## Features

- Converts unstructured engineering logs into structured JSON.
- Uses Prompt Engineering with a strict JSON schema.
- Enforces JSON-only responses using API-level JSON mode.
- Performs automatic JSON validation using Python.
- Demonstrates deterministic output using Temperature = 0.0.
- Suitable for backend automation and enterprise software pipelines.

---

## Sample Input

```text
URGENT LOG ENTRY - 02-AUG-2026 14:22 UTC

System alert raised on High-Pressure Boiler Unit #4.
Thermal sensors detected overheating in the primary coolant intake loop
and pressure relief valve B.

Operator logged issue under INC-88201.
Severity classified as CRITICAL.

Immediate shutdown initiated and technician dispatch required
to replace intake seals.
```

---

## Sample Output

```json
{
  "incident_id": "INC-88201",
  "equipment_name": "High-Pressure Boiler Unit #4",
  "failure_type": "overheating",
  "severity": "CRITICAL",
  "affected_subsystems": [
    "primary coolant intake loop",
    "pressure relief valve B"
  ],
  "recommended_action": "replace intake seals and shutdown"
}
```

---

## How to Run

### 1. Clone the Repository

```bash
git clone <repository-url>
```

### 2. Navigate to the Experiment Folder

```bash
cd Experiment_No_2
```

### 3. Install Required Packages

```bash
pip install openai python-dotenv
```

### 4. Create a `.env` File

```text
Groq_API_Key=YOUR_GROQ_API_KEY
```

---

### 5. Execute the Program

```bash
python exp2.py
```

---

## Expected Output

The program will:

- Display the unstructured engineering log.
- Generate a structured JSON object using the LLM.
- Validate the generated JSON using Python.
- Print the extracted incident details.
- Confirm successful JSON validation.

---

## Learning Outcomes

- Understand Prompt Engineering for structured data extraction.
- Learn schema enforcement using system prompts.
- Understand deterministic inference using Temperature = 0.0.
- Learn API-level JSON generation.
- Validate LLM outputs programmatically using Python.
- Understand how LLMs integrate with software engineering workflows.

---

## Screenshots

### Program Output

Located in:

```
program_output.png
```

---

## Author

**Nihar Padave**

B.Tech Electronics & Computer Science

Shah & Anchor Kutchhi Engineering College

Artificial Intelligence & Data Science (Honours)

Academic Year: 2026–27

---

## License

This project is created for educational and academic purposes as part of the Artificial Intelligence & Data Science (Honours) laboratory coursework.