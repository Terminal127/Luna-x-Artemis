import pyautogui
import time
import os

def open_tabs():
    pyautogui.keyDown("win")
    pyautogui.keyDown("tab")
    pyautogui.keyUp("win")
    pyautogui.keyUp("tab")

def lockscreen():
    os.system("rundll32.exe user32.dll,LockWorkStation")
    
def move_left():
    pyautogui.press("right")
    
def select():
    pyautogui.press("enter")
    
def fast_tabs():
    pyautogui.keyDown("alt")
    pyautogui.keyDown("tab")
    pyautogui.keyUp("alt")
    pyautogui.keyUp("tab")
    
      

def main():
    
    lockscreen()

if __name__ == "__main__":
    main()
