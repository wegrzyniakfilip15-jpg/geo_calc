import math
import tkinter as tk
from importlib.resources import contents
from tkinter import ttk, filedialog
from math import sqrt

measurements = []


entry_left = None
entry_right = None
tabela = None
label_wynik = None

def import_data():
    path = filedialog.askopenfilename(
        title="Wybierz plik z pomiarami",
        filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")],
    )
    print("path:", path)
    if not path:
        return
    with open(path, encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        print(repr(line))
        line = line.strip()

        if not line:
            continue

        if not line[0].isdigit():
            continue

        parts = line.split()
        h1 = float(parts[0].replace(",", "."))
        h2 = float(parts[1].replace(",", "."))
        h1_h2 = (h1, h2)
        measurements.append(h1_h2)
        tabela.insert('', 'end', values=h1_h2)

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


def calc_corr_h():
    c_avg, c_err = calc_c()

    if c_avg == "Brak danych":
        label_wynik.config(text="Błąd: Wczytaj najpierw plik z danymi!")
        return

    try:
        h = float(entry_h.get())
        z = float(entry_z.get())

        z_rad = z * math.pi / 200

        corr_h = h + c_avg/math.sin(z_rad)

        label_wynik.config(text=f"Poprawiony odczyt koła poziomego: {corr_h}")
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
    global entry_h, entry_z, tabela, label_wynik


    btn_import = tk.Button(parent, text="Wczytaj dane z pliku tekstowego", command=import_data)
    btn_import.pack(pady=5)


    tabela = ttk.Treeview(parent, columns=("H1", "H2"), show="headings", height=5)
    tabela.heading("H1", text="Koło Lewe")
    tabela.heading("H2", text="Koło Prawe")
    tabela.pack(pady=5)

    calc_button = tk.Button(parent, text="Oblicz Kolimację", command=show_result)
    calc_button.pack(pady=5)

    clear_button = tk.Button(parent, text="Wyczyść tabelę", command=clear_data)
    clear_button.pack(pady=5)

    label_h = tk.Label(parent, text="Odczyt poziomy:")
    label_h.pack(pady=(30, 0))
    entry_h = tk.Entry(parent)
    entry_h.pack()

    label_z = tk.Label(parent, text="Odległość zenitalna:")
    label_z.pack()
    entry_z = tk.Entry(parent)
    entry_z.pack()

    add_button = tk.Button(parent, text="Oblicz poprawiony odczyt", command=calc_corr_h)
    add_button.pack(pady=5)

    label_wynik = tk.Label(parent, text="Wyniki pojawią się tutaj", pady=10)
    label_wynik.pack()