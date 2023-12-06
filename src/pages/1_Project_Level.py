import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_extras.chart_container import chart_container

if 'project_annot' not in st.session_state:
    st.error('No labels found. Analyze a project first', icon="🚨")
    st.stop()

proj_annot = st.session_state['project_annot']
taxonomy = st.session_state['taxonomy']

st.markdown("# Project Level Stats")
with st.container():
    default = min(len(proj_annot), 10)
    top = st.slider('Show top', 1, len(proj_annot), default)
    df = pd.DataFrame(
        {'Label': [taxonomy[str(x)] for x in range(len(proj_annot))], 'Probability': proj_annot})
    df = df.sort_values('Probability', ascending=False)

    with chart_container(df):
        plot_df = df.head(top)
        fig = px.bar(plot_df, x="Probability", y="Label", color="Label", title="Aggregation: Avg of Files Labels",
                     hover_name="Label", hover_data={'Label': False, 'Probability': ':.6f'})
        fig.update_layout(showlegend=False)
        # fig.update_layout(showlegend=False,
        #                   yaxis=dict(
        #                       tickfont=dict(size=20),
        #                       titlefont=dict(size=20),
        #                   ),
        #                   xaxis=dict(
        #                       tickfont=dict(size=20),
        #                       titlefont=dict(size=20),
        #                   ))
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
#
# with st.container():
#     st.markdown("## Historical Changes")
#     st.markdown("### TODO")
