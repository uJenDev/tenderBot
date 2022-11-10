from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///tenderbot.db")
Base = declarative_base()

class Customers(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    drinkType = Column(String)
    xPos = Column(String)
    yPos = Column(String)
    date = Column(String)

    def __repr__(self):
        return f"<Customer id={self.id}>"
    
    def __str__(self):
        return f"xPos: {self.xPos} yPos: {self.yPos}"

class Drinks(Base):

    __tablename__ = "drinks"

    id = Column(Integer, primary_key=True)
    buttonLink = Column(Integer)
    name = Column(String, unique=True)
    portions = Column(Integer)
    lastUsed = Column(String)

    def __repr__(self):
        return f"<Drink id={self.id}>"
    
    def __str__(self):
        return f"Name: {self.name} "

Base.metadata.create_all(engine)