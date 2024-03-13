import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import json
import os
from icecream import ic
import logic
from logic import *
import sys

############## GENERAL FUNCTIONS ############################

############# INITIALIZE THE GUI ############################

# Create the window
window = tk.Tk()
window.title("Automata Alpha Release 1.0.3")

# Function to get the path of a file in the Theme folder
def get_theme_path(file_name):
    # Get the directory of the current script file
    script_dir = os.path.dirname(__file__)
    # Construct the path to the file in the Theme folder
    theme_path = os.path.join(script_dir, "Theme", file_name)
    return theme_path

# Source the Tcl scripts using the correct paths
window.tk.call("source", get_theme_path("forest-light.tcl"))
window.tk.call("source", get_theme_path("forest-dark.tcl"))

# Set the theme
style = ttk.Style()
style.theme_use("forest-dark")

######### LOAD SAVED DATA FROM .JSON ########################
# Check if the JSON file exists and create it if it doesn't

# This is where the data entered into the GUI is saved and can be reopened again.
# name of the saved data .json file
filename = "data.json"

# if not exist, create a datajson file
if not os.path.exists(filename):
    print(f"Creating {filename}")
    with open(filename, "w") as json_file:
        json.dump({}, json_file)

# Load data from JSON
with open(filename, "r") as json_file:
    saved_data = json.load(json_file)
    print(f"Loaded data from {filename}: {saved_data}")

frame = ttk.Frame(window)
frame.pack()


########### TO CLEAR .JSON FILE #############################
# this function is for the clear fields button
def clear_json_file(file_path):
    try:
        # Open the JSON file in write mode, which clears its contents
        with open(file_path, "w") as json_file:
            # Write an empty JSON structure (an empty dictionary)
            json.dump({}, json_file)
        print(f"Contents of {file_path} cleared successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


############ FOR LIGHT/ DARK MODE ############################
# This function is to toggle light/ dark mode


def toggle_mode():
    if mode_switch.instate(["selected"]):
        style.theme_use("forest-light")
    else:
        style.theme_use("forest-dark")
        
########### UNIVERSAL FIELD DATA DICT ######################
# Initialization of required value libraries to store
# entry widgets path and values ertered into the widgets

info_value = {}
entry_widgets = {}
entered_value = {}  # list for entered values
cus_entry_widgets = {}
cus_saved_entry_widgets = {}

######## LOAD SAVED DATA, IF ANY INTO THE INFO AND MATCHING FIELDS#######

info_value = saved_data.get(
    "info_value", {}
)  # Get info_value or an empty dictionary if it doesn't exist
entered_value = saved_data.get(
    "entered_value", {}
)  # Get entered_value or an empty dictionary if it doesn't exist

ic(info_value)
ic(entered_value)

########### CREATING THE SUB-FRAMES FOR EACH SECTION #########
# Info Frame
info_frame = ttk.LabelFrame(frame, text="Info")
info_frame.grid(row=0, column=0, padx=5, pady=5)
# Field Frame
fields_frame = ttk.LabelFrame(frame, text="Fields")
fields_frame.grid(row=1, column=0, padx=5, pady=5)
# -- Default
default_fields_frame = ttk.LabelFrame(fields_frame, text="Default")
default_fields_frame.grid(row=1, column=0, padx=10, pady=10)
# -- Custom
cusfields_frame = ttk.LabelFrame(fields_frame, text="Custom")
cusfields_frame.grid(row=1, column=1, padx=10, pady=10)
# Status Bar
status_bar_frame = ttk.LabelFrame(frame, text="Status")
status_bar_frame.grid(row=2, column=1, padx=5, pady=5)
# Console Frame
console_frame = ttk.LabelFrame(frame, text="Console")
console_frame.grid(row=0, column=1, padx=5, pady=5)
###############################################################

############ ADD CONSOLE ###################################
class TextRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.configure(state='normal')
        self.widget.insert(tk.END, str)
        self.widget.see(tk.END)
        self.widget.configure(state='disabled')

    def flush(self):
        pass  # This might be needed depending on the Python version.

# ScrolledText widget for the console
console = scrolledtext.ScrolledText(console_frame, state='disabled', height=15)
console.pack(fill=tk.BOTH, expand=True)

# Redirect sys.stdout and sys.stderr
sys.stdout = TextRedirector(console)
sys.stderr = TextRedirector(console)

############################################################


# NAME variables to be created for the info_frame
info_fields = [
    "URL",
    "username",
    "password",
]

# initialization of the info_widgets
info_widgets = {}

# for each variable in info_fields, create an entry widget
for i, var_name in enumerate(info_fields):
    label = ttk.Label(info_frame, text=var_name + ":")
    label.grid(row=i, column=0, sticky="ew", padx=3, pady=3)

    # Create a regular Entry widget for other variables
    entry = ttk.Entry(info_frame)

    entry.grid(row=i, column=1, padx=3, pady=3)
    info_widgets[var_name] = entry


#### FUNCTION to select files for uplaod_file entry ########
def set_path(entry_field):
    path = filedialog.askopenfilename()
    entry_field.delete(0, tk.END)
    entry_field.insert(0, path)
    info_value["upload_file"] = path


csv_label = ttk.Label(info_frame, text="upload_file")
csv_label.grid(row=0, column=3, padx=5, pady=5)
csv_entry = ttk.Entry(info_frame)
csv_entry.grid(row=0, column=4, padx=5, pady=5)
info_widgets["upload_file"] = csv_entry

btn_get_path = ttk.Button(
    info_frame, text="Select File", command=lambda: set_path(csv_entry)
)
btn_get_path.grid(row=1, column=4, padx=2, pady=2)

##### FUNCTION TO PING URL ####################################
def ping_url(url):
    try:
        response = requests.get(url, timeout=5)  # Timeout set to 5 seconds
        # Check if the HTTP status code is OK (200)
        if response.status_code == 200:
            print(f"URL {url} is active and responding.")
            return True
        else:
            print(f"URL {url} is reachable but returned status code {response.status_code}.")
            return False
    except requests.ConnectionError:
        print(f"URL {url} could not be reached.")
        return False
    except requests.Timeout:
        print(f"Request to URL {url} timed out.")
        return False
    except requests.RequestException as e:
        print(f"An error occurred while trying to ping {url}: {e}")
        return False
    
url_entry = info_widgets["URL"]

btn_ping_URL = ttk.Button(
    info_frame, text="Ping URL", command=lambda: ping_url(url_entry.get())
)
btn_ping_URL.grid(row=3, column=4, padx=2, pady=2)

############################################################

############# DEFAULT FIELD FRAME ##########################

variables = [
    "CurveDate",

]

####### CREATE VALUE INPUT FRAME #####################

for i, var_name in enumerate(variables):
    label = ttk.Label(default_fields_frame, text=var_name.capitalize() + ":")
    label.grid(row=i, column=0, sticky="ew")

    # Create a regular Entry widget for other variables
    entry = ttk.Entry(default_fields_frame)

    entry.grid(row=i, column=1, pady=2)
    entry_widgets[var_name] = entry

################# dark/ light mode #########################

# add dark/light mode toggle
mode_switch = ttk.Checkbutton(frame, text="Theme", style="Switch", command=toggle_mode)
mode_switch.grid(row=7, column=0, padx=2, pady=5, sticky="nsew")

############## ADD ENTRY BUTTON FOR CUSTOM FIELDS #############################
def add_entry(frame, widget, key=None, value=None):
    custom_label = ttk.Entry(frame)
    custom_label.grid(row=len(widget), column=0, padx=2, pady=2)
    custom_value = ttk.Entry(frame)
    custom_value.grid(row=len(widget), column=1, padx=2, pady=2)

    if key is not None and key != "":
        custom_label.insert(0, key)
    if value is not None and value != "":
        custom_value.insert(0, value)

    # Store the new entry widgets with descriptive keys (use label text as key)
    widget[custom_label] = custom_value
    # ic(cus_entry_widgets)


add_button = ttk.Button(
    cusfields_frame,
    text="Add Entry",
    command=lambda: add_entry(cusfields_frame, cus_entry_widgets),
)
add_button.grid(row=15, column=0)
###############################################################################

########### GET VALUES BUTTON ########################################


# Get the values from the entry and stored the values in the library
def get_values(widget, entered_values):
    for var_name, entry_widget in widget.items():
        value = entry_widget.get()
        if value is not None and value != "":
            entered_values[var_name] = value

    # Now, you can print the formatted values
    print("Formatted Entered Values:")
    try:
        ic(entered_values)
    except NameError:
        print(entered_values)



def get_custom_values(w, entered_values):
    for cus_label, cus_value in w.items():
        label = cus_label.get()
        value = cus_value.get()

        if label is not None and label != "":
            if value is not None and value != "":
                entered_values[label] = value

    # ic(entered_values)


def get_all_values():
    get_values(info_widgets, entered_values=info_value)
    get_values(entry_widgets, entered_values=entered_value)
    get_custom_values(cus_entry_widgets, entered_values=entered_value)


get_values_button = ttk.Button(
    default_fields_frame,
    text="Get Values",
    command=lambda: get_all_values(),
)
get_values_button.grid(row=len(variables), column=0)


############# CLEAR ALL BUTTON #############################


def clear_fields(widget, database=None):
    for key, value in widget.items():
        if isinstance(key, ttk.Entry):
            key.delete(0, "end")
        if isinstance(value, ttk.Entry):
            value.delete(0, "end")

    if database is not None:
        database.clear()


def clear_all_fields():
    clear_fields(entry_widgets, entered_value)
    clear_fields(cus_entry_widgets, entered_value)
    clear_json_file(filename)


clear_fields_button = ttk.Button(
    default_fields_frame, text="Clear Fields", command=clear_all_fields
)
clear_fields_button.grid(row=len(variables), column=1)

########### STORE ALL GUI DATA #######################


# Function to save the data as JSON
def save_data_as_json(data, filename):
    with open(filename, "w") as json_file:
        json.dump(data, json_file)


# Function to load data from JSON and populate tkinter Entry widgets
def load_data_from_json(filename):
    with open(filename, "r") as json_file:
        loaded_data = json.load(json_file)
        for key, value in loaded_data.items():
            if key in entry_widgets:
                entry_widgets[key].delete(0, "end")
                entry_widgets[key].insert(0, value)


def load_data_from_saved(loaded_data, widget):
    for key, value in loaded_data.items():
        if key in widget:
            widget[key].delete(0, "end")
            widget[key].insert(0, value)


def load_custom_data_from_saved(loaded_data, filter_variables, widget):
    filtered_data = {}
    for key, value in loaded_data.items():
        if key not in filter_variables:
            filtered_data[key] = value

    for idx, (key, value) in enumerate(filtered_data.items()):
        add_entry(cusfields_frame, cus_entry_widgets, key, value)

    ic(filtered_data)


# Example usage to save data as JSON (you can call this when the script exits)
window.protocol("WM_DELETE_WINDOW", lambda: on_closing())


# Define the on_closing function
def on_closing():
    # Saved all data in the same load
    all_data = {"info_value": info_value, "entered_value": entered_value}
    save_data_as_json(all_data, filename)
    # save_data_as_json(cus_entry_widgets, filename)
    window.destroy()


# Example usage to load data from JSON into Entry widgets (you can call this at the script's start)
load_data_from_saved(info_value, info_widgets)
load_data_from_saved(entered_value, entry_widgets)
load_custom_data_from_saved(entered_value, variables, cus_entry_widgets)


########### LOGIC ###########################################


def bulk_upload():
    headers = logic.create_headers(email=info_value["Email"], token=info_value["Token"])
    logic.bulk_ticket_upload(
        info_value["upload_file"],
        headers,
        entered_value,
        info_value["URL"],
    )


upload_button = ttk.Button(
    info_frame,
    text="Upload",
    command=lambda: bulk_upload(),
)
upload_button.grid(row=2, column=4, padx=2, pady=2)


#############################################################
window.mainloop()

# Remember to restore sys.stdout and sys.stderr when closing the application
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__