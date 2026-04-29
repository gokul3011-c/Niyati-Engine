"""
WSGI Entry Point for Render Deployment
This file is required for Gunicorn to run the Flask app
"""
from api_server import app

if __name__ == "__main__":
    app.run()
