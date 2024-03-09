import cv2
import numpy as np

def is_face_present(binary_data):
    try:
         # Convert binary data to numpy array
        buffer = np.frombuffer(binary_data, dtype=np.uint8)

        # Debug: print the binary data (optional)
        print("Binary Data:", buffer)
        print("Binary Data Length:", len(buffer))

        try:
            image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
            if image is None or image.size == 0:
                print("Invalid image data.")
                return False
        except Exception as e:
            print(f"Error decoding image: {e}")
            return False
                # Debug: print the decoded image (optional)
        print("Decoded Image Shape:", image.shape)
        # Check if the image is valid
        if image is None or image.size == 0:
            print("Invalid image data.")
            return False

        # Convert the image to grayscale
        gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Perform face detection or any other processing
        # Load the Haarcascades classifier for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        # Return True if at least one face is detected, otherwise False
        return len(faces) > 0
            # ...

    except Exception as e:
        print(f"Error processing image: {e}")
        return False
