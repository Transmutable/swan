import board
import random
import displayio
import terminalio
import digitalio

from adafruit_display_text import label
import adafruit_displayio_sh1107

from letters import LETTERS

# These are the board buttons for the Adafruit rp2040 Feather so change them for your board
NEXT_BUTTON = board.D5
PREV_BUTTON = board.D6
RAND_BUTTON = board.D9

WIDTH = 128
HEIGHT = 64
BORDER = 1

# Lines of text
NUM_LINES = 5
MAX_LINE_CHARS = 19
LINE_INDENT = 8
LINE_HEIGHT = 12

BLACK = 0x000000
WHITE = 0xFFFFFF

print("Init love letters")

letter_index = random.randint(0, len(LETTERS) - 1)

next_button = digitalio.DigitalInOut(NEXT_BUTTON)
next_button.direction = digitalio.Direction.INPUT
next_button.pull = digitalio.Pull.UP
has_nexted = True

prev_button = digitalio.DigitalInOut(PREV_BUTTON)
prev_button.direction = digitalio.Direction.INPUT
prev_button.pull = digitalio.Pull.UP
has_preved = True

rand_button = digitalio.DigitalInOut(RAND_BUTTON)
rand_button.direction = digitalio.Direction.INPUT
rand_button.pull = digitalio.Pull.UP
has_randed= True

displayio.release_displays()

i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

display = adafruit_displayio_sh1107.SH1107(display_bus, width=WIDTH, height=HEIGHT)
splash = displayio.Group(max_size=10)
display.show(splash)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = WHITE

# Draw outer border
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw inner black rectangle
inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = BLACK
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)

def create_line(index):
    line = label.Label(terminalio.FONT, text=" ", color=WHITE, x=8, y=LINE_INDENT + (index * LINE_HEIGHT))
    splash.append(line)
    return line

lines = [create_line(i) for i in range(NUM_LINES)]

def clear_text():
    for line in lines:
        line.text = ''

def draw_letter(index):
    clear_text()
    for i, letter_line in enumerate(LETTERS[index]):
        lines[i].text = letter_line

draw_letter(letter_index)

while True:
    if next_button.value is not has_nexted:
        if has_nexted:
            letter_index = (letter_index + 1) % len(LETTERS)
            draw_letter(letter_index)
        has_nexted = not has_nexted
    elif prev_button.value is not has_preved:
        if has_preved:
            letter_index = letter_index - 1
            if letter_index < 0:
                letter_index = len(LETTERS) - 1
            draw_letter(letter_index)
        has_preved = not has_preved
    elif rand_button.value is not has_randed:
        if has_randed:
            letters_count = len(LETTERS)
            if letters_count > 1: # Avoid infinite spin because the letters length is 1 or 0
                rand_choice = letter_index
                while rand_choice == letter_index:
                    rand_choice = random.randint(0, letters_count - 1)
                letter_index = rand_choice
                draw_letter(letter_index)
        has_randed = not has_randed

