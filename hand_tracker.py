import cv2
import mediapipe as mp
import time

class HandTracker:
    def __init__(self, mode=False, max_hands=1, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0, draw=True):
        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        return lm_list

    def get_gesture(self, lm_list):
        """
        Simple gesture recognition based on landmark positions.
        Returns: 'LEFT', 'RIGHT', 'ROTATE', 'DROP', or None
        """
        if not lm_list:
            return None
        
        # Example logic:
        # Index finger tip: 8
        # Thumb tip: 4
        # Wrist: 0
        
        # Logic for movement based on wrist position (or index finger) relative to screen center
        # We need screen width to know center, passing generic logic here
        # Assuming normalized coordinates or handling outside
        
        return None  # Placeholder for specific logic implemented in main or passed here

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    
    while True:
        success, img = cap.read()
        if not success:
            break
            
        img = tracker.find_hands(img)
        lm_list = tracker.find_position(img)
        
        if lm_list:
            print(lm_list[8]) # Print index fingertip
            
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
