import databases
import sqlalchemy
import ormar

from settings import DATABASE_URL

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Alias(ormar.Model):
    class Meta(BaseMeta):
        tablename = "alias"

    id: int = ormar.Integer(primary_key=True)
    user_id: str = ormar.String(max_length=100)
    team_name: str = ormar.String(max_length=100)
    alias: str = ormar.String(max_length=100)


engine = sqlalchemy.create_engine(DATABASE_URL)
