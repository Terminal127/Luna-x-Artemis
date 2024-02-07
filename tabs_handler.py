import pyautogui
import time

def change_windows_global():
    pyautogui.keyDown("win")
    pyautogui.keyDown("tab")
    pyautogui.keyUp("win")
    pyautogui.keyUp("tab")
    # time.sleep(0.5)

    # pyautogui.press("right")
    # pyautogui.press("Enter")
    
# def change_widows_local():
#     pyautogui.keyDown("alt")
#     pyautogui.keyDown("tab")
#     pyautogui.keyUp("alt")
#     pyautogui.keyUp("tab")

def move_left():
    pyautogui.press("right")
    
def select():
    pyautogui.press("enter")
    

def main():
    change_windows_global()
    # n=1
    # while n < 10:
    #     change_widows_local()
    #     n = n+1

if __name__ == "__main__":
    main()
