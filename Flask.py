from flask import Flask, jsonify, make_response
from Figure import Chessboard

app = Flask(__name__)
chessboard = Chessboard()
chessboard.setChessboard()
figures = ("pawn", "rook", "knight", "bishop", "queen", "king")


@app.errorhandler(500)
def internal_error(error):
    return make_response("Server Error", 500)


@app.route("/")
def hello_world():
    return "<p>Hello, world!</p>"


@app.route("/api/v1/<string:chess_figure>/<string:current_field>",
           methods=["GET"])
def figure_moves(chess_figure, current_field):
    if len(current_field) != 2:
        return make_response(
            jsonify(
                {
                    "availableMoves": [],
                    "error": "Field does not exist",
                    "currentField": current_field,
                }
            ),
            409,
        )

    # current_field = str(ord(current_field[0])-ord("a")+1)+current_field[1]
    if chess_figure not in figures:
        return make_response(
            jsonify(
                {
                    "available_moves": [],
                    "error": "Chess piece does not exist",
                    "figure": chess_figure,
                    "currentField": current_field,
                }
            ),
            404,
        )

    elif 0 <= ord(current_field[0]) - ord("a") < 8 \
            and 0 < int(current_field[1]) <= 8:
        figure = chessboard.get(current_field)
        if figure is None or figure.__class__.__name__.lower() != chess_figure:
            return make_response(
                jsonify(
                    {
                        "availableMoves": [],
                        "error": "There is no such piece here",
                        "currentField": current_field,
                    }
                ),
                404,
            )

        return jsonify(
            {
                "availableMoves": figure.list_available_moves(chessboard),
                "error": "None",
                "currentField": current_field,
            }
        )
    else:
        return make_response(
            jsonify(
                {
                    "availableMoves": [],
                    "error": "Field does not exist",
                    "currentField": current_field,
                }
            ),
            409,
        )


@app.route(
    "/api/v1/<string:chess_figure>/<string:current_field>/<string:dest_field>",
    methods=["GET"],
)
def figure_validate_move(chess_figure, current_field, dest_field):
    figure_response = figure_moves(chess_figure, current_field)
    if not figure_response.response or figure_response.status_code != 200:
        return figure_response

    moves = figure_response.json["availableMoves"]
    moves = ["".join(str(y) for y in x) for x in moves]
    if dest_field in moves:
        return jsonify(
            {
                "move": "valid",
                "figure": chess_figure,
                "error": "null",
                "current_field": current_field,
                "destField": dest_field,
            }
        )
    else:
        return make_response(
            jsonify(
                {
                    "move": "invalid",
                    "figure": chess_figure,
                    "error": "Current move is not permitted",
                    "current_field": current_field,
                    "destField": dest_field,
                }
            ),
            409,
        )
