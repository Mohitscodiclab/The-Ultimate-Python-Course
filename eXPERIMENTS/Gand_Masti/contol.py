# pip install pyautogui

import pyautogui as s
import time

s.press("win")
time.sleep(1.5)

s.write("notepad", interval=0.2)
s.press("enter")
time.sleep(1)

s.write("Sunn Bahen ke laude ", interval=0.2)
s.press("enter")
s.write("This is a test.", interval=0.2)
s.press("enter")

s.write("Teri Ma chod dunga", interval=0.2)
s.press("enter")
s.write("Bakchodi mt kr Laude", interval=0.2)
s.press("enter")

s.hotkey("ctrl", "s")
time.sleep(1)
s.write("new1.txt", interval=0.2)
s.press("enter")