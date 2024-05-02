from flask import Flask, jsonify, abort, Response, make_response
from werkzeug.exceptions import HTTPException

from Figure import Chessboard, Figure

app = Flask(__name__)
chessboard = Chessboard()
chessboard.setChessboard()
figures = ("pawn", "rook", "knight", "bishop", "queen", "king")
#pawn_pos=""

# @app.errorhandler(404)
# def not_found_error(error):
#     return make_response(jsonify({"availableMoves": [], "error": "Chess piece does not exist"}),404)
#
@app.errorhandler(500)
def internal_error(error):
    return make_response("Server Error",500)
#
# def make_error(status_code, message):
#     response = jsonify()

@app.route("/")
def hello_world():
    return "<p>Hello, world!</p>"

@app.route("/api/v1/<string:chess_figure>/<string:current_field>", methods=["GET"])
def figure_moves(chess_figure, current_field):
    if len(current_field)!=2:
        return make_response(jsonify({"availableMoves": [], "error": "Field does not exist", "currentField": current_field}), 409)
    current_field = str(ord(current_field[0])-ord("a")+1)+current_field[1]
    if chess_figure not in figures:
        return make_response(jsonify({"available_moves": [], "error": "Chess piece does not exist", "figure": chess_figure, "currentField": current_field}), 404)
    elif 0 < int(current_field[0]) <8 and 0 <= int(current_field[1]) <=8:
        figure = chessboard.board[int(current_field[0])-1][int(current_field[1])-1]
        if figure is None:
            return make_response(jsonify({"availableMoves": [], "error": "There is no piece here", "currentField": current_field}),404)
        return jsonify({"availableMoves": figure.list_available_moves(), "error": "None", "currentField": current_field})
    else:
        return make_response(jsonify({"availableMoves": [], "error": "Field does not exist", "currentField": current_field}), 409)

@app.route("/api/v1/<string:chess_figure>/<string:current_field>/<string:dest_field>", methods=["GET"])
def figure_validate_move(chess_figure, current_field, dest_field):
    figure_response = figure_moves(chess_figure, current_field)
    if not figure_response.response or figure_response.status_code != 200:
        return figure_response

    moves = figure_response.json['availableMoves']
    moves = [''.join(str(y) for y in x) for x in moves]
    if dest_field in moves:
        return jsonify({"move":"valid", "figure": chess_figure, "error": "null", "current_field": current_field, "destField": dest_field})
    else:
        return jsonify({"move":"invalid", "figure": chess_figure, "error": "Current move is not permitted", "current_field": current_field, "destField": dest_field})