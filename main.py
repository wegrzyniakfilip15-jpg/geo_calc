from math import sqrt
import tkinter as tk
from tkinter import ttk

okno = tk.Tk()

okno.title("Kalkulator")

label_left = tk.Label(okno, text = "Koło lewe:")
label_left.pack()

entry_left = tk.Entry(okno)
entry_left.pack()

label_right = tk.Label(okno, text = "Koło prawe:")
label_right.pack()

entry_right = tk.Entry(okno)
entry_right.pack()

def fetch_and_add():
    h1 = float(entry_left.get())
    h2 = float(entry_right.get())
    h1_h2 = (h1, h2)
    measurments.append(h1_h2)
    table.insert('', 'end', values=h1_h2)

    entry_left.delete(0, tk.END)
    entry_right.delete(0, tk.END)

add_button = tk.Button(okno, text = "+", command = fetch_and_add)
add_button.pack()


def calc_c():
    c_result = []
    if len(measurments) <= 1:
        raise ValueError("Za mała liczba pomiarów.")
    else:
        for h1, h2 in measurments:
            if h1 < 200:
                c = (h2 - (h1 + 200)) / 2
                c_result.append(c)
            else:
                c = (h2 - (h1 - 200)) / 2
                c_result.append(c)

    c_average = sum(c_result) / len(c_result)
    sum_v = 0
    for c in c_result:
        v = c - c_average
        v = pow(v, 2)
        sum_v += v

    c_error = sqrt(sum_v / (len(c_result)*(len(c_result) - 1)))
    return round(c_average, 4), round(c_error, 4)

def show_result():
    average, error = calc_c()
    label_result.config(text=f"Wynik kolimacji: {average}, Błąd kolimacji: {error}")
    label_result.pack()


table = ttk.Treeview(okno, columns=("h1", "h2"), show="headings")
table.heading("h1", text="Koło lewe")
table.heading("h2", text="Koło prawe")
table.pack()

label_result = tk.Label(okno, text = "Wynik:")
label_result.pack()

calculate_button = tk.Button(okno, text = "Oblicz", command = show_result)
calculate_button.pack()

measurments = []



okno.mainloop()