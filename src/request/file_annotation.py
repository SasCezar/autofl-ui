from typing import List

import numpy as np
import pandas as pd
import requests
import streamlit as st


def get_label(distribution, taxonomy):
    return taxonomy[str(np.argmax(distribution))]


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
    taxonomy = res['taxonomy']
    print(taxonomy)
    entries = []
    files = res['versions'][0]['files']
    for file_name in files:
        file = files[file_name]
        entries.append({
            "path": file["path"],
            "package": file["package"],
            "distribution": file["annotation"]["distribution"],
            "unannotated": file["annotation"]["unannotated"],
            "label": get_label(file["annotation"]["distribution"], taxonomy)
        })

    annotations_df = pd.DataFrame(entries)

    return annotations_df, taxonomy
