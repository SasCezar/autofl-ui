import numpy as np
import pandas as pd
import streamlit as st
from pandas import DataFrame

from analysis.project import top_labels


def argmax_top(x, top):
    top_pos = np.argsort(x)
    for t in top_pos:
        if t in top:
            return t
    return top_pos[0]


@st.cache_data(show_spinner=False)
def package_labels(df: DataFrame, top=10):
    top_proj_labels = np.argsort(top_labels(df))[-top:]
    df_count = df.groupby('package')['package'].count().reset_index(name='Count')
    df = df.groupby('package')['distribution'].apply(lambda x: np.mean(np.array(x.tolist()), axis=0)).reset_index()
    # df['label'] = [np.argmax(x) for x in df['distribution']]
    df['label'] = [argmax_top(x, top_proj_labels) for x in df['distribution']]
    df = df.set_index('package').join(df_count.set_index('package'), how='inner')

    packages = []
    for package in df.index:
        parents = [x for x in package.split('.') if x]
        if not parents:
            parents = ['.']
        parents = parents
        packages.append(parents)

    df = pd.merge(df, pd.DataFrame(packages).add_prefix('parent_'), on=df.index)
    df = df.rename(columns={'key_0': 'Package'})
    df.drop(columns=['distribution'], axis=1)
    df.loc[df['Package'] == '.', 'Count'] = df.loc[df['Package'] == '.', 'Count'] / 4
    df.columns = [x.title() for x in df.columns]
    return df
