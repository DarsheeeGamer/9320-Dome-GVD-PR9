import serial
import logging
import time

def connect_to_arduino(port="COM4", baudrate=9600, retries=5, delay_seconds=1):
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

def read_command(ser):
    """Reads a command from the Arduino."""
    if ser.in_waiting > 0:
        data = ser.readline().decode().strip()
        logging.info(f"Received command: {data}")
        return data
    return None