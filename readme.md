# Setup

requirements python 3.12, npm (node 20+), git

```bash
git clone https://github.com/digitaldominators/hangman.git
```

## backend

install dependencies

    cd backend

create virtual environment

    python -m venv venv

activate virtual environment

windows

    venv\Scripts\activate.bat

linux/mac

    source venv/bin/activate

add `.env` file

- the .env file should look something like the .env.example file
- for development set DEBUG=TRUE in the `.env` file

install all python packages

    pip install -r requirements.txt
    python manage.py migrate

add default categories and words to database

    python manage.py loaddata default_category_data.json

note: if there are no words in the database the game will not allow you to create a single player game.

- create a category in the admin panel
  see django admin section
- add words to category via manage.py command
  `python manage.py add_words filename.txt --category category_name --id category_id`
  the add_words command takes a filepath (relative path to the manage.py file, or absolute path) of a txt file where each line is a new phrase and a category name or id to add the words to.
  if you want to add words to a pre-existing category you can use the category name or id.
  to create a new category use the category name.

---

run backend dev server

    python manage.py runserver

open in browser http://localhost:8000

note: to see the frontend running in the backend server you must run `npm run build` in the frontend
this will build the latest changes.

## frontend

run this in a separate terminal

install dependencies

    cd ../frontend
    npm install
    npm run dev

open in browser http://localhost:5173

### django admin

The admin panel is an easy way to view the relevant data in the database. It allows you to create, edit, and delete the data. This is very useful for testing.

To view the admin you must have an administrator account. To create an account activate the virtual environment
Then in the backend directory run `python manage.py createsuperuser` and follow the prompts.
Make sure the backend server is running then visit http://localhost:8000/admin

#### login to admin

1. go to http://localhost:8000/admin
2. login with your superuser username and password

#### add category

1. login to admin
2. under category there is a categories list item with a plus sign, click the plus sign
3. add a category name and click save

#### add phrases to category

1. login to admin
2. under category there is a phrases list item, click on the plus sign
3. enter the phrase you want to add and choose the category from the dropdown list, If the category is not in the list you can click the plus icon to add the category.
4. click save or click save and add another if you are adding multiple phrases

# documentation

The documentation can be found in the docs folder.
