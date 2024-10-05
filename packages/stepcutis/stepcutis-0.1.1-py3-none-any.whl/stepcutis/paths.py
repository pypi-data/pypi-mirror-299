import sys
import os

def setup_paths():
    project_root = os.path.dirname(os.path.abspath(__file__))
    paths_to_add = [
        os.path.join(project_root, 'projectpackages'),
        os.path.join(project_root, 'projectpackages', 'LakeOCR'),
        os.path.join(project_root, 'GOT-OCR2_0'),
    ]
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.append(path)

if __name__ == "__main__":
    setup_paths()