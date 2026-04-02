from flask import Flask, request, render_template, jsonify
import os
from werkzeug.utils import secure_filename
from utils.detect_skin import SkinToneDetector

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload directory exists
#os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize skin tone detector
detector = SkinToneDetector('model/skin_tone_model.h5')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Lipstick recommendations based on skin tone
LIPSTICK_RECOMMENDATIONS = {
    0: {  # Fair Skin Tone
        'category': 'Fair',
        'shades': [
            {'name': 'Soft Pink', 'code': '#FFB6C1', 'description': 'Natural everyday look'},
            {'name': 'Coral', 'code': '#FF7F50', 'description': 'Warm and vibrant'},
            {'name': 'Rose', 'code': '#FF007F', 'description': 'Classic romantic shade'},
            {'name': 'Nude', 'code': '#E8B5B5', 'description': 'Subtle and elegant'}
        ]
    },
    1: {  # Medium Skin Tone
        'category': 'Medium',
        'shades': [
            {'name': 'Berry', 'code': '#8B008B', 'description': 'Rich and bold'},
            {'name': 'Mauve', 'code': '#B284BE', 'description': 'Sophisticated plum'},
            {'name': 'Terracotta', 'code': '#E2725B', 'description': 'Warm earth tone'},
            {'name': 'Cherry Red', 'code': '#DE3163', 'description': 'Classic statement'}
        ]
    },
    2: {  # Dark Skin Tone
        'category': 'Dark',
        'shades': [
            {'name': 'Deep Plum', 'code': '#4A0022', 'description': 'Bold and dramatic'},
            {'name': 'Burgundy', 'code': '#8B0000', 'description': 'Rich wine shade'},
            {'name': 'Chocolate', 'code': '#7B3F00', 'description': 'Warm and deep'},
            {'name': 'Raspberry', 'code': '#D21F3C', 'description': 'Vibrant berry'}
        ]
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # DEBUG: Print the file path
        print(f"Processing image: {filepath}")
        
        # Detect skin tone
        skin_tone = detector.detect_skin_tone(filepath)
        
        # DEBUG: Print what the detector returned
        print(f"Detected skin_tone value: {skin_tone}")
        
        if skin_tone is not None:
            recommendations = LIPSTICK_RECOMMENDATIONS.get(skin_tone, LIPSTICK_RECOMMENDATIONS[1])
            print(f"Using category: {recommendations['category']}")  # DEBUG
            print(f"Skin tone index: {skin_tone}")  # DEBUG
            
            return jsonify({
                'success': True,
                'skin_tone': recommendations['category'],
                'tone_index': int(skin_tone),
                'recommendations': recommendations['shades'],
                'image_path': filepath
            })
        else:
            print("Skin tone detection returned None!")  # DEBUG
            return jsonify({'error': 'Could not detect skin tone. Please try another image.'}), 400
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)