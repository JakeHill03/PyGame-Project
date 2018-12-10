# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 12:17:03 2018

@author: srtod
"""
import pygame
from os import path

pygame.init()

#defines path to directories for sound files and image files
image_dir = path.join(path.dirname(__file__), 'images') #Add path to use the images folder, so files can be referenced
music_dir = path.join(path.dirname(__file__), 'music') #Add path to use sound folder 

#Loads in sounds
pygame.mixer.music.load(path.join(music_dir, "background_music.wav"))
falling_noise = pygame.mixer.Sound(path.join(music_dir, "falling_sound.wav"))
jumping_noise = pygame.mixer.Sound(path.join(music_dir, "jump_sound.wav"))
powerup_noise = pygame.mixer.Sound(path.join(music_dir, "powerup.wav"))

#initilaises, sets volume and loops background music
pygame.mixer.pre_init(44100,16,2,4096) #initialises the pygame mixer module for loading and playing sound files and music
pygame.mixer.music.set_volume(0.5) #Set music volume
pygame.mixer.music.play(-1) #Play music