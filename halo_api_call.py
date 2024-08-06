import requests, json
import streamlit as st

baseLink = "https://halo.calvin.edu/api"
authLink = "https://halo.calvin.edu/auth/token"

grant_type = "client_credentials"
client_id = st.secrets["CLIENT_ID"]
client_secret = st.secrets["CLIENT_SECRET"]
scope = "all"

data = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": grant_type,
    "scope": scope,
}


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

    # print(body)
    for asset in asset_list:

        body["assettype_name"] = asset[0]
        body["devicetype"] = body["assettype_name"]

        body["inventory_number"] = asset[1]  # asset tag
        body["assettag"] = body["inventory_number"]

        # print(asset)

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

        # print(body)

    response = requests.post(url=url, headers=headers, data=json.dumps([body]))
    return response

def deleteAsset(token, asset_list: list):
    url = baseLink + "/asset/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    for asset in asset_list:
        pass
        
    response = requests.post(url=url, headers=headers, data=json.dumps())
    return response


def getAssets(token):
    assetUrl = baseLink + "/asset/4142"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url=assetUrl, headers=headers)
    print(response.text)
