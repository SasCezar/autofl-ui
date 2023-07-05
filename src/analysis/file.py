import numpy as np
from pandas import DataFrame
import streamlit as st
from scipy.spatial import distance


@st.cache_data(show_spinner=False)
def number_uannanotated(df: DataFrame):
    unannotated = df.groupby(['unannotated'])['unannotated'].count().reset_index(name="count")
    label_map = {True: "Unannotated", False: 'Annotated'}
    unannotated = unannotated.replace({"unannotated": label_map})
    return unannotated


@st.cache_data(show_spinner=False)
def avg_jsd(df: DataFrame):
    res = np.array(df['distribution'].to_list())
    n = len(res[0])
    norm = np.ones(n) / n
    jsd = distance.jensenshannon(res, [norm], axis=1)
    return jsd
