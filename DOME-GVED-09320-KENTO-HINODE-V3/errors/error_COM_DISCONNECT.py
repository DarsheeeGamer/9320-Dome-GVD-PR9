import wmi
import re
import serial
import time
import logging

def find_ch340_com_port():
    """Finds the COM port used by the CH340 driver for the Arduino."""
    c = wmi.WMI()
    for device in c.Win32_PnPEntity():
        if "CH340" in device.Description:  
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

if __name__ == "__main__":
    com_port = find_ch340_com_port()
    if com_port:
        print(f"Found CH340 driver COM port: {com_port}")
        arduino = connect_to_arduino(com_port)
        if arduino:
            # Do something with the connected Arduino
            print("Arduino connected.")
        else:
            print("Error connecting to Arduino.")
    else:
        print("CH340 driver COM port not found. Please check the following:")
        print("- Make sure your Arduino is connected to your computer.")
        print("- Ensure the CH340 driver is installed correctly.")
        print("- Check for any other programs using the COM port.")
        print("- Open Device Manager (search for 'Device Manager') and look for 'Ports (COM & LPT)' to see if the Arduino's COM port is listed.")