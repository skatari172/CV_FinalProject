"""
Web application entry point.
Run this file to start the Flask web server.

Usage: python app.py
Then open http://localhost:5001 in your browser.
"""

# Import the Flask app instance from the web module
from web.app import app

# Only run the server if this file is executed directly (not imported)
if __name__ == '__main__':
    # Start Flask development server
    app.run(debug=True, host='0.0.0.0', port=5001)
