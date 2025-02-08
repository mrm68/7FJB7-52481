from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from django.conf import settings

Base = declarative_base()

class User(Base):
    __tablename__ = 'auth_user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('auth_user.id'))
    seats_reserved = Column(Integer)
    cost = Column(Integer)
    user = relationship('User', back_populates='reservations')

User.reservations = relationship('Reservation', order_by=Reservation.id, back_populates='user')

# Create an engine and session
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables only if they do not exist
Base.metadata.create_all(engine, checkfirst=True)
