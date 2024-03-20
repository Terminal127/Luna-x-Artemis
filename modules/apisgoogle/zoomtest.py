import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize webcam
cap = cv2.VideoCapture(0)

# Store the initial distance between two fingers
initial_distance = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image with MediaPipe Hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2:
        # Extract hand landmarks for two hands
        hand_landmarks_1 = results.multi_hand_landmarks[0]
        hand_landmarks_2 = results.multi_hand_landmarks[1]

        # Get the coordinates of the thumb and index finger for each hand
        thumb_1 = hand_landmarks_1.landmark[mp_hands.HandLandmark.THUMB_TIP]
        index_1 = hand_landmarks_1.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

        thumb_2 = hand_landmarks_2.landmark[mp_hands.HandLandmark.THUMB_TIP]
        index_2 = hand_landmarks_2.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

        # Calculate the distance between the thumb and index finger for each hand
        distance_1 = ((thumb_1.x - index_1.x)**2 + (thumb_1.y - index_1.y)**2)**0.5
        distance_2 = ((thumb_2.x - index_2.x)**2 + (thumb_2.y - index_2.y)**2)**0.5

        # Calculate the average distance
        average_distance = (distance_1 + distance_2) / 2

        # Set the initial distance if not already set
        if initial_distance is None:
            initial_distance = average_distance

        # Simulate zooming based on the change in distance
        zoom_factor = (initial_distance / average_distance) - 1

        # Adjust the zoom factor sensitivity as needed
        zoom_factor *= 10

        # Determine the direction of zooming (in or out)
        zoom_direction = "in" if zoom_factor < 0 else "out"

        # Simulate zooming in or out using pyautogui
        if zoom_direction == "in":
            pyautogui.hotkey("ctrl", "scrollup")  # Simulate zoom in
        else:
            pyautogui.hotkey("ctrl", "scrolldown")  # Simulate zoom out

    cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
