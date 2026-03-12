"""
officer_development.py — Module 6: Officer Development

Supports aspiring lieutenants and captains with command skill development,
including short lessons, command checklists, practice prompts, and
leadership development questions.
"""

import streamlit as st
from modules.llm_client import is_api_available, run_with_spinner, show_no_api_key_warning, module_header, output_header

# ---------------------------------------------------------------------------
# Topic and focus area options
# ---------------------------------------------------------------------------
COMPETENCY_AREAS = [
    "Initial Size-Up & Arrival Report",
    "Strategy & Tactics (Offensive vs. Defensive Decision-Making)",
    "Radio Communication & Command Presence",
    "Personnel Accountability & Crew Tracking",
    "Incident Command Establishment",
    "Fireground Decision-Making Under Pressure",
    "Crew Safety & Risk Management",
    "MAYDAY Management (Receiving & Coordinating RIT)",
    "Multi-Unit Coordination & Span of Control",
    "Post-Incident Critique & Leadership",
    "New Officer Transition — From Firefighter to Company Officer",
    "Training Officer Role & Adult Learning Principles",
]

EXPERIENCE_LEVELS = [
    "Aspiring Officer — No current supervisory experience",
    "New Officer — First 1–2 years in rank",
    "Experienced Officer — 3+ years, seeking advancement",
    "Senior Officer / Captain — Developing subordinate officers",
]

# ---------------------------------------------------------------------------
# Sample output (demo mode)
# ---------------------------------------------------------------------------
SAMPLE_OUTPUT = """
## Officer Development — Initial Size-Up & Arrival Report
**Level:** New Officer — First 1–2 years in rank

---

### Lesson: The First 60 Seconds Define Your Incident

The arrival report is not just a radio transmission — it is the moment you establish command, set the operational tempo, and communicate the tactical picture to every resource responding. Officers who nail their arrival report create a foundation for a coordinated, controlled incident. Officers who skip it or fumble it spend the rest of the incident playing catch-up.

The arrival report should be automatic. It should come out of your mouth before the apparatus stops rolling. By the time you step off the rig, every arriving unit should know: what you see, what you're doing, and who is in command.

---

### The Standard Arrival Report — Structure

A complete arrival report contains five elements (use the mnemonic **"On scene, I see, I have, I'm doing, Command"**):

1. **Unit identification** — who is arriving
2. **Location confirmation** — on scene at [address]
3. **Size-up observation** — what you observe (construction, occupancy, fire/smoke conditions)
4. **Initial action** — what your crew is doing
5. **Command declaration** — who has command and on what channel

**Example — Working Residential Fire:**
> *"Engine 7 is on scene at 1842 Maplewood Drive. We have a two-story wood-frame residence with heavy smoke showing from the first floor, Delta side. Engine 7 is making an offensive interior attack, stretching to the front door. Engine 7 will be Maplewood Command on Fireground Channel 2."*

**Example — Investigative (Nothing Showing):**
> *"Engine 3 is on scene at 550 Commerce Boulevard. We have a four-story commercial building, nothing showing from the exterior. Engine 3 is investigating. Engine 3 has Command."*

---

### Command Checklist — First-Arriving Officer

Use this as a mental checklist in the first 3 minutes of a working incident:

- [ ] **Arrival report transmitted** — unit ID, location, conditions, action, command
- [ ] **360-degree size-up** (or directed to another unit if immediate life safety prevents it)
- [ ] **Strategic mode declared** — offensive, defensive, or transitional
- [ ] **Incident name and command channel established**
- [ ] **First-due crew assigned and confirmed**
- [ ] **Water supply established or assigned** to an incoming unit
- [ ] **Accountability initiated** — know who is on your incident
- [ ] **Initial radio update** given to incoming units within first 3 minutes
- [ ] **Transition to incoming command** if you are going interior (pass command to Sector Officer or transfer to arriving officer)

---

### Practice Prompts

Work through these scenarios out loud or with a partner. Your goal: deliver a complete, confident arrival report in under 20 seconds.

**Scenario 1:** You arrive at a single-story ranch home. Smoke is showing from the attic vents. No flames visible. Your crew of 3 is with you.

**Scenario 2:** You arrive first at a reported alarm activation in a three-story apartment building. Nothing visible on arrival. Several residents are in the parking lot.

**Scenario 3:** You arrive second to a working kitchen fire. The first-due engine has a line deployed. The incident commander asks for your unit's assignment.

**Scenario 4:** You arrive at a commercial strip mall with fire showing from a middle unit. Two exposures on either side. Your second-due is 4 minutes out.

Practice each one until the structure is automatic — the fireground is not the place to remember the format for the first time.

---

### Leadership Development Questions

Reflect on these questions individually or discuss them with your crew or a mentor:

1. **Think of the best arrival report you've ever heard on the radio.** What made it effective? Was it the words, the tone, the information, or the confidence of the officer?

2. **What is the cost of a poor or missing arrival report?** Walk through a working fire where no arrival report was given. What decisions get delayed? What risks increase?

3. **When is it appropriate to skip a formal arrival report and go straight to action?** How does an obvious confirmed life hazard change your initial priorities?

4. **How do you build the habit before you have the opportunity?** What can you do today — on every response, even routine calls — to make arrival reporting automatic?

5. **What does your arrival report communicate beyond information?** Think about tone, pace, and confidence. What does a calm arrival report signal to the crew that is pulling up behind you?

---

### Suggested Follow-Up Drills & Training
- **Tabletop:** Run size-up photos at company training and have each officer candidate deliver a live arrival report
- **Scenario Trainer:** Use FireReady AI's Scenario Trainer to practice decision-making at the arrival point of a working incident
- **Self-Study:** Review NFPA 1021 (Officer Professional Qualifications) — arrival report requirements for Company Officer level
- **Mentorship:** Ride with a senior officer and critique arrival reports together on every response for 30 days

---
*Content generated by FireReady AI. Validate all command procedures against your department's SOGs and applicable NFPA standards.*
"""


def build_prompt(inputs: dict) -> str:
    return f"""Create a comprehensive officer development lesson for the following:

- **Competency Area:** {inputs['competency']}
- **Experience Level:** {inputs['experience']}
- **Specific Focus:** {inputs['focus']}

Structure your response exactly as follows:

## Officer Development — {inputs['competency']}
**Level:** {inputs['experience']}

### Lesson: [Compelling title]
Write a 2–3 paragraph lesson or refresher on this competency. Write like a senior officer mentoring a lieutenant — practical, honest, and grounded in real fire service experience. Avoid textbook language.

### [Core Concept or Framework]
Provide the key framework, model, or mental checklist for this competency. Use a mnemonic, numbered steps, or structured format where appropriate.

### Command Checklist
Provide a practical, actionable checklist (8–12 items) that an officer can use at the incident scene or during training. Format as checkbox items using [ ].

### Practice Prompts
Provide 4 specific practice scenarios or prompts that allow the officer to rehearse this competency. Each should be a brief scenario that the reader can work through out loud or with a partner.

### Leadership Development Questions
Provide 5 reflective questions that challenge the officer to think deeper about this competency. These should go beyond the technical — include questions about leadership, crew trust, decision-making under stress, and self-awareness.

### Suggested Follow-Up Drills & Training
List 4 specific training actions (drills, self-study, mentorship activities) that build on this lesson.

Write in a confident, mentoring tone. Avoid generic advice. This should sound like it came from a 20-year veteran chief who wants to see you succeed."""


def render() -> None:
    """Render the Officer Development module."""
    module_header(
        icon="⭐",
        title="Officer Development",
        description=(
            "Develop command skills, sharpen your tactical thinking, and prepare for the next rank. "
            "Select a competency area to receive a focused lesson, command checklist, practice prompts, "
            "and leadership development questions written in the voice of an experienced chief officer."
        ),
        audience="Aspiring Officers · New Company Officers · Senior Officers",
    )
    st.divider()

    with st.form("officer_dev_form"):
        col1, col2 = st.columns(2)

        with col1:
            competency = st.selectbox(
                "Competency Area / Topic",
                COMPETENCY_AREAS,
            )
            experience = st.selectbox(
                "Experience Level",
                EXPERIENCE_LEVELS,
            )

        with col2:
            focus = st.text_area(
                "Specific Focus or Question (optional)",
                placeholder=(
                    "e.g., I struggle with transitioning from offensive to defensive operations. "
                    "I want to improve my radio presence on working fires. "
                    "I'm preparing for a promotional interview..."
                ),
                height=120,
            )

        submitted = st.form_submit_button("Generate Officer Development Content", use_container_width=True)

    if submitted:
        if not is_api_available():
            show_no_api_key_warning()
            result = SAMPLE_OUTPUT
        else:
            inputs = {
                "competency": competency,
                "experience": experience.split(" —")[0],
                "focus": focus if focus.strip() else "General proficiency and readiness",
            }
            result = run_with_spinner(build_prompt(inputs), max_tokens=2500)
            if result is None:
                st.error("Could not generate content. Check your API key and try again.")
                return

        st.divider()
        output_header("Officer Development Content")
        with st.container(border=True):
            st.markdown(result)

        st.download_button(
            label="⬇  Download as Markdown",
            data=result,
            file_name=f"fireready_officer_dev_{competency[:30].replace(' ', '_')}.md",
            mime="text/markdown",
        )
