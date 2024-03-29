import subprocess
import shutil
import os

def main():
    out_dir=r'dist/dict_data'
    if os.path.exists(os.path.dirname(out_dir)):
        shutil.rmtree(os.path.dirname(out_dir))
    shutil.copytree('dict_data',out_dir)

    result = subprocess.run(['pyinstaller', '--onefile',  'App.py'], capture_output=True, text=True)
    print(result.stdout)
if __name__ == "__main__":
    main()