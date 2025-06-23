# Music Generation API Backend

This is a Django-based backend server designed to support a music generation application. It provides an API to handle song creation requests, which can include both textual descriptions and uploaded audio files.

## Features

-   **CSRF Protection**: Securely handles requests from the frontend using Django's CSRF middleware.
-   **File Uploads**: Accepts multipart/form-data requests to upload audio files.
-   **Request Processing**: Handles POST requests at `/api/create/` to process song descriptions and audio files.
-   **Media File Management**: Saves uploaded audio files to the `/uploads/` directory with unique filenames to prevent conflicts.
-   **API Responses**: Returns structured JSON data upon successful creation, including the new song's ID, name, and a publicly accessible URL.

## Prerequisites

-   Python (3.12 or newer recommended)
-   pip (Python's package installer)

## Setup and Installation

1.  **Clone the repository:**

2.  **Create and activate a virtual environment:**

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    ```bash
    python3 manage.py migrate
    ```

## Configuration

For the backend to work correctly with the frontend, ensure you have the following configurations in your `settings.py`:

1.  **Add `corsheaders` to `INSTALLED_APPS`:**
    ```python
    INSTALLED_APPS = [
        # ... other apps
        'corsheaders',
        'rest_framework',
    ]
    ```

2.  **Configure CORS Middleware:**
    ```python
    MIDDLEWARE = [
        # ...
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        # ...
    ]
    ```

3.  **Set allowed origins for CORS:**
    This allows your frontend (running on port 8081) to communicate with the backend.
    ```python
    CORS_ALLOWED_ORIGINS = [
        'http://127.0.0.1:8081',
    ]
    CORS_ALLOW_CREDENTIALS = True # Important for handling cookies like CSRF
    ```

4.  **Configure Media Files for Uploads:**
    At the end of your `settings.py`, add:
    ```python
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    ```

5.  **Serve Media Files in Development:**
    In your main project's `urls.py` , add the following to serve media files when `DEBUG` is `True`:
    ```python
    from django.conf import settings
    from django.conf.urls.static import static

    # ... your other urlpatterns
    
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    ```

## Running the Server

-   Start the development server with the following command:
    ```bash
    python3 manage.py runserver 8000
    ```
-   The API will be available at `http://localhost:8000`.

