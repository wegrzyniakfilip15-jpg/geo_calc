import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calc_Ng0(wavelength):
    wavelength = wavelength / 1000
    Ng0 = round(287.6155 + 4.8866 / wavelength ** 2 + 0.0680 / wavelength ** 4, 4)
    return Ng0

def show_result(entry_wavelength, label_result):
    try:
        wavenm = float(entry_wavelength.get())
        Ng0 = calc_Ng0(wavenm)
        label_result.configure(text=str(round(Ng0, 4)))
    except ValueError:
        label_result.config(text="Błąd: Sprawdź wprowadzone dane!")


def create_table_and_chart(table_i, frame_chart):

    x_data = []
    y_data = []

    for i in range(400, 1610, 10):
        result = calc_Ng0(i)
        table_i.insert('', 'end', values=(i, result))

        x_data.append(i)
        y_data.append(result)

        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)

    ax.plot(x_data, y_data, color='blue', marker='o', markersize = 3)
    ax.set_title("Wykres zależności dlugości fali od współczynnika Ng0")
    ax.set_xlabel("Długość fali")
    ax.set_ylabel("Ng0")

    canvas = FigureCanvasTkAgg(fig, master = frame_chart)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill="both")


def init_ui(parent):
    tk.Label(parent, text="Długość fali (nm)").pack()
    wavelength = tk.Entry(parent)
    wavelength.pack()

    label_result = tk.Label(parent, text="Wynik")
    label_result.pack(pady = 10)


    tk.Button(parent, text="Oblicz Ng0", command= lambda: show_result(wavelength, label_result)).pack()

    table_i = ttk.Treeview(parent, columns=("Długość fali", "Wynik"), show="headings")
    table_i.heading("Długość fali", text="Dlugość fali")
    table_i.heading("Wynik", text="Wynik")
    table_i.pack()

    frame_chart = tk.Frame(parent)
    frame_chart.pack(expand=True, fill="both")

    create_table_and_chart(table_i, frame_chart)