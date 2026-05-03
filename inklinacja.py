import tkinter as tk
from tkinter import ttk
from math import tan, cos, pi, sqrt

measurements_i = []


def clear_data(table_i, label_result):
    global measurements_i
    measurements_i = []
    for item in table_i.get_children():
        table_i.delete(item)
    label_result.config(text="Dane wyczyszczone.")


def add_to_table(entry_h1, entry_h2, entry_z, entry_c, table_i, label_result):
    try:
        h1 = float(entry_h1.get())
        h2 = float(entry_h2.get())
        z_grad = float(entry_z.get())
        c = float(entry_c.get())

        z_rad = z_grad * (pi / 200)


        if h1 < 200:
            delta_h = (h2 - (h1 + 200)) / 2
        else:
            delta_h = (h2 - (h1 - 200)) / 2


        i = (delta_h * tan(z_rad)) - (c / cos(z_rad))
        i_rounded = round(i, 4)


        measurements_i.append(i)
        table_i.insert('', 'end', values=(h1, h2, z_grad, c, i_rounded))


        entry_h1.delete(0, tk.END)
        entry_h2.delete(0, tk.END)
        entry_z.delete(0, tk.END)

        label_result.config(text=f"Dodano pomiar.")

    except ValueError:
        label_result.config(text="Błąd: Sprawdź wprowadzone dane!")


def calc_result(label_result):
    if len(measurements_i) <= 1:
        label_result.config(text="Błąd: Dodaj co najmniej 2 pomiary do serii!")
        return


    i_average = sum(measurements_i) / len(measurements_i)


    sum_v = 0
    for i_val in measurements_i:
        v = i_val - i_average
        sum_v += pow(v, 2)


    i_error = sqrt(sum_v / (len(measurements_i) * (len(measurements_i) - 1)))

    label_result.config(
        text=f"Średnia Inklinacja (i): {round(i_average, 4)}\nBłąd średni serii (m0): {round(i_error, 4)}")


def init_ui(parent):
    tk.Label(parent, text="Odczyt H1:").pack()
    e_h1 = tk.Entry(parent)
    e_h1.pack()

    tk.Label(parent, text="Odczyt H2:").pack()
    e_h2 = tk.Entry(parent)
    e_h2.pack()

    tk.Label(parent, text="Kąt zenitalny Z (grady):").pack()
    e_z = tk.Entry(parent)
    e_z.pack()

    tk.Label(parent, text="Wartość błędu kolimacji (c):").pack()
    e_c = tk.Entry(parent)
    e_c.pack()

    btn_add = tk.Button(parent, text="+", bg="lightgray",
                        command=lambda: add_to_table(e_h1, e_h2, e_z, e_c, tabela_i, label_result))
    btn_add.pack(pady=5)

    tabela_i = ttk.Treeview(parent, columns=("H1", "H2", "Z", "c", "i"), show="headings", height=5)
    tabela_i.heading("H1", text="H1")
    tabela_i.heading("H2", text="H2")
    tabela_i.heading("Z", text="Z")
    tabela_i.heading("c", text="c")
    tabela_i.heading("i", text="i")

    for col in ("H1", "H2", "Z", "c", "i"):
        tabela_i.column(col, width=80, anchor="center")

    tabela_i.pack(pady=10)


    label_result = tk.Label(parent, text="Wprowadź dane pomiarów z serii", pady=5)

    btn_calc = tk.Button(parent, text="Oblicz Średnią Inklinację",
                         command=lambda: calc_result(label_result))
    btn_calc.pack(pady=5)

    btn_clear = tk.Button(parent, text="Wyczyść tabelę", command=lambda: clear_data(tabela_i, label_result))
    btn_clear.pack(pady=5)

    label_result.pack()