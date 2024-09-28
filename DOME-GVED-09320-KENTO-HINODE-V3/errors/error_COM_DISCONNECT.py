import serial.tools.list_ports
import logging

def find_arduino_com_port():
    """Finds the COM port used by the Arduino."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "CH340" in port.description:
            return port.device
    return None

if __name__ == "__main__":
    com_port = find_arduino_com_port()
    if com_port:
        print(f"Found Arduino COM port: {com_port}")
    else:
        print("Arduino COM port not found. Please check the following:")
        print("- Make sure your Arduino is connected to your computer.")
        print("- Ensure the CH340 driver is installed correctly.")
        print("- Check for any other programs using the COM port.")
        print("- Open Device Manager (search for 'Device Manager') and look for 'Ports (COM & LPT)' to see if the Arduino's COM port is listed.")
