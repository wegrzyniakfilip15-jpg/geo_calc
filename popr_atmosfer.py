import math
import tkinter as tk
from math import exp
from wsp_zalamania import calc_Ng0

def calc_ew(t_wet):
    Ew = 6.1078*math.exp(17.269*t_wet/(237.30 + t_wet))
    return Ew

def calc_e(t_wet, t_dry, pr):
    e = calc_ew(t_wet) - 0.000662 * pr * (t_dry - t_wet)
    return e

def celsius_to_kelvin(c):
    return c + 273.15

def calc_Ng(wavelength, pr, t_dry, t_wet):
    Ng = calc_Ng0(wavelength) * 0.269578 * pr/celsius_to_kelvin(t_dry) - 11.27 * calc_e(t_wet, t_dry, pr)/celsius_to_kelvin(t_dry)
    return Ng

def calc_N_standard(wavelength):
    Ng0 = calc_Ng0(wavelength)
    T_std = 288.15
    p_std = 1013.25
    e_std = 10.87

    N0 = Ng0 * 0.269578 * p_std / T_std - 11.27 * e_std / T_std
    return N0

def calc_corr(wavelength, pr, t_dry, t_wet, measured_l):
    corr_per_km = calc_N_standard(wavelength) - calc_Ng(wavelength, pr, t_dry, t_wet)
    correction = measured_l * (corr_per_km/1000000)
    corr_length = measured_l + correction
    return corr_per_km, correction, corr_length


def show_results(entry_wavelength, entry_temp_dry, entry_temp_wet, entry_air_pressure, entry_measured_length,
                 label_corr_per_km, label_correction, label_corrected_length):
    try:
        wavelength = float(entry_wavelength.get())
        temp_dry = float(entry_temp_dry.get())
        temp_wet = float(entry_temp_wet.get())
        air_pressure = float(entry_air_pressure.get())
        measured_length = float(entry_measured_length.get())

        corr_per_km, correction, corr_length = calc_corr(wavelength, air_pressure, temp_dry, temp_wet, measured_length)

        label_corr_per_km.config(text=f"Poprawka na km: {round(corr_per_km, 4)} ppm")
        label_correction.config(text=f"Poprawka do dł.: {round(correction, 4)} m")
        label_corrected_length.config(text=f"Długość poprawiona: {round(corr_length, 4)} m")

    except ValueError:
        label_corr_per_km.config(text="Błąd: Wprowadź poprawne liczby!")
        label_correction.config(text="")
        label_corrected_length.config(text="")

def init_ui(parent):
    label_wavelength = tk.Label(parent, text="Długość fali: ")
    label_wavelength.pack()
    entry_wavelength = tk.Entry(parent)
    entry_wavelength.pack()

    label_temp_dry = tk.Label(parent, text="Temperatura sucha: ")
    label_temp_dry.pack()
    entry_temp_dry = tk.Entry(parent)
    entry_temp_dry.pack()

    label_temp_wet = tk.Label(parent, text="Temperatura mokra: ")
    label_temp_wet.pack()
    entry_temp_wet = tk.Entry(parent)
    entry_temp_wet.pack()

    label_air_pressure = tk.Label(parent, text="Ciśnienie: ")
    label_air_pressure.pack()
    entry_air_pressure = tk.Entry(parent)
    entry_air_pressure.pack()

    label_measured_length = tk.Label(parent, text="Pomierzona odległość: ")
    label_measured_length.pack()
    entry_measured_length = tk.Entry(parent)
    entry_measured_length.pack()

    calc_button = tk.Button(parent, text="Oblicz poprawkę atmosferyczną",
                            command=lambda: show_results(entry_wavelength, entry_temp_dry, entry_temp_wet,
                                                         entry_air_pressure, entry_measured_length, label_corr_per_km,
                                                         label_correction, label_corrected_length))
    calc_button.pack()

    label_corr_per_km = tk.Label(parent, text="")
    label_corr_per_km.pack()

    label_correction = tk.Label(parent, text="")
    label_correction.pack()

    label_corrected_length = tk.Label(parent, text="")
    label_corrected_length.pack()