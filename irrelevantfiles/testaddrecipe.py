import model










def main():
	# newRecipe = model.Recipe()
	# newRecipe.recipe_name = "Naked Raku"
	# newRecipe.user_id = 1
	# model.session.add(newRecipe)
	# model.session.commit()

	r = model.session.query(model.Recipe).filter_by(recipe_name="Naked Raku").first()
	print r.components

	newComp = model.Component()
	newComp.chem_id = 72
	newComp.percentage = 25
	r.components.append(newComp)
	print r.components[-1].chem_id
	print newComp
	# model.session.commit()

	print newComp.recipe_id

if __name__ == "__main__":
	main()