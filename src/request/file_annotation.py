from typing import List

import pandas as pd
import requests
import streamlit as st


@st.cache_data(show_spinner=False)
def annotate_file(project_name: str, remote: str, languages: List[str]):
    url = 'http://auto-fl:8000/label/files'
    analysis = {
        "name": project_name,  # "Waikato|weka-3.8",
        "remote": remote,  # "https://github.com/Waikato/weka-3.8",
        "languages": languages  # ["java"]
    }

    res = requests.post(url, json=analysis)
    res = res.json()['result']
    annotations_df = pd.DataFrame.from_dict(res['versions'][0]['files_annotation']).transpose()
    package_map = {file.path:file.package for file in res['versions'][0]['files'].values()}
    annotations_df['package'] = [package_map[x] for x in annotations_df.index]
    taxonomy = res['taxonomy']
    return annotations_df, taxonomy
