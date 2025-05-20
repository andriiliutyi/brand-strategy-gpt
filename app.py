import streamlit as st
from utils.prompts import (
    system_prompt,
    step_1_master_prompt,
    step_2_master_prompt,
    step_3_master_prompt,
    step_4_master_prompt,
    step_5_master_prompt,
)
from utils.file_utils import read_file
from utils.openai_utils import generate_step_output
import json

# ---------- State Initialization ----------
if "step" not in st.session_state:
    st.session_state.step = 1
if "step_inputs" not in st.session_state:
    st.session_state.step_inputs = {}
if "step_outputs" not in st.session_state:
    st.session_state.step_outputs = {}
if "selections" not in st.session_state:
    st.session_state.selections = {}
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

st.title("GPT Brand Strategy Generator")

# ----------- STEP 1 -----------
if st.session_state.step == 1:
    st.header("Step 1: Brand Basics")
    brand_name = st.text_input("Brand Name", value=st.session_state.step_inputs.get("brand_name", ""))
    brand_desc = st.text_area("Brand Description", value=st.session_state.step_inputs.get("brand_desc", ""))
    uploaded_file = st.file_uploader("Upload Document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Next"):
            if not brand_name or not uploaded_file:
                st.error("Please fill in the Brand Name and upload a document.")
            else:
                file_text = read_file(uploaded_file)
                st.session_state.step_inputs["brand_name"] = brand_name
                st.session_state.step_inputs["brand_desc"] = brand_desc
                st.session_state.step_inputs["file_text"] = file_text

                st.session_state.messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": step_1_master_prompt},
                    {"role": "user", "content": f"brand name: {brand_name}\nbrand_desc: {brand_desc}"},
                    {"role": "user", "content": f"The content of the uploaded file: {file_text}"},
                ]
                step_1_output = generate_step_output(st.session_state.messages)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": step_1_output
                })
                st.session_state.step_outputs["step_1"] = step_1_output
                st.session_state.step += 1
                # st.experimental_rerun()
    with col2:
        if st.button("Redo"):
            for key in ["brand_name", "brand_desc", "file_text"]:
                st.session_state.step_inputs.pop(key, None)
            st.session_state.step_outputs.pop("step_1", None)
            st.session_state.messages = [{"role": "system", "content": system_prompt}]
            # st.experimental_rerun()

# ---------- STEP 2 SELECTION ----------
if st.session_state.step == 2:
    st.header("Step 2: Select Your Core Directions")
    try:
        data = json.loads(st.session_state.step_outputs["step_1"])
    except Exception as e:
        st.error(f"Could not parse output as JSON: {e}")
        st.text_area("Raw Output", value=st.session_state.step_outputs["step_1"])
        st.stop()

    # --- Example: User picks 1 "primary_idea", 1 "controversial_idea", 1 "primary_tone", etc. ---
    # --- You can add more selectors for other structured options as needed ---

    primary_ideas = data["business_core_ideas"]["primary_ideas"]
    controversial_ideas = data["business_core_ideas"]["controversial_ideas"]
    
    primary_whw = data["why_how_what_statements"]["primary_sets"]
    controversial_whw = data["why_how_what_statements"]["controversial_sets"]
    
    primary_solutions = data["problem_solution_sets"]["primary_sets"]
    controversial_solutions = data["problem_solution_sets"]["controversial_sets"]
    
    primary_tones = data["tone_options"]["primary_tones"]
    controversial_tones = data["tone_options"]["controversial_tones"]

    primary_ideas = data["business_core_ideas"]["primary_ideas"]
    controversial_ideas = data["business_core_ideas"]["controversial_ideas"]

    st.subheader("Choose a Business Core Idea")
    all_ideas = [
        {"label": f"[Primary] {x['micro_core_idea']} — {x['expanded_core_idea']}", "type": "primary", "data": x}
        for x in primary_ideas
    ] + [
        {"label": f"[Controversial] {x['micro_core_idea']} — {x['expanded_core_idea']}", "type": "controversial", "data": x}
        for x in controversial_ideas
    ]
    idea_choice_label = st.radio(
        "Business Core Ideas (Primary & Controversial)",
        [idea["label"] for idea in all_ideas],
        key="business_core_idea_radio"
    )
    selected_idea = next((idea for idea in all_ideas if idea["label"] == idea_choice_label), None)
    
    st.subheader("Choose a why_how_what_statements")
    all_whw = [
        {"label": f"[Primary] — {x['why']} — {x['how']} — {x['what']}", "type": "primary", "data": x}
        for x in primary_whw
    ] + [
        {"label": f"[Controversial] — {x['why']} — {x['how']} — {x['what']}", "type": "controversial", "data": x}
        for x in controversial_whw
    ]
    whw_choice_label = st.radio(
        "why_how_what_statements (Primary & Controversial)",
        [whw["label"] for whw in all_whw],
        key="why_how_what_statements"
    )
    selected_whw = next((whw for whw in all_whw if whw["label"] == whw_choice_label), None)
    
    st.subheader("Choose a problem_solution_sets")
    all_solutions = [
        {"label": f"[Primary] — {x['problem']} — {x['solution']}", "type": "primary", "data": x}
        for x in primary_solutions
    ] + [
        {"label": f"[Controversial] — {x['problem']} — {x['solution']}", "type": "controversial", "data": x}
        for x in controversial_solutions
    ]
    solution_choice_label = st.radio(
        "problem_solution_sets (Primary & Controversial)",
        [solution["label"] for solution in all_solutions],
        key="solution"
    )
    selected_solution = next((solution for solution in all_solutions if solution["label"] == solution_choice_label), None)

    st.subheader("Pick a Tone Option")
    all_tones = [
        {"label": f"[Primary] {x}", "type": "primary", "data": x}
        for x in primary_tones
    ] + [
        {"label": f"[Controversial] {x}", "type": "controversial", "data": x}
        for x in controversial_tones
    ]
    tone_choice = st.radio("Tones (Primary & Controversial)", 
                           [tone["label"] for tone in all_tones],
                           key="tone_radio")
    
    if st.button("Next", key="go_to_step_2"):
        # Save user selections
        st.session_state.selections["step_1"] = {
            "business_core_idea": selected_idea,  # contains .type and .data
            "whw": selected_whw,
            "solution": selected_solution,
            "tone": tone_choice,
        }
        st.session_state.step_inputs["step_2_context"] = f"""
            FOUNDATION PREFACE
            Use the following strategic selections from previous stages as non-negotiable foundations for all outputs. Every line should reflect and extend the logic, tone, and cultural position of this core strategy.
            {st.session_state.selections["step_1"]}
            Please ensure all responses in this prompt reflect and extend this foundation. Reject generic startup speak. Match the tone and strategic specificity of the Brand Inputs Master.
            {step_2_master_prompt}
        """
        # Construct new message for LLM
        st.session_state.messages.append({
            "role": "user",
            "content": st.session_state.step_inputs["step_2_context"]
        })
        step_2_output = generate_step_output(st.session_state.messages)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": step_2_output
        })
        print("================== result 2 ====================")
        print(step_2_output)
        st.session_state.step_outputs["step_2"] = step_2_output
        st.session_state.step += 1
        # st.experimental_rerun()
    if st.button("Redo", key="redo_step_1_selections"):
        st.session_state.selections.pop("step_1", None)
        st.session_state.step_outputs.pop("step_1", None)
        st.session_state.step = 1
        # st.experimental_rerun()

# ---------- STEP 3  ----------
if st.session_state.step == 3:
    st.header("Step 3: Select Cultural Layer Options")
    try:
        data = json.loads(st.session_state.step_outputs["step_2"])
    except Exception as e:
        st.error(f"Could not parse output as JSON: {e}")
        st.text_area("Raw Output", value=st.session_state.step_outputs["step_2"])
        st.stop()

    st.subheader("Story Archetype")
    archetype = data["story_archetype"]
    st.write(archetype)

    # Alliterative (checkboxes)
    st.subheader("Cult Words – Alliterative (Check all that resonate)")
    alliterative = data["cult_words"]["alliterative"]
    sel_allit = []
    for word in alliterative:
        if st.checkbox(word, key=f"allit_{word}"):
            sel_allit.append(word)

    # Operating Principles (checkboxes)
    st.subheader("Operating Principles (Check all that fit)")
    operating = data["cult_words"]["operating_principles"]
    sel_oper = []
    for word in operating:
        if st.checkbox(word, key=f"oper_{word}"):
            sel_oper.append(word)

    st.subheader("Brand Persona")
    persona = data["brand_persona"]
    st.write(persona)

    # Competitors (checkboxes)
    st.subheader("Competitors (Check all relevant)")
    competitors = [f"{c['name']}: {c['differentiation']}" for c in data["competitors"]]
    comp_choice = []
    for comp in competitors:
        if st.checkbox(comp, key=f"comp_{comp}"):
            comp_choice.append(comp)

    # References (checkboxes)
    st.subheader("References (Check all that fit)")
    references = data["references"]
    sel_refs = []
    for ref in references:
        if st.checkbox(ref, key=f"ref_{ref}"):
            sel_refs.append(ref)

    # Red Flags (checkboxes)
    st.subheader("Red Flags (Check all to avoid)")
    red_flags = data["red_flags"]
    sel_red_flags = []
    for flag in red_flags:
        if st.checkbox(flag, key=f"redflag_{flag}"):
            sel_red_flags.append(flag)

    if st.button("Next", key="go_to_step_4"):
        st.session_state.selections["step_2"] = {
            "archetype": archetype,
            "alliterative": sel_allit,
            "operating_principles": sel_oper,
            "persona": persona,
            "competitors": comp_choice,
            "references": sel_refs,
            "red_flags": sel_red_flags
        }
        st.session_state.step_inputs["step_3_context"] = f"""
            FOUNDATION PREFACE
            Use the following strategic selections from previous stages as non-negotiable foundations for all outputs. Every line should reflect and extend the logic, tone, and cultural position of this core strategy.
            {st.session_state.selections["step_2"]}
            Please ensure all responses in this prompt reflect and extend this foundation. Reject generic startup speak. Match the tone and strategic specificity of the Brand Inputs Master.
            {step_3_master_prompt}
        """
        # Construct new message for LLM
        st.session_state.messages.append({
            "role": "user",
            "content": st.session_state.step_inputs["step_3_context"]
        })
        step_3_output = generate_step_output(st.session_state.messages)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": step_3_output
        })
        print("================== result 3 ====================")
        print(step_3_output)
        st.session_state.step_outputs["step_3"] = step_3_output
        st.session_state.step += 1
        
    if st.button("Redo", key="redo_step_3_selections"):
        st.session_state.selections.pop("step_2", None)
        st.session_state.step_outputs.pop("step_2", None)
        st.session_state.step = 3
        # st.experimental_rerun()

# ----------- STEP 4-----------
if True or st.session_state.step == 4:
    st.header("Step 4: Select Brand Directions")
    try:
        data = json.loads(st.session_state.step_outputs["step_3"])
    except Exception as e:
        st.error(f"Could not parse output as JSON: {e}")
        st.text_area("Raw Output", value=st.session_state.step_outputs["step_3"])
        st.stop()

    brand_directions = data["brand_directions"]
    st.markdown("#### Review the directions and select any that resonate as potential paths for the brand. (You can pick more than one!)")

    # Collect selected directions
    selected_directions = []
    for i, direction in enumerate(brand_directions):
        label = f"**Direction #{i+1}:**\n- {direction['description']}\n- *Core Words:* {', '.join(direction['core_words'])}\n- *Tag:* {direction['direction_tag']}"
        checked = st.checkbox(label, key=f"dir_{i}")
        if checked:
            selected_directions.append(direction)

    if st.button("Next", key="go_to_step_5"):
        if not selected_directions:
            st.warning("Please select at least one direction to continue!")
            st.stop()
        st.session_state.selections["step_4"] = {
            "selected_brand_directions": selected_directions
        }
        st.session_state.step_inputs["step_4_context"] = f"""
            FOUNDATION PREFACE
            Use the following strategic selections from previous stages as non-negotiable foundations for all outputs. Every line should reflect and extend the logic, tone, and cultural position of this core strategy.
            {st.session_state.selections["step_4"]}
            Please ensure all responses in this prompt reflect and extend this foundation. Reject generic startup speak. Match the tone and strategic specificity of the Brand Inputs Master.
            {step_4_master_prompt}
        """
        # Construct new message for LLM
        st.session_state.messages.append({
            "role": "user",
            "content": st.session_state.step_inputs["step_4_context"]
        })
        step_4_output = generate_step_output(st.session_state.messages)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": step_4_output
        })
        print("================== result 4 ====================")
        print(step_4_output)
        st.session_state.step += 1
        # st.experimental_rerun()
    if st.button("Redo", key="redo_step_4_selections"):
        st.session_state.selections.pop("step_3", None)
        st.session_state.step_outputs.pop("step_3", None)
        st.session_state.step = 4
        # st.experimental_rerun()