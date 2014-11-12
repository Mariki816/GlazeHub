from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import Column, Float, String, Integer
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship, backref

# import model

# ENGINE = None
# Session = None

engine = create_engine("sqlite:///glazehub.db", echo = False)
session = scoped_session(sessionmaker(bind = engine, autocommit = False, autoflush = False))


Base = declarative_base()
Base.query = session.query_property()




#Class declarations

#This is the CP chemical database and a few functions for the class itself
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

	@classmethod
	def getChemNameByID(cls,chemID):
		return session.query(Chem).get(chemID).chem_name

	@classmethod
	def getChemIDbyName(cls,chemNAME):
		return session.query(Chem).get(chemNAME).id


#This is the table of users
class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key = True)
	user_name = Column(String(64), nullable = False)
	email = Column(String(64), nullable = False)
	password = Column(String(64), nullable = False)

	@classmethod
	def getUserID(cls):
		return session.query(User).get(id)

	@classmethod
	def getUserByEmail(cls, email):
		return session.query(User).filter_by(email=email).first()

	@classmethod
	def getUserNameByID(cls, id):
		return session.query(User).filter_by(id = id).first()

	@classmethod
	def getUserPasswordByEmail(cls,email):
		return session.query(User).filter_by(email=email).first().password


#This is the table of recipes.
class Recipe(Base):
	__tablename__ = "recipes"
	id = Column(Integer, primary_key = True)
	recipe_name = Column(String (120))
	user_id = Column(Integer, ForeignKey('users.id'))

	user = relationship("User", backref = backref("recipes", order_by=id))

	@classmethod
	def getRecipeNamesByUserID(cls, user_id):
		return session.query(Recipe).filter_by(user_id = user_id).all()

	@classmethod
	def getRecipeIDByName(cls, recipe_name, user_id):
		return session.query(Recipe).filter_by(recipe_name=recipe_name).filter_by(user_id = user_id)


#This is the table of Components
class Component(Base):
	__tablename__ = "components"
	id = Column(Integer, primary_key = True)
	chem_id = Column(Integer, ForeignKey('chemicals.id'), nullable = False)
	recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable = False)
	percentage = Column(Float, nullable = False)

	chem = relationship("Chem", backref = backref("components", order_by=id))
	recipe = relationship("Recipe", backref = backref("components", order_by=id))


def getComponentsByRecipeID(recipeID):
	components = session.query(Component).filter_by(recipe_id = recipeID).all()

	for comp in components:
		compName = getChemNameByID(comp.chem_id)
		compPercent = comp.percentage
		compChemID= getChemIDbyName(compName)

	return compName, compPercent, compChemID

# def connect():
# 	global ENGINE

# 	ENGINE = create_engine("sqlite:///chemicals.db", echo = True)
# 	Session = sessionmaker(bind = ENGINE)

# 	return Session()




# def getUserNameByID(userID):
# 	#testing if I can get the user right
# 	user = session.query(User).get(userID)
# 	# print user.user_name


# def getUserIDByEmail(userEmail):
# 	print "This is userEmail", userEmail
# 	user = session.query(User).filter_by(email=userEmail).first()
# 	if not user:
# 		print "List is empty"

# 	else:
# 		print "This is user", user
# 		print "This is user.id", user.id
# 		return user.id

	#create function to add new User

# def addNewUser(newUserName, newUserEmail, newUserPassword):
# 	print "This is newUserEmail", newUserEmail
# 	newUser = model.User()
# 	newUser.user_name = newUserName
# 	newUser.email = newUserEmail
# 	newUser.password = newUserPassword

# 	return newUser


# def getRecipesByUserID(userID):
# 	# user = model.session.query(model.User).get(user_id)

# 	recipenames = session.query(Recipe).filter_by(user_id=userID).all()

# 	# for rname in recipenames:
# 		# print rname.recipe_name
# 		# getComponentsByRecipeID(rname.id)

# 	return recipenames

# def getChemNameByID(chemID):
# 	chemName = session.query(Chem).get(chemID).chem_name
# 	return chemName



# def getChemIDbyName(chemNAME):
# 	chems=session.query(Chem)
# 	for c in chems:
# 		if c.chem_name == chemNAME:
# 			chemID = c.id

# 	return chemID

# def getRecipeIDByName(userID, recipename):
# 	recipes = session.query(Recipe).filter_by(user_id = userID).all()

# 	for recipe in recipes:
# 		if recipes.recipe_name == recipename:
# 			recipeID = recipes.id

# 	return recipeID


		# print "This is compChemID", compChemID, compName



def main():
	"""In case we need this"""
	pass

	if __name__ == "__main)__":
		main()