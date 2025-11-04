# RECIPE FINDER

#### Description:

### INSPIRATION
One day I come home, and i opened my refrigerator, and i found the ingredients but not the food, so i decided to make a web application that will that will help people like me to find the recipes and make the food.

### Template folder
#### layout.html
This is the main html page that will be used in other html pages as well. It has a nav bar that shows the main option like saved, recipe finder, create your own (only if the user is logged in else it will show login and register options)

#### register.html
This is the html page that will take input email and password and password confirmation to register the user and store the user into the database, the form has an attribute action that will trigger the register route in the backend.

#### register route in app.py
This route has a method name register and it takes email, password, confirmation and store them in a variable. It then checks whether the couumns of the form is filled or not, if empty it returns an error.
Then it checks whether the password is matching the confirmation password or not, it then checks if the user has submitted the valid email or not. And after that it selects the email from the database and if the result of the select statement is empty it registers the user by inserting the credentials into the database. And after Registering it will render the home page of the recipe finder

#### login.html
This is the html page that will take input email and password to login the user, the form has an attribute action that will trigger the login route in the backend.

#### login route in app.py
This route has a method named login, that will forget any user_id if already there, it then checks whether the email and password is submitted or not, if submitted it will check if the email and the password provided correct or not, and it will set the session userid to remeber which user logged in and then will redirect to the homepage

#### logout route in app.py
This route will be triggered when the logout option is clicked from the navbar and when it is clicked it will clear the session (forget any user_id) and will redirect to the homepage that will redirect to the login page

#### index.html
This html page is the homepage of the recipe finder and it shows the cards (like vegetarian, non vegetarian, dessert, breakfast, saved, recipe finder, create your own ) each connected with its own routes and the own methods, which when clicked will trigger it.

#### vegetarian route in app.py
When this route is triggered the vegetarian recipes will be shown.

It has a function named vegetarian and inside it we have stored the url which will be used to search the recipes based on the parameters which is also stored on the different variable that parameter variable contains diet as vegetarian, number as 6 (number of recipes to be searched), and the api key which will be used to search the recipes. After getting the result we will have a different url that will get us the detailed recipes of the result we get with the help of recipe id which we got from the above result.
And if everything goes well we will render vegetarian.html with detailed recipes as arguments that will show the recipes to the users.

#### vegetarian.html
This html page will show the detailed vegetarian recipes according to the parameters defined in the vegetarian function in app.py . The recipes will be shown in the form of cards and each recipe will contain a saved button which when clicked that particular recipe will be saved on the saved section.

#### non_vegetarian route in app.py
When this route is triggered the non vegetarian recipes will be shown.

It has a function named non_vegetarian and inside it we have stored the url which will be used to search the recipes based on the parameters which is also stored on the different variable that parameter variable contains includeIngredients as chicken, pork, fish, number as 6 (number of recipes to be searched), and the api key which will be used to search the recipes. After getting the result we will have a different url that will get us the detailed recipes of the result we get with the help of recipe id which we got from the above result.
And if everything goes well we will render non_vegetarian.html with detailed recipes as arguments that will show the recipes to the users.

#### non_vegetarian.html
This html page will show the detailed non_vegetarian recipes according to the parameters defined in the non_vegetarian function in app.py . The recipes will be shown in the form of cards and each recipe will contain a saved button which when clicked that particular recipe will be saved on the saved section.

#### dessert route in app.py
When this route is triggered the dessert recipes will be shown.

It has a function named dessert and inside it we have stored the url which will be used to search the recipes based on the parameters which is also stored on the different variable that parameter variable contains type as dessert, number as 6 (number of recipes to be searched), and the api key which will be used to search the recipes. After getting the result we will have a different url that will get us the detailed recipes of the result we get with the help of recipe id which we got from the above result.
And if everything goes well we will render dessert.html with detailed recipes as arguments that will show the recipes to the users.

#### dessert.html
This html page will show the detailed dessert recipes according to the parameters defined in the dessert function in app.py . The recipes will be shown in the form of cards and each recipe will contain a saved button which when clicked that particular recipe will be saved on the saved section.

#### breakfast route in app.py
When this route is triggered the breakfast recipes will be shown.

It has a function named breakfast and inside it we have stored the url which will be used to search the recipes based on the parameters which is also stored on the different variable that parameter variable contains type as breakfast, number as 6 (number of recipes to be searched), and the api key which will be used to search the recipes. After getting the result we will have a different url that will get us the detailed recipes of the result we get with the help of recipe id which we got from the above result.
And if everything goes well we will render breakfast.html with detailed recipes as arguments that will show the recipes to the users.

#### breakfast.html
This html page will show the detailed breakfast recipes according to the parameters defined in the breakfast function in app.py . The recipes will be shown in the form of cards and each recipe will contain a saved button which when clicked that particular recipe will be saved on the saved section.

#### saved route in app.py
When this route is triggered the saved recipes will be shown.

This route has a function named saved which will first get user_id and the recipe_id and then store the recipe_id according to the user_id in the database. It will then get the detailed recipe from the recipe_id using the url, and store it in the saved_recipe and will render the saved.html and pass the saved_recipe as the argument

#### saved.html
This html page will show the detailed saved recipes. The recipes will be shown in the form of cards and each recipe will contain a unsave recipe button which when clicked that particular recipe will be unsaved from the saved section.

#### unsave route in app.py
When this route is triggered the saved recipes will be shown.

This route has a function named unsave_recipe which will first get user_id and the recipe_id and then will delete the recipe_id according to the user_id in the database. Then it will redirect to the saved route.

#### recipe_maker.html
This html page will help you find the the recipe by the name of the food. It has a form that asks you to enter the name of food and the other is the submit when clicked it will trigger recipe_maker route.

#### recipe_maker route in app.py
When this route is triggered the recipes whose name is submitted will be shown.

It has a function named recipe_maker and inside it we have stored the url which will be used to search the recipes based on the parameters which is also stored on the different variable that parameter variable contains query as recipe_name, number as 6 (number of recipes to be searched), and the api key which will be used to search the recipes. After getting the result we will have a different url that will get us the detailed recipes of the result we get with the help of recipe id which we got from the above result.
And if everything goes well we will render result.html with detailed recipes as arguments that will show the recipes to the users.

#### result.html
This html page will show the detailed recipes which is searched according to the parameters defined in the breakfast function in app.py . The recipes will be shown in the form of cards and each recipe will contain a saved button which when clicked that particular recipe will be saved on the saved section.

#### create_your_own.html
This html page has a form that asks user to enter the ingredients and the number of people for whome the recipe is to be made and preferences, when submitted it will trigger create_your_own route and after that if everythings goes well it will show the recipe in the form of card and a button to send it to the users email using smtp

#### create_your_own route in app.py
When this route is triggered the recipes will be shown according to the user inputs

It first store the users input and the prompt for the gemini api as a f string.
It then will generate the result as text and then pass the result to the function named format_recipe_to_html function and after that the recipe will be stored in the session to send it via the email, and after all that the recipe is sent to the create_your_own.html with the formatted_recipe as the argument

#### format_recipe_to_html function in app.py
This function formats the response sent by the gemini api into user friendly output that helps user understand the recipe better, it then match the section header and assign it to the correct section, it then generates the output into html format as f string and return it into the create_your_own function

#### send_to_mail route in app.py

When this route is triggered the recipe is sent to the users email

This route has a function named send_to_user which gets users email from the database, and then it will get the recipe from the session.
Then it will send the email with the subject "Your Generated Recipe"


### project.db
This project has a databse whose name is project.db and has 2 tables named users, and saved_recipe.
The users table have 3 columns which store the user id, users email, and the password.
The saved_recipe table have 3 columns which store user id which is also a foriegn key to the table users and the other column which store recipe_id.


### Static Folder
#### Images folder
This folder contains the images which are used to make the project.
#### style.css
This contains the cascading stylesheet of the project
