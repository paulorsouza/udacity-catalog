from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import desc
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()
engine = create_engine('postgresql:///catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class User(Base):
    __tablename__ = 'user_profile'
    id = Column(Integer, primary_key=True)
    picture = Column(String)
    email = Column(String)
    name = Column(String) 
    created_at = Column(DateTime, default=datetime.now)

    @classmethod
    def get_or_create(cls, name, email, picture):
        user = session.query(User).filter_by(email=email).first()
        if not user:
            user = User(
                name = name,
                picture = picture, 
                email = email)
            session.add(user)
            session.commit()

        return user


class PetFamily(Base):
    __tablename__ = 'pet_family'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    detail = Column(String)
    picture = Column(String)
    created_at = Column(DateTime, default=datetime.now)

    @classmethod
    def create(cls, name, detail, picture):
        family = PetFamily(name=name,
                           detail=detail, 
                           picture=picture)
        session.add(family)
        session.commit()
        return family

    @classmethod
    def all(cls):
        return session.query(PetFamily).all()

class PetType(Base):
    __tablename__ = 'pet_type'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    detail = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    edited_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user_profile.id'))
    user = relationship(User)
    family_id = Column(Integer, ForeignKey('pet_family.id'))
    family = relationship(PetFamily)
    
    @classmethod
    def news(cls):
        return session.query(PetType).order_by(
            desc(PetType.created_at)
        ).limit(10)

    @classmethod
    def create(cls, name, detail, user_id, family_id):
        pet_type = PetType(name=name,
                           detail=detail,
                           user_id=user_id, 
                           family_id=family_id)
        session.add(pet_type)
        session.commit()
        return pet_type

