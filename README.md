# Adafruit MacroPad RP2040
**Work in progress**

Custom codes for the [Adafruit RP2040 Macropad](https://learn.adafruit.com/adafruit-macropad-rp2040).

## Using
The [`update_code.sh`](/update_code.sh) script uploads a selected code to a mounted CIRCUITPY drive.

Use it like so:
```sh
./update_code.sh <code_name> [<mount_point>]
```

If no `code_name` is specified, it will list available codes to upload.
`mount_point` is optional. It will default to an available CIRCUITPY drive if it's the only one available.

## Codes
### MIDI
[`midi`](/codes/midi/code.py) is a code that sends MIDI messages.

### Shortcuts
[`shortcuts`](/codes/shortcuts/code.py) is a code that handles custom keyboard shortcuts.

## Assets
- [`assets/fonts/`](/assets/fonts/) are fonts :D. I'm using the [cherry](https://github.com/turquoise-hexagon/cherry) font.
- [`assets/audio/`](/assets/audio/) has a dumb startup jingle that I don't really use.
