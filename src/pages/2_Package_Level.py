import pandas as pd
import streamlit as st

if 'annotations' not in st.session_state:
    st.error('No labels found. Analyze a project first', icon="🚨")
    st.stop()

annot: pd.DataFrame = st.session_state['annotations']