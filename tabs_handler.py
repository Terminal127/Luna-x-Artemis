import pyautogui
import time

def open_tabs():
    pyautogui.keyDown("win")
    pyautogui.keyDown("tab")
    pyautogui.keyUp("win")
    pyautogui.keyUp("tab")

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
    fast_tabs()
    time.sleep(1)
    fast_tabs()

if __name__ == "__main__":
    main()
