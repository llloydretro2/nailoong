import os
import re

path = r"C:\Users\15532\OneDrive\Code\python\symmetry\video"

for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".mp4"):
            print(file)
            new_name = str(int(re.search(r"\d+", file).group())) + ".mp4"
            print(new_name)
            os.rename(os.path.join(root, file), os.path.join(root, new_name))