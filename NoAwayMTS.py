import pyautogui
import math
import time
import keyboard

def draw_circle_around_center():
    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2
    num_points = 20
    angular_step = (2 * math.pi) / num_points
    radius = 200
    
    # centraliza o cursor
    pyautogui.moveTo(center_x, center_y, duration=0.5)
    
    while True:
        for i in range(num_points + 1):
            angle = i * angular_step
            x = int(center_x + radius * math.sin(angle))
            y = int(center_y + radius * math.cos(angle))
            pyautogui.moveTo(x, y, duration=0.2)
            time.sleep(0.001)  # suavidade da transição
            
            # pausa no esc
            if keyboard.is_pressed("esc"):
                print("Parou tudoooo")
                return

if __name__ == "__main__":
    try:
        draw_circle_around_center()
    except KeyboardInterrupt:
        print(" Continua trabalhando... ;) ")
