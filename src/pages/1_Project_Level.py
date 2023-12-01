import random
import string

import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_extras.chart_container import chart_container

from analysis.project import top_labels

if 'annotations' not in st.session_state:
    st.error('No labels found. Analyze a project first', icon="🚨")
    st.stop()

annot: pd.DataFrame = st.session_state['annotations']


def get_random_string(length):
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str


st.markdown("# Project Level Stats")
with st.container():
    #st.markdown("## Top Labels")
    res = top_labels(annot)
    default = min(len(res), 10)
    top = st.slider('Show top', 1, len(res), default)
    df = pd.DataFrame({'Label': [st.session_state['taxonomy'][str(x)] for x in range(len(res))], 'Probability': res})
    df = df.sort_values('Probability', ascending=False)

    with chart_container(df):
        plot_df = df.head(top)
        fig = px.bar(plot_df, x="Probability", y="Label", color="Label", title="Aggregation: Avg of Files Labels",
                     hover_name="Label", hover_data={'Label': False, 'Probability': ':.6f'})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

with st.container():
    st.markdown("## Historical Changes")
    st.markdown("### TODO")
