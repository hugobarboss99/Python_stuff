import tkinter as tk

# Cria janela
root = tk.Tk()
root.title("Header Popup")
root.attributes("-topmost", True)

# Adiciona label na janela
label = tk.Label(root, text="This is a header popup!")
label.pack()

root.mainloop()
