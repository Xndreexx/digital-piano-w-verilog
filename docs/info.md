<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this file and reference them in the markdown. Each image must be packaged into
the repository and placed in the `docs/` folder.

-->

## How it works

This project implements a 3-voice polyphonic digital piano synthesizer designed to fit within a single Tiny Tapeout tile (`1x1`).

- **12-Note Chromatic Keyboard:** Reads 7 white keys (`ui_in[6:0]`) and 5 black keys (`uio_in[4:0]`) to assign up to 3 simultaneous notes to independent 20-bit Numerically Controlled Oscillators (NCOs).
- **4-Octave Range (Octaves 2 to 5):** Uses a compact combinational lookup table for Octave 2 (`C2` to `B2`) and applies bit-shifting (`<< octave`) controlled by `uio_in[6:5]` for accurate tuning without extra logic gates.
- **4 Selectable Timbres (`{uio_in[7], ui_in[7]}`):**
  - `00` — **Acoustic Piano:** Triangle waveform with upper-octave harmonic accent and a multiplierless exponential decay envelope.
  - `01` — **Flute:** Pure sustained triangle waveform.
  - `10` — **Strings:** Sawtooth waveform with a gradual attack envelope.
  - `11` — **8-Bit Retro:** 50% duty-cycle square wave.
- **Audio Output & Display:** The 3 voices are mixed and converted into a 1-bit Sigma-Delta audio stream on `uo_out[0]`, while `uo_out[7:1]` drives a 7-segment display showing the active primary note (`C` through `b`).

## How to test

1. Apply a 10 MHz clock to `clk` and assert `rst_n` high (`1`) with `ena` set to `1`.
2. Select the desired octave (`00` for Octave 2 up to `11` for Octave 5) on `uio_in[6:5]` and choose one of the 4 timbres on `{uio_in[7], ui_in[7]}`.
3. Drive one or up to three key inputs high (`ui_in[6:0]` for white keys `C`–`B`, `uio_in[4:0]` for black keys `C#`–`A#`).
4. Verify that the 7-segment output on `uo_out[7:1]` displays the corresponding note letter and observe the high-frequency Sigma-Delta pulse train on `uo_out[0]`.

## External hardware

- **Audio Output:** Connect a simple first-order RC low-pass filter (`R = 1 kΩ`, `C = 100 nF`) to `uo_out[0]` and feed the filtered output into a speaker amplifier or audio interface.
- **Keyboard Inputs:** 12 momentary pushbuttons with pull-down resistors connected to `ui_in[6:0]` and `uio_in[4:0]`, plus 3 slide switches or DIP switches for octave and timbre selection.
- **Display:** Standard common-cathode 7-segment LED display connected to `uo_out[7:1]`.
