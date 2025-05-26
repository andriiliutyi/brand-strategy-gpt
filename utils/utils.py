def editable_radio(st, label, options, field_labels, session_key_prefix):
    # options: List of dicts with fields to edit (e.g., micro_core_idea, expanded_core_idea)
    if f"{session_key_prefix}_selected" not in st.session_state:
        st.session_state[f"{session_key_prefix}_selected"] = 0

    edited_options = []
    for idx, option in enumerate(options):
        cols = st.columns([0.1] + [0.9/len(field_labels)] * len(field_labels))
        with cols[0]:
            if st.button("●" if st.session_state[f"{session_key_prefix}_selected"] == idx else "○", key=f"{session_key_prefix}_radio_{idx}"):
                st.session_state[f"{session_key_prefix}_selected"] = idx
        field_values = {}
        for f_idx, field in enumerate(field_labels):
            with cols[f_idx+1]:
                if len(field_labels) > 1:
                    field_val = st.text_input(field, value=option.get(field, ""), key=f"{session_key_prefix}_{field}_{idx}")
                else:
                    field_val = st.text_area(field, value=option.get(field, ""), key=f"{session_key_prefix}_{field}_{idx}")
                field_values[field] = field_val
        edited_options.append(field_values)
    selected_option = edited_options[st.session_state[f"{session_key_prefix}_selected"]]
    return selected_option, st.session_state[f"{session_key_prefix}_selected"], edited_options
