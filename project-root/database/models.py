from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ServerSetting(Base):
    __tablename__ = 'server_settings'

    server_id = Column(Integer, primary_key=True)
    default_prefix = Column(String(255), nullable=False, default='!')
    default_source = Column(String(255), nullable=False, default='youtube')
    allowed_sources = Column(String(255), nullable=False, default='youtube,spotify,soundcloud')

    playlists = relationship("Playlist", backref="server_setting")

class Playlist(Base):
    __tablename__ = 'playlists'

    server_id = Column(Integer, ForeignKey('server_settings.server_id'), primary_key=True)
    name = Column(String(255), nullable=False, primary_key=True)
    songs = Column(String, nullable=False)

    server_setting = relationship("ServerSetting", backref="playlists")