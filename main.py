import tkinter as tk
from tkinter import ttk
import kolimacja
import inklinacja

def main():
    root = tk.Tk()
    root.title("Kalkulator Geodezyjny")
    root.geometry("800x600")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')


    tab_kolimacja = ttk.Frame(notebook)
    notebook.add(tab_kolimacja, text="Kolimacja")
    kolimacja.init_ui(tab_kolimacja)


    tab_inklinacja = ttk.Frame(notebook)
    notebook.add(tab_inklinacja, text="Inklinacja (Wysoki Cel)")
    inklinacja.init_ui(tab_inklinacja)

    root.mainloop()

if __name__ == "__main__":
    main()