from typing import List

import streamlit as st

from request.file_annotation import annotate_file

st.set_page_config(
    page_title="Analysis",
    page_icon="👋",
    layout="wide"
)


def run_file_annotation(project_name: str, remote: str, languages: List[str]):
    if not project_name:
        return
    annotations, taxonomy = annotate_file(project_name, remote, languages)
    st.session_state['annotations'] = annotations
    st.session_state['taxonomy'] = taxonomy


st.markdown("## Analyse Project")
with st.container():
    with st.form("my_form"):
        st.markdown("### Select a Project to Analyze")

        project_name = st.text_input('Project Name')

        remote = st.text_input('Remote URL')
        languages = st.multiselect('What Languages to Analyze', ['java', 'python', 'cpp', 'c_sharp', 'c'], ['java'])
        res = st.form_submit_button(type='primary', use_container_width=True)

        if res:
            if not project_name:
                st.error('Fill the fields')

            col1, col2, col3 = st.columns(3)
            with col2:
                with st.spinner(f'Analyzing {project_name} @ {remote}'):
                    run_file_annotation(project_name, remote, languages)

            st.success("Project analyzed", icon="✅")
