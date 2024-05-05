"""Script to find mam data hopefully."""

import os
import sys
import csv
import glob
import time

from satisfactory_save_reader.save_reader import SaveReader

# File location variables for reading
SAVE_FILE_DIR = sys.argv[1]


def get_key(recipe_loc):
    """Get recipe from recipe location."""
    return recipe_loc.split("Schematic_")[1].split(".")[0]


def find_latest_save_file(directory):
    """Find the latest save file in the given directory."""
    save_files = glob.glob(os.path.join(directory, "*.sav"))
    if not save_files:
        raise FileNotFoundError("No save files found in the specified directory.")
    return max(save_files, key=os.path.getctime)


recipes = {}
with open("recipes.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    recipes = {row[0]: row[1] for row in reader}


while True:
    try:
        save_file = find_latest_save_file(SAVE_FILE_DIR)
        save_data = SaveReader(f"{save_file}")

        data = {}
        objects = save_data.get_objects()
        for obj_name, obj in objects.items():
            if "ResearchManager" not in obj_name:
                continue

            props = obj["properties"]
            for item in props:
                if item["name"] == "mSavedOngoingResearch":
                    pending_rewards = item["value"]["values"][0][0]["value"]["values"][
                        2
                    ]
                    research_loc = pending_rewards["value"]["values"]

                    recipe_list = []
                    for r in research_loc:
                        name = r["pathName"]
                        recipe_list.append(recipes.get(get_key(name), name))

                    data["recipes"] = recipe_list

        print(data)
        time.sleep(5)
    except FileNotFoundError as e:
        print(e)
