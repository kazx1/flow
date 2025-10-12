
import os, sys 
from PIL import Image

folder = sys.argv[1] if len(sys.argv)>1 else "." 
max_side = int(os.getenv("MAX_SIDE","1600")) 
outdir = os.getenv("OUT","resized") 
os.makedirs(outdir, exist_ok=True) 

for name in os.listdir(folder):
    if name.lower().endswith((".jpg",".jpeg",".png")):
        p = os.path.join(folder, name)
        with Image.open(p) as im:
            im.thumbnail((max_side, max_side))
            savep = os.path.join(outdir, os.path.splitext(name)[0]+".jpg")
            im.convert("RGB").save(savep, "JPEG", optimize=True, quality=85)
            print("→", savep)
