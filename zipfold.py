
import shutil, os

base = "C:/Users/You/Documents"
for folder in os.listdir(base):
    fpath = os.path.join(base, folder)
    if os.path.isdir(fpath):
        shutil.make_archive(fpath, "zip", fpath)
        print("Zipped:", folder)
