import tkinter as tk
from tkinter import ttk
import kolimacja
import inklinacja
import wsp_zalamania
import popr_atmosfer
import roznica_łuk_cieciwa
import portrs232

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

    tab_wsp_zalamania = ttk.Frame(notebook)
    notebook.add(tab_wsp_zalamania, text="Współczynnik załamania światła")
    wsp_zalamania.init_ui(tab_wsp_zalamania)

    tab_popr_atmosfer = ttk.Frame(notebook)
    notebook.add(tab_popr_atmosfer, text="Obliczanie poprawki atmosferycznej")
    popr_atmosfer.init_ui(tab_popr_atmosfer)

    tab_roznica_luk_cieciwa = ttk.Frame(notebook)
    notebook.add(tab_roznica_luk_cieciwa, text="Różnica między cięciwą a łukiem")
    roznica_łuk_cieciwa.init_ui(tab_roznica_luk_cieciwa)

    tab_portrs232 = ttk.Frame(notebook)
    notebook.add(tab_portrs232, text="Import danych z portu szeregowego")
    portrs232.init_ui(tab_portrs232)
    root.mainloop()

if __name__ == "__main__":
    main()