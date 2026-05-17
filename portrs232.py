import serial.tools.list_ports
import tkinter as tk
import tkinter.ttk as ttk
import threading
import serial

serial_port = None

def get_available_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]


def connect_to_port(port_cb, text_log):
    global serial_port

    chosen_port = port_cb.get()

    if not chosen_port:
        text_log.insert(tk.END, "Błąd: Wybierz port z listy!\n")
        return

    try:
        serial_port = serial.Serial(chosen_port, 9600, timeout=1)
        text_log.insert(tk.END, f"Połączono z {chosen_port}\n")

        threading.Thread(target=read_from_port, args=(text_log,), daemon=True).start()

    except Exception as e:
        text_log.insert(tk.END, f"Błąd połączenia: {e}\n")


def read_from_port(text_log):

    global serial_port
    while serial_port and serial_port.is_open:
        try:
            if serial_port.in_waiting > 0:
                line = serial_port.readline().decode('ascii', errors='ignore').strip()

                if line:
                    text_log.after(0, lambda l = line: (text_log.insert(tk.END, l + '\n'), text_log.see(tk.END)))
                    pass
        except Exception as e:
            break

def init_ui(parent):
    tk.Label(parent, text="Wybierz port RS232:").pack(pady=(10, 0))

    available_ports = get_available_ports()
    port_cb = ttk.Combobox(parent, values=available_ports, state="normal")
    port_cb.pack()

    text_log = tk.Text(parent, height=15)

    btn_connect = tk.Button(parent, text="Połącz", command=lambda: connect_to_port(port_cb, text_log))
    btn_connect.pack(pady=10)

    text_log.pack(expand=True, fill="both")