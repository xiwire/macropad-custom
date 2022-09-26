# vim:foldmethod=marker
# SPDX-FileCopyrightText: 2022 XIWIRE
# SPDX-License-Identifier: MIT
# Personal setup for keyboard shortcuts
import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_hid.keycode import Keycode
from adafruit_macropad import MacroPad
from rainbowio import colorwheel


# CONSTANTS
OFF = 0.0
ROTATION = 90  # knob on top left
WIDTH = 10
HEIGHT = 21
NUM_KEYS = 12


# Shortcut constants
COMMAND_NAME = 0
COMMAND_KEY_CODE = 1
COMMAND_KEY_INPUT = 2


# Colorwheel colors
RED = 0
VIOLET = 180


def hcenter(text: str) -> str:
    return text.center(WIDTH)


macropad = MacroPad(rotation=ROTATION)
macropad.display.auto_refresh = False
macropad.pixels.auto_write = False

# Pixel setup
key_color = colorwheel(180)
macropad.pixels.brightness = 1
macropad.pixels.fill(OFF)

# Font setup
FONT_FILE = "cherry-10-r.pcf"

FONTS_FOLDER = "/assets/fonts"
FONT_PATH = f"{FONTS_FOLDER}/{FONT_FILE}"
FONT = bitmap_font.load_font(FONT_PATH)

HEADER = "~Shortcuts~"

# --- Display text setup ---
text_lines = macropad.display_text(hcenter(HEADER), font=FONT)
text_lines.show()

last_encoder_position = macropad.encoder  # store knob position state

SHORTCUTS = [
    # General
    ("Copy", [Keycode.CONTROL, Keycode.C], "C-c"),
    ("Paste", [Keycode.CONTROL, Keycode.V], "C-v"),
    ("Terminal", [Keycode.CONTROL, Keycode.ALT, Keycode.T], "!!!"),
    ("nothing", [Keycode.SHIFT, Keycode.WINDOWS, Keycode.T], "!!!"),
    ("Workspace", [Keycode.CONTROL, Keycode.F1], "1"),
    ("Workspace", [Keycode.CONTROL, Keycode.F2], "2"),
    ("Workspace", [Keycode.CONTROL, Keycode.F3], "3"),
    ("Workspace", [Keycode.CONTROL, Keycode.F4], "4"),
]


def input_command(command: list) -> None:
    for key in command:
        macropad.keyboard.press(key)
    macropad.keyboard.release_all()


def main_loop() -> None:
    # handle encoder {{{
    # encoder press
    macropad.encoder_switch_debounced.update()
    if macropad.encoder_switch_debounced.pressed:
        macropad.red_led = True
    if macropad.encoder_switch_debounced.released:
        macropad.red_led = False

    # encoder position
    global last_encoder_position
    position = macropad.encoder
    if position != last_encoder_position:
        last_encoder_position = position
    # handle encoder }}}

    # event loop {{{
    events_to_handle = True
    while events_to_handle:
        event = macropad.keys.events.get()
        if not event:
            events_to_handle = False
            continue
        if event.key_number >= len(SHORTCUTS):
            continue
        key_number = event.key_number
        if event.pressed:
            command_name, command_key_code, command_key_input = SHORTCUTS[key_number]
            text_lines[key_number].text = f"{command_name}: {command_key_input}"
            macropad.pixels[key_number] = colorwheel(VIOLET)
            input_command(command_key_code)
        if event.released:
            macropad.pixels[key_number] = OFF
            text_lines[key_number].text = ""
    # }}}
    macropad.pixels.show()
    macropad.display.refresh()


while True:
    main_loop()
