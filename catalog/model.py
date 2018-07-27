from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String,DateTime
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

class Family(Base):
    __tablename__ = 'pet_family'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    detail = Column(String)
    picture = Column(String)
    created_at = Column(DateTime, default=datetime.now)


engine = create_engine('postgresql:///catalog')
 

Base.metadata.create_all(engine)
    
