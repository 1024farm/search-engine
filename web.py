import streamlit as st

with st.form("import document"):
    title = st.text_input('Title')
    content = st.text_area('Content')

    # Every form must have a submit button.
    submitted = st.form_submit_button("Save")
    if submitted:
        st.write("title", title, "content", content)
