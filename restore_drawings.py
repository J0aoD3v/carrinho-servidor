#!/usr/bin/env python3
"""
Script to restore original Excalidraw format from optimized files.
Use this if you need to revert the performance optimizations.
"""

import os
import re
import json
from pathlib import Path

def restore_drawings(repo_path="."):
    repo_path = Path(repo_path)
    drawings_dir = repo_path / '.excalidraw'
    index_file = drawings_dir / 'index.json'
    
    if not index_file.exists():
        print("No optimization index found. Nothing to restore.")
        return
    
    # Load index
    with open(index_file, 'r') as f:
        index_data = json.load(f)
    
    for file_path, drawing_info in index_data.items():
        full_path = repo_path / file_path
        drawing_file = repo_path / drawing_info['drawing_file']
        
        if not full_path.exists() or not drawing_file.exists():
            print(f"Skipping {file_path} - files not found")
            continue
        
        # Read current content and drawing data
        with open(full_path, 'r') as f:
            content = f.read()
        
        with open(drawing_file, 'r') as f:
            drawing_data = f.read()
        
        # Replace reference with original drawing data
        hash_ref = drawing_info['drawing_hash']
        pattern = f'(```compressed-json\\n)<!-- DRAWING_REFERENCE: {hash_ref} -->(\\n```)'
        replacement = f'\\1{drawing_data}\\2'
        
        restored_content = re.sub(pattern, replacement, content)
        
        # Remove lazy loading comments
        restored_content = re.sub(r'<!-- EXCALIDRAW_LAZY_LOADER -->.*?(?=\n[^\s<])', '', restored_content, flags=re.DOTALL)
        
        # Write restored content
        with open(full_path, 'w') as f:
            f.write(restored_content)
        
        print(f"Restored: {file_path}")
    
    print("\nRestoration complete!")
    print("You can now delete the .excalidraw directory if desired.")

if __name__ == "__main__":
    restore_drawings()
