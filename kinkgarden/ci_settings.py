from .settings import *

SECRET_KEY = "insecure"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

DEBUG = True

TEMPLATES[0]["OPTIONS"]["debug"] = True
