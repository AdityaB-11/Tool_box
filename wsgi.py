import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask application from application.py
from application import app

if __name__ == "__main__":
    app.run() 