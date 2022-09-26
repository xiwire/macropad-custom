# SPDX-FileCopyrightText: 2022 XIWIRE
# SPDX-License-Identifier: MIT
# Personal setup for live playing
import displayio
from adafruit_macropad import MacroPad
from rainbowio import colorwheel
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label

OFF = 0
HWIDTH = 21

def hcenter(text: str) -> str:
    return f"{text:^21}"

macropad = MacroPad(rotation=90)  # create the macropad object, rotate orientation
macropad.display.auto_refresh = False  # avoid lag

# --- Pixel setup --- #
key_color = colorwheel(0)  # fill with cyan to start
macropad.pixels.brightness = 0.0
macropad.pixels.fill(key_color)

# MODES
MODE_MUTES = 0
MODE_SCENE = 1
MODE_FX = 1
mode = MODE_MUTES
mode_text = ["Mutes", "Scenes", "FX"]

# MUTES MODE
mutes = [True, True, True, True,
         True, True, True, True,
         True, True, True, True]

encoder_ccn = 69
encoder_ccv = 0

current_scene = 13

FONT = bitmap_font.load_font("fonts/ProggyTiny.pcf")

# --- Display text setup ---
text_lines = macropad.display_text("{:^21}".format("~*~cMIDI~*~"), font=FONT)
text_lines.show()


last_knob_pos = macropad.encoder  # store knob position state

PRESS   = 0
RELEASE = 1
LATCH   = 2
RLATCH  = 3

operation = PRESS
operation_text = ["press", "release", "latch", "~latch"]
N_OPERATION = 4

tracks = ("BD", "SD", "RS",
          "BT", "LT", "MT",
          "CH", "CY",
          "T1", "T2", "T3", "T4")

while True:
    changed = False
    while macropad.keys.events:  # check for key press or release
        changed = True
        key_event = macropad.keys.events.get()
        if key_event:
            if key_event.pressed:
                key = key_event.key_number
                macropad.pixels[key] = colorwheel(10)  # light up green
                #text_lines[1].text = "MUTE: {}".format(key)
                macropad.midi.send(macropad.ControlChange(70 + key, 127))
                macropad.pixels[key] = key_color

            if key_event.released:
                key = key_event.key_number
                # macropad.midi.send(macropad.NoteOff(midi_notes[key], 0))
                macropad.midi.send(macropad.ControlChange(70 + key, 0))
                macropad.pixels[key] = OFF

    macropad.encoder_switch_debounced.update()  # check the knob switch for press or release
    if macropad.encoder_switch_debounced.pressed:
        mode = (mode+1) % 3
        macropad.red_led = macropad.encoder_switch
        #text_lines[1].text = " "  # clear the note line

    if macropad.encoder_switch_debounced.released:
        macropad.red_led = macropad.encoder_switch

    if last_knob_pos is not macropad.encoder:  # knob has been turned
        knob_pos = macropad.encoder  # read encoder
        knob_delta = knob_pos - last_knob_pos  # compute knob_delta since last read
        last_knob_pos = knob_pos  # save new reading
        operation += knob_delta
        operation %= N_OPERATION

        encoder_ccv += knob_delta
        encoder_ccv = max(min(encoder_ccv, 127), 0)
        macropad.midi.send(macropad.ControlChange(encoder_ccn, int(encoder_ccv)))



        if mode == 1:  # CC
            pass #midi_values[mode] = min(max(midi_values[mode] + knob_delta, 0), 31)  # scale the value
            #macropad.midi.send(macropad.ControlChange(CC_NUM, int(midi_values[mode]*4.1)))
            #text_lines[0].text = ("%s %d" % (mode_text[mode], int(midi_values[mode]*4.1)))

        if mode == 2:  # PitchBend
            pass #midi_values[mode] = min(max(midi_values[mode] + knob_delta, 0), 15)  # smaller range
            #macropad.midi.send(macropad.PitchBend((midi_values[mode]*1024)))  # range * mult = 16384
            #text_lines[0].text = ("%s %d" % (mode_text[mode], midi_values[mode]-8))

        last_knob_pos = macropad.encoder

    #if changed and mode == MODE_MUTES:  # ProgramChange
    #    s = []
    #    for i, m in enumerate(mutes):
    #        if m:
    #            macropad.pixels[i] = colorwheel(10)
    #        else:
    #            macropad.pixels[i] = 0


    #text_lines[0].text = ("- {:7} -".format(mode_text[mode]))
    #text_lines[1].text = ("- {:7} -".format(operation_text[operation]))

    macropad.display.refresh()
