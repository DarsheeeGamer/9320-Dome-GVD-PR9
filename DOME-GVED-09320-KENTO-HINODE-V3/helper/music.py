import pygame
import time
import logging
import os
import random

class MusicPlayer:
    def __init__(self, music_folder):
        self.music_folder = music_folder
        pygame.mixer.init()
        self.corrupted_songs = []

    def is_playing(self):
        return pygame.mixer.music.get_busy()

    def play_random_song(self):
        """Loads and plays a random song from the music folder."""
        try:
            song_files = [f for f in os.listdir(self.music_folder) 
                           if f.endswith(".mp3") and f not in self.corrupted_songs]
            if song_files:
                random.shuffle(song_files)
                song_file = os.path.join(self.music_folder, song_files[0])
                pygame.mixer.music.load(song_file)
                pygame.mixer.music.play()
                logging.info(f"Playing song: {song_file}")
            else:
                logging.error("No playable songs found.")
                print("No playable songs found in the 'songs' folder.")
        except pygame.error as e:
            logging.error(f"Error playing song {song_file}: {e}")
            print(f"Error playing {song_file}. Skipping to next song.")
            self.corrupted_songs.append(song_file) # Mark as corrupted

    def stop_song(self):
        """Stops the currently playing song."""
        pygame.mixer.music.stop()
        logging.info("Song playback stopped.")