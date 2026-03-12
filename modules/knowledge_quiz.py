"""
knowledge_quiz.py — Module 2: Knowledge & Quiz Center

Study mode: generates a structured study guide for the selected topic.
Quiz mode: generates 5 multiple-choice questions, presents them one at a time,
           tracks answers, and provides a scored results summary.
"""

import re
import streamlit as st
from modules.llm_client import is_api_available, run_with_spinner, show_no_api_key_warning, module_header, output_header

# ---------------------------------------------------------------------------
# Topic list
# ---------------------------------------------------------------------------
TOPICS = [
    "Fire Behavior & Dynamics",
    "Building Construction",
    "Hose Operations",
    "Ground Ladders",
    "Search & Rescue",
    "Ventilation",
    "Knots & Rope Rescue Basics",
    "Incident Command System (ICS)",
    "EMS Basics for Firefighters",
    "Firefighter Survival",
    "MAYDAY Procedures",
    "Pump Operations",
]

# ---------------------------------------------------------------------------
# Sample study guide (demo mode)
# ---------------------------------------------------------------------------
SAMPLE_STUDY_GUIDE = """
## Fire Behavior & Dynamics — Study Guide

---

### Core Concepts

**The Fire Tetrahedron**
Fire requires four components: fuel, heat, oxygen, and a chemical chain reaction. Remove any one element and combustion stops. Modern firefighting tactics leverage this — water removes heat; foam smothers oxygen; dry chemical interrupts the chain reaction.

**Heat Transfer**
- **Conduction:** Heat moves through direct contact (e.g., metal door handle warns of fire on the other side)
- **Convection:** Heat moves through gases and liquids — the primary mechanism of fire spread in a structure
- **Radiation:** Heat travels as electromagnetic waves — how exposures ignite across open space

**Stages of Fire Development**
1. **Incipient:** Low heat, limited fuel consumption — window for safe intervention
2. **Growth:** Fire grows as it finds fuel and oxygen; temps rise rapidly
3. **Flashover:** All combustibles in the compartment reach ignition temperature simultaneously — a survivability threshold
4. **Fully Developed:** Peak heat release rate; structural damage likely
5. **Decay:** Fuel or oxygen exhausts — fire diminishes

---

### Critical Modern Concepts

**Ventilation-Limited vs. Fuel-Limited Fires**
Most modern structure fires (synthetic furnishings, energy-efficient construction) are *ventilation-limited* — the fire is oxygen-starved and waiting for an opening. Opening a door or window can dramatically accelerate fire growth. Coordinate ventilation with water application.

**Flow Path**
Air moves from high pressure (outside) to low pressure (the fire compartment). Understanding flow path tells you where fire and hot gases will travel when openings are created. Firefighters entering a structure are often moving against the flow path.

**Thermal Layering (Stratification)**
Hot gases rise and stratify — coolest air is at floor level. Maintain low body position during interior operations. Unnecessary ventilation breaks thermal layering and may push superheated gases toward crews.

**Backdraft**
Occurs when a smoldering, oxygen-depleted fire receives a sudden air supply. Warning signs: puffing or breathing smoke from openings, oily smoke deposits on windows, absence of visible flames. Tactical response: ventilate above the fire before opening entry points.

**Rollover / Flameover**
Flames rolling across the ceiling layer ahead of the main fire front. A warning indicator of impending flashover. Take immediate action: apply water to the ceiling, retreat, or both.

---

### Key Takeaways

- **Modern fire behavior is faster and more dangerous** than legacy training suggested — synthetics ignite and burn more intensely than legacy wood/cotton furnishings
- **Uncoordinated ventilation kills** — always communicate with the attack crew before opening the building
- **Flow path awareness is a survival skill** — know where air is going and where fire will follow
- **Flashover is rarely survivable** — recognize the pre-indicators and act before it happens

---

### Recommended References
- IFSTA *Essentials of Fire Fighting*, Chapter 2 (Fire Behavior)
- NFPA 1001 Standard (Firefighter I & II Knowledge Requirements)
- UL Firefighter Safety Research Institute: *Impact of Fire Attack Utilizing Interior and Exterior Streams*
"""

# ---------------------------------------------------------------------------
# Sample quiz questions (demo mode)
# ---------------------------------------------------------------------------
SAMPLE_QUESTIONS = [
    {
        "question": "Which component of the fire tetrahedron do dry chemical agents primarily target?",
        "options": ["A) Fuel", "B) Oxygen", "C) Heat", "D) Chemical chain reaction"],
        "correct": "D",
        "explanation": "Dry chemical agents work by chemically interrupting the chain reaction that sustains combustion, making them effective on Class B and C fires.",
    },
    {
        "question": "A ventilation-limited fire is one that:",
        "options": [
            "A) Has insufficient fuel to sustain combustion",
            "B) Is oxygen-starved and will accelerate rapidly if air is introduced",
            "C) Has already reached flashover",
            "D) Can be safely extinguished without water",
        ],
        "correct": "B",
        "explanation": "Ventilation-limited fires are common in modern structures with energy-efficient construction. They are starved of oxygen and can dramatically accelerate if a door or window is opened — coordinated VES and attack timing is critical.",
    },
    {
        "question": "What is the primary mechanism of fire spread inside a structure?",
        "options": ["A) Conduction", "B) Radiation", "C) Convection", "D) Direct flame impingement"],
        "correct": "C",
        "explanation": "Convection — the movement of heat through gases — is the primary spread mechanism inside buildings. Hot gases rise, travel through openings, and preheat combustibles in adjacent compartments.",
    },
    {
        "question": "Which of the following is a warning sign of potential backdraft conditions?",
        "options": [
            "A) Heavy flame visible through all windows",
            "B) Doors that are cool to the touch",
            "C) Puffing or rhythmic movement of smoke from small openings",
            "D) Rapid flame extension from the eaves",
        ],
        "correct": "C",
        "explanation": "Puffing or breathing smoke from small openings (the fire is literally 'breathing') indicates an oxygen-starved compartment seeking air — a classic backdraft indicator. Other signs include oily deposits on windows and absence of visible flames.",
    },
    {
        "question": "What is 'flow path' in the context of modern fire behavior?",
        "options": [
            "A) The route water travels from the hydrant to the nozzle",
            "B) The movement of air from high pressure areas to low pressure (the fire compartment)",
            "C) The path firefighters take during a primary search",
            "D) The progression of fire between floors via pipe chases",
        ],
        "correct": "B",
        "explanation": "Flow path describes the movement of air (and hot gases) based on pressure differentials. Fresh air moves toward the fire; hot gases move away. Firefighters working against the flow path are in a high-risk environment.",
    },
]


# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------
def build_study_guide_prompt(topic: str) -> str:
    return f"""Create a comprehensive but concise study guide on the fire service topic: **{topic}**

Structure it as follows:

## {topic} — Study Guide

### Core Concepts
Cover the 3–5 most important foundational concepts a firefighter must understand. Use clear explanations. Define terms the first time they appear.

### Critical Operational Knowledge
Cover what a firefighter must know to apply this knowledge safely on the fireground. Include relevant warnings, indicators, or decision points.

### Key Takeaways
Bullet list of the 4–6 most important things to remember.

### Recommended References
List 2–3 relevant NFPA standards, IFSTA chapters, or USFA publications.

Keep the language direct and practical — this is for working firefighters reviewing before a test or drill, not an academic audience."""


def build_quiz_prompt(topic: str, num_questions: int) -> str:
    return f"""Generate {num_questions} multiple-choice quiz questions on the fire service topic: **{topic}**

Format each question EXACTLY as follows (use these exact markers):

QUESTION: [Question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
CORRECT: [Letter only — A, B, C, or D]
EXPLANATION: [1–2 sentence explanation of why the correct answer is right and why the others are wrong]
---

Rules:
- Questions should test practical, operational knowledge
- Include a mix of conceptual and applied questions
- Distractors (wrong answers) should be plausible, not obviously wrong
- Explanations should reinforce the learning, not just repeat the answer
- Cover different aspects of the topic across the {num_questions} questions"""


# ---------------------------------------------------------------------------
# Quiz parser
# ---------------------------------------------------------------------------
def parse_quiz_questions(raw: str) -> list[dict]:
    """Parse LLM output into a list of question dicts."""
    questions = []
    blocks = re.split(r"\n---+\n", raw.strip())

    for block in blocks:
        block = block.strip()
        if not block:
            continue
        try:
            q_match = re.search(r"QUESTION:\s*(.+?)(?=\nA\))", block, re.DOTALL)
            a_match = re.search(r"A\)\s*(.+?)(?=\nB\))", block, re.DOTALL)
            b_match = re.search(r"B\)\s*(.+?)(?=\nC\))", block, re.DOTALL)
            c_match = re.search(r"C\)\s*(.+?)(?=\nD\))", block, re.DOTALL)
            d_match = re.search(r"D\)\s*(.+?)(?=\nCORRECT:)", block, re.DOTALL)
            correct_match = re.search(r"CORRECT:\s*([A-D])", block)
            explanation_match = re.search(r"EXPLANATION:\s*(.+)", block, re.DOTALL)

            if all([q_match, a_match, b_match, c_match, d_match, correct_match, explanation_match]):
                questions.append({
                    "question": q_match.group(1).strip(),
                    "options": [
                        f"A) {a_match.group(1).strip()}",
                        f"B) {b_match.group(1).strip()}",
                        f"C) {c_match.group(1).strip()}",
                        f"D) {d_match.group(1).strip()}",
                    ],
                    "correct": correct_match.group(1).strip(),
                    "explanation": explanation_match.group(1).strip(),
                })
        except Exception:
            continue  # Skip malformed blocks

    return questions


# ---------------------------------------------------------------------------
# Session state helpers
# ---------------------------------------------------------------------------
def init_quiz_state() -> None:
    defaults = {
        "quiz_questions": [],
        "quiz_index": 0,
        "quiz_answers": [],
        "quiz_complete": False,
        "quiz_submitted": False,
        "quiz_topic": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_quiz() -> None:
    keys = ["quiz_questions", "quiz_index", "quiz_answers", "quiz_complete",
            "quiz_submitted", "quiz_topic"]
    for key in keys:
        if key in st.session_state:
            del st.session_state[key]
    init_quiz_state()


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------
def render() -> None:
    """Render the Knowledge & Quiz Center module."""
    module_header(
        icon="📚",
        title="Knowledge & Quiz Center",
        description=(
            "Brush up on core fire service knowledge with AI-generated study guides, "
            "or challenge yourself with a scored interactive quiz. Covers 12 essential topics — "
            "from fire behavior and building construction to MAYDAY procedures and pump operations."
        ),
        audience="Firefighters · Promotional Candidates · Recruits",
    )
    st.divider()

    init_quiz_state()

    # Mode selector
    mode = st.radio("Select Mode", ["Study Mode", "Quiz Mode"], horizontal=True)
    topic = st.selectbox("Select Topic", TOPICS)

    # =========================================================
    # STUDY MODE
    # =========================================================
    if mode == "Study Mode":
        if st.button("Generate Study Guide", use_container_width=True):
            if not is_api_available():
                show_no_api_key_warning()
                result = SAMPLE_STUDY_GUIDE
            else:
                result = run_with_spinner(build_study_guide_prompt(topic), max_tokens=2000)
                if result is None:
                    st.error("Could not generate study guide. Check your API key.")
                    return

            st.divider()
            output_header(f"Study Guide — {topic}")
            with st.container(border=True):
                st.markdown(result)
            st.download_button(
                label="⬇  Download Study Guide",
                data=result,
                file_name=f"fireready_study_{topic.replace(' ', '_')}.md",
                mime="text/markdown",
            )

    # =========================================================
    # QUIZ MODE
    # =========================================================
    else:
        num_q = st.radio("Number of Questions", [5, 10], horizontal=True)

        # Start quiz button (only show if no active quiz)
        if not st.session_state.quiz_questions:
            if st.button("Start Quiz", use_container_width=True):
                reset_quiz()
                st.session_state.quiz_topic = topic

                if not is_api_available():
                    show_no_api_key_warning()
                    st.session_state.quiz_questions = SAMPLE_QUESTIONS[:num_q]
                else:
                    with st.spinner("Generating quiz questions..."):
                        raw = run_with_spinner(
                            build_quiz_prompt(topic, num_q), max_tokens=2500
                        )
                    if not raw:
                        st.error("Could not generate quiz. Check your API key.")
                        return
                    parsed = parse_quiz_questions(raw)
                    if not parsed:
                        st.error(
                            "Could not parse quiz questions from the AI response. "
                            "Try again — this can occasionally happen with formatting."
                        )
                        return
                    st.session_state.quiz_questions = parsed
                st.rerun()

        # Active quiz
        if st.session_state.quiz_questions and not st.session_state.quiz_complete:
            idx = st.session_state.quiz_index
            questions = st.session_state.quiz_questions
            total = len(questions)

            st.divider()
            st.markdown(f"**Topic:** {st.session_state.quiz_topic}")
            st.progress((idx) / total, text=f"Question {idx + 1} of {total}")

            q = questions[idx]
            st.subheader(f"Q{idx + 1}: {q['question']}")

            # Use a unique key per question to avoid state conflicts
            answer_key = f"quiz_answer_{idx}"
            selected = st.radio(
                "Select your answer:",
                q["options"],
                key=answer_key,
                index=None,
            )

            col1, col2 = st.columns([1, 4])
            with col1:
                submit_q = st.button("Submit Answer", disabled=(selected is None))

            if submit_q and selected is not None:
                # Extract letter from selection (e.g., "A) Option text" → "A")
                selected_letter = selected[0]
                is_correct = selected_letter == q["correct"]
                st.session_state.quiz_answers.append({
                    "question": q["question"],
                    "selected": selected_letter,
                    "correct": q["correct"],
                    "is_correct": is_correct,
                    "explanation": q["explanation"],
                })

                if is_correct:
                    st.success("Correct!")
                else:
                    st.error(f"Incorrect. The correct answer is **{q['correct']}**.")

                with st.expander("Explanation", expanded=True):
                    st.markdown(q["explanation"])

                # Advance to next question
                if idx + 1 < total:
                    if st.button("Next Question →"):
                        st.session_state.quiz_index += 1
                        st.rerun()
                else:
                    if st.button("See Results →"):
                        st.session_state.quiz_complete = True
                        st.rerun()

        # Quiz results
        if st.session_state.quiz_complete and st.session_state.quiz_answers:
            answers = st.session_state.quiz_answers
            score = sum(1 for a in answers if a["is_correct"])
            total = len(answers)
            pct = int((score / total) * 100)

            st.divider()
            output_header("Quiz Results")

            if pct >= 80:
                st.success(f"Score: **{score}/{total} ({pct}%)** — Strong performance!")
            elif pct >= 60:
                st.warning(f"Score: **{score}/{total} ({pct}%)** — Review the missed topics.")
            else:
                st.error(f"Score: **{score}/{total} ({pct}%)** — Recommend a full review of this topic.")

            st.markdown("---")
            for i, a in enumerate(answers, 1):
                icon = "✅" if a["is_correct"] else "❌"
                with st.expander(f"{icon} Q{i}: {a['question'][:80]}..."):
                    st.markdown(f"**Your answer:** {a['selected']}")
                    st.markdown(f"**Correct answer:** {a['correct']}")
                    st.markdown(f"**Explanation:** {a['explanation']}")

            # Build exportable summary
            export_lines = [
                f"# Quiz Results — {st.session_state.quiz_topic}",
                f"**Score: {score}/{total} ({pct}%)**\n",
            ]
            for i, a in enumerate(answers, 1):
                status = "CORRECT" if a["is_correct"] else "INCORRECT"
                export_lines.append(
                    f"### Q{i} [{status}]\n{a['question']}\n"
                    f"Your answer: {a['selected']} | Correct: {a['correct']}\n"
                    f"Explanation: {a['explanation']}\n"
                )
            export_text = "\n".join(export_lines)

            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "⬇  Download Results",
                    data=export_text,
                    file_name="fireready_quiz_results.md",
                    mime="text/markdown",
                )
            with col2:
                if st.button("Retake Quiz / New Topic"):
                    reset_quiz()
                    st.rerun()
