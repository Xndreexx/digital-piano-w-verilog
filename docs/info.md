## How it works

This project implements a 3-voice polyphonic digital piano synthesizer (`tt_um_uabc_piano`) designed for a single Tiny Tapeout tile (`1x1`).

- **12-Note Chromatic Keyboard:** Reads 7 white keys (`ui_in[6:0]`) and 5 black keys (`uio_in[4:0]`) to assign up to 3 simultaneous notes to independent 20-bit Numerically Controlled Oscillators (NCOs).
- **4-Octave Range (Octaves 2 to 5):** Uses a combinational lookup table for Octave 2 (`C2` to `B2`) and bit-shifting (`<< octave`) controlled by `uio_in[6:5]`.
- **4 Selectable Timbres (`{uio_in[7], ui_in[7]}`):** Acoustic Piano (`00`), Flute (`01`), Strings (`10`), and 8-Bit Retro (`11`).
- **Audio Output & Display:** Mixes the 3 voices into a 1-bit Sigma-Delta audio stream on `uo_out[0]`, while `uo_out[7:1]` drives a 7-segment display showing the primary active note.

## How to test

1. Apply a 10 MHz clock to `clk`, assert `rst_n` high (`1`), and set `ena` to `1`.
2. Select the octave on `uio_in[6:5]` and the timbre on `{uio_in[7], ui_in[7]}`.
3. Assert up to three key inputs (`ui_in[6:0]` and `uio_in[4:0]`) high simultaneously.
4. Observe the 7-segment note letter on `uo_out[7:1]` and the Sigma-Delta audio pulse train on `uo_out[0]`.

## External hardware

- First-order RC low-pass filter (`R = 1 kΩ`, `C = 100 nF`) on `uo_out[0]` connected to an audio amplifier.
- 12 momentary pushbuttons with pull-down resistors, 3 switches for octave/timbre selection, and a common-cathode 7-segment display on `uo_out[7:1]`.
