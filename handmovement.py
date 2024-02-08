import cv2
import mediapipe as mp
import tabs_handler
import sys

cv2.CAP_DSHOW = 0
cap = cv2.VideoCapture(0)


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

prev_hand_x = 0  
movement_threshold = 200 
movement_threshold_x = 200
movement_threshold_exit = 500
frame_count = 0  
c = 0  

def show_tabs():
    global prev_hand_y, gesture_count

    gesture_count = 0
    prev_hand_y = 0  

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


                if movement_up < -movement_threshold:
                    print("Finger moved up:")
                    cv2.waitKey(1000)
                    tabs_handler.open_tabs()
                    swipe()
        
                prev_hand_y = index_tip_y
        
        cv2.imshow('Hand Gesture', frame)
        
    
        
        if cv2.waitKey(1) == ord('q'):
            break

def swipe():
    global prev_hand_x, frame_count
    prev_hand_x = 0

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
                
                if movement > movement_threshold_x:
                    print("Index finger moved left")
                    tabs_handler.move_left()
                elif movement < -movement_threshold_exit:
                    
                    print("exit received")
                    tabs_handler.select()                    
                    cap.release()
                    cv2.destroyAllWindows()
                prev_hand_x = index_tip_x
        
        
        if cv2.waitKey(1) == ord('q'):
            break

def fast_swipe():
    global prev_hand_x, frame_count
    prev_hand_x = 0

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
                
                if movement > movement_threshold_x:
                    print("Index finger moved left")
                    tabs_handler.fast_tabs()
                
                elif movement < -movement_threshold_exit:
                    print("exit received")
                    tabs_handler.select()                    
                    cap.release()
                    cv2.destroyAllWindows()
                prev_hand_x = index_tip_x
                
        
        # cv2.imshow('Hand Gesture', frame)
        
        
        if cv2.waitKey(1) == ord('q'):
            break

def text():
    print ("hello world")

def main():
    # show_tabs()
    fast_swipe()
    

if __name__ == "__main__":
    main()
    # show_tabs()
    # cap.release()
    # cv2.destroyAllWindows()
