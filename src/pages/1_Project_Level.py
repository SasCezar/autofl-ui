import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt
from analysis.project import top_labels

if 'annotations' not in st.session_state:
    st.error('No labels found. Analyze a project first', icon="🚨")
    st.stop()

annot: pd.DataFrame = st.session_state['annotations']

res = top_labels(annot)
default = min(len(res), 10)
top = st.slider('Show top', 1, len(res), default)
df = pd.DataFrame({'label': [str(x) for x in range(len(res))], 'prob': res})
df = df.sort_values('prob', ascending=False)
df = df.head(top)

fig = px.bar(df, x="prob", y="label", color="label", title="Project level labels (avg)")
st.plotly_chart(fig, theme="streamlit")

# chart = (
#     alt.Chart(df)
#     .mark_bar()
#     .encode(
#         x=alt.X("prob", type="quantitative", title=""),
#         y=alt.Y("label", type="nominal", title=""),
#         color=alt.Color("label", type="nominal", title=""),
#         order=alt.Order("prob", sort="descending"),
#     )
# )
#
# st.altair_chart(chart, use_container_width=True)
