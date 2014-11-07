from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Float, String
from sqlalchemy.orm import sessionmaker

ENGINE = None
Session = None


Base = declarative_base()

class Chem(Base):
	__tablename__ = "chemicals"
	id = Column(String(120), primary_key = True)
	quarter = Column(Float)
	half = Column(Float)
	onelb = Column(Float)
	fivelb = Column(Float)
	tenlb = Column(Float)
	twentyfivelb = Column(Float)
	fiftylb = Column(Float)
	onehundlb = Column(Float)
	fivehundlb = Column(Float)
	fivehundpluslb = Column(Float)


def connect():
	global ENGINE

	ENGINE = create_engine("sqlite:///chemicals.db", echo = True)
	Session = sessionmaker(bind = ENGINE)

	return Session()

def main():
	"""In case we need this"""
	pass

	if __name__ == "__main)__":
		main()