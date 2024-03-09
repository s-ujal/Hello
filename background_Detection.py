import cv2
import numpy as np
import os
import sys

def vfx_background_detection(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Define the range of green color in BGR
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([70, 255, 255])

    # Threshold the image to get only green color
    mask = cv2.inRange(img, lower_green, upper_green)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img, img, mask=mask)

    # Set the green color to white in the mask
    mask[np.where((mask > 0))] = 255

    # Find the contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get the largest contour which is the foreground object
    largest_contour = max(contours, key=cv2.contourArea)

    # Get the bounding rectangle around the foreground object
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Crop the foreground object from the original image
    cropped_img = img[y:y+h, x:x+w]

    # Display the result
    cv2.imshow('Original Image', img)
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', cropped_img)

    # If the cropped image has a background, then the original image has been tampered with
    if cv2.countNonZero(mask) < mask.shape[0] * mask.shape[1]:
        print("Image has been tampered with")
    else:
        print("Image is most likely original")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
if __name__ == '__main__':
    image_path = 'F:/HTML'
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import background_Detections  # replace 'first_code' with the actual name of the first code file
    background_Detections.apply_background_detection(image_path)
# image_path = 'path/to/image/captured/by/first/code.png'
# vfx_background_detection(image_path)