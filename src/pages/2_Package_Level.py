import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_extras.chart_container import chart_container

from analysis.package import package_labels

if 'file_annot' not in st.session_state:
    st.error('No labels found. Analyze a project first', icon="🚨")
    st.stop()

proj_annot = st.session_state['project_annot']
annot: pd.DataFrame = st.session_state['file_annot']
taxonomy: pd.DataFrame = st.session_state['taxonomy']

st.markdown("# Package Level Stats")

with st.container():
    st.markdown("## Package Labels")
    top = st.slider('Only Top Labels', 1, len(taxonomy) + 1, 20)
    package_df = package_labels(annot, proj_annot, top)
    parents = [x for x in package_df.columns if 'Parent_' in x]
    default = min(len(parents) + 1, 10)
    depth = len(parents) + 1 #st.slider('Depth', 1, len(parents) + 1, default)

    levels = [px.Constant("Project")] + parents
    package_df['Label'] = [taxonomy[str(x)] for x in package_df['Label']]
    print(package_df)
    with chart_container(package_df.drop(parents, axis=1)):
        fig = px.treemap(package_df, path=levels, color='Label', values='Count', maxdepth=depth,
                         hover_name="Package", hover_data=dict(Label=True, Count=True))
        fig.update_layout(height=1000, font=dict(size=20))
        st.plotly_chart(fig, theme="streamlit", use_container_width=True, height=1000)

    # with chart_container(package_df.drop(parents, axis=1)):
    #     fig = px.sunburst(package_df, path=levels, color='Label', values='Count', maxdepth=depth,
    #                       hover_name="Package", hover_data=dict(Label=True, Count=True))
    #     fig.update_layout(height=1000)
    #     st.plotly_chart(fig, theme="streamlit", use_container_width=True, height=1000)
