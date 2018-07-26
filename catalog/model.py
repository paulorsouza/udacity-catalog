from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy import desc
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'provider_user'
    id = Column(Integer, primary_key=True)
    picture = Column(String)
    email = Column(String)
    name = Column(String) 
    provider = Column(String)
    inserted_at = Column(DateTime, default=datetime.now)


engine = create_engine('postgresql:///catalog')
 

Base.metadata.create_all(engine)
    
