import xml.etree.ElementTree as ET
import json
from pathlib import Path

DATA_DIR = Path("data")
XML_FILE = DATA_DIR / "cameras_metashape.xml"
OUTPUT_JSON = DATA_DIR / "threejs_scene.json"

tree = ET.parse(XML_FILE)
root = tree.getroot()

cameras_out = []
cam_idx = 0

# Find all <camera> nodes
for cam in root.findall(".//camera"):
    label = cam.get("label")
    transform_el = cam.find("transform")

    # Skip unaligned cameras (no transform)
    if transform_el is None:
        continue

    # Parse the 4x4 transform matrix (16 numbers, row-major)
    vals = list(map(float, transform_el.text.split()))
    if len(vals) != 16:
        continue

    # Row-major: [r11 r12 r13 tx r21 r22 r23 ty r31 r32 r33 tz 0 0 0 1]
    r11, r12, r13, tx, \
    r21, r22, r23, ty, \
    r31, r32, r33, tz, \
    _,   _,   _,   _  = vals

    # Use the translation part as the camera center.
    # This is consistent with Metashape's exported point cloud coordinates.
    center = [tx, ty, tz]

    # For this project we do not need accurate rotations in the viewer,
    # so we can just store the rotation matrix as identity.
    rotation = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ]
    translation = [0.0, 0.0, 0.0]

    # Your image files are named like "<uuid>.JPG" in processed_images/
    image_file = f"{label}.JPG"

    cameras_out.append({
        "id": cam_idx,
        "center": center,
        "rotation": rotation,
        "translation": translation,
        "image_file": image_file,
    })
    cam_idx += 1

# Build final JSON structure
scene_cfg = {
    "pointcloud_file": "merged_room.ply",
    # Folder where your images are served from in the web server
    "images_base": "processed_images",
    "cameras": cameras_out,
}

OUTPUT_JSON.write_text(json.dumps(scene_cfg, indent=4), encoding="utf-8")
print(f"[OK] Wrote {OUTPUT_JSON} with {len(cameras_out)} cameras.")