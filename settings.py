from decouple import config

URL = config("URL")

DATABASE_URL = config("DATABASE_URL", "sqlite:///db/db.sqlite")

REQUEST_TIMEOUT = config("TIMEOUT", 180, cast=int)
