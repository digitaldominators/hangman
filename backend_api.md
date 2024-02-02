# Backend API reference
When making a post or put request a csrf token is needed. To add a csrf token add a header called `X-CSRFToken` 
and set it to the value of the `csrftoken` cookie that has been
set in the browser. You can use the readCookie function for this.

The headers should look like:

    headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    "X-CSRFToken": readCookie("csrftoken")
    }



## Game
The basic game object shows:
* game_slug - code used to join the game and is used as the game id to run any action on the game.
* is_multiplayer - boolean if game is a multiplayer game.
* full - boolean if the game has all the players needed to start the game.
* timer - int - number of seconds between turns - 0 means timer is off. (this value is not currently used by the backend it is just saved for the frontend to use.)
* level - int 1 to 3 - game difficulty level
* status - next action that must be taken by player (won/loss/choose word/wait for other player to join/your turn/other players turn)
* player - int 1 if this player is the first player 2 if second player (1st player created the game)
* correct_guesses - list of letters/words - correct guesses
* incorrect_guesses - list of letters/words - incorrect guesses
* word - string - outline of the word each letter except spaces replaces with `_` unless user guesses the letter. If the word is `heads up` and the user guessed `e` `s` and `u` it would return `_e__s u_`.
* game_score - int - current score in game
* other_player_game_score - int - current score of the other players game

### new game
To create a new game post data to /api/game/. 

    {
        "multiplayer": false, // required (true/false)
        "word": "heads up", // required if multiplayer - set other players word. - If multi player is false this doesn't do anything.
        "timer": null, // optional - set time between modes
        "level": null // optional - set difficulty level - default 1
    }
### join game
To join a multiplayer game post data to /api/game/join_game/

    {
        "game_slug":"IPBS2BE9" // code to join game
    }

after joining the game the user must set the word for the other player
### set first player word
To set the first players word player must have already joined the game. Post data to /api/game/<game_slug>/choose_word/

    {
        "word": "heads up" // set the word for the first player
    }
### list games
To get a list of the current users games use a get request to /api/game/
### game details
To get details of a specific game use a get request to /api/game/<game_slug>/
### make a guess
To guess a letter or word make a post request to /api/game/<game_slug>/

    {
        "guess":"a" // the guess letter or word goes here
    }
### update timer setting
To change the timer amount make a post request to /api/game/<game_slug>/

    {
        "timer":0 // number of seconds before turn is over
    }

## Scoreboard
make a get request to /api/scoreboard/
Returns the top 50 total scores and average scores. 
Will return something like:

    {
        "total_scores": [
            {
                "user": "user1",
                "score": 8750
            },
            {
                "user": "user2",
                "score": 6800
            }
            ...
        ],
        "average_scores": [
            {
                "user": "user2",
                "score": 900
            },
            {
                "user": "user1",
                "score": 730
            }
            ...
        ]
    }

## Accounts
### Registration
To create a new account, post data to /accounts/register/

    {
        "username": "bob", // required unique username
        "email": "bob@youruncle.com, // required unique email address
        "password": "password", // required password
        "password2": "password" // required matching password
    }

### Login
To login with an existing user, post data to /accounts/login_user/

    {
        "username": "bob", // required username
        "password": "password" // required password
    }

### Logout
To logout of an existing session, post data to /accounts/logout_user/
Requires active session as an authenticated user.
