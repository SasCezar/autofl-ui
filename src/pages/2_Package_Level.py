import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_extras.chart_container import chart_container

from analysis.package import package_labels

if 'annotations' not in st.session_state:
    st.error('No labels found. Analyze a project first', icon="🚨")
    st.stop()

annot: pd.DataFrame = st.session_state['annotations']

st.markdown("# Package Level Stats")

package_df = package_labels(annot)

with st.container():
    st.markdown("## Package Labels")
    parents = [x for x in package_df.columns if 'Parent_' in x]
    default = min(len(parents) + 1, 10)
    depth = st.slider('Depth', 1, len(parents) + 1, default)
    levels = [px.Constant("Project")] + parents
    package_df['Label'] = package_df['Label'].astype(str)

    with chart_container(package_df.drop(parents, axis=1)):
        fig = px.treemap(package_df, path=levels, color='Label', values='Count', maxdepth=depth,
                         hover_name="Package", hover_data=dict(Label=True, Count=True))
        fig.update_layout(height=1000)

        #fig.update_traces(hovertemplate='%{Package}<br>Label= %{Label}<br>Count= %{Count}<extra></extra>')
        st.plotly_chart(fig, theme="streamlit", use_container_width=True, height=1000)
