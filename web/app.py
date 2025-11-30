"""
Flask web application for whiteboard to LaTeX conversion.
"""

import os
import sys
import uuid
from flask import Flask, render_template, request, jsonify

# Add parent directory to path to import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.preprocess import preprocess_image
from src.model_infer import Pix2TexModel

# Get the web directory path
web_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize Flask app with template and static folders
app = Flask(
    __name__,
    template_folder=os.path.join(web_dir, 'templates'),
    static_folder=os.path.join(web_dir, 'static')
)

# Get the project root directory (one level up from web/)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.config['UPLOAD_FOLDER'] = os.path.join(project_root, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize model globally (loads once when server starts)
print("Initializing pix2tex model...")
model = Pix2TexModel()


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_image():
    """Process uploaded image and return LaTeX result."""
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP'}), 400
    
    try:
        # Generate unique filename to avoid conflicts
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        unique_id = str(uuid.uuid4())
        input_filename = f"input_{unique_id}.{file_ext}"
        preprocessed_filename = f"preprocessed_{unique_id}.png"
        
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        preprocessed_path = os.path.join(app.config['UPLOAD_FOLDER'], preprocessed_filename)
        
        # Save uploaded file
        file.save(input_path)
        
        # Preprocess image
        preprocess_image(input_path, preprocessed_path)
        
        # Run model inference
        latex_result = model.predict(preprocessed_path)
        
        # Clean up temporary files
        try:
            os.remove(input_path)
            os.remove(preprocessed_path)
        except:
            pass  # Ignore cleanup errors
        
        return jsonify({
            'success': True,
            'latex': latex_result
        })
    
    except Exception as e:
        # Clean up on error
        try:
            if 'input_path' in locals() and os.path.exists(input_path):
                os.remove(input_path)
            if 'preprocessed_path' in locals() and os.path.exists(preprocessed_path):
                os.remove(preprocessed_path)
        except:
            pass
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
