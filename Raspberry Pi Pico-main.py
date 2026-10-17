#This script manages the custom triangle rendering engine for the large chubby star, smooth border bouncing physics, background sparkling dust, and expression-cycling loops.

import random
import time
from machine import I2C, Pin
import ssd1306

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

WIDTH = 128
HEIGHT = 64
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

starX = 64.0
starY = 32.0
vx = 0.5
vy = 0.4

expression_timer = 0
current_expression = "smile"

NUM_BG_STARS = 12
bg_stars = [[random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1), random.uniform(0.5, 1.5)] for _ in range(NUM_BG_STARS)]

def fill_triangle(x0, y0, x1, y1, x2, y2, color):
    pts = sorted([(x0, y0), (x1, y1), (x2, y2)], key=lambda p: p[1])
    (ax, ay), (bx, by), (cx, cy) = pts
    if cy == ay: return

    def draw_span(y, sx, ex):
        if sx > ex: sx, ex = ex, sx
        oled.hline(int(sx), int(y), int(ex - sx + 1), color)

    for y in range(int(ay), int(by) + 1):
        if by == ay: break
        draw_span(y, ax + (cx - ax) * (y - ay) / (cy - ay), ax + (bx - ax) * (y - ay) / (by - ay))
        
    for y in range(int(by), int(cy) + 1):
        if cy == by: break
        draw_span(y, ax + (cx - ax) * (y - ay) / (cy - ay), bx + (cx - bx) * (y - by) / (cy - by))

def draw_large_star(x, y, expression):
    cx, cy = int(x), int(y)
    
    # Core body & Star points
    oled.fill_rect(cx - 8, cy - 8, 16, 16, 1)
    fill_triangle(cx, cy - 26, cx - 8, cy - 5, cx + 8, cy - 5, 1)
    fill_triangle(cx - 24, cy - 6, cx - 7, cy - 8, cx - 5, cy + 5, 1)
    fill_triangle(cx + 24, cy - 6, cx + 7, cy - 8, cx + 5, cy + 5, 1)
    fill_triangle(cx - 15, cy + 24, cx - 6, cy + 3, cx - 1, cy + 6, 1)
    fill_triangle(cx + 15, cy + 24, cx + 6, cy + 3, cx + 1, cy + 6, 1)

    # V-Dip & rounded smoothing
    oled.fill_rect(cx - 2, cy + 5, 5, 6, 0)
    oled.pixel(cx, cy + 6, 0); oled.pixel(cx, cy + 7, 0); oled.pixel(cx, cy + 8, 0)
    oled.pixel(cx - 9, cy - 9, 0); oled.pixel(cx + 9, cy - 9, 0)

    # Facial Expressions
    if expression == "smile":
        oled.fill_rect(cx - 7, cy - 3, 5, 8, 0)
        oled.pixel(cx - 6, cy - 2, 1); oled.pixel(cx - 5, cy, 1)
        oled.fill_rect(cx + 3, cy - 3, 5, 8, 0)
        oled.pixel(cx + 4, cy - 2, 1); oled.pixel(cx + 5, cy, 1)
        oled.pixel(cx - 11, cy + 2, 0); oled.pixel(cx - 10, cy + 2, 0)
        oled.pixel(cx + 9, cy + 2, 0); oled.pixel(cx + 10, cy + 2, 0)
        oled.fill_rect(cx - 1, cy + 2, 3, 2, 0)
        oled.pixel(cx - 1, cy + 2, 1); oled.pixel(cx + 1, cy + 2, 1); oled.pixel(cx, cy + 3, 1)
    elif expression == "sad":
        oled.pixel(cx - 6, cy - 2, 0); oled.pixel(cx - 5, cy - 3, 0); oled.pixel(cx - 4, cy - 2, 0)
        oled.pixel(cx + 4, cy - 2, 0); oled.pixel(cx + 5, cy - 3, 0); oled.pixel(cx + 6, cy - 2, 0)
        oled.pixel(cx - 11, cy + 2, 0); oled.pixel(cx - 10, cy + 2, 0)
        oled.pixel(cx + 9, cy + 2, 0); oled.pixel(cx + 10, cy + 2, 0)
        oled.pixel(cx - 1, cy + 2, 0); oled.pixel(cx, cy + 2, 0); oled.pixel(cx + 1, cy + 2, 0)

while True:
    oled.fill(0)
    expression_timer += 1
    if expression_timer > 60:
        expression_timer = 0
        current_expression = "sad" if current_expression == "smile" else "smile"

    for star in bg_stars:
        oled.pixel(int(star[0]), int(star[1]), 1)
        star[1] += star[2]
        if star[1] >= HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, WIDTH - 1)

    draw_large_star(starX, starY, current_expression)
    starX += vx; starY += vy
    if starX <= 26 or starX >= WIDTH - 26: vx *= -1
    if starY <= 28 or starY >= HEIGHT - 28: vy *= -1

    oled.show()
    time.sleep(0.04)
