import wmi
import re
import serial
import time
import logging

def find_ch340_com_port():
    """Finds the COM port used by the CH340 driver for the Arduino."""
    c = wmi.WMI()
    for device in c.Win32_PnPEntity():
        if "CH340" in device.Description:  # Check if "CH340" is in the device description
            match = re.search(r"COM(\d+)", device.DeviceID)
            if match:
                return f"COM{match.group(1)}"
    return None

def connect_to_arduino(port, baudrate=9600, retries=5, delay_seconds=1):
    """Establishes a serial connection to the Arduino with retries."""
    for attempt in range(retries):
        try:
            ser = serial.Serial(port, baudrate)
            logging.info(f"Connected to Arduino on port {port}")
            return ser
        except Exception as e:
            logging.error(f"Error connecting to Arduino on attempt {attempt + 1}: {e}")
            if attempt < retries - 1:
                time.sleep(delay_seconds)
    return None

def handle_evc9223_error(baudrate=9600):
    """Handles EVC9223 (Arduino disconnection) error. Prompts for reconnect."""
    print("Arduino disconnected (EVC9223 error).")
    input("Please reconnect the Arduino and press Enter to continue...")
    new_com_port = find_ch340_com_port()
    if new_com_port:
        print(f"Trying to reconnect on port {new_com_port}...")
        return connect_to_arduino(new_com_port, baudrate)
    else:
        print("CH340 driver COM port not found. Please check connections.")
        return None