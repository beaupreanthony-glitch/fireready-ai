"""
annual_planner.py — Module 3: Training Officer Annual Planner

Generates a full-year progressive training calendar for a fire department
using a Crawl → Walk → Run structure with monthly breakdowns, learning
objectives, and a capstone event.
"""

import streamlit as st
from modules.llm_client import is_api_available, run_with_spinner, show_no_api_key_warning, module_header, output_header

# ---------------------------------------------------------------------------
# Sample annual plan (demo mode)
# ---------------------------------------------------------------------------
SAMPLE_PLAN = """
## Annual Training Plan — Riverside Volunteer Fire Department
**Type:** Volunteer | **Drill Frequency:** Biweekly | **Department Size:** 28 members
**Focus Areas:** Residential fire attack, search & rescue, pump operations, MAYDAY
**Burn Building Access:** Yes | **Capstone:** Integrated Burn Day (November)

---

## Training Philosophy & Progression Framework

This plan follows a **Crawl → Walk → Run** model across three phases:

| Phase | Timeframe | Focus |
|-------|-----------|-------|
| **Crawl** | Jan–Apr | Foundational skills — individual task proficiency |
| **Walk** | May–Aug | Company-level integration — crew coordination under pressure |
| **Run** | Sep–Nov | Full-scale integrated drills and capstone evolution |
| **Sustain** | December | Review, AAR, planning for next year |

**Annual Goal:** By November, every firefighter should be able to perform all Firefighter I skills independently, function within a crew under simulated fireground conditions, and execute MAYDAY procedures correctly.

---

## Month-by-Month Training Calendar

### JANUARY — Orientation & Baseline (Crawl)
**Theme:** Know your equipment. Know your crew.

| Drill | Date | Topic | Format | Duration |
|-------|------|-------|--------|----------|
| Drill 1 | Jan 7 | PPE Donning, Doffing & Inspection | Classroom + skills station | 2 hrs |
| Drill 2 | Jan 21 | SCBA Confidence — Donning, Low-Profile, Ladder Bail | Station drill | 2 hrs |

**Learning Objectives:**
- Don full PPE/SCBA to NFPA standard within time benchmarks
- Identify and correct PPE deficiencies
- Demonstrate confidence in SCBA operations in a controlled environment

**Equipment Needed:** Full PPE sets, SCBA units, ladder (for bail practice), timing sheets
**Prerequisites:** None — baseline entry point for all members

---

### FEBRUARY — Hose Operations (Crawl)
**Theme:** Water on the fire starts with hose work.

| Drill | Date | Topic | Format | Duration |
|-------|------|-------|--------|----------|
| Drill 1 | Feb 4 | Hose loads, deployment, and nozzle selection | Station + parking lot | 2 hrs |
| Drill 2 | Feb 18 | Advancing lines — stairs, through doorways, in smoke | Smoke trainer or dark building | 2 hrs |

**Learning Objectives:**
- Correctly deploy and advance a 1¾" attack line to the front door
- Demonstrate proper nozzle technique for residential fires
- Navigate with a charged line in limited visibility

**Equipment Needed:** Attack lines, fog/smooth bore nozzles, smoke machine or dark prop
**Prerequisites:** SCBA proficiency (January)

---

### MARCH — Search & Rescue (Crawl)
**Theme:** Find them. Get them out. Know when to get yourself out.

| Drill | Date | Topic | Format | Duration |
|-------|------|-------|--------|----------|
| Drill 1 | Mar 4 | Primary search techniques — oriented, vent-enter-search | Classroom + hands-on | 2 hrs |
| Drill 2 | Mar 18 | Victim removal — carries, drags, packaging | Hands-on with mannequin | 2 hrs |

**Learning Objectives:**
- Execute a systematic primary search using the right-hand or left-hand wall technique
- Move a victim using at least two removal methods
- Communicate search progress and "all clear" on the radio correctly

**Equipment Needed:** Search mannequin, blindfolds or blackout masks, radio for each crew member
**Prerequisites:** SCBA, hose basics

---

### APRIL — Ground Ladders & Ventilation (Crawl)
**Theme:** Ladders are access. Ventilation is a tactical tool — not a default.

| Drill | Date | Topic | Format | Duration |
|-------|------|-------|--------|----------|
| Drill 1 | Apr 1 | Ground ladder carries, raises, and placement | Parking lot + building | 2 hrs |
| Drill 2 | Apr 15 | Ventilation — horizontal vs. vertical, coordination with attack | Classroom + tabletop | 2 hrs |

**Learning Objectives:**
- Raise a 24-ft extension ladder to a second-floor window, solo and as a pair
- Explain when to ventilate, where to ventilate, and who gives the order
- Identify the flow path and predict how ventilation will affect fire behavior

**Equipment Needed:** 24-ft and 35-ft extension ladders, whiteboard for flow path diagram
**Prerequisites:** PPE/SCBA proficiency

---

### MAY — Pump Operations (Walk Phase Begins)
**Theme:** The engineer is the foundation of every interior attack.

| Drill | Date | Topic | Format | Duration |
|-------|------|-------|--------|----------|
| Drill 1 | May 6 | Pump theory, hydrant hookup, tank-to-pump | Apparatus bay + hydrant | 2.5 hrs |
| Drill 2 | May 20 | Relay pumping, multi-line ops, pressure management | Street drill with two engines | 2.5 hrs |

**Learning Objectives:**
- Connect to a hydrant and establish a supply line within 60 seconds
- Maintain correct operating pressure on two simultaneous attack lines
- Troubleshoot common pump problems (cavitation, pressure surge)

**Equipment Needed:** Two pumpers, hydrant wrenches, supply and attack lines
**Prerequisites:** Hose operations (February)

---

### JUNE — Company Evolutions (Walk)
**Theme:** Individual skills only matter when the crew works together.

| Drill | Date | Topic | Format | Duration |
|-------|------|-------|--------|----------|
| Drill 1 | Jun 3 | Residential attack evolution — line stretch, entry, search | Full company drill | 2.5 hrs |
| Drill 2 | Jun 17 | Multi-unit coordination — engine + truck company ops | Two-company drill | 3 hrs |

**Learning Objectives:**
- Execute a coordinated residential fire attack from arrival to primary all clear
- Demonstrate effective radio discipline and command communication
- Assign and track crew accountability throughout the evolution

**Equipment Needed:** Full apparatus complement, accountability system, radios for all
**Prerequisites:** All Crawl-phase skills

---

### JULY — ICS & Command (Walk)
**Theme:** Someone has to be in charge — and they have to know what they're doing.

| Drill | Date | Topic | Format | Duration |
|-------|------|-------|--------|----------|
| Drill 1 | Jul 1 | ICS 100/200 review — command structure, span of control | Classroom + tabletop | 2 hrs |
| Drill 2 | Jul 15 | Tabletop scenario — multi-unit residential fire | Officer-level tabletop | 2.5 hrs |

**Learning Objectives:**
- Assign ICS roles at a residential fire with 3+ units
- Demonstrate radio reports: arrival, size-up, and progress reports
- Correctly implement PAR (Personnel Accountability Report)

**Equipment Needed:** Tabletop props, scenario cards, accountability tags
**Prerequisites:** Company evolutions (June)

---

### AUGUST — MAYDAY & Firefighter Survival (Walk)
**Theme:** Train for the worst so you're ready for it.

| Drill | Date | Topic | Format | Duration |
|-------|------|-------|--------|----------|
| Drill 1 | Aug 5 | MAYDAY declaration — LUNAR, RIT activation, communication | Classroom + scenario | 2 hrs |
| Drill 2 | Aug 19 | RIT operations — packaging, removal, emergency egress | Hands-on building drill | 3 hrs |

**Learning Objectives:**
- Transmit a correct MAYDAY using the LUNAR format
- Activate and deploy an RIT team within 2 minutes of MAYDAY declaration
- Perform emergency egress from a second-floor window using a hook or personal escape system

**Equipment Needed:** Mannequin, personal escape systems, RIT packs, air monitors
**Prerequisites:** All previous skills; this module assumes task proficiency under stress

---

### SEPTEMBER — Multi-Unit Integrated Scenarios (Run Phase Begins)
**Theme:** Full integration under realistic conditions.

| Drill | Date | Topic | Format | Duration |
|-------|------|-------|--------|----------|
| Drill 1 | Sep 2 | Full structure fire — 3-unit response, all companies integrated | Full-scale scenario | 3 hrs |
| Drill 2 | Sep 16 | Special hazards — basement fire, garage fire, limited access | Scenario rotation | 3 hrs |

**Learning Objectives:**
- Execute all company operations simultaneously without instructor prompting
- Demonstrate adaptive decision-making when conditions change mid-evolution
- Conduct a structured after-action review (AAR) as a company

**Prerequisites:** All Crawl and Walk content — this is full integration

---

### OCTOBER — Special Operations & Mutual Aid (Run)
**Theme:** Real incidents don't respect your jurisdiction.

| Drill | Date | Topic | Format | Duration |
|-------|------|-------|--------|----------|
| Drill 1 | Oct 7 | Mutual aid integration — joint drill with adjacent department | Joint company drill | 3 hrs |
| Drill 2 | Oct 21 | MVA with entrapment, mass casualty awareness, EMS/fire interface | Multi-agency scenario | 3 hrs |

**Learning Objectives:**
- Operate within a unified command structure with mutual aid companies
- Integrate with EMS on a combined fire/rescue incident
- Demonstrate accountability procedures across agencies

**Equipment Needed:** Coordination with mutual aid departments; extrication tools if available
**Prerequisites:** ICS, command, and scenario experience

---

### NOVEMBER — CAPSTONE: Integrated Burn Day (Run)
**Theme:** This is what everything has been building toward.

**Event:** Full live-fire training day at the burn building
**Duration:** Full operational day (0800–1600)
**Format:** Rotating evolutions — all crews rotate through attack, search, RIT, command, and support roles

**Learning Objectives:**
- Apply every skill from the annual training calendar in a live-fire environment
- Operate under real thermal conditions with actual smoke and fire
- Demonstrate crew accountability and command coordination under operational stress

**Safety Requirements:** Certified live-fire instructor on site; safety officer designated; rehab station established; EMS standing by; all NFPA 1403 requirements met

**Equipment Needed:** Full apparatus, SCBA, burn building access, EMS unit, rehab supplies

---

### DECEMBER — After-Action Review & Year-End Planning (Sustain)

| Drill | Date | Topic | Format | Duration |
|-------|------|-------|--------|----------|
| Final | Dec 2 | Annual AAR, training records review, next year planning | Officer + crew meeting | 2 hrs |

**Agenda:**
- Review training completion rates and competency gaps
- Celebrate achievements — recognize individual and crew progress
- Identify focus areas for next year's plan
- Update training records and certifications

---

## Equipment & Staffing Summary
- **Attack lines (1¾", 2½"):** Required monthly May–November
- **SCBA units:** Required for all interior drill months
- **Ground ladders (24-ft, 35-ft):** April, September, Capstone
- **Burn building:** November Capstone — coordinate access 60+ days in advance
- **Mutual aid coordination:** October drill — contact neighboring departments by August

## Probationary Firefighter Notes
Probationary members should complete an accelerated Crawl-phase review in January before joining company evolutions. Assign a designated mentor for each probie throughout the year. Evaluate probie progress at the 90-day and 6-month marks.

---
*Plan generated by FireReady AI. Adapt all training events to your department's SOGs, local protocols, and applicable NFPA standards.*
"""


def build_prompt(inputs: dict) -> str:
    focus_str = ", ".join(inputs["focus_areas"]) if inputs["focus_areas"] else "General readiness"
    constraints_str = inputs["constraints"] if inputs["constraints"].strip() else "None noted"
    probie_str = inputs["probie_notes"] if inputs["probie_notes"].strip() else "None noted"

    return f"""Create a detailed annual training plan for a fire department with the following profile:

- **Department Type:** {inputs['dept_type']}
- **Drill Frequency:** {inputs['frequency']}
- **Department Size:** {inputs['size']} members
- **Annual Focus Areas:** {focus_str}
- **Burn Building Access:** {inputs['burn_building']}
- **Weather / Seasonal Constraints:** {constraints_str}
- **Probationary Firefighter Notes:** {probie_str}

Structure the plan exactly as follows:

## Annual Training Plan — [Department Name Placeholder]
Start with a brief header showing the department profile.

## Training Philosophy & Progression Framework
Describe the Crawl → Walk → Run progression philosophy and provide a table showing which months fall into each phase.

## Month-by-Month Training Calendar
For EACH month (January through December), provide:

### [MONTH] — [Theme Title] ([Phase: Crawl/Walk/Run/Sustain])
**Theme:** One sentence description

A table with: Drill number | Date suggestion | Topic | Format | Duration

**Learning Objectives:** 3–4 measurable objectives for this month

**Equipment Needed:** List the specific equipment required

**Prerequisites:** Skills that should be mastered before this month

Rules for the calendar:
- January–April: CRAWL — individual skills (PPE, SCBA, hose, ladders, search)
- May–August: WALK — company-level integration, pump ops, ICS, MAYDAY
- September–November: RUN — integrated multi-company scenarios, special ops
- December: SUSTAIN — AAR, records, planning
- The final capstone event should be in October or November (use burn building if available)
- Show clear skill prerequisites that build toward the capstone

## Equipment & Staffing Summary
List key equipment needs by month/event and staffing considerations.

## Probationary Firefighter Notes
Specific guidance for incorporating probationary members into the plan.

Make it comprehensive, realistic, and specific enough that a training officer could hand this to their chief for approval."""


def render() -> None:
    """Render the Annual Training Planner module."""
    module_header(
        icon="📅",
        title="Annual Training Planner",
        description=(
            "Generate a full-year progressive training calendar for your department using the "
            "Crawl → Walk → Run framework. Outputs include month-by-month drill topics, "
            "learning objectives, equipment needs, prerequisite skill progressions, and a "
            "capstone event — ready to present to your chief."
        ),
        audience="Training Officers · Company Officers · Department Leadership",
    )
    st.divider()

    with st.form("annual_plan_form"):
        col1, col2 = st.columns(2)

        with col1:
            dept_type = st.selectbox(
                "Department Type",
                ["Volunteer", "Combination (volunteer + career)", "Career / Paid"],
            )
            frequency = st.selectbox(
                "Training Frequency",
                ["Weekly", "Biweekly (every 2 weeks)", "Monthly"],
            )
            size = st.number_input(
                "Department / Company Size (members)",
                min_value=5, max_value=200, value=25, step=5,
            )
            burn_building = st.radio(
                "Burn Building Access",
                ["Yes", "No"],
                horizontal=True,
            )

        with col2:
            focus_areas = st.multiselect(
                "Annual Focus Areas (select up to 5)",
                [
                    "Residential fire attack",
                    "Commercial fire attack",
                    "Search & rescue",
                    "Pump operations",
                    "Ground ladders",
                    "Ventilation",
                    "MAYDAY & firefighter survival",
                    "Incident command",
                    "EMS / fire interface",
                    "Hazmat awareness",
                    "Wildland / brush fire",
                    "Mutual aid integration",
                ],
                default=["Residential fire attack", "Search & rescue", "MAYDAY & firefighter survival"],
                max_selections=5,
            )
            constraints = st.text_area(
                "Seasonal / Weather Constraints (optional)",
                placeholder="e.g., outdoor drills limited Dec–Feb due to cold, burn building unavailable July–August...",
                height=80,
            )
            probie_notes = st.text_area(
                "Probationary Firefighter Notes (optional)",
                placeholder="e.g., 3 new members joining in January, all need FF1 completion by June...",
                height=80,
            )

        submitted = st.form_submit_button("Generate Annual Training Plan", use_container_width=True)

    if submitted:
        if not is_api_available():
            show_no_api_key_warning()
            result = SAMPLE_PLAN
        else:
            inputs = {
                "dept_type": dept_type,
                "frequency": frequency,
                "size": size,
                "burn_building": burn_building,
                "focus_areas": focus_areas,
                "constraints": constraints,
                "probie_notes": probie_notes,
            }
            result = run_with_spinner(build_prompt(inputs), max_tokens=4000)
            if result is None:
                st.error("Could not generate the training plan. Check your API key and try again.")
                return

        st.divider()
        output_header("Annual Training Plan")
        with st.container(border=True):
            st.markdown(result)

        st.download_button(
            label="⬇  Download Plan as Markdown",
            data=result,
            file_name="fireready_annual_training_plan.md",
            mime="text/markdown",
        )
