import pygame
from pygame.locals import *
from time import sleep
import math
import numpy

size = (1366, 720)
bits = 16
sample_rate = 44100
baud_rate = 45
symbol_duration = 1.0/baud_rate # in seconds
n_samples = int(round(symbol_duration*sample_rate))
max_sample = 2**(bits - 1) - 1

pygame.mixer.pre_init(sample_rate, -bits, 2, 1)
pygame.init()
_display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)

def make_sound(freq):
    buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
    for x in range(n_samples):
        t = float(x)/sample_rate # time in seconds

        buf[x][0] = int(round(max_sample*math.sin(2*math.pi*freq*t))) # left
        buf[x][1] = int(round(max_sample*math.sin(2*math.pi*freq*t))) # right

    return buf

sym_space_buf = make_sound(2295)
sym_mark_buf  = make_sound(2125)

sound_space = pygame.sndarray.make_sound(sym_space_buf)
sound_mark  = pygame.sndarray.make_sound(sym_mark_buf)

def send_symbol(char):
    # Start message
    sound_space.play(loops = 0) ; sleep(symbol_duration)

    # Message
    if char == 'R':
        sound_space.play(loops = 0) ; sleep(symbol_duration)
        sound_mark.play(loops = 0) ; sleep(symbol_duration)
        sound_space.play(loops = 0) ; sleep(symbol_duration)
        sound_mark.play(loops = 0) ; sleep(symbol_duration)
        sound_space.play(loops = 0) ; sleep(symbol_duration)
    elif char == 'Y':
        sound_mark.play(loops = 0) ; sleep(symbol_duration)
        sound_space.play(loops = 0) ; sleep(symbol_duration)
        sound_mark.play(loops = 0) ; sleep(symbol_duration)
        sound_space.play(loops = 0) ; sleep(symbol_duration)
        sound_mark.play(loops = 0) ; sleep(symbol_duration)
    else: # Unknown character; send "U" for "Unknown"
        sound_mark.play(loops = 0) ; sleep(symbol_duration)
        sound_mark.play(loops = 0) ; sleep(symbol_duration)
        sound_mark.play(loops = 0) ; sleep(symbol_duration)
        sound_space.play(loops = 0) ; sleep(symbol_duration)
        sound_space.play(loops = 0) ; sleep(symbol_duration)

    # End message
    sound_mark.play(loops = 0) ; sleep(symbol_duration)
    sound_mark.play(loops = 0) ; sleep(symbol_duration)

_running = True
while _running:
    send_symbol('R') 
    send_symbol('Y') 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _running = False
            break

pygame.quit()
