# FireReady AI

**An AI-powered firefighter readiness and training platform for individual firefighters and department training officers.**

> FireReady AI is a training, planning, and education tool. It is **not** a live incident command or emergency response system.

---

## Features

| Module | Description |
|--------|-------------|
| **Fitness Planner** | Build role-relevant weekly physical readiness plans |
| **Knowledge & Quiz Center** | Study guides and quizzes across 12 fire service topics |
| **Annual Training Planner** | Crawl-Walk-Run annual drill calendar for training officers |
| **Scenario Trainer** | Branching text-based scenario simulator with debrief |
| **Company Drill Builder** | Single drill night planner with objectives, timeline, and safety |
| **Officer Development** | Command skills, checklists, and leadership prompts |

---

## Setup Instructions

### 1. Prerequisites

- Python 3.10 or higher
- pip

### 2. Clone / Download the Project

Place the project folder on your machine. All files should be in the same root directory.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Your Anthropic API Key

FireReady AI uses the Claude API to generate all content. You need an Anthropic API key.

**Option A — Environment variable (recommended):**

On macOS/Linux:
```bash
export ANTHROPIC_API_KEY=your_key_here
```

On Windows (Command Prompt):
```cmd
set ANTHROPIC_API_KEY=your_key_here
```

On Windows (PowerShell):
```powershell
$env:ANTHROPIC_API_KEY="your_key_here"
```

**Option B — `.env` file:**

Create a file named `.env` in the project root:
```
ANTHROPIC_API_KEY=your_key_here
```

The app will load this automatically via `python-dotenv`.

> If no API key is set, the app will launch in demo mode with pre-written sample content.

### 5. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## Project Structure

```
AI Final/
├── app.py                      # Main Streamlit entry point and routing
├── requirements.txt
├── README.md
└── modules/
    ├── __init__.py
    ├── llm_client.py           # Shared Claude API wrapper and key management
    ├── fitness_planner.py      # Module 1 — Fitness Planner
    ├── knowledge_quiz.py       # Module 2 — Knowledge & Quiz Center
    ├── annual_planner.py       # Module 3 — Annual Training Planner
    ├── scenario_trainer.py     # Module 4 — Interactive Scenario Trainer
    ├── drill_builder.py        # Module 5 — Company Drill Builder
    └── officer_development.py  # Module 6 — Officer Development
```

---

## Architecture Notes

- **Framework:** Streamlit (single-page app with sidebar navigation)
- **AI Backend:** Anthropic Claude API (`claude-opus-4-6`) via the `anthropic` Python SDK
- **State Management:** Streamlit `st.session_state` for multi-step flows (quiz, scenario trainer)
- **Modularity:** Each module is a self-contained Python file with a `render()` entry function called by `app.py`
- **No database:** All session data lives in Streamlit session state; outputs can be exported as Markdown via download buttons
- **Prompt design:** Each module uses a structured system prompt and user prompt to produce consistently formatted, fire-service-specific outputs

---

## How AI Was Used During Development

Claude (claude-opus-4-6) was used in the following ways during the development of this project:

1. **Code generation:** Initial scaffolding and module structure were drafted with Claude assistance, then reviewed and refined manually.
2. **Prompt engineering:** The AI prompts inside each module were iteratively designed to produce practical, realistic fire service language rather than generic chatbot output.
3. **Content design:** Sample scenarios, quiz questions, and training plan structures were tested against Claude outputs to validate realism and educational value.
4. **Code review:** The final codebase was reviewed with Claude to identify error handling gaps and improve UX consistency across modules.

This project demonstrates responsible AI integration: Claude generates training content at runtime, but all prompts, validation logic, UI design, and product framing decisions were made by the developer.

---

## Important Disclaimer

FireReady AI is a **training and education tool only**. It is not intended for use during live emergency incidents. All outputs are AI-generated and should be validated against your department's SOGs, NFPA standards, and local protocols before operational use.
