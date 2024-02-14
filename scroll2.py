import pyautogui
import time
import keyboard

total_scrolled = 0
while True:
    pyautogui.scroll(-20)
    total_scrolled += 20
    time.sleep(0.01)
    
    #Ve a distancia que foi "descida"
    if total_scrolled > 1000:
        #print('Fim da pagina')
        pyautogui.scroll(16000)
        time.sleep(5)
        total_scrolled = 0
        
    elif keyboard.is_pressed('esc'):
        print('Pausa')
        break
