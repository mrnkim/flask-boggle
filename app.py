from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    game_dict = {"gameId": game_id, "board": game.board}
    return jsonify(game_dict)

@app.post("/api/score-word")
def score_word():
    """check if the word is in the word list and if it's findable on the board"""

    game = BoggleGame()
    print(game.board)
    # breakpoint()
    response = request.json #JSON: {game_id, word}
    print(request)

    if game.is_word_in_word_list(f"{response['word']}"):
       if game.check_word_on_board(f"{response['word']}"):
           return jsonify({"result": "ok"})
       else:
           return jsonify({"result": "not-on-board"})
    else:
        return jsonify({"result": "not-word"})
