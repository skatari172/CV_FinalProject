"""
Flask web application for whiteboard to LaTeX conversion.
This handles the web interface - serving the HTML page and processing image uploads.
"""

# Standard library imports
import os  # File system operations
import sys  # Path manipulation
import uuid  # Generate unique filenames for uploads

# Flask imports - framework for building the web API
from flask import Flask, render_template, request, jsonify

# Import our core processing modules and cv model
from src.preprocess import preprocess_image
from src.model_infer import Pix2TexModel

# Add parent directory to Python path so we can import from src/
# This is needed because Flask app is in web/ subdirectory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Get paths for Flask configuration
web_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create Flask app and tell it where to find HTML templates and CSS/JS files
app = Flask(
    __name__,
    template_folder=os.path.join(web_dir, 'templates'),
    static_folder=os.path.join(web_dir, 'static')
)

# Configure where to store uploaded images
app.config['UPLOAD_FOLDER'] = os.path.join(project_root, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Create uploads folder if it doesn't exist yet
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the model once when server starts - this takes time, so we do it once
# The same model instance is reused for all requests (much faster)
print("Initializing pix2tex model...")
model = Pix2TexModel()


def allowed_file(filename):
    """
    Check if the uploaded file has an allowed image extension.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """
    Serve the main web page - the HTML with upload form and result display.
    """
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_image():
    """
    Handle image upload and processing.
    This is the API endpoint that the frontend calls when user clicks "Process Image".
    Returns JSON with either the LaTeX result or an error message.
    """
    # Check that an image file was actually uploaded
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    # Make sure user selected a file (not just an empty form)
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Verify it's a supported image type
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP'}), 400
    
    try:
        # Generate unique filenames using UUID so multiple users can upload simultaneously
        # without overwriting each other's files
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        unique_id = str(uuid.uuid4())
        input_filename = f"input_{unique_id}.{file_ext}"
        preprocessed_filename = f"preprocessed_{unique_id}.png"
        
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        preprocessed_path = os.path.join(app.config['UPLOAD_FOLDER'], preprocessed_filename)
        
        # Save the uploaded file to disk
        file.save(input_path)
        
        # Step 1: Clean up and enhance the image (grayscale, blur, contrast, deskew, resize)
        preprocess_image(input_path, preprocessed_path)
        
        # Step 2: Run the pic2text model to convert image to LaTeX text
        latex_result = model.predict(preprocessed_path)
        
        # Delete temporary files to save disk space
        try:
            os.remove(input_path)
            os.remove(preprocessed_path)
        except:
            pass  # If cleanup fails, it's not critical - just continue
        
        # Send success response with the LaTeX code
        return jsonify({
            'success': True,
            'latex': latex_result
        })
    
    except Exception as e:
        # If anything goes wrong, try to clean up files and return error message
        try:
            if 'input_path' in locals() and os.path.exists(input_path):
                os.remove(input_path)
            if 'preprocessed_path' in locals() and os.path.exists(preprocessed_path):
                os.remove(preprocessed_path)
        except:
            pass
        
        # Return error response with details
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

#when app is ran, init the flask server on port 5001, discoverable on local network ip
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
