import time
import logging

def handle_arduino_command(command, music_player):
    """Parses commands from the Arduino and controls music playback."""
    if command == "play":
        if not music_player.is_playing():
            music_player.play_random_song()
    elif command == "stop":
        if music_player.is_playing():
            music_player.stop_song()