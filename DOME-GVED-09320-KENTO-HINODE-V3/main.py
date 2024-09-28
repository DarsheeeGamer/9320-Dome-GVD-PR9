import time
import os
import random
import logging
import pygame
import serial.tools.list_ports

from helper.music import MusicPlayer
from helper.serial import connect_to_arduino, read_command
from helper.arduino_parser import handle_arduino_command
from helper.logger import setup_logger
from errors.error_COM_DISCONNECT import find_arduino_com_port
from errors.error_COM_EVC9223_rstrt import handle_evc9223_error
from errors.error_DEPENDENCY_P398 import handle_dependency_error

# --- Configuration ---
# Music folder
music_folder = "songs"  # Path to the folder containing your MP3 files

# --- Setup ---
# Configure error logging
setup_logger()

# Find Arduino COM port
arduino_port = find_arduino_com_port()
if arduino_port is None:
    logging.error("Arduino COM port not found. Exiting...")
    exit()
else:
    logging.info(f"Arduino COM port set to: {arduino_port}")

# Connect to Arduino
arduino = connect_to_arduino(arduino_port)
if arduino is None:
    exit()

# Initialize music player
music_player = MusicPlayer(music_folder)

# --- Main Loop ---
song_playing = False  # Flag to track if a song is currently playing
last_play_time = 0    # Timestamp of the last "play" command

while True:
    try:
        if arduino.is_open: # Check if Arduino is connected
            command = read_command(arduino)
            if command:
                handle_arduino_command(command, music_player)
                last_play_time = time.time()  # Update last_play_time

                # Show that the Arduino sent the command
                if command == "play":
                    print("Arduino sent 'play' command. Triggering song...")
                elif command == "stop":
                    print("Arduino sent 'stop' command. Stopping song...")

        else:
            arduino = handle_evc9223_error()
            if arduino is None:
                logging.error("Failed to reconnect to Arduino. Exiting...")
                exit()

    except Exception as e:
        # Check if it's a dependency error
        if str(e).startswith("P398"): 
            if handle_dependency_error(str(e)):
                print("Dependencies installed successfully. Please restart the script.")
                exit()
            else:
                print("Error installing dependencies. Check the logs for details.")
        else:
            logging.error(f"Error in main loop: {e}")

    time.sleep(0.01)  # Faster polling interval (10ms) for responsiveness
