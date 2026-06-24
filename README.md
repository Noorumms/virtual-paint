# 🎨 Virtual Paint — AI-Powered Color Tracking App

A real-time virtual painting application built with Python and OpenCV. Draw on your screen using colored objects — no mouse, no touchscreen, just a webcam and any colored marker cap or object.

---

## 📸 Demo

> Point a colored object at your webcam and paint in the air in real time.

---

## ✨ Features

- 🎨 **Multi-color detection** — detects orange, purple, and green simultaneously
- 🖌️ **Adjustable brush size** — switch between small, medium, and large
- 🧹 **Eraser tool** — erase parts of your drawing without clearing everything
- 🗑️ **Clear canvas** — wipe the entire drawing instantly
- 💾 **Save drawing** — export your artwork as a PNG image
- 📊 **Live UI header** — always shows current color, brush size, and controls on screen

---

## 🛠️ Built With

- **Python 3.x**
- **OpenCV** — computer vision and image processing
- **NumPy** — array and pixel manipulation

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/virtual-paint.git
cd virtual-paint
```

**2. Install dependencies**
```bash
pip install opencv-python numpy
```

**3. Run the app**
```bash
python virtual_paint.py
```

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| `Z` | Small brush |
| `X` | Medium brush |
| `V` | Large brush |
| `E` | Toggle eraser on / off |
| `C` | Clear canvas |
| `S` | Save drawing as PNG |
| `Q` | Quit |

---

## 🔧 How It Works

```
Webcam captures frame
        ↓
Frame converted from BGR to HSV color space
        ↓
Each color range checked against every pixel (inRange)
        ↓
Contours found in mask → tip position (x, y) extracted
        ↓
Tip position saved to points list with color and brush size
        ↓
All saved points drawn as circles on canvas every frame
        ↓
Looks like a continuous painted trail on screen
```

### Why HSV instead of BGR?
BGR mixes color and brightness together making color detection unreliable under different lighting. HSV separates them — Hue controls the color, Saturation the vividness, Value the brightness — making it far easier to isolate a specific color regardless of lighting conditions.

---

## 🎨 Adding Your Own Colors

Open `virtual_paint.py` and edit these two lists:

```python
# HSV range for detection  [h_min, s_min, v_min, h_max, s_max, v_max]
myColors = [
    [5,  107, 0,  19,  255, 255],   # orange
    [133, 56, 0,  159, 156, 255],   # purple
    [5,   76, 0,  100, 255, 255],   # green
]

# BGR value for drawing that color on screen
myColorValues = [
    [51,  153, 255],   # orange
    [255,   0, 255],   # purple
    [0,   255,   0],   # green
]
```

To find HSV values for a new color, run the included `color_detector.py` trackbar tool and slide until your color is isolated — then copy those 6 numbers into `myColors`.

---

## 📁 Project Structure

```
virtual-paint/
│
├── virtual_paint.py       # main application
├── color_detector.py      # trackbar tool to find HSV values
├── README.md              # this file
└── drawings/              # saved drawings go here
```

---

## 💡 Possible Improvements

- Add more colors
- Undo last stroke
- Change background to white for a whiteboard feel
- Add shape drawing mode (circle, rectangle)
- Add text stamp tool

---

## 👤 Author

**Noor Fatima**
- Learning computer vision through hands-on projects

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
