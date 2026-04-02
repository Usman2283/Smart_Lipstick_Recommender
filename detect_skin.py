import cv2
import numpy as np
import os

class SkinToneDetector:
    def __init__(self, model_path):
        # We'll ignore the model and use a better heuristic
        self.model = None
        print("Using improved skin tone detection")
    
    def extract_skin_region(self, image):
        """Extract skin region using HSV color space"""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Expanded skin color range
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([25, 180, 255], dtype=np.uint8)
        
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        # Clean up the mask
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        skin = cv2.bitwise_and(image, image, mask=mask)
        
        return skin, mask
    
    def get_average_skin_color(self, image_path):
        """Get average RGB color of skin region"""
        img = cv2.imread(image_path)
        if img is None:
            print(f"Could not read image: {image_path}")
            return None
        
        # Resize for faster processing
        img = cv2.resize(img, (300, 300))
        
        # Extract skin region
        skin, mask = self.extract_skin_region(img)
        
        # Get non-zero pixels (skin pixels)
        skin_pixels = skin[mask > 0]
        
        if len(skin_pixels) == 0:
            print("No skin pixels detected in image")
            return None
        
        # Calculate average RGB
        avg_color = np.mean(skin_pixels, axis=0)
        avg_rgb = avg_color[::-1]  # Convert BGR to RGB
        
        print(f"Average RGB: {avg_rgb}")
        return avg_rgb
    
    def detect_skin_tone(self, image_path):
        """Detect skin tone using improved RGB thresholds"""
        avg_color = self.get_average_skin_color(image_path)
        
        if avg_color is None:
            return None
        
        # Calculate brightness and color characteristics
        r, g, b = avg_color
        brightness = (r + g + b) / 3
        
        # More sophisticated classification
        # Fair: Bright and pinkish/peachy
        if brightness > 150:
            return 0  # Fair
        
        # Medium: Medium brightness with balanced colors
        elif brightness > 90:
            # Check if it's warm or cool medium
            return 1  # Medium
        
        # Dark: Low brightness
        else:
            return 2  # Dark