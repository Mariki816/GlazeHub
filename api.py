import model

def listChemNames():
	chems = model.session.query(model.Chem).all()
	chemicalNames = [chem.chem_name for chem in chems]
	return chemicalNames