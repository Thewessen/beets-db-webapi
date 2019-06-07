from sqlalchemy import (Integer,
                        String,
                        Column,
                        create_engine,
                        DateTime,
                        ForeignKey,
                        func)
from sqlalchemy.orm import (scoped_session,
                            sessionmaker,
                            relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///beets.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Album(Base):
    """NOTE: Only partially representative of actual database table,
    since many fields in it won't be used (at least for now).
    """
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    name = Column('album', String)
    album_artist = Column('albumartist', String)
    year = Column(Integer)
    genre = Column(String)
