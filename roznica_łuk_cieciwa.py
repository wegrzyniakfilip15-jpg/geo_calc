import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.ttk as ttk

plt.style.use('seaborn-v0_8-darkgrid')

def calc_difference(table):
    d = 1
    r = 6371 * 8

    x_val = []
    y_val = []
    while d < 101:
        delta = round(d ** 3 / (24 * r ** 2) * 1000000, 3)

        table.insert('', 'end', values=(d, delta))

        x_val.append(d)
        y_val.append(delta)
        d += 1
    return x_val, y_val


def draw_chart(table, parent):
    x_val, y_val = calc_difference(table)
    fig, ax = plt.subplots(figsize=(6, 4))

    ax.scatter(x_val, y_val)
    ax.set_title("Wpływ krzywizny Ziemi na pomiar")
    ax.set_xlabel("Długość łuku[km]")
    ax.set_ylabel("Różnica długości między łukiem a cięciwą[mm]")
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill="both")

def init_ui(parent):
    frame_table = tk.Frame(parent)
    frame_table.pack(side="top", expand=True, fill="both")

    table = ttk.Treeview(frame_table, columns=("d", "delta"), show="headings")
    table.heading("d", text="Długość łuku")
    table.heading("delta", text="Róznica długości między łukiem a cięciwą")

    scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    table.pack(expand=True, fill="both")

    frame_chart = tk.Frame(parent)
    frame_chart.pack(side="bottom", expand=True, fill="both")

    draw_chart(table, frame_chart)
