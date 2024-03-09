# import cv2
# import mediapipe as mp

# # Initialize MediaPipe Face Detection
# mp_face_mesh = mp.solutions.face_mesh
# mp_drawing = mp.solutions.drawing_utils
# face_mesh = mp_face_mesh.FaceMesh()

# # Open the webcam
# cap = cv2.VideoCapture(0)

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Convert the BGR image to RGB
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Process the image and get face landmarks
#     results = face_mesh.process(rgb_frame)

#     if results.multi_face_landmarks:
#         for landmarks in results.multi_face_landmarks:
#             # Extract eye landmarks
#             left_eye_landmarks = [landmarks.landmark[i] for i in range(159, 145, -1)]  # Example range for the left eye
#             right_eye_landmarks = [landmarks.landmark[i] for i in range(386, 374, -1)]  # Example range for the right eye

#             # Get the center of the left eye
#             left_eye_center = (
#                 int((left_eye_landmarks[0].x + left_eye_landmarks[5].x) * frame.shape[1] / 2),
#                 int((left_eye_landmarks[0].y + left_eye_landmarks[5].y) * frame.shape[0] / 2)
#             )

#             # Get the center of the right eye
#             right_eye_center = (
#                 int((right_eye_landmarks[0].x + right_eye_landmarks[5].x) * frame.shape[1] / 2),
#                 int((right_eye_landmarks[0].y + right_eye_landmarks[5].y) * frame.shape[0] / 2)
#             )

#             # Draw a circle at the center of each eye
#             cv2.circle(frame, left_eye_center, 5, (0, 255, 0), -1)
#             cv2.circle(frame, right_eye_center, 5, (0, 255, 0), -1)

#             # Calculate horizontal eye movement (difference in X coordinates)
#             eye_movement_horizontal = right_eye_center[0] - left_eye_center[0]

#             # Calculate vertical eye movement (difference in Y coordinates)
#             eye_movement_vertical = right_eye_center[1] - left_eye_center[1]

#             # Display eye movement values
#             cv2.putText(frame, f'Horizontal: {eye_movement_horizontal}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#             cv2.putText(frame, f'Vertical: {eye_movement_vertical}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#     # Display the result
#     cv2.imshow('Eye Movement Tracking', frame)

#     # Break the loop if 'q' key is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the webcam and close the window
# cap.release()
# cv2.destroyAllWindows()

import cv2
import mediapipe as mp

# Initialize MediaPipe Face Detection
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
face_mesh = mp_face_mesh.FaceMesh()

# Open the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and get face landmarks
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            # Extract eye landmarks
            left_eye_landmarks = [landmarks.landmark[i] for i in range(159, 145, -1)]  # Example range for the left eye
            right_eye_landmarks = [landmarks.landmark[i] for i in range(386, 374, -1)]  # Example range for the right eye

            # Get the center of the left eye
            left_eye_center = (
                int((left_eye_landmarks[0].x + left_eye_landmarks[5].x) * frame.shape[1] / 2),
                int((left_eye_landmarks[0].y + left_eye_landmarks[5].y) * frame.shape[0] / 2)
            )

            # Get the center of the right eye
            right_eye_center = (
                int((right_eye_landmarks[0].x + right_eye_landmarks[5].x) * frame.shape[1] / 2),
                int((right_eye_landmarks[0].y + right_eye_landmarks[5].y) * frame.shape[0] / 2)
            )

            # Draw a circle at the center of each eye
            cv2.circle(frame, left_eye_center, 5, (0, 255, 0), -1)
            cv2.circle(frame, right_eye_center, 5, (0, 255, 0), -1)

            # Get the coordinates of the pupils
            left_pupil = (
                int(left_eye_landmarks[3].x * frame.shape[1]),
                int(left_eye_landmarks[3].y * frame.shape[0])
            )
            right_pupil = (
                int(right_eye_landmarks[3].x * frame.shape[1]),
                int(right_eye_landmarks[3].y * frame.shape[0])
            )

            # Draw a circle at the center of each pupil
            cv2.circle(frame, left_pupil, 3, (0, 0, 255), -1)
            cv2.circle(frame, right_pupil, 3, (0, 0, 255), -1)

            # Calculate horizontal eye movement (difference in X coordinates)
            eye_movement_horizontal = right_pupil[0] - left_pupil[0]

            # Calculate vertical eye movement (difference in Y coordinates)
            eye_movement_vertical = right_pupil[1] - left_pupil[1]

            # Display eye movement values
            cv2.putText(frame, f'Horizontal: {eye_movement_horizontal}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Vertical: {eye_movement_vertical}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the result
    cv2.imshow('Eye and Pupil Movement Tracking', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()

