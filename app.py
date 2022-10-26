import flask
from flask import Flask, make_response
from flask.templating import render_template
from flask_cors import CORS
import json
from flask import request, json
import game
from game import Game
from typing import Dict, List

app = Flask(__name__)
CORS(app)

# will be stored in a nosql database later
ongoing_games: List[Game] = []


# num_ongoing_games = 0

def find_game(game_id: int) -> Game:
    return next(game_obj for game_obj in ongoing_games if game_obj.id == game_id)


@app.route('/', methods=["GET"])
def start():
    board_conf_file = 'board_configuration1.txt'
    with open(board_conf_file, 'r') as f:
        board_conf = f.readlines()
    ongoing_game = Game(len(ongoing_games))
    ongoing_game.initialize_players(board_conf)
    ongoing_games.append(ongoing_game)
    return make_response(json.jsonify(board=ongoing_game.get_positions(), game_id=ongoing_game.id), 200)


@app.route('/<int:game_id>/move', methods=["POST"])
def make_move(game_id: int):
    move = request.get_json()['move']
    ongoing_game = find_game(game_id)
    ongoing_game.make_move(move)
    if ongoing_game.is_invalid_move:
        return make_response("invalid move", 400)
    else:
        return make_response(json.jsonify(ongoing_game.get_status()), 200)


@app.route('/<int:game_id>/positions', methods=["GET"])
def get_positions(game_id: int):
    try:
        ongoing_game = find_game(game_id)
        return make_response(json.jsonify(board=ongoing_game.get_positions(), moves=ongoing_game.get_status()), 200)
    except Exception:
        return make_response("error in finding game with id:{}".format(game_id), 400)


def view_board(game_id: int):
    ongoing_game = find_game(game_id)
    print(ongoing_game.board_map)
    return json.jsonify(ongoing_game.board_map.tolist())


if __name__ == "__main__":
    app.run(debug=True)
