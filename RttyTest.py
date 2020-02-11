import pygame
from pygame.locals import *
from time import sleep
import math
import numpy

bits = 16
sample_rate = 44100
baud_rate = 45
symbol_duration = 1.0/baud_rate # in seconds
n_samples = int(round(symbol_duration*sample_rate))
max_sample = 2**(bits - 1) - 1

freq_space = 2295
freq_mark  = 2125

pygame.mixer.pre_init(sample_rate, -bits, 2, 1)
pygame.init()

def make_sound(freq):
    buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
    for x in range(n_samples):
        t = float(x)/sample_rate # time in seconds

        buf[x][0] = int(round(max_sample*math.sin(2*math.pi*freq*t))) # left
        buf[x][1] = int(round(max_sample*math.sin(2*math.pi*freq*t))) # right

    return buf

sym_space_buf = make_sound(freq_space)
sym_mark_buf  = make_sound(freq_mark)

sound_space = pygame.sndarray.make_sound(sym_space_buf)
sound_mark  = pygame.sndarray.make_sound(sym_mark_buf)

ascii_to_baudot = {
  'A': 0x03,
  'B': 0x19,
  'C': 0x0E,
  'D': 0x09,
  'E': 0x01,
  'F': 0x0D,
  'G': 0x1A,
  'H': 0x14,
  'I': 0x06,
  'J': 0x0B,
  'K': 0x0F,
  'L': 0x12,
  'M': 0x1C,
  'N': 0x0C,
  'O': 0x18,
  'P': 0x16,
  'Q': 0x17,
  'R': 0x0A,
  'S': 0x05,
  'T': 0x10,
  'U': 0x07,
  'V': 0x1E,
  'W': 0x13,
  'X': 0x1D,
  'Y': 0x15,
  'Z': 0x11,
  ' ': 0x04,
  '\n': 0x02
}

def send_symbol(char):
    # Start bit
    sound_space.play(loops = 0) ; sleep(symbol_duration)

    baudot_char = ascii_to_baudot.get(char.upper(), 0x07)

    # Payload
    for shift in range(0, 5):
        mask = 1 << shift
        if baudot_char & mask != 0:
            sound_mark.play(loops = 0) ; sleep(symbol_duration)
        else:
            sound_space.play(loops = 0) ; sleep(symbol_duration)

    # Stop bits
    sound_mark.play(loops = 0) ; sleep(symbol_duration)
    sound_mark.play(loops = 0) ; sleep(symbol_duration)

def send_message(message):
    for char in message:
        send_symbol(char)

while True:
    send_message('RYRYRYRYRYRYRYRYRYRY\nTHIS IS A TEST\nRYRYRYRYRYRYRYRYRYRY\n\n')
