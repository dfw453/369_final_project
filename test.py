import cv2
import mediapipe as mp

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Initialize MediaPipe Drawing module (to draw landmarks)
mp_drawing = mp.solutions.drawing_utils

# Start webcam capture
camera_index = 0 # Default webcam
# camera_index = 1 # External Webcam
cap = cv2.VideoCapture(camera_index)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)
    # Convert the image to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and get the hand landmarks
    results = hands.process(rgb_frame)

    # If hands are detected
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks on the frame
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the coordinates for wrist (landmark 0) and middle finger (landmark 12, 9, etc.)
            wrist = landmarks.landmark[mp_hands.HandLandmark.WRIST]
            middle_finger_tip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

            # Check the relative position of wrist and middle finger to classify the pointing direction
            if middle_finger_tip.y < wrist.y:  # Middle finger tip is above wrist, pointing up
                gesture = "Pointing Up"
            else:  # Middle finger tip is below wrist, pointing down
                gesture = "Pointing Down"

            # Display the detected gesture on the frame
            cv2.putText(frame, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the frame with the gesture label
    cv2.imshow("Hand Gesture Detection", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()

