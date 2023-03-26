with open("get_links.py", "r") as get_links_file:
    exec(get_links_file.read())
print("Finished fetching links...")
with open("get_data.py", "r") as get_data_file:
    exec(get_data_file.read())
print("Finished fetching data...")
with open("json_to_csv.py", "r") as json_to_csv_file:
    exec(json_to_csv_file.read())
print("Done!")