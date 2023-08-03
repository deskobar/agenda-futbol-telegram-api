from fastapi import FastAPI

from .graphql import graphql_app
from models import database, metadata, engine

app = FastAPI()
app.include_router(graphql_app, prefix="/api/graphql")


@app.on_event("startup")
async def startup_event():
    try:
        metadata.create_all(engine)
    except Exception as e:  # noqa
        print(e)


@app.on_event("shutdown")
async def shutdown():
    try:
        await database.disconnect()
        pass
    except Exception as e:  # noqa
        print(e)
