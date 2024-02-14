import pyautogui
import time

def zoom_out():
    number_of_times = 4
    time.sleep(10) # Espera 5s
    for i in range(number_of_times):
        pyautogui.hotkey('ctrl', '-')
    
    print(f"Zoomed out {number_of_times} times.")
    
# Example usage: zoom_out_by_fixed_number_of_times(3)
zoom_out()