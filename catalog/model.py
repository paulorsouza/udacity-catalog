from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String,DateTime,ForeignKey
from sqlalchemy import desc
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user_profile'
    id = Column(Integer, primary_key=True)
    picture = Column(String)
    email = Column(String)
    name = Column(String) 
    created_at = Column(DateTime, default=datetime.now)

class PetFamily(Base):
    __tablename__ = 'pet_family'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    detail = Column(String)
    picture = Column(String)
    created_at = Column(DateTime, default=datetime.now)

class PetType(Base):
    __tablename__ = 'pet_type'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    detail = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    edited_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user_profile.id'))
    user = relationship('User')
    family_id = Column(Integer, ForeignKey('pet_family.id'))
    family = relationship(PetFamily, back_populates='pet_type')


engine = create_engine('postgresql:///catalog')
 

Base.metadata.create_all(engine)
    
