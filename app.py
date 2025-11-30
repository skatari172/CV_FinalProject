"""
Web application entry point.
Run this file to start the Flask web server.
"""

from web.app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
