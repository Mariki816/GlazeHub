from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import Column, Float, String, Integer
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship, backref

# ENGINE = None
# Session = None

engine = create_engine("sqlite:///glazehub.db", echo = False)
session = scoped_session(sessionmaker(bind = engine, autocommit = False, autoflush = False))


Base = declarative_base()
Base.query = session.query_property()




#Class declarations
class Chem(Base):
	__tablename__ = "chemicals"
	id = Column(Integer, primary_key = True)
	chem_name = Column(String(120))
	quarter = Column(Float)
	half = Column(Float)
	onelb = Column(Float)
	fivelb = Column(Float)
	tenlb = Column(Float)
	twentyfivelb = Column(Float)
	fiftylb = Column(Float)
	onehundlb = Column(Float)
	fivehundlb = Column(Float)

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key = True)
	user_name = Column(String(64), nullable = False)
	email = Column(String(64), nullable = False)
	password = Column(String(64), nullable = False)

class Recipe(Base):
	__tablename__ = "recipes"
	id = Column(Integer, primary_key = True)
	recipe_name = Column(String (120))
	user_id = Column(Integer, ForeignKey('users.id'))

	user = relationship("User", backref = backref("recipes", order_by=id))

class Component(Base):
	__tablename__ = "components"
	id = Column(Integer, primary_key = True)
	chem_id = Column(Integer, ForeignKey('chemicals.id'), nullable = False)
	recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable = False)
	percentage = Column(Float, nullable = False)

	chem = relationship("Chem", backref = backref("components", order_by=id))
	recipe = relationship("Recipe", backref = backref("components", order_by=id))


# def connect():
# 	global ENGINE

# 	ENGINE = create_engine("sqlite:///chemicals.db", echo = True)
# 	Session = sessionmaker(bind = ENGINE)

# 	return Session()



def main():
	"""In case we need this"""
	pass

	if __name__ == "__main)__":
		main()