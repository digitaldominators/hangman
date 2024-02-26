The backend is build using django and django rest framework. The backend is organized into a few folders:

accounts - contains the views and serializers for the accounts app. This is where the registration and login views are.

categories - contains the views and serializers for the categories app. This is where the api endpoint for listing all the categories lives.

game - contains the views and serializers for the main game app. This is where the api endpoints to create, list, or make a guess live.

scoreboard - contains the views and serializers for the scoreboard app. This is where the api endpoint for listing the top 50 scores lives.

settings - contains the settings for the django app and is the entry point for the app with the wsgi.py file.

