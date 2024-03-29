import subprocess
import shutil
import os

def main():
    result = subprocess.run(['pyinstaller', '--onefile','--windowed',  'App.py'], capture_output=True, text=True)
    print(result.stdout)
if __name__ == "__main__":
    main()
