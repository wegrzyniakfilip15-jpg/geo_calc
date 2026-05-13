import math
import tkinter as tk
from codecs import ignore_errors
from tkinter import ttk, filedialog
from math import tan, cos, pi, sqrt, tan

measurements_i = []
z_file = 0.0
c_file = 0.0

def import_data(table_i):
    global z_file, c_file, measurements_i
    measurements_i = []

    for item in table_i.get_children():
        table_i.delete(item)


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


        parts = line.split()

        if parts[0] == "c":
            c_file = float(parts[1].replace(",", "."))
            continue
        if parts[0] == "mc":
            mc = float(parts[1].replace(",", "."))
            continue
        if parts[0] == "z":
            z_file = float(parts[1].replace(",", "."))
            continue
        try:
            h1 = float(parts[0].replace(",", "."))
            h2 = float(parts[1].replace(",", "."))

            z_rad_file = z_file * (math.pi / 200)
            if h1 < 200:
                delta_h = (h2 - (h1 + 200)) / 2
            else:
                delta_h = (h2 - (h1 - 200)) / 2

            i_val = (delta_h * math.tan(z_rad_file)) - ((c_file / 10000) / math.cos(z_rad_file))

            measurements_i.append(i_val)

            table_i.insert('', 'end', values=(h1, h2, z_file, c_file, round(i_val, 4)))
        except ValueError:
            continue



def clear_data(table_i, label_result):
    global measurements_i
    measurements_i = []
    for item in table_i.get_children():
        table_i.delete(item)
    label_result.config(text="Dane wyczyszczone.")




def calc_result(label_result):
    if len(measurements_i) <= 1:
        label_result.config(text="Błąd: Dodaj co najmniej 2 pomiary do serii!")
        return


    i_avg = sum(measurements_i) / len(measurements_i)


    sum_v = 0
    for i_val in measurements_i:
        v = i_val - i_avg
        sum_v += pow(v, 2)


    i_err = sqrt(sum_v / (len(measurements_i) * (len(measurements_i) - 1)))

    label_result.config(
        text=f"Średnia Inklinacja (i): {round(i_avg, 4)}\nBłąd średni serii (m0): {round(i_err, 4)}")
    return i_avg, i_err

def calc_corr_h(e_h, e_z, label_result, label_h_result):
    try:
        result = calc_result(label_result)
        if result is None:
            return
        i_avg, i_err = result
        e_h = float(e_h.get())
        e_z = float(e_z.get())

        z_rad = e_z * math.pi / 200

        if z_rad == 0:
            label_h_result.config(text="Błąd: Odległość zenitalna nie może być 0!")
            return

        corr_h = e_h + i_avg * 1/math.tan(z_rad)

        label_h_result.config(text=f"Poprawiony odczyt poziomy: {round(corr_h, 4)}")
    except ValueError:
        label_h_result.config(text="Błąd: Wprowadź poprawne liczby w oknach!")



def init_ui(parent):

    btn_add = tk.Button(parent, text="Wczytaj dane z pliku", command=lambda:import_data(tabela_i))
    btn_add.pack(pady=5)

    tabela_i = ttk.Treeview(parent, columns=("H1", "H2", "Z", "c", "i"), show="headings", height=5)
    tabela_i.heading("H1", text="H1")
    tabela_i.heading("H2", text="H2")
    tabela_i.heading("Z", text="Z")
    tabela_i.heading("c", text="c")
    tabela_i.heading("i", text="i")

    for col in ("H1", "H2", "Z", "c", "i"):
        tabela_i.column(col, width=80, anchor="center")

    tabela_i.pack()

    label_result = tk.Label(parent, text="Wprowadź dane pomiarów z serii")
    label_result.pack()

    btn_calc = tk.Button(parent, text="Oblicz Średnią Inklinację",
                         command=lambda: calc_result(label_result))
    btn_calc.pack(pady=5)

    btn_clear = tk.Button(parent, text="Wyczyść tabelę", command=lambda: clear_data(tabela_i, label_result))
    btn_clear.pack(pady=5)

    tk.Label(parent, text="Odczyt poziomy:").pack(pady=(20, 0))
    e_h = tk.Entry(parent)
    e_h.pack()

    tk.Label(parent, text="Odległość zenitalna:").pack()
    e_z = tk.Entry(parent)
    e_z.pack()

    label_h_result = tk.Label(parent, text="", pady=5)
    label_h_result.pack()

    btn_corr = tk.Button(parent, text="Oblicz poprawiony odczyt H",
                         command=lambda: calc_corr_h(e_h, e_z, label_result, label_h_result))
    btn_corr.pack()

