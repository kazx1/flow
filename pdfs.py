#!/usr/bin/env python3

"""
Usage:
  python merge_pdfs.py input1.pdf input2.pdf [input3.pdf ...] output.pdf
  python merge_pdfs.py /path/to/folder output.pdf
  python merge_pdfs.py --recursive /path/to/folder output.pdf
"""

import argparse 
import sys
from pathlib import Path
from PyPDF2 import PdfMerger

def gather_pdfs(paths, recursive=False):
    pdfs = []
    for p in paths:
        path = Path(p)
        if path.is_file() and path.suffix.lower() == ".pdf":
            pdfs.append(path)
        elif path.is_dir(): #if its a folder do:
            it = path.rglob("*.pdf") if recursive else path.glob("*.pdf") 
            pdfs.extend(sorted(it))
        else:
            print(f"⚠️  Skipping: {path}") 
    pdfs = sorted(set(pdfs), key=lambda x: x.name.lower())
    return pdfs
  
def merge_pdfs(files, output):
    merger = PdfMerger(strict=False)
    for f in files:
        try: 
            merger.append(str(f))
            print(f"  ✓ Added {f}")
        except Exception as e:
            print(f"  ⚠️  Skipped {f}: {e}")
    with open(output, "wb") as fh: 
        merger.write(fh) 
    merger.close() 
    print(f"\n✅ Merged {len(files)} file(s) → {output}") 

def main(): 
    ap = argparse.ArgumentParser(description="Merge multiple PDF files into one.")
    ap.add_argument("inputs", nargs="+", help="PDF files or folders; last arg can be output file")
    ap.add_argument("--recursive", action="store_true", help="Search folders recursively")
    args = ap.parse_args()

    *ins, last = args.inputs
    if last.lower().endswith(".pdf"):
        output = Path(last).resolve()
        in_paths = ins
    else:
        output = Path("merged.pdf").resolve()
        in_paths = args.inputs

    pdfs = gather_pdfs(in_paths, recursive=args.recursive)
    if not pdfs: 
        print("No PDF files found.")
        sys.exit(1)

    merge_pdfs(pdfs, output)

if __name__ == "__main__":
    main()
