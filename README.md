# Geodetic Calculator

A Python-based desktop GUI application designed to calculate corrections for geodetic surveying measurements.

## Technologies
* **Python 3.x** - Core application language.
* **Matplotlib** - Data visualization and chart generation.
* **Tkinter** - Graphical User Interface (GUI) framework.
* **PySerial** - RS232 serial port communication with external surveying instruments.

## Features
* Communication with external surveying devices and data logging via the RS232 port.
* Calculation of the Earth's curvature effect on distance measurements.
* Calculation of collimation and inclination errors for angle measurements.
* Calculation of atmospheric corrections for distance measurements.

## Screenshots

![image](https://github.com/user-attachments/assets/3b3dccfa-1efb-49f3-a6d4-5227591e4d9b)
![image](https://github.com/user-attachments/assets/444c61b1-4c6a-419e-91f8-1f3eb00a6b91)

## Getting Started

### Option 1: Run the executable (Easiest)
1. Download the compiled application from the [Releases] tab.
2. Run the `main` executable directly. No Python installation is required.

### Option 2: Run from source
1. **Clone the repository:**
   ```bash
   git clone https://github.com/wegrzyniakfilip15-jpg/geo_calc
   cd geo_calc
   ```

2. **Install required libraries:**
   ```bash
   pip install pyserial matplotlib
   ```
   *(Note: Tkinter is included in the standard Python library and does not require installation via pip).*

3. **Run the application:**
   ```bash
   python main.py
   ```

##  Demo Usage

To test the application's functionality without external instruments, you can use the sample text files provided directly in the repository.

## Future improvements

Refactoring the codebase to Object-Oriented Programming (OOP) to eliminate global variables and improve maintainability.
   ```

