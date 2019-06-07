import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from beetsdbwebapi.models import Album as AlbumModel
#from beetsdbwebapi.models import db_session


class Album(SQLAlchemyObjectType):
    class Meta:
        model = AlbumModel


class Query(graphene.ObjectType):
    albums = graphene.List(Album, contains=graphene.String())

    def resolve_albums(_, info, contains=None):
        q = Album.get_query(info)
        if contains is not None:
            return q.filter(AlbumModel.name.ilike(f'%{contains}%')).all()
        else:
            return q.all()


schema = graphene.Schema(query=Query)
