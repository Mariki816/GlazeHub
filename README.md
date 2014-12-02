GlazeHub
========

My Glaze Calculator Project

GlazeHub is a specialized tool for ceramic artists to calculate and save glaze recipes. 
Glaze testing, notetaking, getting price quotes of mixed glazes as well as ordering from Clay Planet 
is made simple with this app. 

When a user creates a free account, they can then save their most-used recipes or test 
recipes as well as make notes.

Back end is written in Python. Front end makes use of HTML, CSS, JavaScript, JQuery and Bootstrap.

GlazeHub started out as an idea in January 2014. After a discussion with some ceramic friends about a glaze calculator, we discovered that there is really only one. (http://glazecalculator.com/). It's a neat little site, but there were a few things we or rather I wanted to change.

1. Allow the user to decide how many components were in the glaze.
2. Allow the user to enter in a batch size (kilos or pounds) and the app would calculate the amount of each chemical needed.
3. Allow the user to order their custom glaze from Clay Planet, a clay supply store in Santa Clara

A few things helped, mostly, the other members of this discussion own Clay Planet and they graciously allowed me access to their chemical list and the prices attached to them. (This list is confidential and not saved in this github repository. Because of this, my app will not run on any other machine but my own) Other things that helped were: access to other potters who were interested in using this tool and provided encouragement, experienced glaze mixers who helped me with how to write the calculation formula and a guideline/framework for a minimum viable product.

So here was the framework for that product:

1. Create a calculation page where users could add or subtract components - does not require log in
2. Allow users to save their recipes, but protect them so that they cannot be shared or seen by other users - log in required.
3. Show a price quote from Clay Planet that includes chemical (price rate dependant on weight) and handling
4. Add tax and shipping
5. Send an email to Clay Planet when the customer is ready to order that includes the recipe, weight needed for each chemical, shipping, tax and price quote.


Data Model
========
The first step was to set up my data model using Python. Each object was written as a class and then class particuar methods were written to retrieve data from that class.

![DataModel](/screencaps/GH_datamodel.jpg)

The hardest part for me here was changing the way I thought of a recipe as being the "binding" table. I thought the "one-to-many" should have been set up as one recipe with many components. However, that started getting very complicated by becoming more of a "many-to-many" relationship. After a discussion with and help from an advisor, I came up with the model (see image above).

The chemical object has an id, name and price rates from a quarter pound to 500 lbs. User table object has an id, email, user name and password. Recipe object has an id, reipe name, user id(backref to the User object and user notes. The component object is the 'binding' object in that it relates the chemicals to a recipe as well as a percentage of each component or chemical for that particular recipe.

Once the data model was set up, I used SQLAlchemy queries to write up class methods for retrieving prices, ids, recipe names and such from each table.

Design/UX flow
========
