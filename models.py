import databases
import orm
from settings import DATABASE_URL

database = databases.Database(DATABASE_URL)
models = orm.ModelRegistry(database=database)


class Alias(orm.Model):
    tablename = "alias"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "user_id": orm.String(max_length=100),
        "team_name": orm.String(max_length=100),
        "alias": orm.String(max_length=100),
    }
