import cv2
import mediapipe as mp
import tabs_handler

cv2.CAP_DSHOW = 0
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

prev_hand_x = 0  # Store previous hand landmark x-coordinate
movement_threshold = 200 
movement_threshold_x = 150# Adjust this value for sensitivity
frame_count = 0  # Counter to keep track of frames
c = 0  # Gesture count

def open_tabs():
    global prev_hand_y, gesture_count

    gesture_count = 0  # Initialize gesture count within the function
    prev_hand_y = 0  # Initialize prev_hand_y at the beginning of the function

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                index_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * frame.shape[1]
                movement_up = index_tip_y - prev_hand_y

                # Determine direction and perform actions
                if movement_up < -movement_threshold:
                    print("Finger moved up:")
                    tabs_handler.change_windows_global()
                    swipe()

                prev_hand_y = index_tip_y

        if cv2.waitKey(1) == ord('q'):
            break

def swipe():
    global prev_hand_x, frame_count

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                index_tip_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame.shape[1]
                
                movement = index_tip_x - prev_hand_x
                
                if movement > movement_threshold:
                    print("Index finger moved left")
                    tabs_handler.move_left()

                prev_hand_x = index_tip_x


        if cv2.waitKey(1) == ord('q'):
            break


def main():
    open_tabs()
    

if __name__ == "__main__":
    main()

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
