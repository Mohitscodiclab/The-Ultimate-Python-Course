

# System Protector - USB Key Authentication

## Overview
This Python script provides an additional layer of security for your Windows computer by requiring a specific USB drive to be connected during system startup. If the authorized USB isn't detected within the specified time limit, the system will automatically shut down.

## Features
- Requires a specific USB drive (by volume name) to be connected
- Provides visual warnings and countdown timer
- Automatically shuts down the system if USB isn't detected
- Can be configured to run at system startup

## Prerequisites
- Windows operating system
- Python 3.x installed
- Administrator privileges to set up startup tasks

## Setup Instructions

### 1. Prepare Your USB Drive
- Format your USB drive (NTFS or FAT32)
- Rename the USB volume to "LUCIFER" (or modify the script with your preferred name)
  - To rename: Right-click the USB drive in File Explorer > Select "Rename" > Enter the name

### 2. Configure the Script
- Open the Python script in a text editor
- Modify these variables if needed:
  ```python
  allowed_usb_name = "LUCIFER"  # Change to your USB volume name
  timeout_seconds = 20          # Time before shutdown (in seconds)
  ```

### 3. Create a Batch File
1. Create a new text file
2. Add the following content:
   ```batch
   @echo off
   python "C:\path\to\your\script.py"
   ```
   (Replace `C:\path\to\your\script.py` with the actual path to your Python script)
3. Save the file with a `.bat` extension (e.g., `usb_protector.bat`)

### 4. Set Up Automatic Startup
1. Press `Win + R`, type `shell:startup`, and press Enter
2. Copy your batch file to this startup folder
3. Alternatively, use Task Scheduler:
   - Open Task Scheduler
   - Create a new task that runs at system startup
   - Set the action to run your batch file
   - Configure to run with highest privileges

## How It Works
1. When your computer starts, the script automatically runs
2. It checks for the presence of the authorized USB drive
3. If the USB is detected:
   - Shows "ACCESS GRANTED" message
   - System continues normal startup
4. If the USB is not detected:
   - Shows warning message with countdown timer
   - Waits for the specified time (default: 20 seconds)
   - If USB is inserted during countdown, shutdown is cancelled
   - If USB isn't inserted, system initiates shutdown

## Troubleshooting
- **Shutdown initiated by mistake**: Press `Win + R`, type `shutdown /a`, and press Enter to abort
- **USB not recognized**: Ensure the volume name exactly matches (case-sensitive)
- **Script doesn't run at startup**: Verify batch file location and permissions
- **Python not found**: Ensure Python is installed and added to PATH

## Important Notes
- This script is designed as an additional security layer, not a complete security solution
- Always keep a backup of your files
- Test the system thoroughly before relying on it
- To temporarily disable protection, remove the batch file from the startup folder
- The script only checks at startup - removing the USB after startup won't trigger shutdown

## Customization Options
You can modify these variables in the script:
- `allowed_usb_name`: Change to match your USB volume name
- `timeout_seconds`: Adjust the countdown duration
- Uncomment alternative actions in the script:
  - `#os.system("rundll32.exe user32.dll,LockWorkStation")` to lock workstation instead of shutdown
  - `#os.system("netsh interface set interface Wi-Fi disable")` to disable Wi-Fi

## Disclaimer
This script is provided as-is without warranty. Use at your own risk. The creators are not responsible for any data loss or system damage that may occur.

## Support
For issues or questions, refer to the script comments or seek assistance from a qualified technician.
