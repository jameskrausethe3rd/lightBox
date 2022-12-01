# Example showing how functions, that accept tuples of rgb values,
# simplify working with gradients

import time
import math
import random
import utime
from utime import sleep_ms
from neopixel import Neopixel
from machine import Pin

numpix = 100
strip = Neopixel(numpix, 0, 28, "GRB")
button = machine.Pin(4, machine.Pin.IN)

led = Pin(25, Pin.OUT)
led.toggle()

red = (255, 0, 0)
orange = (255, 50, 0)
yellow = (255, 100, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
indigo = (100, 0, 90)
violet = (200, 0, 100)
white = (255,180,180)
black = (0, 0, 0)
cycle = [black, red, orange, yellow, green, blue, violet, white]
colors = [red, orange, yellow, green, blue, indigo, violet]
num_colors = len(cycle)

button_count = 0
last_value = 0

def set_color ():
    strip.brightness(255)
    strip.fill(cycle[button_count%(num_colors+5)])
    strip.show()

def candle ():
    while True:
        strip.fill((252,100,0))
        strip.brightness(random.randrange(40,80))
        strip.show()
        if button.value() == 1:
            return
        time.sleep(.035)
        
def fastFill ():
    while True:
        cur_value = button.value()
        strip.brightness(255)
        
        for curcolor in colors:
            for x in range(0,numpix):
                if button.value() == 1:
                    return
                strip.set_pixel(x, (curcolor))
                strip.show()
                time.sleep(0.01)
            else:
                continue

def gradient ():
    step = round(numpix / num_colors)
    current_pixel = 0
    strip.brightness(255)

    for color1, color2 in zip(colors, colors[1:]):
        strip.set_pixel_line_gradient(current_pixel, current_pixel + step, color1, color2)
        current_pixel += step
        
    strip.set_pixel_line_gradient(current_pixel, numpix-1, violet, red)

    while True:
        cur_value = button.value()
        strip.rotate_right(1)
        time.sleep(0.01)
        strip.show()
        if button.value() == 1:
            break
        
def bottomUp():
    count = 0
    start = [0, 29, 59, 89]
    end = [28, 58, 88, 99]
    while True:
        for s, e in zip(start, end):
            strip.set_pixel_line(s, e, colors[count%len(colors)])
            strip.show()
            time.sleep(.016)
        for i in range(150000):
            if button.value() == 1:
                return
        count = count + 1
        
def fade():
    strip.brightness(255)
    while True:
        strip.fill(red)
        for x in range(0, 255):
            if button.value() ==1:
                return
            strip.fill((255-x, 0+x, 0))
            strip.show()
        for x in range(0, 255):
            strip.fill((0, 255-x, 0+x))
            strip.show()
        for x in range(0, 255):
            strip.fill((0+x, 0, 255-x))
            strip.show()

def wings():
    while True:
        strip.brightness(255)
        for x in range(103):
            if x > 2:
                strip.set_pixel(x-3, black)
                strip.set_pixel((99-x)+3, black)
            if x < 100:
                strip.set_pixel(x, violet)
                strip.set_pixel(99-x, violet)
            time.sleep(.01)
            strip.show()
            
def policeLights():
    while True:
        strip.brightness(255)
        for i in range(20):
            showColor = bool(random.getrandbits(1))
            if showColor:
                strip.fill(black)
                strip.set_pixel_line(0, 15, blue)
                strip.set_pixel_line(30, 45, blue)
                strip.set_pixel_line(60, 75, blue)
                strip.set_pixel_line(90, 99, blue)
                strip.show()
            else:
                strip.fill(black)
                strip.show()
        for i in range(20):
            showColor = bool(random.getrandbits(1))
            if showColor:
                strip.fill(black)
                strip.set_pixel_line(16, 29, red)
                strip.set_pixel_line(46, 59, red)
                strip.set_pixel_line(76, 89, red)
                strip.show()
            else:
                strip.fill(black)
                strip.show()

while True:
    cur_value = button.value()
    if button_count % (num_colors + 5) < num_colors:
        set_color()
    sleep_ms(10)
    if last_value > cur_value:
        print("You released the button!")
        button_count = button_count + 1
        if button_count % (num_colors+5) == num_colors:
            gradient()
        elif button_count % (num_colors+5) == num_colors+1:
            fastFill()
        elif button_count % (num_colors+5) == num_colors+2:
            bottomUp()
        elif button_count % (num_colors+5) == num_colors+3:
            candle()
        elif button_count % (num_colors+5) == num_colors+4:
            fade()
        else:
            set_color()
    if cur_value == 1:
        last_value = 1
    if cur_value == 0:
        last_value = 0