import requests, json, os
import streamlit as st
from dotenv import load_dotenv

DEV_MODE_ON = False
DEBUG = False

baseLink = "https://halo.calvin.edu/api"
authLink = "https://halo.calvin.edu/auth/token"

if DEV_MODE_ON:
    load_dotenv()

    client_id =os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

else:
    client_id = st.secrets["CLIENT_ID"]
    client_secret = st.secrets["CLIENT_SECRET"]

grant_type = "client_credentials"
scope = "all"

data = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": grant_type,
    "scope": scope,
}

# messages = st.container(height=300)

def getToken():

    response = requests.post(authLink, data=data)
    token = response.json()["access_token"]

    return token


def createAsset(token, asset_list: list):
    url = baseLink + "/asset"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    body = {}
    with open("./sample_asset.json", "r") as file:
        body = json.load(file)

    if DEBUG:
        print(body)

    for asset in asset_list:

        body["assettype_name"] = asset[0]
        body["devicetype"] = body["assettype_name"]

        body["inventory_number"] = asset[1]  # asset tag
        body["assettag"] = body["inventory_number"]

        if DEBUG:
            print(asset)

        # body["fields"][0]["value"] = ""  # name TODO: differentiate between MAC and PC
        body["fields"][1]["value"] = asset[2]  # model
        body["fields"][2]["value"] = asset[3]  # serial number
        body["fields"][7]["value"] = asset[4]  # manufacturer
        body["fields"][3]["value"] = asset[5]  # date purchased
        body["fields"][5]["value"] = asset[7]  # inventory date
        body["fields"][4]["value"] = asset[6]  # who inventoried

        body["fields"][6]["value"] = (
            "PC" + str(body["assettag"])
            if body["assettype_name"] in ("Laptop", "Desktop")
            else ""
        )  # machine name

        body["notes"] = asset[-1]

        if DEBUG:
            print(body)

    response = requests.post(url=url, headers=headers, data=json.dumps([body]))
    return response

def deleteAsset(token, asset_list: list):
    url = baseLink + "/asset/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        for asset in asset_list:
            asset_id = getAssetID(token, asset)
            if asset_id != -1:
                delete_resp = requests.delete(url=url + str(asset_id), headers=headers)
                st.toast(f"Asset \"{asset}\" Deleted", icon="✅")
            else:
                st.toast(f"Asset \"{asset}\" Does Not Exist", icon="🚨")
                continue
    except Exception as e:
        print(e)


def getAssetID(token, asset_number):
    assetUrl = baseLink + "/asset/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    response = requests.get(url=assetUrl + f"?search={asset_number}", headers=headers)

    if DEBUG:
        print(response, response.text)

    if response.json()["record_count"] <= 0:
        if DEBUG:
            print("Asset Doesn't Exist")

        return -1
    else:
        temp_id_holder = response.json()["assets"][0]
        return(temp_id_holder["id"])
