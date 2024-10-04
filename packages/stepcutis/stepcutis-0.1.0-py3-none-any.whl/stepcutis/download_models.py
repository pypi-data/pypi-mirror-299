import os
import subprocess
import sys

def download():
    try:
        # Install git-lfs
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'git-lfs'])
        subprocess.check_call(['git-lfs', 'install'])
        
        # Clone the model repo
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_dir = os.path.join(current_dir, 'GOT-OCR2_0')
        if not os.path.exists(model_dir):
            subprocess.check_call(['git', 'clone', 'https://huggingface.co/stepfun-ai/GOT-OCR2_0', model_dir])
            print("Model files downloaded successfully.")
        else:
            print("Model directory already exists. Skipping download.")
    except subprocess.CalledProcessError as e:
        print(f"Error during model download: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download()