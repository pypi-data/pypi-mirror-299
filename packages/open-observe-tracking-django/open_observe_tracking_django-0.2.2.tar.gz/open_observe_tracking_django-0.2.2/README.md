# Django Celery Logging with OpenObserve

This Django project provides middleware and utilities for logging request/response cycles, exceptions, and custom logs to an external logging system (OpenObserve) asynchronously using Celery.

## Features
- **Request and Response Logging**: Logs details of every request and response.
- **Exception Logging**: Logs unhandled exceptions during requests.
- **Custom Logging**: Allows developers to log custom information with different log levels.
- **Asynchronous Logging**: Uses Celery to send logs asynchronously, ensuring no delay in the request/response cycle.
  
## Requirements
- Django
- Celery
- OpenObserve account (for external log tracking)

## Installation (when using the library in a django project)

### 1. Install Package

Install the required dependencies with:

    pip install open_observe_tracking_django

### 2. Configure Celery in Django

Create a `celery.py` file in the Django project directory (where `settings.py` is located):

Note: Change mysite.settings to your_django_project_name.settings


    # mysite/mysite/celery.py


    import os
    from pathlib import Path
    from celery import Celery
    from django.conf import settings


    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

        # SETUP CELERY 
        # Create the folder if not exists
        app = Celery( __name__)
        app.config_from_object('django.conf:settings',namespace='CELERY')

        if settings.BROKER_DATA_FOLDER:
          path = Path(settings.BROKER_DATA_FOLDER)
          if not path.exists():
              path.mkdir(parents=True, exist_ok=True)
        # Load tasks from all registered Django app configs.
        app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


Modify `__init__.py` in the same folder to import Celery:

    # mysite/mysite/__init__.py

    from .celery import app as celery_app

    __all__ = ('celery_app',)

### 3. Configure Celery in `settings.py` 

Add the following configurations to your `settings.py`:

    # Celery Configuration
    CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Redis as the broker
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

Or this if you want to use filesystem as brocker

    # Celery Configuration
    BROKER_DATA_FOLDER = './.data/broker'
    BROKER_DATA_FOLDER_PATH = Path(BROKER_DATA_FOLDER)
    if not BROKER_DATA_FOLDER_PATH.exists():
        BROKER_DATA_FOLDER_PATH.mkdir(parents=True, exist_ok=True)

    CELERY_BROKER_URL = 'filesystem://'
    CELERY_BROKER_TRANSPORT_OPTIONS = {
        'data_folder_in': BROKER_DATA_FOLDER,
        'data_folder_out':BROKER_DATA_FOLDER,
    }



### 4. Set Up OpenObserve

Create a logging configuration for OpenObserve in the `settings.py` file:

Note: Set open_observe_stream_name as your app name, this will be the identifier in open observe

    # Open observe
    OPENOBSERVE_CONFIG = {
      "open_observe_host":"http(s)://open_observe_host:port",
      "open_observe_organization_name":'development-dev',
      "username":'your_user_name',
      "password":'password',
      "open_observe_stream_name":"app_name",
    }

### 5. Create a Logging Middleware

The middleware automatically logs each request and response, as well as unhandled exceptions:

    # Add OpenObserveTrackingMiddleware to your MIDDLEWARE list in settings.py
    MIDDLEWARE = [
        'open_observe_tracking_django.OpenObserveTrackingMiddleware', # Put as the first one so all requests are logged
        # Other middleware...
    ]


### 6. Custom Logging

You can log custom information in your views using the `log_to_open_observe` function:

    # In your views.py

    from open_observe_tracking_django import log_to_open_observe, LogLevel

    def my_view(request):
        info = {"user_action": "Login attempt", "username": "example_user"}
        log_to_open_observe(request, LogLevel.INFO, info)
        return HttpResponse("Logging Test")

### 8. Start Celery

Ensure your brocker is running, if  other than filesystem is being used. You can start the Celery worker to handle asynchronous tasks using: (mysite is the name of the django project)

    celery -A mysite worker --loglevel=info 

### 9. Running the Django Application

Run the Django application with:

    python manage.py runserver

## Usage

After setting up the project, logs from request/response cycles, exceptions, and custom logs will be sent to OpenObserve asynchronously using Celery.

You can monitor the logs on your OpenObserve dashboard.


## Modify the library
Edit the code, build the library with 
```bash
python setup.py sdist bdist_wheel
```
