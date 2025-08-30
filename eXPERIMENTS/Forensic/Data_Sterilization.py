import os
import random
import shutil
import sys
import time
from pathlib import Path

# Import GUI components only when needed
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

def get_target_path(target_type):
    """Get target path via GUI dialog or command line input"""
    if GUI_AVAILABLE and target_type in ['file', 'dir']:
        root = tk.Tk()
        root.withdraw()  # Hide main window
        
        try:
            if target_type == 'file':
                path = filedialog.askopenfilename(
                    title="Select file to sterilize",
                    filetypes=[("All files", "*.*")]
                )
            else:  # directory
                path = filedialog.askdirectory(title="Select directory to sterilize")
            
            if not path:  # User cancelled
                print("No selection made. Exiting.")
                sys.exit(0)
            return path
        finally:
            root.destroy()
    else:
        # Fallback to command line input
        if target_type == 'file':
            return input("Enter file path: ")
        elif target_type == 'dir':
            return input("Enter directory path: ")
        else:  # disk or ssd
            path = input("Enter disk path (e.g., /dev/sdb): ")
            print(f"WARNING: You're about to sterilize {path} ({target_type})")
            print("This will permanently destroy all data on the device!")
            confirm = input("Type 'YES' to continue: ")
            if confirm != 'YES':
                print("Operation cancelled.")
                sys.exit(0)
            return path

def overwrite_file(file_path, passes=7):
    """Overwrite a single file with 7 passes"""
    try:
        file_size = os.path.getsize(file_path)
        patterns = [
            bytes([0x00] * file_size),  # Zero pattern
            bytes([0xFF] * file_size),  # One pattern
            os.urandom(file_size),      # Random pattern
        ]
        
        for pass_num in range(1, passes + 1):
            pattern = patterns[pass_num % 3]
            with open(file_path, 'r+b') as f:
                f.write(pattern)
                f.flush()
                os.fsync(f.fileno())
            print(f"Pass {pass_num}/{passes} completed")
            
        os.remove(file_path)
        print(f"✅ File sterilized: {file_path}")
    except Exception as e:
        print(f"❌ Error overwriting {file_path}: {e}")

def overwrite_directory(dir_path, passes=7):
    """Recursively overwrite all files in a directory"""
    for root, _, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            overwrite_file(file_path, passes)
    shutil.rmtree(dir_path)
    print(f"✅ Directory sterilized: {dir_path}")

def overwrite_disk(disk_path, passes=7, block_size=4096):
    """Overwrite entire disk with 7 passes"""
    try:
        disk_size = os.path.getsize(disk_path)
        patterns = [
            bytes([0x00] * block_size),  # Zero pattern
            bytes([0xFF] * block_size),  # One pattern
            os.urandom(block_size),      # Random pattern
            bytes([0x55] * block_size),  # 01010101 pattern
            bytes([0xAA] * block_size),  # 10101010 pattern
        ]
        
        for pass_num in range(1, passes + 1):
            print(f"Pass {pass_num}/{passes} on {disk_path}...")
            pattern = patterns[pass_num % 5]
            with open(disk_path, 'r+b') as disk:
                disk.seek(0)
                bytes_written = 0
                while bytes_written < disk_size:
                    disk.write(pattern)
                    bytes_written += block_size
                    if bytes_written % (1024 * 1024) == 0:  # Progress every 1MB
                        disk.flush()
                        os.fsync(disk.fileno())
                disk.flush()
                os.fsync(disk.fileno())
        print(f"✅ Disk sterilized: {disk_path}")
    except Exception as e:
        print(f"❌ Error overwriting disk {disk_path}: {e}")

def secure_erase_ssd(disk_path):
    """Use ATA Secure Erase for SSDs"""
    print(f"Attempting SSD Secure Erase on {disk_path}...")
    try:
        # Check if frozen
        frozen = os.system(f"hdparm -I {disk_path} | grep -q 'frozen'")
        if frozen == 0:
            print("⚠️ Disk is frozen. Try suspending/resuming system.")
            return
        
        # Set temporary password
        os.system(f"hdparm --user-master u --security-set-pass NULL {disk_path}")
        
        # Execute secure erase
        result = os.system(f"hdparm --user-master u --security-erase NULL {disk_path}")
        if result == 0:
            print("✅ SSD Secure Erase completed successfully.")
        else:
            print("❌ Secure Erase failed. Try manufacturer tools.")
    except Exception as e:
        print(f"❌ SSD Erase Error: {e}")

def main():
    # Get target type
    if len(sys.argv) > 1:
        target_type = sys.argv[1].lower()
    else:
        if GUI_AVAILABLE:
            root = tk.Tk()
            root.withdraw()
            target_type = messagebox.askquestion(
                "Select Target Type",
                "What do you want to sterilize?",
                icon='question',
                type='yesno',
                default='yes',
                detail='Yes: File/Folder\nNo: Disk/SSD'
            )
            root.destroy()
            target_type = 'file' if target_type == 'yes' else 'disk'
        else:
            target_type = input("Enter target type (file/dir/disk/ssd): ").lower()
    
    # Validate target type
    if target_type not in ['file', 'dir', 'disk', 'ssd']:
        print("❌ Invalid type. Use: file, dir, disk, ssd")
        sys.exit(1)
    
    # Get target path
    if len(sys.argv) > 2:
        target_path = sys.argv[2]
    else:
        target_path = get_target_path(target_type)
    
    # Get number of passes (default 7)
    passes = 7
    if len(sys.argv) > 3:
        try:
            passes = int(sys.argv[3])
        except ValueError:
            print("Invalid passes value. Using default (7)")
    
    # Final confirmation for dangerous operations
    if target_type in ['disk', 'ssd']:
        if GUI_AVAILABLE:
            root = tk.Tk()
            root.withdraw()
            confirm = messagebox.askyesno(
                "Final Confirmation",
                f"⚠️ WARNING: This will permanently destroy all data on:\n{target_path}\n\nContinue?",
                icon='warning'
            )
            root.destroy()
            if not confirm:
                print("Operation cancelled.")
                sys.exit(0)
        else:
            print(f"⚠️ WARNING: You're about to sterilize {target_path} ({target_type})")
            print("This will permanently destroy all data on the device!")
            confirm = input("Type 'YES' to continue: ")
            if confirm != 'YES':
                print("Operation cancelled.")
                sys.exit(0)
    
    # Execute sterilization
    if target_type == "file":
        overwrite_file(target_path, passes)
    elif target_type == "dir":
        overwrite_directory(target_path, passes)
    elif target_type == "disk":
        overwrite_disk(target_path, passes)
    elif target_type == "ssd":
        secure_erase_ssd(target_path)

if __name__ == "__main__":
    main()
