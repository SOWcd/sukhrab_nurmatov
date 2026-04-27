import os

os.makedirs('practice_root/sub_folder/target', exist_ok=True)

files_and_dirs = os.listdir('.')
print(files_and_dirs)

current_path = os.getcwd()
print(current_path)

if os.path.exists('practice_root'):
    for root, dirs, files in os.walk('practice_root'):
        print(f"Directory: {root}")
        for d in dirs:
            print(f"  Folder: {d}")
        for f in files:
            print(f"  File: {f}")