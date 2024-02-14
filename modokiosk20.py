import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# Importar o submódulo By para localizar os elementos da página
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading
import pyautogui
import keyboard
import ctypes

ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 )


# Criar o root
root = tk.Tk()

# Define um índice para selecionar o próximo texto
indiceTextos = 0
indiceSites = 0

#Define o máximo pixels de scroll
max_scroll = 10000
#Define uma variável que armaneza quantos pixels foi dado de scroll
total_scrolled = 0

def login(driver):
    # Abrir o site de login
    driver.get("https://opsvision.corp.wabtec.com/connect/")

    # Aguardar 2 segundos para a página carregar
    time.sleep(2)

    # Localizar o campo de usuário pelo atributo name
    user_field = driver.find_element(By.NAME, "username")

    # Digitar o usuário no campo
    user_field.send_keys("shopfloorctg")

    # Localizar o campo de senha pelo atributo name
    password_field = driver.find_element(By.NAME, "password")

    # Digitar a senha no campo
    password_field.send_keys("Contagem*1")

    # Localizar o botão de login pelo atributo type e value
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Sign In']")

    # Clicar no botão de login
    login_button.click()

    # Aguardar 2 segundos para o login ser efetuado
    time.sleep(5)

def auto_scroll(root, driver):
    global max_scroll
    global total_scrolled

    #total_scrolled = 0
    while True:
        pyautogui.scroll(-20)
        total_scrolled += 20
        time.sleep(0.001)
        
        #Ve a distancia que foi "descida"
        if total_scrolled > 3000:
            #print('Fim da pagina')
            pyautogui.scroll(3000)
            time.sleep(5)
            total_scrolled = 0
            
        elif keyboard.is_pressed('esc'):
            print('Pausa')
            break
        

def create_popup_title(textos, driver, label):
    """
    Creates a popup title element and adds it to the page.

    Args:
        title: The title to display in the popup.
    """
    # Usa a variável global indice
    global indiceTextos
    # Incrementa o indice em 1, usando o módulo pelo tamanho da lista para evitar estouro
    indiceTextos = (indiceTextos + 1) % len(textos)
    # Seleciona o próximo texto da lista
    proximo_texto = textos[indiceTextos]
    # Altera o texto do label usando o método config
    label.config(text=proximo_texto)    

def switch_page_with_popup_title(sites, textos, driver, label):
    """
    Navigates to a different page and displays a popup title in the top center.

    Args:
        url: The URL of the page to navigate to.
        title: The title to display in the popup.
    """
    # Usa a variável global indice
    global indiceSites
    global chrome_pid

    # Incrementa o indice em 1, usando o módulo pelo tamanho da lista para evitar estouro
    indiceSites = (indiceSites + 1) % len(sites)

    # Seleciona o próximo texto da lista
    proximo_site = sites[indiceSites]
    
    # Navigate to the specified URL
    driver.get(proximo_site)

    # Create and display the popup title
    create_popup_title(textos, driver, label)

    # Add a delay to give the page time to render
    #time.sleep(1)

def navigate(root, driver, sites, textos, label):
    global max_scroll
    global total_scrolled
    
    while True:
        #for site in sites:
        switch_page_with_popup_title(sites, textos, driver, label)
        total_scrolled = max_scroll
        time.sleep(30)
        print(1)
        switch_page_with_popup_title(sites, textos, driver, label)
        total_scrolled = max_scroll
        time.sleep(30)
        print(2)

def update():
    # atualiza interface Tkinter
    root.after(1000, update)

def main():
    
    # Create a new Chrome driver instance
    chrome_options = Options()
    chrome_options.add_argument("--kiosk")
    driver = webdriver.Chrome(options=chrome_options)

    login(driver)

    # Define a geometria para centralizar e posicionar no topo
    print("login done")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = screen_width
    height = 50
    x = (screen_width/2) - (width/2)
    y = 0
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

    # Remove as bordas
    root.overrideredirect(True)

    # Define sempre no topo
    root.attributes("-topmost", True)

    label = tk.Label(root, text="OPSVISION", justify="center", font=("Arial", 30))
    label.pack(expand=True)

    # Define uma lista de textos possíveis
    textos = ["Escalate GCM - MANUTENÇÃO",
              "Escalate GCT - MANUTENÇÃO"
              ]

    sites = ["https://opsvision.corp.wabtec.com/connect/gcm/escalate/dashboard?sort=type&view=summary%20view&type=aponte%20o%20risco%20-%20seguran%C3%A7a%20pessoal%20ou%20ambiental&type=m%C3%A1quina%20quebrada&type=parada%20de%20trabalho%20-%20stop%20work&type=pe%C3%A7a%20danificada%20na%20manufatura%C2%A0&type=preciso%20de%20empilhadeira",
             "https://opsvision.corp.wabtec.com/connect/gct/escalate/dashboard?sort=newest%20first&view=summary%20view&type=aponte%20o%20risco%20-%20seguran%C3%A7a%20pessoal%20ou%20ambiental&type=m%C3%A1quina%20quebrada&type=parada%20de%20trabalho%20-%20stop%20work&type=pe%C3%A7a%20danificada%20na%20manufatura%20&type=preciso%20de%20empilhadeira"
            ]
    
    # Chama a função pela primeira vez
    #create_popup_title(textos, driver, label)

    # Start the navigation thread
    thread = threading.Thread(target=navigate, args=[root, driver, sites, textos, label])
    thread.start()

    threadScroll = threading.Thread(target=auto_scroll, args=[root, driver])
    threadScroll.start() 

    # Start the update thread
    update()

    root.withdraw()  
    #time.sleep(1)
    root.deiconify()
    
    # Start the Tkinter main loop
    root.mainloop()

    # Quit the Chrome driver
    driver.quit()

    thread.join()
    threadScroll.join()

if __name__ == "__main__":
    main()
