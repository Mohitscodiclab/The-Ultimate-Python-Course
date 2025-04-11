


import os
import ctypes
import time

# Set your USB's volume name here
allowed_usb_name = "LUCIFER"  # Replace with your USB's volume name
timeout_seconds = 20 # Time before shutdown

# Function to check if the USB is connected
def is_usb_connected():
    drives = os.popen("wmic logicaldisk get name, volumename").read()
    return allowed_usb_name in drives

# If USB is not connected initially
if not is_usb_connected():
    # Show warning popup
    ctypes.windll.user32.MessageBoxW(
        0,
        f"⚠️ Security Alert:\n\nAuthorized USB not detected.\nYou have {timeout_seconds} seconds to insert the USB or the system will shut down.",
        "ACCESS DENIED",
        0x30  # Warning icon
    )

    # Countdown loop: check every second
    for i in range(timeout_seconds):
        print(f"Waiting for USB... {timeout_seconds - i} seconds remaining")
        time.sleep(1)
        if is_usb_connected():
            # USB inserted during countdown — cancel shutdown
            ctypes.windll.user32.MessageBoxW(
                0,
                "✅ USB key has been inserted.\nShutdown cancelled.",
                "ACCESS GRANTED",
                0x40
            )
            os.system("shutdown /a")  # Abort any scheduled shutdown (just in case)
            break
    else:
        # If USB not found after waiting
        os.system("shutdown /s /t 20")  # Shutdown in 20 seconds (final warning)
        #os.system("rundll32.exe user32.dll,LockWorkStation")
    #os.system("netsh interface set interface Wi-Fi disable")
else:
    # USB was already connected — show access granted
    ctypes.windll.user32.MessageBoxW(
        0,
        "✅ USB key detected.\nACCESS GRANTED.",
        "Security Check",
        0x40
    )





# Note: Create a batch file to run this script on startup.
# when ever you turn on the pc this will automaticly run and check for the usb key.
# you have only 20 seconds to insert the usb key or the pc will shutdown.
# To create a batch file Read the README.md file properly and follow the instructions.