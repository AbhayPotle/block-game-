# 🎮 NEON BLOCKS: AI HAND-CONTROLLED GAME

> **"The Tetris of the Cyberpunk Era."**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![MediaPipe](https://img.shields.io/badge/AI-MediaPipe-orange?style=for-the-badge&logo=google)
![JavaScript](https://img.shields.io/badge/Web-Canvas_API-yellow?style=for-the-badge&logo=javascript)
![CSS3D](https://img.shields.io/badge/Style-CSS_3D-pink?style=for-the-badge&logo=css3)
![Vibe Coded](https://img.shields.io/badge/Vibe_Coded-AI_Generated-8A2BE2?style=for-the-badge&logo=openai)

> **⚡ This project was "Vibe Coded" entirely using AI assistance.**

---

## 🌐 3D REALISTIC INTERFACE
This isn't just a block game. It's a **spatial computing experience**.

### ✨ Key Visual Features
*   **Active 3D Parallax**: The interface physically tilts and reacts to your mouse movement in real-time `(Web Version)`.
*   **Hyperspace Grid**: An infinite moving background that creates a sense of speed and depth.
*   **Neon Glassmorphism**: UI panels designed with a frosted glass effect and glowing neon borders.
*   **Cyber-Glitch Typography**: Text that jitters and shifts to simulate a hacked system terminal.


---

## 🏗️ HOW IT WAS CREATED
This project combines **Computer Vision (AI)** with **Retro-Arcade Logic**.

### 1. The "Virtual Joystick" (AI Layer)
Instead of pressing keys, your **hand is the controller**.
*   **MediaPipe Hands**: We use Google's advanced ML model to track 21 points on your hand in real-time.
*   **Zone Logic**: The screen is divided into invisible interaction zones.
    *   `[LEFT 40%]` -> Move Piece Left
    *   `[CENTER 20%]` -> Hold Position (Neutral)
    *   `[RIGHT 40%]` -> Move Piece Right
*   **Gesture Recognition**: Specifically tracks the distance between your **Index Finger** and **Thumb**. A "Pinch" gesture triggers the rotation.

### 2. The Game Engine (Logic Layer)
Built from scratch without heavy game engines.
*   **Grid System**: A 20x10 matrix that stores state for every cell.
*   **Collision Detection**: Mathematical checks ensure blocks don't phase through walls or each other.
*   **State Management**: Seamless transitions between `Landing`, `Scanning`, `Playing`, and `Game Over` states.

---

## 🚀 HOW TO PLAY

### Standard Web Version (Recommended)
No installation needed. Just drag the `web/` folder to any browser or hosting service.

1.  **Start the System**: Click "INITIALIZE SYSTEM".
2.  **Scan Hand**: Show your hand to the camera to unlock the controls.
3.  **Play**:
    *   👋 **Move Hand Left/Right**: Slide the block.
    *   👌 **Pinch (Index+Thumb)**: Rotate the block.
    *   🛑 **Center Hand**: Stop moving.

### Python Version (Developer Mode)
If you want to run the raw Python version with OpenCV:
```bash
pip install -r requirements.txt
python main.py
```

---

## 📂 PROJECT STRUCTURE
```
📦 Block-Game
 ┣ 📂 web/                  # The Next-Gen Web Experience
 ┃ ┣ 📜 index.html          # Structure & DOM Layout
 ┃ ┣ 📜 style.css           # 3D Transforms & Neon Effects
 ┃ ┗ 📜 script.js           # Game Logic + MediaPipe Integration
 ┣ 📜 game.py               # Core Python Game Engine
 ┣ 📜 hand_tracker.py       # AI Vision Processor
 ┣ 📜 main.py               # Entry Point (Python)
 ┗ 📜 README.md             # You are here
```

---

<div align="center">

**Developed by Abhay Potle**  
*Powered by MediaPipe & Imagination*

</div>
