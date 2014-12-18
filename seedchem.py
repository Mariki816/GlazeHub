# from pprint import pprint
import model
import csv


def load_chems(session):
    with open('chemlist121114b.csv', 'rb') as csvfile:
        linereader = csv.reader(csvfile, delimiter=',')

        for row in linereader:
            chem = model.Chem()
            chem.chem_name = row[0]
            chem.quarter = row[1]
            chem.half = row[2]
            chem.onelb = row[3]
            chem.fivelb = row[4]
            chem.tenlb = row[5]
            chem.twentyfivelb = row[6]
            chem.fiftylb = row[7]
            chem.onehundlb = row[8]
            chem.fivehundlb = row[9]
            session.add(chem)
        session.commit()


def load_recipes(session):
    with open('testfiles/recipes.csv', 'rb') as csvfile:
        linereader = csv.reader(csvfile, delimiter=',')

        for row in linereader:
            recipe = model.Recipe()
            recipe.recipe_name = row[0]
            recipe.user_id = row[1]
            recipe.user_notes = row[2]
            session.add(recipe)
        session.commit()


def load_users(session):
    with open('testfiles/usertest.csv', 'rb') as csvfile:
        linereader = csv.reader(csvfile, delimiter=',')

        for row in linereader:
            user = model.User()
            user.user_name = row[0]
            user.email = row[1]
            user.password = row[2]
            session.add(user)
        session.commit()


def load_components(session):
    with open('testfiles/components.csv', 'rb') as csvfile:
        linereader = csv.reader(csvfile, delimiter=',')

        for row in linereader:
            component = model.Component()
            component.chem_id = row[0]
            component.recipe_id = row[1]
            component.percentage = row[2]
            session.add(component)
        session.commit()


def main(session):
# You'll call each of the load_* functions with the session as an argument
    load_chems(session)
    load_recipes(session)
    load_users(session)
    load_components(session)


# load_ratings(session)
if __name__ == "__main__":
    s = model.session
    main(s)
