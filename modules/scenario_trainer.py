"""
scenario_trainer.py — Module 4: Interactive Scenario Trainer

Provides branching text-based training scenarios. Users step through:
  1. Dispatch information
  2. Arrival / size-up
  3. Decision Point 1 (3 choices)
  4. Consequence + tactical update
  5. Decision Point 2 (3 choices)
  6. Final outcome + training debrief

A full pre-written sample scenario is included for demo mode (no API key).
"""

import streamlit as st
from modules.llm_client import is_api_available, call_claude, show_no_api_key_warning, module_header, output_header

# ---------------------------------------------------------------------------
# Scenario type options
# ---------------------------------------------------------------------------
SCENARIO_TYPES = [
    "Structure Fire — 2-Story Residential",
    "Basement Fire",
    "Kitchen Fire (Contained)",
    "Commercial Building — Alarm Activation",
    "Dumpster Fire Extending to Exposure",
    "Motor Vehicle Accident with Entrapment",
    "MAYDAY Incident (Firefighter Down)",
    "Brush / Wildland-Urban Interface Fire",
    "Hazmat Awareness Scene",
    "Vehicle Fire in Enclosed Parking Structure",
]

# ---------------------------------------------------------------------------
# Pre-written sample scenario (Structure Fire — 2-Story Residential)
# Used when no API key is set.
# ---------------------------------------------------------------------------
SAMPLE_SCENARIO = {
    "type": "Structure Fire — 2-Story Residential",
    "dispatch": """**DISPATCH — Engine 7, Truck 4, Medic 3**

*Time: 14:23 | Response: Structure fire, reported working*

Dispatch advises: **1842 Maplewood Drive** — two-story single-family residence. Caller reports heavy smoke from the first floor and front door. A second caller states a neighbor may still be inside. No additional units on scene. Weather: clear, winds 8 mph from the southwest. Nearest hydrant: 150 feet from the structure on the east side of the street.""",

    "arrival": """**ARRIVAL / SIZE-UP — Engine 7 on scene**

You arrive as the first-due officer. Here is what you see:

- **Alpha (front):** Heavy black smoke pushing from under the front door and first-floor windows. Flames visible in the kitchen window (right side, first floor).
- **Bravo (left side):** No visible fire or smoke extension. Wooden fence abutting a detached garage.
- **Charlie (rear):** Unknown — neighbor says there is a back door.
- **Delta (right side):** Kitchen fire clearly visible. No exposures on this side.
- **Construction:** 1960s wood-frame, balloon construction suspected. Two stories, attic vent present.
- **Occupancy:** Neighbor on lawn: *"Mrs. Callahan lives alone. I didn't see her come out."*
- **Your crew:** Driver/engineer + 2 firefighters. Truck 4 is 3 minutes out. Medic 3 is 4 minutes out.""",

    "decision1_prompt": "You are the first-arriving officer. The clock is running. What is your immediate priority?",
    "choices1": [
        "Initiate an immediate offensive attack — stretch a 1¾\" line, enter the front door, and conduct a simultaneous primary search.",
        "Complete a full 360-degree size-up of all four sides before committing any crew to the interior.",
        "Establish a water supply first — have your engineer hook up to the hydrant, charge the line, then enter once water is confirmed.",
    ],
    "consequences1": {
        "A": """**CONSEQUENCE — Immediate Offensive Attack**

Your crew deploys. The line is at the front door in 90 seconds. Visibility inside: zero. Your nozzleman opens the line and begins knocking down the kitchen fire. One firefighter initiates a right-hand primary search of the first floor.

*Thermal imaging (if available) shows a heat signature in the rear bedroom — possible victim location.*

**TACTICAL UPDATE:** Truck 4 radios: 2 minutes out. Your engineer reports tank water only — hydrant hookup not yet established. You have approximately 500 gallons of tank water remaining. Fire is being knocked down in the kitchen, but smoke in the hallway is thickening.""",

        "B": """**CONSEQUENCE — Full 360 Size-Up**

You complete the size-up in 50 seconds. Side Charlie (rear) reveals: the fire has extended up an exterior wall and is now showing from a first-floor rear window. More critically — **an elderly woman is at a second-floor window, Side Alpha, waving for help.** She cannot egress on her own.

**TACTICAL UPDATE:** Life safety priority is now confirmed and located. You have a conscious victim on the second floor, exterior wall fire threatening below her position. Ground ladder to the second floor is your immediate life safety action. Water supply still needs to be established.""",

        "C": """**CONSEQUENCE — Establish Water Supply First**

Your engineer begins the hydrant hookup. The line is charged and ready in 2 minutes and 10 seconds. In that time: flames have grown to two windows on Side Alpha, and smoke is now pushing from second-floor eaves — indicating possible attic involvement.

**TACTICAL UPDATE:** You now have a charged line and confirmed water supply. Neighbors confirm Mrs. Callahan's bedroom is on the second floor — no visual of her yet. Truck 4 is 1 minute out. Your line is at the front door, ready for entry.""",
    },

    "decision2_prompt": "Given the updated conditions, what is your next command decision?",
    "choices2": {
        "A": [
            "Direct your search firefighter to the second floor — target the rear bedroom based on thermal imaging. Maintain the attack line on the first floor.",
            "Withdraw your crew from the interior — tank water is low, attic involvement is likely, and conditions are deteriorating. Transition to defensive.",
            "Radio Truck 4 to bring a second line to the rear — cut off extension to the second floor while your crew continues the primary attack.",
        ],
        "B": [
            "Raise a 24-ft ground ladder to the second-floor window, Side Alpha — rescue the occupant immediately.",
            "Direct one firefighter to stretch a line to the front door while you personally raise the ladder and perform the rescue.",
            "Declare a working fire and request a second alarm — your crew cannot safely perform simultaneous rescue and fire attack.",
        ],
        "C": [
            "Enter the front door with your charged line — push the kitchen fire and initiate a systematic primary search.",
            "Send one firefighter to check the rear door for a second entry point while your nozzle team enters the front.",
            "Reassess the situation — the 2-minute delay and fire growth suggest transitioning to a defensive posture until more resources arrive.",
        ],
    },

    "debrief": """---

## Training Debrief

**Scenario:** Structure Fire — 2-Story Residential | First-Arriving Officer

---

### Key Training Points

**1. Life Safety Is the First Strategic Priority**
NFPA 1710 and NFPA 1500 both establish life safety as the first priority in fire operations. When a confirmed life hazard is present, all resource deployment should be viewed through that lens first — fire attack is a *means* to life safety, not a separate objective.

**2. The Value of the 360-Degree Size-Up**
In Choice B, the 360 revealed a conscious victim that would not have been visible from Side Alpha. Forty-five to sixty seconds on the exterior can change your entire operational plan. The instinct to "get water on the fire immediately" is understandable — but uninformed speed can be fatal. *Ready, aim, fire — not fire, aim, ready.*

**3. Water Supply Is Not Optional**
Interior offensive operations require a reliable water supply. Choice A demonstrated the risk of committing to an interior attack on tank water alone. If tank water depletes before the fire is controlled, your crew is inside a burning building with no water. The engineer establishing supply is a critical parallel task, not an afterthought.

**4. Crew Limitations and Resource Management**
Three firefighters cannot safely conduct simultaneous fire attack, primary search, and rescue without a plan. Recognizing the limits of your initial crew and calling for additional resources *early* is a sign of experience — not weakness. A second-alarm requested at arrival is far better than a MAYDAY 10 minutes in.

**5. There Is No Single Correct Answer**
Every decision in this scenario involves trade-offs. An experienced officer might make different choices depending on additional context: crew experience, weather, building age, time of day, and resource availability. The goal of scenario training is to develop your **decision-making process and situational awareness** — not to memorize a script.

---

### Applicable References
- NFPA 1710: *Standard for the Organization and Deployment of Fire Suppression Operations*
- NFPA 1500: *Standard on Fire Department Occupational Safety, Health, and Wellness Program*
- IFSTA *Essentials of Fire Fighting*, Chapter: Initial Company Operations
- USFA: *Residential Structure Fires — Tactical Decision-Making Guide*

---

### Recommended Follow-Up Training
- **Tabletop:** Run this scenario with your crew at the kitchen table — no props needed
- **Skills station:** Ground ladder raises to second-floor windows, timed
- **Drill evolution:** Full residential attack from a parked apparatus with water supply establishment timed
- **Study:** Review your department's SOG for first-arriving officer responsibilities""",
}


# ---------------------------------------------------------------------------
# LLM prompt builders
# ---------------------------------------------------------------------------
SCENARIO_SYSTEM = (
    "You are a fire service training officer creating realistic, educational scenario training "
    "content. Write in a direct, operational tone — like a dispatch center and a realistic fireground, "
    "not a textbook. Use actual fire service terminology. Be specific about conditions."
)


def build_intro_prompt(scenario_type: str) -> str:
    return f"""Write a realistic fire service training scenario introduction for: **{scenario_type}**

Format your response with these EXACT section headers:

## DISPATCH
Write 3–4 sentences of realistic dispatch information: time of day, location (use a realistic street address), nature of the call, any additional caller information, weather conditions, nearest hydrant or water supply.

## ARRIVAL / SIZE-UP
Write 4–5 sentences describing exactly what the first-arriving officer observes on arrival. Be specific: which sides have fire/smoke, construction type, occupancy clues, crew size, status of mutual aid.

## DECISION POINT 1
Write one sentence framing the immediate tactical decision the officer must make.

**Option A:** [First realistic tactical option]
**Option B:** [Second realistic tactical option]
**Option C:** [Third realistic tactical option]

Keep all three options realistic — avoid obviously wrong choices. Each option should represent a defensible tactical approach with real trade-offs."""


def build_consequence_prompt(scenario_type: str, intro_text: str, choice_letter: str, choice_text: str) -> str:
    return f"""Continue this fire service training scenario. The officer chose Option {choice_letter}: {choice_text}

Original scenario:
{intro_text}

Format your response with these EXACT section headers:

## CONSEQUENCE
Write 3–4 sentences describing what happens as a direct result of this decision. Be realistic — show both positive outcomes and new complications that arise from this choice.

## TACTICAL UPDATE
Write 2–3 sentences about how conditions have evolved. Include at least one new piece of information that changes the tactical picture (a new resource arriving, conditions changing, a new life safety concern, etc.).

## DECISION POINT 2
Write one sentence framing the next critical decision the officer must make given the updated conditions.

**Option A:** [First realistic follow-up option]
**Option B:** [Second realistic follow-up option]
**Option C:** [Third realistic follow-up option]"""


def build_debrief_prompt(
    scenario_type: str,
    choice1_letter: str,
    choice1_text: str,
    choice2_letter: str,
    choice2_text: str,
) -> str:
    return f"""Write a training debrief for this fire service scenario.

**Scenario:** {scenario_type}
**Decision 1:** Option {choice1_letter} — {choice1_text}
**Decision 2:** Option {choice2_letter} — {choice2_text}

Format with these sections:

## Training Debrief

### Key Training Points
List 4–5 key training points as numbered items. Each should be a bold header followed by 2–3 sentences of explanation. Reference real fire service principles (life safety priority, water supply, crew resource management, etc.).

### A Note on Decision-Making
Write 2–3 sentences acknowledging that there is rarely one perfect answer, and that the goal of scenario training is to develop reasoning and situational awareness.

### Applicable References
List 3–4 relevant NFPA standards, IFSTA chapters, or USFA publications.

### Recommended Follow-Up Training
List 3–4 specific follow-up training actions (drills, studies, tabletops) that would reinforce the lessons from this scenario."""


# ---------------------------------------------------------------------------
# Session state management
# ---------------------------------------------------------------------------
def init_scenario_state() -> None:
    defaults = {
        "scenario_step": 0,       # 0=not started, 1=dispatch+arrival, 2=decision1,
                                   # 3=consequence, 4=decision2, 5=debrief
        "scenario_data": {},       # stores generated text for each section
        "scenario_type": "",
        "choice1_letter": "",
        "choice1_text": "",
        "choice2_letter": "",
        "choice2_text": "",
        "using_sample": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def reset_scenario() -> None:
    keys = ["scenario_step", "scenario_data", "scenario_type", "choice1_letter",
            "choice1_text", "choice2_letter", "choice2_text", "using_sample"]
    for k in keys:
        if k in st.session_state:
            del st.session_state[k]
    init_scenario_state()


# ---------------------------------------------------------------------------
# Helper: render a callout-style box
# ---------------------------------------------------------------------------
def info_box(label: str, content: str) -> None:
    st.markdown(
        f"""<div style="background:#0d2137;border-left:4px solid #E67E22;
        padding:1rem 1.2rem;border-radius:0 8px 8px 0;margin:0.5rem 0;">
        <strong style="color:#E67E22;">{label}</strong><br><br>{content.replace(chr(10), '<br>')}
        </div>""",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------
def render() -> None:
    """Render the Interactive Scenario Trainer module."""
    module_header(
        icon="🎯",
        title="Scenario Trainer",
        description=(
            "Step through realistic fireground scenarios, make tactical decisions at key decision points, "
            "and see the consequences of your choices play out. Each scenario ends with a structured "
            "training debrief focused on reasoning, procedure, and leadership."
        ),
        audience="Firefighters · Company Officers · Promotional Candidates",
    )
    st.info(
        "**Training Simulator Only.** This module is for educational use. "
        "It is not intended for use during live emergency incidents.",
        icon="🎓",
    )
    st.divider()

    init_scenario_state()

    # ---- Scenario selection (only shown before scenario starts) ------------
    if st.session_state.scenario_step == 0:
        scenario_type = st.selectbox("Select Scenario Type", SCENARIO_TYPES)
        col1, col2 = st.columns([2, 1])
        with col1:
            start = st.button("Start Scenario", use_container_width=True)
        with col2:
            st.caption("Using sample scenario in demo mode if no API key is set.")

        if start:
            st.session_state.scenario_type = scenario_type

            # Check if this is the sample scenario type or no API key
            if not is_api_available() or scenario_type == SCENARIO_TYPES[0]:
                if not is_api_available():
                    show_no_api_key_warning()
                # Load sample scenario
                st.session_state.scenario_data = SAMPLE_SCENARIO
                st.session_state.using_sample = True
            else:
                # Generate via API
                with st.spinner("Generating scenario..."):
                    try:
                        intro_text = call_claude(
                            build_intro_prompt(scenario_type),
                            system=SCENARIO_SYSTEM,
                            max_tokens=1200,
                        )
                        if not intro_text:
                            show_no_api_key_warning()
                            st.session_state.scenario_data = SAMPLE_SCENARIO
                            st.session_state.using_sample = True
                        else:
                            st.session_state.scenario_data = {"intro_text": intro_text}
                            st.session_state.using_sample = False
                    except Exception as e:
                        st.error(f"Error generating scenario: {e}")
                        return

            st.session_state.scenario_step = 1
            st.rerun()

    # ---- Step 1: Dispatch + Arrival + Decision Point 1 --------------------
    elif st.session_state.scenario_step == 1:
        data = st.session_state.scenario_data

        st.markdown(f"### Scenario: {st.session_state.scenario_type}")
        st.divider()

        if st.session_state.using_sample:
            # Render pre-written sample
            st.markdown("#### Dispatch")
            st.markdown(data["dispatch"])
            st.divider()
            st.markdown("#### Arrival / Size-Up")
            st.markdown(data["arrival"])
            st.divider()
            st.markdown(f"#### {data['decision1_prompt']}")
            choices = data["choices1"]
        else:
            # Render LLM-generated intro
            raw = data.get("intro_text", "")
            # Split on section headers to display cleanly
            st.markdown(raw)
            st.divider()
            # Parse choices from the text for the radio widget
            import re
            choices_raw = re.findall(r"\*\*Option [ABC]:\*\*\s*(.+)", raw)
            if not choices_raw:
                choices_raw = re.findall(r"Option [ABC]:\s*(.+)", raw)
            if len(choices_raw) < 3:
                choices = ["Option A (advance with line)", "Option B (complete 360)", "Option C (establish water supply)"]
            else:
                choices = choices_raw[:3]

        # Radio for decision 1
        selected = st.radio(
            "Select your tactical decision:",
            [f"A — {choices[0]}", f"B — {choices[1]}", f"C — {choices[2]}"],
            key="decision1_radio",
            index=None,
        )

        col1, col2 = st.columns([2, 1])
        with col1:
            confirm = st.button("Commit to This Decision →", disabled=(selected is None))
        with col2:
            if st.button("Start Over"):
                reset_scenario()
                st.rerun()

        if confirm and selected:
            letter = selected[0]  # "A", "B", or "C"
            idx = ord(letter) - ord("A")
            text = choices[idx]
            st.session_state.choice1_letter = letter
            st.session_state.choice1_text = text

            if st.session_state.using_sample:
                # Load pre-written consequence
                consequence_text = data["consequences1"].get(letter, "Consequence not available.")
                st.session_state.scenario_data["consequence1"] = consequence_text
                # Pre-load decision 2 choices for sample
                st.session_state.scenario_data["choices2_active"] = data["choices2"].get(letter, data["choices2"]["A"])
            else:
                # Generate via API
                with st.spinner("Generating consequence..."):
                    try:
                        consequence_text = call_claude(
                            build_consequence_prompt(
                                st.session_state.scenario_type,
                                data.get("intro_text", ""),
                                letter,
                                text,
                            ),
                            system=SCENARIO_SYSTEM,
                            max_tokens=1000,
                        )
                        if not consequence_text:
                            st.error("Could not generate consequence. Check your API key.")
                            return
                        st.session_state.scenario_data["consequence1"] = consequence_text
                    except Exception as e:
                        st.error(f"Error: {e}")
                        return

            st.session_state.scenario_step = 2
            st.rerun()

    # ---- Step 2: Show consequence + Decision Point 2 ----------------------
    elif st.session_state.scenario_step == 2:
        data = st.session_state.scenario_data

        st.markdown(f"### Scenario: {st.session_state.scenario_type}")
        st.markdown(f"**Your Decision 1:** Option {st.session_state.choice1_letter} — {st.session_state.choice1_text}")
        st.divider()

        consequence_text = data.get("consequence1", "")
        st.markdown(consequence_text)
        st.divider()

        # Get choices for decision 2
        if st.session_state.using_sample:
            choices2 = data.get("choices2_active", ["Option A", "Option B", "Option C"])
            st.markdown("#### What is your next command decision?")
        else:
            # Parse decision 2 from consequence text
            import re
            choices2_raw = re.findall(r"\*\*Option [ABC]:\*\*\s*(.+)", consequence_text)
            if not choices2_raw:
                choices2_raw = re.findall(r"Option [ABC]:\s*(.+)", consequence_text)
            if len(choices2_raw) < 3:
                choices2 = ["Continue offensive operations", "Transition to defensive", "Request additional resources"]
            else:
                choices2 = choices2_raw[:3]

        selected2 = st.radio(
            "Select your next tactical decision:",
            [f"A — {choices2[0]}", f"B — {choices2[1]}", f"C — {choices2[2]}"],
            key="decision2_radio",
            index=None,
        )

        col1, col2 = st.columns([2, 1])
        with col1:
            confirm2 = st.button("Commit to This Decision →", disabled=(selected2 is None))
        with col2:
            if st.button("Start Over"):
                reset_scenario()
                st.rerun()

        if confirm2 and selected2:
            letter2 = selected2[0]
            idx2 = ord(letter2) - ord("A")
            text2 = choices2[idx2]
            st.session_state.choice2_letter = letter2
            st.session_state.choice2_text = text2

            if st.session_state.using_sample:
                st.session_state.scenario_data["debrief"] = data.get("debrief", "")
            else:
                with st.spinner("Generating final outcome and debrief..."):
                    try:
                        debrief_text = call_claude(
                            build_debrief_prompt(
                                st.session_state.scenario_type,
                                st.session_state.choice1_letter,
                                st.session_state.choice1_text,
                                letter2,
                                text2,
                            ),
                            system=SCENARIO_SYSTEM,
                            max_tokens=1500,
                        )
                        if not debrief_text:
                            st.error("Could not generate debrief. Check your API key.")
                            return
                        st.session_state.scenario_data["debrief"] = debrief_text
                    except Exception as e:
                        st.error(f"Error: {e}")
                        return

            st.session_state.scenario_step = 3
            st.rerun()

    # ---- Step 3: Final outcome + debrief ----------------------------------
    elif st.session_state.scenario_step == 3:
        data = st.session_state.scenario_data

        st.markdown(f"### Scenario Complete: {st.session_state.scenario_type}")
        st.success("Scenario concluded. Review your decisions and the training debrief below.")
        st.divider()

        st.markdown(f"**Decision 1:** Option {st.session_state.choice1_letter} — {st.session_state.choice1_text}")
        st.markdown(f"**Decision 2:** Option {st.session_state.choice2_letter} — {st.session_state.choice2_text}")
        st.divider()

        debrief = data.get("debrief", "Debrief not available.")
        output_header("Training Debrief")
        with st.container(border=True):
            st.markdown(debrief)

        # Build export content
        export = f"""# Scenario Training Report
## {st.session_state.scenario_type}

**Decision 1:** Option {st.session_state.choice1_letter} — {st.session_state.choice1_text}
**Decision 2:** Option {st.session_state.choice2_letter} — {st.session_state.choice2_text}

---

{debrief}
"""
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "⬇  Download Debrief",
                data=export,
                file_name="fireready_scenario_debrief.md",
                mime="text/markdown",
            )
        with col2:
            if st.button("Run Another Scenario"):
                reset_scenario()
                st.rerun()
