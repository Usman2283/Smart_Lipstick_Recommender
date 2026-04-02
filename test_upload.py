from utils.detect_skin import SkinToneDetector
import os

detector = SkinToneDetector(None)

# Test all images in uploads folder
uploads_folder = "static/uploads"

if os.path.exists(uploads_folder):
    for filename in os.listdir(uploads_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(uploads_folder, filename)
            print(f"\nTesting: {filename}")
            result = detector.detect_skin_tone(filepath)
            print(f"Skin tone index: {result}")
else:
    print(f"Folder {uploads_folder} doesn't exist!")