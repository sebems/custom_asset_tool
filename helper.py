import streamlit as st
import pandas as pd
from halo_api_call import *

def convertDataFrameToList(dataframe: pd.DataFrame):
    """
        Converts DataFrame entries into a list
    """
    result = dataframe.values.tolist()
    return result

def delete(dataframe: pd.DataFrame):
    """
        Deletes DataFrame entries from Halo
    """
    delete_list = dataframe['Assets'].tolist()

    token = getToken()
    deleteAsset(token, delete_list)

def export(dataframe: pd.DataFrame):
    """
        Uses the POST API call from halo_api_call.py to push dataframe to Halo
    """
    export_list = convertDataFrameToList(dataframe)

    token = getToken()
    response = createAsset(token, export_list)    # returns a request object

    if (response.ok):
        st.toast('Export Successful!', icon="✅")
    else:
        st.toast(response.status_code + " " + response.reason, icon="🚨")
