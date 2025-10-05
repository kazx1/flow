
import os, shutil, pathlib 

space = pathlib.Path.home() / "Downloads" 
other_folder = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".webp"],
    "Docs": [".pdf", ".docx", ".txt"],
    "Archives": [".zip", ".rar", ".7z"],
    "Videos": [".mp4", ".mov", ".mkv"]
}

for file in space.iterdir():
    if file.is_file():
        for folder, exts in other_folder.items():
            if file.suffix.lower() in exts:
                target = space / folder
                target.mkdir(exist_ok=True)
                shutil.move(str(file), str(target / file.name))
                print(f"Moved {file.name} → {folder}")
