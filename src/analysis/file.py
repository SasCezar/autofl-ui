from pandas import DataFrame
import streamlit as st


@st.cache_data(show_spinner=False)
def unannotated_percent(df: DataFrame):
    unannotated = df.groupby(['unannotated'])['unannotated'].count().reset_index(name="count")
    return unannotated
