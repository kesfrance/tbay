#!/usr/bin/python3
#
# @author Francis Kessie
#
# tbay.py
#
"""A modelling the backend of an auction web application using sqlachemy"""
#
#TO DOs
#Create User, Bid and Item classes
#Model the relationships between the three classes as follows
#Users should be able to auction multiple items
#Users should be able to bid on multiple items
#Multiple users should be able to place a bid on an item



from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

engine = create_engine('postgresql://francis:YXZ@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)    
    items = relationship("Item", backref="user")
    bids = relationship("Bid", backref="user")
    
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    bids = relationship("Bid", backref="items")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

class Bid(Base):
    __tablename__ = "bid"
    
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False) 
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)     
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

#create three users
alex = User(username="Alexander Hoper", password="Alex20")
kesfrance = User(username="Francis Kessie", password="kessie2")
joe = User(username="Joe Blogger", password="joe15")


#user alex has auctioned a baseball and a TV
ball = Item(name="Baseball", description="A black baseball", user=alex)
tvblack = Item(name="Sumsung HD4TV", description="A slim sumsung TV")
alex.items.append(tvblack)

#users joe and kesfrance have placed bids on the baseball as follows
joe_bid = Bid(price =16.0, items =ball, user = joe)
kesfrance_bid = Bid(price=18.0, items =ball, user = kesfrance)


session.add_all([alex, kesfrance, joe, ball, tvblack, joe_bid])
session.commit()   
    
#User.id==Address.user_id

#Perform a query to find out which user placed the highest bid
hb = session.query(User.username, Bid.price).join(Bid, Item).filter(Item.name =="Baseball").order_by(Bid.price).all()
print("{0[0]}: placed the highest bid of ${0[1]}".format(hb[-1]))


