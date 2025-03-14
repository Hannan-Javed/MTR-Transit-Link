import os
import json

def update_keys(data):
    updated_data = {}
    for key, value in data.items():
        new_key = key
        if key.endswith("Po Lam"):
            new_key = key.replace("Po Lam", "Po Lam/LOHAS Park")
        if key.endswith("AsiaWorld"):
            new_key = key.replace("AsiaWorld", "AsiaWorld-Expo")
        if key.startswith("Line"):
            new_key = key.replace("Line", "Island Line", 1)
        if key.endswith("Lo Wu"):
            new_key = key.replace("Lo Wu", "Lo Wu/Lok Ma Chau", 1)
        updated_data[new_key] = value
    return updated_data

def filter_line_names(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            updated_data = update_keys(data)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(updated_data, file, ensure_ascii=False, indent=4)

