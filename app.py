
from flask import Flask, render_template, request, redirect, session, jsonify
from functools import wraps
from flask_session import Session
import requests
import re
from flask_mail import Mail, Message # For sending mails to the users
from flask_cors import CORS # To access api hosted on another domain
#from tenacity import retry, wait_random_exponential, stop_after_attempt
import google.generativeai as genai
from cs50 import SQL

gemeni_key = "your gemini api key"
genai.configure(api_key=gemeni_key)
spoonacular_api_key="your spoonacular api key"
app = Flask(__name__)

CORS(app, resources = {r"/*": {"origins": "*"}}) # Enable CORS for all resources
print(genai.__version__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your mail id'
app.config['MAIL_PASSWORD'] = 'your mail password'
app.config['MAIL_DEFAULT_SENDER'] = ('Ann a teaser', 'mail id')
mail = Mail(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

# Rendring the default page
@app.route("/")
@login_required
def index():
    """Shows the home page"""
    return render_template("index.html")

# Rendring saved page, users can view saved recipe
@app.route('/saved', methods=["GET", "POST"])
@login_required
def saved():
    """View Saved Recipes"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    # Getting the recipe id
    user_id = session['user_id']
    user_id = int(user_id)
    recipe_id = str(request.form.get('recipe_id'))

    if not recipe_id:
        return jsonify({'error': 'Recipe ID is required'}), 400

    # Saving the recipe in the database
    if recipe_id != 'None':
        db.execute("INSERT INTO saved_recipe (user_id, recipe_id) VALUES (?, ?)", user_id, recipe_id)

    rows = db.execute("SELECT recipe_id FROM saved_recipe WHERE user_id = ?", (user_id,))
    recipe_ids = [row['recipe_id'] for row in rows]

    # Fetch full recipe details from Spoonacular API
    saved_recipes = []
    api_key = spoonacular_api_key
    for recipe_id in recipe_ids:
        response = requests.get(f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}")
        if response.status_code == 200:
            saved_recipes.append(response.json())

    # Render saved.html with the saved recipes
    return render_template('saved.html', recipes=saved_recipes)

# Delete the recipe from saved recipe section
@app.route('/unsave', methods=["POST", "GET"])
@login_required
def unsave_recipe():
    """Unsave a Recipe"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session['user_id']
    recipe_id = str(request.form.get('recipe_id'))

    if not recipe_id:
        return jsonify({'error': 'Recipe ID is required'}), 400

    # Delete the recipe from the database
    db.execute("DELETE FROM saved_recipe WHERE user_id = ? AND recipe_id = ?", user_id, recipe_id)

    # Redirect to the updated saved page
    return redirect('/saved')

# Rendring vegetarian page
@app.route('/vegetarian')
def vegetarian():
    """View Vegetarian recipe"""
    spoonacular_search_url = "https://api.spoonacular.com/recipes/complexSearch" # base url for searching the recipe

    # paramtheres to be used while searching the recipes
    search_params = {
            'diet': 'vegetarian',
            'number': 6,  # Number of results to fetch
            'apiKey': spoonacular_api_key
        }

    # getting the result from the url sent
    search_response = requests.get(spoonacular_search_url, params=search_params)
    if search_response.status_code != 200:
        return jsonify({'error': 'Failed to fetch search results.'}), search_response.status_code

    search_data = search_response.json()

    # getting the detailed recipe
    detailed_recipes = []
    for recipe in search_data.get('results', []):
        recipe_id = recipe['id']
        detail_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
        detail_params = {'apiKey': spoonacular_api_key}
        detail_response = requests.get(detail_url, params=detail_params)
        if detail_response.status_code == 200:
            detailed_recipes.append(detail_response.json())
    return render_template('vegetarian.html', recipes=detailed_recipes)

# Rendring non Vegetarian section
@app.route('/non_vegetarian')
def non_vegetarian():
    """View Non Vegetarian recipe"""
    spoonacular_search_url = "https://api.spoonacular.com/recipes/complexSearch"

    search_params = {
            'includeIngredients': "chicken,pork,fish",
            'number': 6,  # Number of results to fetch
            'apiKey': spoonacular_api_key,
            'excludeCuisine': "vegetarian, vegan",
        }

    search_response = requests.get(spoonacular_search_url, params=search_params)
    if search_response.status_code != 200:
        return jsonify({'error': 'Failed to fetch search results.'}), search_response.status_code

    search_data = search_response.json()

    # getting the detailed recipe
    detailed_recipes = []

    for recipe in search_data.get('results', []):
        recipe_id = recipe['id']
        detail_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
        detail_params = {'apiKey': spoonacular_api_key}
        detail_response = requests.get(detail_url, params=detail_params)
        if detail_response.status_code == 200:
            detailed_recipes.append(detail_response.json())
    return render_template('non_vegetarian.html', recipes=detailed_recipes)

# Rendring Dessert section
@app.route('/dessert')
def dessert():
    """View Dessert recipe"""
    spoonacular_search_url = "https://api.spoonacular.com/recipes/complexSearch"

    search_params = {
            'type': "dessert",
            'number': 6,  # Number of results to fetch
            'apiKey': spoonacular_api_key,
        }

    search_response = requests.get(spoonacular_search_url, params=search_params)
    if search_response.status_code != 200:
        return jsonify({'error': 'Failed to fetch search results.'}), search_response.status_code

    search_data = search_response.json()

    # getting the detailed recipe
    detailed_recipes = []

    for recipe in search_data.get('results', []):
        recipe_id = recipe['id']
        detail_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
        detail_params = {'apiKey': spoonacular_api_key}
        detail_response = requests.get(detail_url, params=detail_params)
        if detail_response.status_code == 200:
            detailed_recipes.append(detail_response.json())
    return render_template('dessert.html', recipes=detailed_recipes)

# Rendring breakfast section
@app.route('/breakfast')
def breakfast():
    """View Breakfast recipe"""
    spoonacular_search_url = "https://api.spoonacular.com/recipes/complexSearch"

    search_params = {
            'type': "breakfast",
            'number': 6,  # Number of results to fetch
            'apiKey': spoonacular_api_key,
        }

    search_response = requests.get(spoonacular_search_url, params=search_params)
    if search_response.status_code != 200:
        return jsonify({'error': 'Failed to fetch search results.'}), search_response.status_code

    search_data = search_response.json()

    # getting the detailed recipe
    detailed_recipes = []

    for recipe in search_data.get('results', []):
        recipe_id = recipe['id']
        detail_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
        detail_params = {'apiKey': spoonacular_api_key}
        detail_response = requests.get(detail_url, params=detail_params)
        if detail_response.status_code == 200:
            detailed_recipes.append(detail_response.json())
    return render_template('breakfast.html', recipes=detailed_recipes)

# Users sign up / register
@app.route('/register', methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        # checking the fields are empty or not
        if not email or not password or not confirmation:
            return "Dont Leave Any Field Empty"

        # checking the password fields match or not
        if password != confirmation:
            return "Password do not match"

        # checking if the user submitted the valid email or not
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return "Invalid email format"

        u = db.execute("SELECT email FROM users WHERE email= ?",
                        request.form.get("email"))

        # Regestring users in the database and rendring home page
        if not u:
            db.execute('INSERT INTO users (email, password) VALUES (?, ?)', email, password)
            new_user_id = db.execute("SELECT id FROM users WHERE email = ?",
                                        request.form.get("email"))[0]["id"]
            session["user_id"] = new_user_id
            return redirect("/")
        else:
            return "username already taken"


    else:
        return render_template('register.html')

# Users log in
@app.route('/login', methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("email"):
            return "must provide email", 403

        # Ensure password was submitted
        elif not request.form.get("password"):
            return "must provide password", 403

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE email = ?", request.form.get("email")
        )

        # Check if the user exists and the password matches
        if len(rows) != 1 or rows[0]["password"] != request.form.get("password"):
            return "Invalid username or password"

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
            return render_template('login.html')

# users can logout
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# Guided by Mr. Parth Verma, linkedin : https://www.linkedin.com/in/parth-verma-33bb27134?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app
@app.route('/create_your_own', methods=["GET", "POST"])
@login_required
#@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def create_your_own():
    """Make Recipe with chatbot"""
    if request.method == "POST":
        model = genai.GenerativeModel("gemini-2.0-flash")

        Ingredients = request.form.get("user_input")
        Preference = request.form.get("user_input2")
        numpeople = request.form.get("num_people")

        if not Ingredients or not Preference or not numpeople:
            return "Error: Please provide all required information", 400

        prompt = f"""
        You are a chef at a 5-star restaurant.
        Create a complete and detailed recipe using {Ingredients} for {numpeople} people.
        The dish should be {Preference}.

        Your output must include ALL the following sections — none should be empty:

        **Title:**
        **Subtitle:**
        **Prep Time:**
        **Cook Time:**
        **Total Time:**
        **Quantity:**
        **Ingredients:** (List clearly)
        **Equipment:** (List necessary tools)
        **Instructions:** (Step-by-step, numbered)
        **Serving Suggestion:**
        **Chef's Note:**

        End the response only after completing all sections.
        """

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 8192
            }
        )

        response_text = response.text
        formatted_recipe = format_recipe_to_html(response_text)
        session["last_generated_recipe"] = formatted_recipe

        return render_template('create_your_own.html', recipe_text=formatted_recipe)
    
    return render_template('create_your_own.html')


# used for displaying data structurally
def format_recipe_to_html(response_text):
    """Format the raw recipe text into structured HTML."""
    # Initialize a dictionary to hold different sections of the recipe
    sections = {
        'title': '',
        'subtitle': '',
        'prep_time': '',
        'cook_time': '',
        'total_time': '',
        'quantity': '',
        'ingredients': [],
        'equipment': [],
        'instructions': [],
        'serving_suggestion': '',
        'chefs_note': ''
    }

    # Split the response into lines
    lines = response_text.split("\n")
    current_section = None

    for line in lines:
        line = line.strip()

        # Match the section headers and assign the correct section
        if line.startswith("**Title:**"):
            sections['title'] = line.replace("**Title:**", "").strip()
            current_section = 'title'
        elif line.startswith("**Subtitle:**"):
            sections['subtitle'] = line.replace("**Subtitle:**", "").strip()
            current_section = 'subtitle'
        elif line.startswith("**Prep Time:**"):
            sections['prep_time'] = line.replace("**Prep Time:**", "").strip()
            current_section = 'prep_time'
        elif line.startswith("**Cook Time:**"):
            sections['cook_time'] = line.replace("**Cook Time:**", "").strip()
            current_section = 'cook_time'
        elif line.startswith("**Total Time:**"):
            sections['total_time'] = line.replace("**Total Time:**", "").strip()
            current_section = 'total_time'
        elif line.startswith("**Quantity:**"):
            sections['quantity'] = line.replace("**Quantity:**", "").strip()
            current_section = 'quantity'
        elif line.startswith("**Ingredients:**"):
            sections['ingredients'] = []
            current_section = 'ingredients'
        elif line.startswith("**Equipment:**"):
            sections['equipment'] = []
            current_section = 'equipment'
        elif line.startswith("**Instructions:**"):
            sections['instructions'] = []
            current_section = 'instructions'
        elif line.startswith("**Serving Suggestion:**"):
            sections['serving_suggestion'] = line.replace("Serving Suggestion:", "").strip()
            current_section = 'serving_suggestion'
        elif line.startswith("**Chef's Note:**"):
            sections['chefs_note'] = line.replace("Chef's Note:", "").strip()
            current_section = 'chefs_note'
        elif current_section == 'ingredients' and line:
            sections['ingredients'].append(line.replace("**", "").strip())
        elif current_section == 'equipment' and line:
            sections['equipment'].append(line.replace("**", "").strip())
        elif current_section == 'instructions' and line:
            sections['instructions'].append(line.replace("**", "").strip())
        elif current_section == 'serving_suggestion' and line:
            sections['serving_suggestion'] = line.replace("**", "").strip()
        elif current_section == 'chefs_note' and line:
            sections['chefs_note'] = line.replace("**", "").strip()

    # Generate the HTML output
    html_content = f"""

        <h1>{sections['title']}</h1>
        <h2>{sections['subtitle']}</h2>
        <p><strong>Prep Time:</strong> {sections['prep_time']}</p>
        <p><strong>Cook Time:</strong> {sections['cook_time']}</p>
        <p><strong>Total Time:</strong> {sections['total_time']}</p>
        <p><strong>Quantity:</strong> {sections['quantity']}</p>

        <h3>Ingredients:</h3>
        <p>
            {''.join([f"<li>{ingredient}</li>" for ingredient in sections['ingredients']])}
        </p>

        <h3>Equipment:</h3>
        <p>
            {''.join([f"<li>{equipment}</li>" for equipment in sections['equipment']])}
        </p>

        <h3>Instructions:</h3>
        <p>
            {''.join([f"<li>{instruction}</li>" for instruction in sections['instructions']])}
        </p>

        <h3>Serving Suggestion:</h3>
        <p>{sections['serving_suggestion']}</p>

        <h3>Chef's Note:</h3>
        <p>{sections['chefs_note']}</p>
    """
    return html_content

# Rendring recipe finder page
@app.route('/recipe_maker', methods=["GET", "POST"])
@login_required

def recipe_maker():
    """Find Recipe with name"""
    if request.method == "POST":

        recipe_name = request.form.get("recipe_name")
        if not recipe_name:
            return jsonify({'error': 'Please provide a recipe to be searched.'}), 400

        # url to search the recipe by the name
        spoonacular_search_url = "https://api.spoonacular.com/recipes/complexSearch"

        search_params = {
                'query': recipe_name,
                'number': 6,  # Number of results to fetch
                'apiKey': spoonacular_api_key
            }

        search_response = requests.get(spoonacular_search_url, params=search_params)
        if search_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch search results.'}), search_response.status_code

        search_data = search_response.json()

        # getting the detailed recipe
        detailed_recipes = []

        for recipe in search_data.get('results', []):
            recipe_id = recipe['id']
            detail_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
            detail_params = {'apiKey': spoonacular_api_key}
            detail_response = requests.get(detail_url, params=detail_params)
            if detail_response.status_code == 200:
                detailed_recipes.append(detail_response.json())
        return render_template('result.html', recipes=detailed_recipes)
    return render_template('recipe_maker.html')

# Sending the recipe generated by create_your_own () function to the email using smtp
@app.route('/send_to_mail', methods=["GET", "POST"])
@login_required

def send_to_mail():
    """Route to send the generated recipe to email"""
    user_id = session.get("user_id")
    if not user_id:
        return "Error: User not logged in", 401
    user = db.execute("SELECT email from users where id = ?", user_id)
    user_email = user[0]['email'] if user else None

    recipe = session.get("last_generated_recipe")
    if not recipe:
        return "Error: No recipe to send", 400
    msg = Message(
        subject="Your Generated Recipe",
        recipients=[user_email]
    )
    msg.html = recipe
    mail.send(msg)

    return render_template('create_your_own.html', message="email sent!")

if __name__ == "__main__":
    app.run(debug=True)