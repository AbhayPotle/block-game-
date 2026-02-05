import cv2
import pygame
import numpy as np
from hand_tracker import HandTracker
from game import TetrisGame

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("HandBlock - Controlled by Hand")

# Game Clock
clock = pygame.time.Clock()
FPS = 30

# Initialize CV
cap = cv2.VideoCapture(0)
tracker = HandTracker(max_hands=1)

# Initialize Game
game = TetrisGame(rows=20, cols=10, block_size=30)
GAME_X = 50
GAME_Y = 50

# Control State
last_move_time = 0
MOVE_DELAY = 150 # ms
last_rotate_time = 0
ROTATE_DELAY = 500 # ms
fall_time = 0
FALL_SPEED = 500 # ms

def main():
    global last_move_time, last_rotate_time, fall_time, FALL_SPEED
    
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        
        # 1. Event Handling (Keyboard fallback)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    game.move(1, 0)
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    game.move(0, 1)

        # 2. Camera & Hand Tracking
        success, img = cap.read()
        if not success:
            continue
            
        img = cv2.flip(img, 1) # Mirror image
        img = cv2.resize(img, (640, 480))
        h, w, c = img.shape
        
        img = tracker.find_hands(img)
        lm_list = tracker.find_position(img, draw=False)
        
        # 3. Gesture Logic
        gesture_text = "Neutral"
        if lm_list:
            # Index Finger Tip (8)
            index_x, index_y = lm_list[8][1], lm_list[8][2]
            thumb_x, thumb_y = lm_list[4][1], lm_list[4][2]
            
            # Draw point for visualization
            cv2.circle(img, (index_x, index_y), 10, (0, 255, 255), cv2.FILLED)
            
            # Movement Logic based on screen zones
            # Left Zone: < 1/3 width
            # Right Zone: > 2/3 width
            
            left_boundary = w // 3
            right_boundary = 2 * w // 3
            
            cv2.line(img, (left_boundary, 0), (left_boundary, h), (0, 255, 0), 2)
            cv2.line(img, (right_boundary, 0), (right_boundary, h), (0, 255, 0), 2)
            
            if current_time - last_move_time > MOVE_DELAY:
                if index_x < left_boundary:
                    game.move(-1, 0)
                    gesture_text = "Left"
                    last_move_time = current_time
                elif index_x > right_boundary:
                    game.move(1, 0)
                    gesture_text = "Right"
                    last_move_time = current_time
            
            # Rotation Logic: Pinch (Distance between 4 and 8)
            length = np.hypot(index_x - thumb_x, index_y - thumb_y)
            if length < 30: # Threshold for pinch
                if current_time - last_rotate_time > ROTATE_DELAY:
                    game.rotate()
                    gesture_text = "Rotate"
                    last_rotate_time = current_time
                    cv2.circle(img, (index_x, index_y), 15, (0, 0, 255), cv2.FILLED)

        # 4. Game Update (Gravity)
        if current_time - fall_time > FALL_SPEED:
            game.move(0, 1)
            fall_time = current_time

        # 5. Drawing
        screen.fill(BLACK)
        
        # Render Pygame
        game.draw(screen, GAME_X, GAME_Y)
        
        # Render Information
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {game.score}", True, WHITE)
        screen.blit(score_text, (GAME_X + 350, 50))
        
        controls = [
            "Controls:",
            "Left Zone: Move Left",
            "Right Zone: Move Right",
            "Pinch (Index+Thumb): Rotate"
        ]
        for i, line in enumerate(controls):
            text = font.render(line, True, GRAY)
            screen.blit(text, (GAME_X + 350, 100 + i * 40))

        # Convert OpenCV image to Pygame Surface
        # Resize to fit in the window next to game or overlay
        # Let's put it on the right side
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_rgb = np.rot90(img_rgb) # Rotate for Pygame coordinate system if needed? No, just transpose
        # cv2 (H, W, C) -> Pygame (W, H)
        img_surface = pygame.surfarray.make_surface(img_rgb) 
        # By default make_surface expects (W, H, 3) where W is x-axis. 
        # numpy array from cv2 is (Row, Col, Depth) i.e. (H, W, Depth).
        # We need to swap axes to (W, H, Depth)
        img_surface = pygame.surfarray.make_surface(img_rgb.transpose(1, 0, 2))
        
        # Scale it down to fit
        preview_width = 400
        preview_height = int(preview_width * (h / w))
        img_surface = pygame.transform.scale(img_surface, (preview_width, preview_height))
        
        screen.blit(img_surface, (GAME_X + 350, 300))
        
        # Draw status on screen
        status_text = font.render(f"Action: {gesture_text}", True, (255, 0, 0))
        screen.blit(status_text, (GAME_X + 350, 260))

        pygame.display.flip()
        clock.tick(FPS)

    cap.release()
    pygame.quit()

if __name__ == "__main__":
    main()
