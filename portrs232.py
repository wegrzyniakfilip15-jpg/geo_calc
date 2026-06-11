import serial.tools.list_ports
import tkinter as tk
import tkinter.ttk as ttk
import threading
import tkinter.filedialog as filedialog
import serial

serial_port = None
log_file = None
log_path = None

def get_available_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def choose_log_file(log_path_var):
    global log_path
    path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")],
        title="Wybierz plik logów"
    )
    if path:
        log_path = path
        log_path_var.set(path)

def connect_to_port(port_cb, text_log):
    global serial_port, log_file, log_path

    chosen_port = port_cb.get()

    if not chosen_port:
        text_log.insert(tk.END, "Błąd: Wybierz port z listy!\n")
        return
    current_path = log_path if log_path else "log.txt"
    log_file = open(current_path, "a", encoding="utf-8")
    try:
        serial_port = serial.Serial(chosen_port, 9600, timeout=1)
        text_log.insert(tk.END, f"Połączono z {chosen_port}\n")

        threading.Thread(target=read_from_port, args=(text_log,), daemon=True).start()

    except Exception as e:
        text_log.insert(tk.END, f"Błąd połączenia: {e}\n")


def read_from_port(text_log):

    global serial_port, log_file
    while serial_port and serial_port.is_open:
        try:
            if serial_port.in_waiting > 0:
                line = serial_port.readline().decode('ascii', errors='ignore').strip()

                if line:
                    text_log.after(0, lambda l = line: (text_log.insert(tk.END, l + '\n'), text_log.see(tk.END)))
                    if log_file:
                        log_file.write(line + '\n')
                        log_file.flush()
                    pass
        except Exception as e:
            break

def disconnect():
    global serial_port, log_file
    if serial_port:
        serial_port.close()
        serial_port = None
    if log_file:
        log_file.close()
        log_file = None

def init_ui(parent):
    tk.Label(parent, text="Wybierz port RS232:").pack(pady=(10, 0))

    available_ports = get_available_ports()
    port_cb = ttk.Combobox(parent, values=available_ports, state="normal")
    port_cb.pack()

    log_path_var = tk.StringVar()
    log_path_var.set("Domyślny: log.txt")

    frame_log = tk.Frame(parent)
    frame_log.pack(pady=10)

    btn_log = tk.Button(frame_log, text="Wybierz plik zapisu", command=lambda: choose_log_file(log_path_var))
    btn_log.pack(side=tk.LEFT, padx=5)

    lbl_log = tk.Label(frame_log, textvariable=log_path_var, fg="gray")
    lbl_log.pack(side=tk.LEFT, padx=5)

    text_log = tk.Text(parent, height=15)

    frame_btn = tk.Frame(parent)
    frame_btn.pack(pady=10)

    btn_connect = tk.Button(frame_btn, text="Połącz", command=lambda: connect_to_port(port_cb, text_log))
    btn_connect.pack(side=tk.LEFT, padx=5)

    btn_disconnect = tk.Button(frame_btn, text="Rozłącz", command=disconnect)
    btn_disconnect.pack(side=tk.LEFT, padx=5)

    text_log.pack(expand=True, fill="both")