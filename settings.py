from decouple import config

URL = config("URL")

DATABASE_URL = config("DATABASE_URL", "sqlite:///db/db.sqlite")
