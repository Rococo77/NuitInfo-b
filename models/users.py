import sqlalchemy
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.types import Boolean

print("SQLAlchemy version:", sqlalchemy.__version__)

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    iswordscloud = Column(Boolean)
    logo = Column(Integer)
    role = Column(String)


engine = create_engine(
    "postgresql+psycopg://postgres:root@localhost/KyoDB_"
)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()