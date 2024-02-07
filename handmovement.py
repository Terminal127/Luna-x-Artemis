import cv2
import pyautogui
import mediapipe as mp

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

prev_hand_x = 0  # Store previous hand landmark x-coordinate
movement_threshold = 20  # Adjust this value for sensitivity
frame_count = 0  # Counter to keep track of frames

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if frame_count % 50 == 0:  # Check if it's every third frame
                # Get the x-coordinate of a suitable landmark (e.g., wrist or index finger tip)
                # Use the index finger tip landmark instead of the wrist
                index_tip_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame.shape[1]

                # Calculate movement
                movement = index_tip_x - prev_hand_x

                # Determine direction and perform actions
                if movement > movement_threshold:
                    print("Index finger moved right")
                    # Perform actions for rightward movement here

                elif movement < -movement_threshold:
                    print("Index finger moved left")
                    # Perform actions for leftward movement here

                # Update previous landmark position
                prev_hand_x = index_tip_x

    # Update frame counter
    frame_count += 1

    cv2.imshow('Hand Gesture', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
