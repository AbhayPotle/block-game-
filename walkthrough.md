# Hand-Controlled Block Game Walkthrough

## Overview
You have successfully created a "Block Game" that you can control with hand gestures! The game uses your webcam to track your hand movements and translates them into game controls.

## How to Run
1. Ensure your webcam is connected.
2. Run the main script:
   ```bash
   python main.py
   ```

### Web Version
To play in your browser without installing Python:
1. Go to the `blocks/web` folder.
2. Open `index.html` in your browser (Chrome/Edge recommended).
3. Allow camera access when prompted.

**Want to share with friends?**
See [DEPLOY.md](file:///c:/Users/abhay/blocks/DEPLOY.md) for instructions on how to create a public link.

## Controls
The game is controlled by a "Virtual Joystick" mapping your hand position:
- **Move Left**: Move your hand to the **LEFT** side of the screen (into the Pink Zone).
- **Move Right**: Move your hand to the **RIGHT** side of the screen (into the Pink Zone).
- **Hold Position**: Keep your hand in the **CENTER** (Transparent Zone) to stop moving.
- **Rotate Block**: **PINCH** your index finger and thumb together.

## Debugging
- If the game runs slow, ensure good lighting for the camera so MediaPipe can track your hand faster.
- If controls feel reversed, remember the camera image is mirrored for natural interaction (moving your hand right moves the cursor right).

## Files Created
- [hand_tracker.py](file:///c:/Users/abhay/blocks/hand_tracker.py): Handles the AI hand tracking.
- [game.py](file:///c:/Users/abhay/blocks/game.py): Contains the Tetris game logic.
- [main.py](file:///c:/Users/abhay/blocks/main.py): The main entry point.
