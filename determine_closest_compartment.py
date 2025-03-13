import os
import json
from pathlib import Path

def process_exit_and_station_data(exits_folder, stations_folder, output_folder):
    """
    Processes exit and station data to determine the closest compartment (front, middle, or back)
    for each exit in the corresponding station files. The results are saved as separate files
    for each station in the specified output folder.

    Args:
        exits_folder (str): Path to the folder containing exit coordinate files.
        stations_folder (str): Path to the folder containing station data files.
        output_folder (str): Path to the folder where output files will be saved.
    """

    # Ensure the output folder exists
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Function to determine the closest train compartment for an exit
    def get_closest_compartment(exit_x, compartments):
        min_distance = float('inf')
        closest = None

        for comp, x_coord in compartments.items():
            distance = abs(exit_x - x_coord)
            if distance < min_distance:
                min_distance = distance
                closest = comp

        if closest == "0":
            return "Front"
        elif closest == "1":
            return "Middle"
        elif closest == "2":
            return "Back"

    # Process each file in the exits folder
    for exit_file_name in os.listdir(exits_folder):
        if exit_file_name.endswith(".json"):
            exit_file_path = os.path.join(exits_folder, exit_file_name)
            station_file_path = os.path.join(stations_folder, exit_file_name)
            
            # Skip if the corresponding station file does not exist
            if not os.path.exists(station_file_path):
                print(f"Station file missing for {exit_file_name}. Skipping.")
                continue

            # Load the exits and station data
            with open(exit_file_path, "r") as exit_file:
                exits_data = json.load(exit_file)
            
            with open(station_file_path, "r") as station_file:
                stations_data = json.load(station_file)

            # Prepare the results
            results = {}
            for line, compartments in stations_data.items():
                line_result = {}

                for exit_name, exit_coords in exits_data.items():
                    exit_x = exit_coords[0]  # Only x-axis is relevant
                    closest = get_closest_compartment(exit_x, compartments)
                    line_result[exit_name] = closest

                results[line] = line_result
            
            # Sort the results by keys before writing
            results = dict(sorted(results.items()))
            # Write the results to a separate file in the output folder
            output_file_path = os.path.join(output_folder, exit_file_name)
            with open(output_file_path, "w") as output_file:
                json.dump(results, output_file, indent=4)

            print(f"Processed {exit_file_name} and saved results to {output_file_path}.")
