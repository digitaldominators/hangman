# Setup
requirements python 3.12(anything past 3.9 should be fine), npm, git

git clone ...

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
