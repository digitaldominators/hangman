# Setup
requirements python 3.12(anything past 3.9 should be fine), npm, git

git clone https://github.com/smark-1/hangman.git

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

install all python packages

    pip install -r requirements.txt
    python manage.py migrate

## frontend
install dependencies

    cd ../frontend
    npm install

# run dev servers
these should be run in separate terminals
## frontend

    cd frontend
    npm run dev

open in browser http://localhost:5173
## backend

    cd backend

activate virtual environment

windows

    venv\Scripts\activate.bat
linux/mac

    source venv/bin/activate
run backend dev server

    python manage.py runserver

open in browser http://localhost:8000

# notes
when pulling new changes you might have to update some stuff
### frontend dependencies

    cd frontend
    npm install
### backend dependencies
activate virtual environment

windows

    venv\Scripts\activate.bat
linux/mac
    
    source venv/bin/activate

install all python packages

    pip install -r requirements.txt

### database migrations
activate virtual environment

windows

    venv\Scripts\activate.bat
linux/mac

    source venv/bin/activate

migrate database

    python manage.py migrate

### django admin
The admin panel is an easy way to view the relevant data in the database. It allows you to create, edit, and delete the data. This is very useful for testing.
 
To view the admin you must have an administrator account. To create an account activate the virtual environment
Then in the backend directory run `python manage.py createsuperuser` and follow the prompts.
Make sure the backend server is running then visit http://localhost:8000/admin