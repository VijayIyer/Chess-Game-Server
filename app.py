import flask
from flask import Flask, make_response
from flask_cors import CORS
import json
from flask import request, json
import game
from game import Game

app = Flask(__name__)
CORS(app)

ongoing_game = Game()


@app.route('/')
def start():
    board_conf_file = 'board_configuration1.txt'
    with open(board_conf_file, 'r') as f:
        board_conf = f.readlines()
    ongoing_game.initialize_players(board_conf)
    return "Board Initialized!"


@app.route('/move', methods=["POST"])
def make_move():
    move = request.get_json()['move']
    print(move)
    ongoing_game.make_move(move)
    if ongoing_game.is_invalid_move:
        return make_response("invalid move", 400)
    else:
        return make_response(json.jsonify(ongoing_game.get_status()), 200)


@app.route('/positions')
def get_positions():
    return json.jsonify(board=ongoing_game.get_positions())


@app.route('/board')
def view_board():
    print(ongoing_game.board_map)
    return json.jsonify(ongoing_game.board_map.tolist())


if __name__ == "__main__":
    app.run(debug=True)
