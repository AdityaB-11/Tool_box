import os
from ..config.config import ALLOWED_EXTENSIONS

# Create a fixed uploads directory in the project folder
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'uploads')

# Ensure uploads directory exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    print(f"Created uploads directory at: {UPLOAD_DIR}")

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_extension(filename):
    """Get the extension of a file"""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else '' 