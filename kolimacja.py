import tkinter as tk
from tkinter import ttk
from math import sqrt

measurements = []


entry_left = None
entry_right = None
tabela = None
label_wynik = None


def calc_c():
    c_result = []
    if len(measurements) <= 1:
        return "Brak danych", "Brak danych"

    for h1, h2 in measurements:
        if h1 < 200:
            c = (h2 - (h1 + 200)) / 2
        else:
            c = (h2 - (h1 - 200)) / 2
        c_result.append(c)

    c_average = sum(c_result) / len(c_result)

    sum_v = 0
    for c in c_result:
        v = c - c_average
        v = pow(v, 2)
        sum_v += v

    c_error = sqrt(sum_v / (len(c_result) * (len(c_result) - 1)))

    return round(c_average, 4), round(c_error, 4)


def fetch_and_add():
    try:
        h1 = float(entry_left.get())
        h2 = float(entry_right.get())
        h1_h2 = (h1, h2)

        measurements.append(h1_h2)
        tabela.insert('', 'end', values=h1_h2)


        entry_left.delete(0, tk.END)
        entry_right.delete(0, tk.END)
    except ValueError:
        label_wynik.config(text="Błąd: Wprowadź poprawne liczby!")

def clear_data():
    global measurements
    measurements = []
    for item in tabela.get_children():
        tabela.delete(item)
    label_wynik.config(text="Dane wyczyszczone.")


def show_result():
    average, error = calc_c()
    if average == "Brak danych":
        label_wynik.config(text="Błąd: Dodaj co najmniej 2 pomiary!")
    else:
        label_wynik.config(text=f"Wynik kolimacji: {average}\nBłąd kolimacji: {error}")


def init_ui(parent):
    global entry_left, entry_right, tabela, label_wynik


    label_left = tk.Label(parent, text="Koło lewe:")
    label_left.pack()
    entry_left = tk.Entry(parent)
    entry_left.pack()

    label_right = tk.Label(parent, text="Koło prawe:")
    label_right.pack()
    entry_right = tk.Entry(parent)
    entry_right.pack()

    add_button = tk.Button(parent, text="+", command=fetch_and_add)
    add_button.pack(pady=5)


    tabela = ttk.Treeview(parent, columns=("H1", "H2"), show="headings", height=5)
    tabela.heading("H1", text="Koło Lewe")
    tabela.heading("H2", text="Koło Prawe")
    tabela.pack(pady=5)

    clear_button = tk.Button(parent, text="Wyczyść tabelę", command=clear_data)
    clear_button.pack(pady=5)

    calc_button = tk.Button(parent, text="Oblicz Kolimację", command=show_result)
    calc_button.pack(pady=5)

    label_wynik = tk.Label(parent, text="Wyniki pojawią się tutaj", pady=10)
    label_wynik.pack()