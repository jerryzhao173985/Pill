#!/usr/bin/env python3
"""
Setup script to prepare the mock environment for Pill development
"""

import os
import sys
import shutil

def ensure_file_exists(filename, content):
    """Ensure a file exists with the given content"""
    if not os.path.exists(filename):
        print(f"Creating {filename}")
        with open(filename, "w") as f:
            f.write(content)
    else:
        print(f"File {filename} already exists")

def create_layermap():
    """Create a basic layermap file"""
    content = """
# Layer definition format: layer_name layer_number datatype
diff 65 20
poly 66 20
li1  67 20
met1 68 20
licon1 66 44
mcon 67 44
"""
    ensure_file_exists("mytech.layermap", content)

def backup_original_files():
    """Backup original files before modifying them"""
    files_to_backup = ["entry.py", "runtime.py"]
    for file in files_to_backup:
        if os.path.exists(file) and not os.path.exists(file + ".original"):
            print(f"Backing up {file} to {file}.original")
            shutil.copy2(file, file + ".original")

def setup_mock_environment():
    """Set up the mock environment"""
    print("Setting up mock environment for Pill development")
    
    # Create necessary directories
    os.makedirs("mockup", exist_ok=True)
    
    # Create layermap file
    create_layermap()
    
    # Backup original files
    backup_original_files()
    
    # Create test script
    test_script = """
proc(myTestProc()
    let((cv)
        cv = ddGetObj("mytech" "test_cell")
        rodCreateRect("diff" 1.0 2.0)
    )
)
"""
    ensure_file_exists("mockup/test.il", test_script)
    
    print("\nMock environment setup complete!")
    print("You can now run 'python entry.py' to test the mock environment")

if __name__ == "__main__":
    setup_mock_environment() 