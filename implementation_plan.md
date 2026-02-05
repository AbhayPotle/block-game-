# Hand-Controlled Block Game Implementation Plan

## Goal Description
Create a "Block Game" (Tetris-style) playable using hand gestures captured via a webcam. The project uses Computer Vision and Deep Learning (via MediaPipe) to interpret hand movements as game controls.

## User Review Required
- **Control Scheme**: I propose using hand position relative to the screen center for movement (Left/Right) and specific gestures (e.g., pinch or fist) for rotation/drop.
- **Dependencies**: Requires a webcam and installation of `opencv-python`, `mediapipe`, and `pygame`.

## Proposed Changes

### Setup
#### [NEW] [requirements.txt](file:///c:/Users/abhay/blocks/requirements.txt)
- opencv-python
- mediapipe
- pygame
- numpy

### Hand Tracking
#### [NEW] [hand_tracker.py](file:///c:/Users/abhay/blocks/hand_tracker.py)
- Class `HandTracker` to handle initialization of MediaPipe.
- Methods to process frames and return landmarks.
- specific logic to return "Action" based on hand state (e.g., "Left", "Right", "Rotate").

### Game Engine
#### [NEW] [game.py](file:///c:/Users/abhay/blocks/game.py)
- Pygame main loop.
- `Block` class for the falling pieces.
- Game state management (score, grid, game over).

### Main Entry Point
#### [MODIFY] [init.py](file:///c:/Users/abhay/blocks/init.py)
- Rename to `main.py` or keep as `init.py` (entry point).
- Orchestrates the video feed and the game update loop.

## Web Version (New)
To satisfy the request for a "link", we will build a web-based version.

### Web Setup
#### [NEW] [index.html](file:///c:/Users/abhay/blocks/web/index.html)
- Main entry point for the browser.
- Loads MediaPipe and Game scripts.

#### [NEW] [style.css](file:///c:/Users/abhay/blocks/web/style.css)
- Styling for the side-by-side layout (Video + Game Canvas).

#### [NEW] [script.js](file:///c:/Users/abhay/blocks/web/script.js)
- **Hand Tracking**: Use `@mediapipe/hands` and `@mediapipe/camera_utils`.
- **Game Engine**: Port Python `TetrisGame` class to JS Class.
- **Rendering**: Use HTML5 `<canvas>`.
- **Logic**: update loop using `requestAnimationFrame`.

## UI/UX Overhaul (Phase 2)

### Design System
- **Theme**: Cyberpunk/Sci-Fi. Dark background (`#0d0d0d`), Neon accents (`Cyan`, `Magenta`, `Lime`).
- **Font**: 'Orbitron' or 'Rajdhani' (Google Fonts).
- **Structure**:
    - **Landing Overlay**: Title, "Start Game" button, Instructions. Fades out on start.
    - **Game HUD**: Neon borders, Score with glow effect.

### [NEW] 3D Visual Upgrade
#### [MODIFY] [style.css](file:///c:/Users/abhay/blocks/web/style.css)
- Implement `perspective` on container.
- Add `transform: rotateX() rotateY()` to landing card.
- Create "Moving Grid" background animation.
- Add "Glitch" text effect.

#### [MODIFY] [script.js](file:///c:/Users/abhay/blocks/web/script.js)
- Add mousemove event listener to calculate tilt angles.
- Apply transform to `.landing-content`.

### [NEW] 3D Game Over Visuals
#### [MODIFY] [script.js](file:///c:/Users/abhay/blocks/web/script.js)
- Update mousemove event to target *any* visible `.landing-content` (Start or Game Over).

#### [MODIFY] [style.css](file:///c:/Users/abhay/blocks/web/style.css)
- Add "Critical Failure" red pulse animation for Game Over.
- Add "Shake" effect on appearance.

### Improved Controls (One-Hand)
- **Concept**: Virtual Joystick.
    - **Neutral Zone**: Center 20% of screen.
    - **Move Left**: Hand in Left 40%. Speed increases further left? Or constant.
    - **Move Right**: Hand in Right 40%.
    - **Rotate**: Pinch (Index + Thumb). Visual indicator on screen (e.g., "PINCH DETECTED" or a rotating icon).
    - **Feedback**: Draw a "Cursor" on the game canvas corresponding to hand position.

### Implementation Details
#### [MODIFY] [style.css](file:///c:/Users/abhay/blocks/web/style.css)
- Add CSS Animations for "Start" button.
- Add Glassmorphism effects.

#### [MODIFY] [index.html](file:///c:/Users/abhay/blocks/web/index.html)
- Add Landing Page elements.
- Import Google Fonts.

#### [MODIFY] [script.js](file:///c:/Users/abhay/blocks/web/script.js)
- Refine `onResults` logic.
- Add `drawNeonBlock` function for glowing blocks.

## Verification Plan

### Manual Verification
- Run the python script.
- Verify camera feed opens.
- Verify hand tracking landmarks are visible.
- Verify game window opens and blocks fall.
- **Critical**: Test that hand movements accurately move the blocks in the game.
