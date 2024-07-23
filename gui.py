import streamlit as st
import pandas as pd
import numpy as np
from halo_api_call import *


def convertDataFrameToList(dataframe):
    result = dataframe.values.tolist()
    return result


def export(dataframe):
    export_list = convertDataFrameToList(dataframe)

    token = getToken()
    createAsset(token, export_list)


def uploadFile():
    pass


main_df = ""

st.set_page_config("Halo Asset Import", layout="wide")
st.title("Halo Asset Import")

default_df = pd.DataFrame(
    columns=[
        "Asset Type",
        "Asset Number",
        "Model",
        "Serial Number",
        "Manufacturer",
        "Purchase Date",
        "Who Inventoried",
        "Inventory Date",
        "Notes",
    ]
)

config = {
    "Asset Type": st.column_config.SelectboxColumn(
        "Asset Type", options=["Laptop", "Monitor", "Desktop"]
    ),
    "Asset Number": st.column_config.NumberColumn("Asset Number", format="%d"),
    "Purchase Date": st.column_config.DateColumn(
        "Purchase Date (MM-DD-YYYY)", format="MM-DD-YYYY"
    ),
    "Inventory Date": st.column_config.DateColumn(
        "Inventory Date (MM-DD-YYYY)", format="MM-DD-YYYY"
    ),
}

uploaded_file = st.file_uploader(label="Choose a file (BETA)", type=["csv"])
if uploaded_file is not None:
    match uploaded_file.type:
        case "text/csv":
            asset_file = pd.read_csv(uploaded_file)
            main_df = asset_file
            st.data_editor(
                asset_file,
                column_config=config,
                num_rows="dynamic",
                use_container_width=True,
            )

        case "application/vnd.ms-excel":
            asset_file = pd.read_csv(uploaded_file)
            st.data_editor(
                asset_file,
                column_config=config,
                num_rows="dynamic",
                use_container_width=True,
            )
            main_df = asset_file

        case _:
            print(uploaded_file.type)

else:
    edited_df = st.data_editor(
        default_df, column_config=config, num_rows="dynamic", use_container_width=True
    )
    main_df = edited_df


with st.container():
    col1, col2 = st.columns(2, gap="small")

    with col1:
        export_btn = st.button(label="Export to Halo", on_click=export, args=(main_df,))

    with col2:
        with open("./sample.csv", "rb") as file:
            btn = st.download_button(
                "Download Sample", data=file, file_name="sample.csv", mime="text/csv"
            )  # download template
