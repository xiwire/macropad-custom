# SPDX-FileCopyrightText: 2022 XIWIRE
# SPDX-License-Identifier: MIT
# Personal setup for keyboard shortcuts
import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_macropad import MacroPad
from rainbowio import colorwheel


OFF = 0

ROTATION = 90  # knob on top left
WIDTH = 10
HEIGHT = 21


def hcenter(text: str) -> str:
    return text.center(WIDTH)


macropad = MacroPad(rotation=ROTATION)  # create the macropad object, rotate orientation
macropad.display.auto_refresh = False  # avoid lag

# --- Pixel setup --- #
key_color = colorwheel(0)  # fill with cyan to start
macropad.pixels.brightness = 0.0
macropad.pixels.fill(key_color)

FONT_FILE = "cherry-10-r.pcf"

FONTS_FOLDER = "/assets/fonts"
FONT_PATH = f"{FONTS_FOLDER}/{FONT_FILE}"
FONT = bitmap_font.load_font(FONT_PATH)

HEADER = "Shortcuts"

# --- Display text setup ---
text_lines = macropad.display_text(hcenter(HEADER), font=FONT)
text_lines.show()

last_knob_pos = macropad.encoder  # store knob position state

while True:
    macropad.display.refresh()
