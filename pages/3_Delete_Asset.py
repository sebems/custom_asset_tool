import streamlit as st
from helper import *

st.set_page_config("Delete Assets", page_icon="🗑️",layout="wide")

st.sidebar.header("Delete Assets")

# default dataframe w/ columns
default_df = pd.DataFrame(
    columns=[
        "Assets",
    ]
)

main_df = st.data_editor(
    default_df, num_rows="dynamic", width=1000
)


# DELETE BUTTON
delete_btn = st.button(label="Delete Assets", on_click=delete, type="primary", args=(main_df,))

