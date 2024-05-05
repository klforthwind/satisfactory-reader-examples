"""Script to find mam data hopefully."""

import sys
import csv

from satisfactory_save_reader.save_reader import SaveReader

# File location variables for reading
SAVE_FILE = sys.argv[1]


def get_key(recipe_loc):
    """Get recipe from recipe location."""
    return recipe_loc.split("Schematic_")[1].split(".")[0]


save_data = SaveReader(f"{SAVE_FILE}")

recipes = {}
with open("recipes.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    recipes = {row[0]: row[1] for row in reader}

data = {}
objects = save_data.get_objects()
for obj_name, obj in objects.items():
    if "ResearchManager" not in obj_name:
        continue

    props = obj["properties"]
    for item in props:
        if item["name"] == "mSavedOngoingResearch":
            pending_rewards = item["value"]["values"][0][0]["value"]["values"][2]
            research_loc = pending_rewards["value"]["values"]

            recipe_list = []
            for r in research_loc:
                name = r["pathName"]
                recipe_list.append(recipes.get(get_key(name), name))

            data["recipes"] = recipe_list

print(data)
