import csv
import json
from pathlib import Path

DATA_DIR = Path("data")
CSV_FILE = DATA_DIR / "cameras_metashape.csv"
OUTPUT_JSON = DATA_DIR / "threejs_scene.json"

# Inspect the first line of your CSV in a text editor to confirm these names.
# Metashape often uses something like: "Label,X,Y,Z,..." or "photo,x,y,z,..."
CAMERA_NAME_COL = "label"   # or "Photo" or "image" etc.
X_COL = "x"
Y_COL = "y"
Z_COL = "z"

cameras = []
with CSV_FILE.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader):
        name = row[CAMERA_NAME_COL]
        x = float(row[X_COL])
        y = float(row[Y_COL])
        z = float(row[Z_COL])

        # Use the CSV filename directly as the image filename. If your Three.js
        # viewer expects images in processed_images/, just keep the name here
        # and ensure the files exist in that folder.
        image_file = name

        cameras.append({
            "id": idx,
            # Metashape coordinates for the camera center
            "center": [x, y, z],
            # We don’t actually need rotation/translation for your viewer to work;
            # set them to identity / zero for simplicity.
            "rotation": [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ],
            "translation": [0.0, 0.0, 0.0],
            "image_file": image_file,
        })

scene_cfg = {
    "pointcloud_file": "merged_room.ply",
    # Folder from which your viewer will serve images.
    # Change to "images" if that’s where you host them; or "processed_images".
    "images_base": "processed_images",
    "cameras": cameras,
}

with OUTPUT_JSON.open("w", encoding="utf-8") as f:
    json.dump(scene_cfg, f, indent=4)

print(f"Wrote {OUTPUT_JSON} with {len(cameras)} cameras.")