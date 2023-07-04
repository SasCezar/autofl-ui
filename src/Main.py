import time
from typing import List

import streamlit as st

from request.file_annotation import annotate_file

st.set_page_config(
    page_title="Analysis",
    page_icon="👋",
)


def run_file_annotation(project_name: str, remote: str, languages: List[str]):
    annotations = annotate_file(project_name, remote, languages)
    st.session_state['annotations'] = annotations


with st.container():
    with st.form("my_form"):
        st.write("Select a project to analyze")

        project_name = st.text_input('Project name', '')

        remote = st.text_input('Remote URL', '')
        languages = st.multiselect('What languages to analyze', ['java', 'python', 'cpp', 'c_sharp', 'c'], ['java'])
        res = st.form_submit_button(on_click=run_file_annotation, args=(project_name, remote, languages))
