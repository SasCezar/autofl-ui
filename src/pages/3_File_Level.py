import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_extras.chart_container import chart_container

from analysis.file import number_uannanotated, avg_jsd

if 'annotations' not in st.session_state:
    st.error('No labels found. Analyze a project first', icon="🚨")
    st.stop()

annot: pd.DataFrame = st.session_state['annotations']

df = number_uannanotated(annot)

st.markdown("# File Level Stats")
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("## JSD Distribution")
        jsd = [x for x in avg_jsd(annot)]
        with chart_container(pd.DataFrame(jsd)):
            bins = st.slider('Bins', 0, 100, 30, step=5)
            fig = px.histogram(x=jsd, nbins=bins,
                               marginal="box")
            fig.update_layout(xaxis_title="JSD",
                               yaxis_title="Count")
            #                   font=dict(size=20),
            #                   yaxis=dict(
            #                       tickfont=dict(size=20)),
            #                   xaxis=dict(
            #                       tickfont=dict(size=20)),
            #                   legend=dict(font=dict(size=20)),
            #                   hoverlabel=dict(font_size=20)
            #                   )

            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    with col2:
        st.markdown("## Unannotated Files")

        with chart_container(annot[annot.columns.intersection(['unannotated'])]):
            fig = px.pie(df, values='count', names='unannotated', hole=.5, hover_name="unannotated",
                         hover_data={'unannotated': False})
            fig.update_layout(margin=dict(b=0, l=0, r=0))
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

with st.container():
    st.markdown("## File Labels")
    file_labels_df = annot.reset_index()
    file_labels_df['label'] = [np.argmax(x) for x in file_labels_df['distribution']]
    file_labels_df['label'] = file_labels_df['label'].astype(str)
    file_labels_df['file'] = file_labels_df['index'].apply(lambda x: x.split('/')[-1])
    file_labels_df = file_labels_df.drop(columns=['distribution', 'labels'], axis=1)
    with chart_container(file_labels_df):
        fig = px.treemap(file_labels_df, path=[px.Constant("Project"), 'package', 'file'], color='label')
        fig.update_layout(height=1000)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True, height=1000)
