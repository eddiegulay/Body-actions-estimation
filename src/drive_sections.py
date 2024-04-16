import cv2
import mediapipe as mp
import numpy as np
from drive_actions import perform_action

def track_hand():
    # Initialize MediaPipe Hand module
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_drawing = mp.solutions.drawing_utils

    # Initialize video capture
    cap = cv2.VideoCapture(0)

    # Get the frame width and height
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the regions for left and right hands
    left_hand_region = (0, 0, width // 2, height)
    right_hand_region = (width // 2, 0, width // 2, height)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)

        # Convert BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect hand landmarks
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            # Create a black mask image
            mask = np.zeros_like(frame)

            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks on the mask
                mp_drawing.draw_landmarks(mask, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                           mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2),
                                           mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2))

                # Perform actions based on hand position
                # Get the palm landmark
                palm_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                # Get the coordinates of the palm landmark
                palm_x = int(palm_landmark.x * width)
                palm_y = int(palm_landmark.y * height)
                # Check if the palm is in the left hand region
                if palm_x < width // 2:
                    cv2.putText(frame, "Left Hand", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    # Perform action for left hand (e.g., steer left)
                    perform_action("steer_left")
                # Check if the palm is in the right hand region
                else:
                    cv2.putText(frame, "Right Hand", (width - 200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    # Perform action for right hand (e.g., steer right)

            # Overlay the mask on the original frame
            frame = cv2.bitwise_and(frame, mask)

        # Draw the regions for left and right hands on the frame
        cv2.rectangle(frame, (left_hand_region[0], left_hand_region[1]), (left_hand_region[0] + left_hand_region[2], left_hand_region[1] + left_hand_region[3]), (255, 0, 0), 2)
        cv2.rectangle(frame, (right_hand_region[0], right_hand_region[1]), (right_hand_region[0] + right_hand_region[2], right_hand_region[1] + right_hand_region[3]), (255, 0, 0), 2)

        cv2.imshow('Hand Landmarks', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    track_hand()