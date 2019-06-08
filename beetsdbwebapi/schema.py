import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from beetsdbwebapi.models import Album as AlbumModel
from beetsdbwebapi.models import db_session


class Album(SQLAlchemyObjectType):
    class Meta:
        model = AlbumModel


class UpdateAlbum(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        genre = graphene.String()
        year = graphene.String()
        album_artist = graphene.String()

    success = graphene.Boolean()
    album_before = graphene.Field(lambda: Album)
    album = graphene.Field(lambda: Album)

    def mutate(self,
               info,
               id,
               name=None,
               genre=None,
               year=None,
               album_artist=None):
        q = Album.get_query(info)
        album = q.filter(AlbumModel.id == id).first()
        album_before = AlbumModel(id=id,
                                  name=album.name,
                                  genre=album.genre,
                                  year=album.year,
                                  album_artist=album.album_artist)
        if name is not None:
            album.name = name
        if genre is not None:
            album.genre = genre
        if year is not None:
            album.year = year
        if album_artist is not None:
            album.album_artist = album_artist
        
        db_session.add(album)
        db_session.commit()
        success = True
        return UpdateAlbum(success=success, album_before=album_before, album=album)


class Query(graphene.ObjectType):
    albums = graphene.List(Album, contains=graphene.String())

    def resolve_albums(_, info, contains=None):
        q = Album.get_query(info)
        if contains is not None:
            return q.filter(AlbumModel.name.ilike(f'%{contains}%')).all()
        else:
            return q.all()

class Mutation(graphene.ObjectType):
    album = UpdateAlbum.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
