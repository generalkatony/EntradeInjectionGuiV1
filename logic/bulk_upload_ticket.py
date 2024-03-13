import requests
import json
import pandas as pd
from openpyxl import load_workbook
from icecream import ic
from logic import *


###### THIS IS HEADER FUNCTION FOR MOLECULE ###
def create_headers(email, token):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-email": email,
        "x-token": token,
    }
    return headers


###############################################


########## THE CORE FUNCTION FOR THIS FILE ##########################
########## READS CSV FILE AND BULK UPLOADS TO MOLECULE AS TICKETS ###
########## TRADE LINKAGE INCLUDED ###################################
def bulk_ticket_upload(upload_file, headers, match_field, url):
    # Reads the specified CSV FILE
    df_data = pd.read_csv(
        f"{upload_file}",
        header=0,
    )

    # for possible empty entries in the CSV file, panda fills the data set with an empty ""
    df_data = df_data.fillna("")

    print(df_data)

    # Iterates through each row inside the CSV file

    for idx, data in df_data.iterrows():
        # Populate the payload with booleans fill, boolean dedupe_external_id and the subleg_id depending whether if trade_id exists
        payload = {}

        for key, value in match_field.items():
            try:
                payload[key] = data[value]
            except KeyError as e:
                print(f"Key error: {e}. This key was not found in the data. Skipping this key.")


        ####################### FILTER DATA SECTION ###########################################

        ######### remove n/a data from package ########################

        # Define values to remove
        values_to_remove = {"", "n/a", "N/a", "N/A", "n/A", "empty"}

        # filter the payload
        filtered_payload = {
            key: value
            for key, value in payload.items()
            if value is not None and value not in values_to_remove
        }

        ######## check if CHECKBOX condition is valid##################

        allowed_statuses = {}

        # Define the allowed statuses

        for key, value in allowed_statuses.items():
            if key in filtered_payload and filtered_payload[key] not in value:
                del filtered_payload[key]

        ############### UPLOAD DATA N PRINT RESPONSE ###########################################

        ticket_url = f"{url}"

        # Send the JSON data in the request
        response = requests.post(
            ticket_url, data=json.dumps(filtered_payload), headers=headers
        )
        print("\n sent package looks like " + json.dumps(filtered_payload))

        # print(f"\n Request failed with status code: {response.status_code}")
        print(f"\n Status code: {response.status_code} ( {response.reason} )\n")
        print(
            "Ticket loaded as: \n\n"
            + json.dumps(response.json(), separators=(",", ":"), indent=4)
        )
