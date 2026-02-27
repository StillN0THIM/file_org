import cv2
import os
import numpy as np
from sklearn.cluster import KMeans
import shutil
import json

IMAGE_FOLDER = r"C:\Users\Himanshu\Downloads\sorted\Images"
OUTPUT_FOLDER = r"C:\Users\Himanshu\Downloads\sorted\Images_clustered"
N_CLUSTERS = 25
LOG_FILE = "undo_log.json"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

orb = cv2.ORB_create()
features = []
image_names = []

for file in os.listdir(IMAGE_FOLDER):
    path = os.path.join(IMAGE_FOLDER, file)
    img = cv2.imread(path, 0)

    if img is None:
        continue

    kp, des = orb.detectAndCompute(img, None)

    if des is not None:
        features.append(des.mean(axis=0))
        image_names.append(file)

features = np.array(features)

kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=0)
labels = kmeans.fit_predict(features)

# Create cluster folders
for i in range(N_CLUSTERS):
    os.makedirs(os.path.join(OUTPUT_FOLDER, f"cluster_{i}"), exist_ok=True)

undo_log = {}

# Move images + log original location
for name, label in zip(image_names, labels):
    src = os.path.join(IMAGE_FOLDER, name)
    dst = os.path.join(OUTPUT_FOLDER, f"cluster_{label}", name)
    shutil.move(src, dst)
    undo_log[dst] = src
    print(f"{name}  -->  cluster_{label}")

# Save undo log
with open(LOG_FILE, "w") as f:
    json.dump(undo_log, f, indent=4)

print("\nClustering done.")
print("Run undo_clusters.py to undo.")