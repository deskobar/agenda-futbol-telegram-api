from strawberry.fastapi import GraphQLRouter

from api.graphql.schema import schema

graphql_app = GraphQLRouter(schema)
