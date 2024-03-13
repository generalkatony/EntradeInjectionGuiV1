Guide for Molecule Injection Script

- Generate the token and email from molecule API keys.
- url is based on the molecule environment/ region.
  For example, for the EU, its eu.molecule.io
  for the ct-EU, its ct-eu.molecule.io

This is the default template for matching the fields
between the CSV files and the molecule columns.
####################################################

# match_field = {

# "fulfillment_date": "fulfillment_date",

# "commodity": "commodity",

# "volume": "volume",

# "price": "price",

# "asset": "asset",

# "status": "status",

# "final_delivery": "final_delivery",

# "external_id": "external_id",

# "external_source": "external_source",

# "custom_field_name": "custom_field_name",

# }

# test_url = "ct-eu.molecule.io"

# file = "Test Data\Example_data.csv"

####################################################

This project consists of three folders: test_data, Automa_GUI, and logic.

Logic consists of .py files to provide functionalities for the frontend UI.

- bulk_upload_ticket.py: iterates through the csv files, for each row check if they have a trade_id, if so fetch the existing subleg_id from molecule, pick one and upload the trades to Molecule.

- status_bar.py: supposed to provide a create progressbar function to be created in automa_gui.py, and updated by the iteraton idx in the bulk_upload_ticket function. However, this feature is to be continued to be worked on.
