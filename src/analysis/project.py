import numpy as np
import streamlit as st
from pandas import DataFrame


@st.cache_data(show_spinner=False)
def top_labels(df: DataFrame):
    df: DataFrame = df[df['unannotated'] == False]
    annotations = np.array(df['distribution'].to_list())
    res = annotations.mean(axis=0)
    return res


@st.cache_data(show_spinner=False)
def percentage_composition(df: DataFrame):
    pass
