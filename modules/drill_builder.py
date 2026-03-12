"""
drill_builder.py — Module 5: Company Drill Builder

Generates a complete single drill night or company training event plan,
including objectives, timeline, equipment list, safety considerations,
evaluation criteria, and follow-on suggestions.
"""

import streamlit as st
from modules.llm_client import is_api_available, run_with_spinner, show_no_api_key_warning, module_header, output_header

# ---------------------------------------------------------------------------
# Sample drill plan (demo mode)
# ---------------------------------------------------------------------------
SAMPLE_DRILL = """
## Company Drill Plan
**Topic:** SCBA Emergency Procedures & Low-Air MAYDAY
**Crew Size:** 6 | **Time Available:** 2.5 hours | **Setting:** Indoor — apparatus bay + adjacent hallway
**Skill Level:** Intermediate | **Apparatus/Equipment:** Engine 1, full SCBA complement, drill props

---

### Drill Objectives
By the end of this drill, all participants will be able to:

1. **Demonstrate emergency SCBA procedures** — activate emergency bypass valve, conserve air in a low-air situation, and initiate controlled egress
2. **Transmit a correct MAYDAY** using the LUNAR format (Location, Unit, Name, Air, Resources needed) with proper radio discipline
3. **Perform buddy breathing** using a compatible SCBA system or air-sharing hood, if department-equipped
4. **Execute a self-rescue sequence** — find the wall, follow to an egress point, and signal RIT using a personal alert device

---

### Drill Timeline

| Time | Activity | Lead | Notes |
|------|----------|------|-------|
| 0:00–0:15 | Arrival, accountability, safety briefing | Company Officer | Cover emergency stop procedures, designated safety officer |
| 0:15–0:30 | Classroom segment — MAYDAY protocol review | Training Officer | LUNAR format, radio channel, RIT activation |
| 0:30–0:45 | Skills station: MAYDAY transmission (pairs) | Training Officer | Each pair practices dispatch to RIT activation on radio |
| 0:45–1:15 | Skills station: SCBA emergency procedures | Senior FF | Emergency bypass, purge valve, low-air egress |
| 1:15–1:45 | Practical scenario: Simulated low-air MAYDAY | Company Officer | Blackout masks, hallway, monitor with TIC |
| 1:45–2:00 | Rotation & switch (second group runs scenario) | Safety Officer | Same scenario, different crew members |
| 2:00–2:15 | Debrief — group AAR | Company Officer | Structured: What went well / What to improve |
| 2:15–2:30 | Equipment check, clean-up, documentation | All | Log training attendance, note deficiencies |

---

### Equipment List
- [ ] Full SCBA units — one per participant (cylinders topped off)
- [ ] Blackout masks or SCBA facepiece covers (for limited visibility simulation)
- [ ] Portable radios — one per pair minimum
- [ ] Thermal imaging camera (if available)
- [ ] Accountability board and tags
- [ ] Personal alert safety systems (PASS devices — ensure all are functional)
- [ ] Whiteboard or flip chart for classroom segment
- [ ] Training log / sign-in sheet

---

### Safety Considerations
- **Designated Safety Officer:** Assign one person with no other role — this is non-negotiable for SCBA drills
- **Emergency stop signal:** Establish a clear verbal or radio signal to immediately halt all activity
- **No running:** All movement during blackout portions is walking pace only
- **Cylinder management:** Do not allow cylinders to deplete below 25% during drills — replenish between rotations
- **Medical:** Know the location of the AED and first aid kit before the drill begins
- **PASS device check:** All PASS devices must be armed and functioning before any blackout scenario begins

---

### Evaluation Criteria
Officers should observe and evaluate each participant on:

| Skill | Standard | Pass/Fail |
|-------|----------|-----------|
| MAYDAY transmission | Correct LUNAR format, appropriate radio channel | Pass/Fail |
| SCBA emergency bypass | Activates valve correctly within 15 seconds | Pass/Fail |
| Low-air egress | Exits to predetermined point within 60 seconds of low-air alarm | Pass/Fail |
| Radio discipline | Clear, calm communication; no unnecessary traffic during MAYDAY | Observed |
| Situational awareness | Maintains wall contact and directional orientation | Observed |

---

### After-Action Review Guide
Ask the group:
1. "What was the most difficult part of the MAYDAY scenario?" — normalizes struggle, surfaces training gaps
2. "What would you do differently if this happened on a real incident?" — connects drill to operational context
3. "What equipment or procedure was unclear?" — identifies SOG gaps

---

### Follow-On Training Suggestions
1. **Next Drill:** RIT operations — packaging and removal of a downed firefighter (builds directly on today's MAYDAY work)
2. **Self-Study:** Review your department's MAYDAY SOG and compare it to NFPA 1407 guidelines
3. **Individual Skill:** Practice MAYDAY radio transmissions at home using the LUNAR format until it is automatic
4. **Scenario Trainer:** Run the MAYDAY Incident scenario in FireReady AI's Scenario Trainer module for tabletop practice

---
*Drill plan generated by FireReady AI. Modify all safety procedures to comply with your department's SOGs and applicable NFPA standards.*
"""


def build_prompt(inputs: dict) -> str:
    return f"""Create a detailed, practical company drill plan for the following:

- **Topic / Skill:** {inputs['topic']}
- **Crew Size:** {inputs['crew_size']} personnel
- **Time Available:** {inputs['time_available']}
- **Skill Level:** {inputs['skill_level']}
- **Apparatus / Equipment Available:** {inputs['equipment']}
- **Setting:** {inputs['setting']}

Structure your response exactly as follows:

## Company Drill Plan
Start with a clean header showing all inputs as a profile summary.

### Drill Objectives
List 3–5 specific, measurable learning objectives. Start each with an action verb. These should describe what a firefighter will be able to *do* after completing this drill.

### Drill Timeline
Provide a table with columns: Time | Activity | Lead | Notes
Cover the full time available. Include setup, briefing, skills work, practical evolution, debrief, and cleanup. Be realistic about timing — most drills need 15 min for setup and 15 min for debrief.

### Equipment List
Bulleted checklist of all equipment needed. Be specific (e.g., "1¾\" attack line, 200 ft" not just "hose"). Format as checkboxes using [ ].

### Safety Considerations
List 5–7 specific safety considerations relevant to this topic. Include: designated safety officer requirement, emergency stop procedure, any topic-specific hazards, and physical/environmental safety notes.

### Evaluation Criteria
A table showing: Skill | Performance Standard | Pass/Fail or Observed
Give 4–5 measurable criteria that officers can use to evaluate each participant.

### After-Action Review Guide
Provide 3–4 specific debrief questions officers can use to facilitate the AAR discussion.

### Follow-On Training Suggestions
List 3–4 specific next training steps that build on this drill.

Make it realistic and operational. A company officer should be able to hand this to their captain and run the drill tonight with no additional planning."""


def render() -> None:
    """Render the Company Drill Builder module."""
    module_header(
        icon="🛠️",
        title="Company Drill Builder",
        description=(
            "Generate a complete drill night or company training event plan in minutes. "
            "Outputs include specific learning objectives, a timed drill timeline, equipment checklist, "
            "safety considerations, evaluation criteria, and follow-on training recommendations."
        ),
        audience="Company Officers · Training Officers",
    )
    st.divider()

    with st.form("drill_builder_form"):
        col1, col2 = st.columns(2)

        with col1:
            topic = st.text_input(
                "Drill Topic / Skill",
                placeholder="e.g., Hose stretches, SCBA MAYDAY procedures, Ground ladder operations...",
                value="SCBA Emergency Procedures & Low-Air MAYDAY",
            )
            crew_size = st.number_input(
                "Crew Size (number of participants)",
                min_value=2, max_value=50, value=6, step=1,
            )
            time_available = st.selectbox(
                "Time Available",
                ["1 hour", "1.5 hours", "2 hours", "2.5 hours", "3 hours", "4 hours (half day)"],
                index=2,
            )

        with col2:
            skill_level = st.selectbox(
                "Crew Skill Level",
                ["Recruit / Basic — minimal experience",
                 "Intermediate — Firefighter I certified or equivalent",
                 "Advanced — experienced, multi-year members",
                 "Mixed — range of experience levels"],
                index=1,
            )
            equipment = st.text_area(
                "Apparatus & Equipment Available",
                placeholder="e.g., Engine 1, SCBA units, 200 ft of 1¾\" hose, ground ladders...",
                value="Engine 1, full SCBA complement, portable radios, thermal imaging camera",
                height=80,
            )
            setting = st.radio(
                "Drill Setting",
                ["Indoor — apparatus bay / station", "Outdoor — parking lot / training ground",
                 "Mixed indoor/outdoor"],
                index=0,
            )

        submitted = st.form_submit_button("Generate Drill Plan", use_container_width=True)

    if submitted:
        if not topic.strip():
            st.warning("Please enter a drill topic.")
            return

        if not is_api_available():
            show_no_api_key_warning()
            result = SAMPLE_DRILL
        else:
            inputs = {
                "topic": topic,
                "crew_size": crew_size,
                "time_available": time_available,
                "skill_level": skill_level.split(" —")[0],
                "equipment": equipment,
                "setting": setting,
            }
            result = run_with_spinner(build_prompt(inputs), max_tokens=2500)
            if result is None:
                st.error("Could not generate drill plan. Check your API key and try again.")
                return

        st.divider()
        output_header("Drill Plan")
        with st.container(border=True):
            st.markdown(result)

        st.download_button(
            label="⬇  Download Drill Plan as Markdown",
            data=result,
            file_name=f"fireready_drill_{topic[:30].replace(' ', '_')}.md",
            mime="text/markdown",
        )
