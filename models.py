import databases
import sqlalchemy
import ormar

from settings import DATABASE_URL

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


class Alias(ormar.Model):
    ormar_config = ormar.OrmarConfig(
        database=database,
        metadata=metadata,
        tablename="alias",
    )

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    user_id: str = ormar.String(max_length=100)
    team_name: str = ormar.String(max_length=100)
    alias: str = ormar.String(max_length=100)


engine = sqlalchemy.create_engine(DATABASE_URL)
