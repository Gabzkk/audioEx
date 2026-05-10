# Audio Steganography Tool (LSB)

A GUI-based Python steganography tool for hiding and extracting audio files inside image files using Least Significant Bit (LSB) encoding.

Built for educational purposes, CTF competitions, and steganography experimentation.

## Features

- Hide audio files inside images
- Extract hidden audio from stego images
- Simple GUI using Tkinter
- Supports PNG/JPG/BMP cover images
- Supports WAV/MP3/OGG/FLAC secret audio
- Dark-themed CTF-inspired interface


# Requirements

- Python 3.10+
- Pillow library

## Python Dependencies

Install required packages:

```bash
pip install Pillow
```

---

# Installation

## Linux / macOS

Clone the repository:

```bash
git clone https://github.com/Gabzkk/audioEx.git
```

Go into the project folder:

```bash
cd audio-stego-tool
```

Install dependencies:

```bash
pip install Pillow
```

Run the program:

```bash
python3 audioEX.py
```

---

## Windows

Install:
- Python 3
- Pillow

Then run:

```powershell
python audio_stego.py
```

---

# Usage

## Hide Audio

1. Open the program
2. Go to the **Hide Audio** tab
3. Select:
   - Cover image
   - Secret audio file
4. Click **Hide Audio**
5. Output image will be saved as:

```text
originalname_stego.png
```

---

## Extract Audio

1. Open the program
2. Go to the **Extract Audio** tab
3. Select stego PNG image
4. Click **Extract Audio**
5. Extracted audio will be saved as:

```text
originalname_extracted.wav
```

---

# How It Works

The tool uses Least Significant Bit (LSB) steganography.

- Audio data is converted into binary
- Binary bits are embedded into image pixel values
- A 4-byte header stores the hidden data size
- Extraction reconstructs the original audio from embedded bits

---

# Limitations

- Large audio files require large images
- PNG output is recommended to avoid compression artifacts
- Lossy image formats may corrupt hidden data

---

# Security Notice

This tool is intended for:

- Educational use
- Research
- Authorized CTF competitions

Do not use it for unauthorized or malicious activity.

---

# Author

TOBI6000

---

# License

MIT License
