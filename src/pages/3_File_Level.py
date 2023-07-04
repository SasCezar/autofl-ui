import pandas as pd
import streamlit as st
import plotly.express as px
from analysis.file import unannotated_percent

if 'annotations' not in st.session_state:
    st.error('No labels found. Analyze a project first', icon="🚨")
    st.stop()

annot: pd.DataFrame = st.session_state['annotations']


df = unannotated_percent(annot)
fig = px.pie(df, values='count', names='unannotated', hole=.3)
st.plotly_chart(fig, theme="streamlit")
