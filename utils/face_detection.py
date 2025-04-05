import cv2
import numpy as np
from PIL import Image

def is_human_face(image):
    """
    Check if the image contains a human face using OpenCV's face detection.
    Checks for both frontal and profile faces.
    
    Args:
        image: PIL Image or path to image
        
    Returns:
        bool: True if a face is detected, False otherwise
    """
    try:
        # Convert PIL Image to OpenCV format
        if isinstance(image, str):
            # It's a file path
            cv_image = cv2.imread(image)
        else:
            # It's a PIL Image
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # Load the face cascade classifiers
        face_cascade_frontal = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        face_cascade_profile = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
        
        # Detect frontal faces
        frontal_faces = face_cascade_frontal.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Detect profile faces
        profile_faces = face_cascade_profile.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Also try with flipped image to detect profiles facing the other direction
        flipped = cv2.flip(gray, 1)
        profile_faces_flipped = face_cascade_profile.detectMultiScale(
            flipped,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Return True if any type of face is detected
        return len(frontal_faces) > 0 or len(profile_faces) > 0 or len(profile_faces_flipped) > 0
    except Exception as e:
        print(f"Error in face detection: {e}")
        return False

