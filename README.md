#  Gallery Website

A lightweight, containerized Python web application for uploading, managing, and displaying image galleries. 

## Features
* **Image Uploading:** Securely upload images directly to the server.
* **Gallery Display:** View uploaded images in a clean, responsive layout.
* **Containerized:** Includes a `Dockerfile` for easy, consistent deployment across any environment.

## Tech Stack
* **Backend:** Python (Flask/FastAPI)
* **Frontend:** HTML, CSS, JavaScript (rendered via `templates/` and `static/`)
* **Deployment:** Docker

##  Project Structure
```text
.
├── static/             # CSS, JavaScript, and static assets
├── templates/          # HTML template files
├── uploads/            # Storage directory for uploaded images
├── app.py              # Main application entry point
├── requirements.txt    # Python dependencies
└── Dockerfile          # Docker configuration for containerization
