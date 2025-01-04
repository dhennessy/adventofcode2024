from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_P4)

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

WHITE = display.create_pen(255, 255, 255)
GRAY = display.create_pen(127, 127, 127)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)

WIDTH, HEIGHT = display.get_bounds()
SCALE = (WIDTH // 8) // 8

display.set_font("bitmap8")

def clear():
    display.set_pen(BLACK)
    display.clear()

def draw_text_centered(text, scale, width, y):
    draw_width = display.measure_text(text, scale)
    display.text(text, (width-draw_width)//2, y, scale=scale)
    
def draw_text_right(text, scale, x, y):
    draw_width = display.measure_text(text, scale)
    display.text(text, x-draw_width, y, scale=scale)
    
def draw_title():
    display.set_pen(GREEN)
    draw_text_centered("Advent of Code 2024", 2, 320, 0)

def cell_for_day(i):
    SIZE = 40
    row = i // 5
    col = i % 5
    return 112+col*SIZE, 30+row*SIZE, SIZE, SIZE

def draw_grid():
    display.set_pen(GREEN)
    for i in range(25):
        x, y, w, h = cell_for_day(i)
        display.line(x, y, x+w, y)
        display.line(x+w, y, x+w, y+h)
        display.line(x, y+h, x+w, y+h)
        display.line(x, y, x, y+h)
    display.set_pen(GRAY)
    for i in range(5):
        x, y, w, h = cell_for_day(i*5)
        draw_text_right(f"{i*5+1}", 2, x-5, y + 14)

def draw_stars(cell, count):
    x, y, w, h = cell_for_day(cell)
    if count == 0:
        return
    if count == 1:
        display.set_pen(GRAY)
    else:
        display.set_pen(YELLOW)
    display.text("*", x+24, y+14, scale=3)
    display.set_pen(YELLOW)
    display.text("*", x+8, y+2, scale=3)

def draw_stat(title, value, y):
    display.set_pen(GRAY)
    display.text(title, 8, y, scale=2)
    display.set_pen(WHITE)
    display.text(value, 8, y+22, scale=2)

def draw_screen(progress: list[int], test_results: list[int]):
    clear()
    draw_title()
    draw_grid()
    for i in range(len(progress)):
        draw_stars(i, progress[i])
    draw_stat("Stars", f"{sum(progress)}/50", 30)
    draw_stat("Tests", f"{sum(test_results)}/50", 80)
    display.update()
                          
