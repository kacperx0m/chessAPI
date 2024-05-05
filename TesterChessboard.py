import copy
from Figure import *

"""
plik z testami dotyczącymi wyświetlania ruchów dla odpowiednich figur szachowych
oraz sprawdzającymi poprawność ruchu
"""

board = Chessboard()

def test_available_moves_all_figures():
    # test dla figury king
    boardCopy = copy.copy(board)
    king = King("h1", "white")
    boardCopy.set(king)
    moves = ["g1", "g2", "h2"]
    assert sorted(king.list_available_moves()) == sorted(moves)

    # test dla figury knight
    knight = Knight("h1", "white")
    boardCopy.set(knight)
    moves = ["f2", "g3"]
    assert sorted(knight.list_available_moves()) == sorted(moves)

    # test dla figury pawn
    pawn = Pawn("h1", "black")
    boardCopy.set(pawn)
    moves = []
    assert sorted(pawn.list_available_moves()) == sorted(moves)

    # test dla figury queen
    queen = Queen("h1", "white")
    boardCopy.set(queen)
    moves = ["h2", "h3", "h4", "h5", "h6", "h7", "h8",
             "g1", "f1", "e1", "d1", "c1", "b1", "a1",
             "g2", "f3", "e4", "d5", "c6", "b7", "a8"]
    assert sorted(queen.list_available_moves()) == sorted(moves)

    # test dla figury bishop
    bishop = Bishop("h1", "white")
    boardCopy.set(bishop)
    moves = ["g2", "f3", "e4", "d5", "c6", "b7", "a8"]
    assert sorted(bishop.list_available_moves()) == sorted(moves)

    # test dla figury rook
    rook = Rook("h1", "white")
    boardCopy.set(rook)
    moves = ["h2", "h3", "h4", "h5", "h6", "h7", "h8",
             "g1", "f1", "e1", "d1", "c1", "b1", "a1"]
    assert sorted(rook.list_available_moves()) == sorted(moves)


boardCopy = copy.copy(board)
def test_valid_moves():
    # test dla figury king
    king = King("b2", "white")
    boardCopy.set(king)
    assert king.validate_move("c3", boardCopy.board)

    # test dla figury knight
    knight = Knight("d4", "white")
    boardCopy.set(knight)
    assert knight.validate_move("e6", boardCopy.board)

    # test dla figury pawn
    pawn = Pawn("a7", "white")
    boardCopy.set(pawn)
    assert pawn.validate_move("a8", boardCopy.board)

    # test dla figury queen
    queen = Queen("f6", "white")
    boardCopy.set(queen)
    assert queen.validate_move("f1", boardCopy.board)

    # test dla figury bishop
    bishop = Bishop("h2", "white")
    boardCopy.set(bishop)
    assert bishop.validate_move("b8", boardCopy.board)

    # test dla figury rook
    rook = Rook("c6", "white")
    boardCopy.set(rook)
    assert rook.validate_move("c5", boardCopy.board)

def test_invalid_moves():
    # test dla figury king
    king = King("b1", "black")
    boardCopy.set(king)
    assert not king.validate_move("b0", boardCopy.board)

    # test dla figury knight
    knight = Knight("f3", "white")
    boardCopy.set(knight)
    assert not knight.validate_move("d4", boardCopy.board)

    # test dla figury pawn
    pawn = Pawn("a6", "white")
    boardCopy.set(pawn)
    assert not pawn.validate_move("a7", boardCopy.board)

    # test dla figury queen
    queen = Queen("g5", "white")
    boardCopy.set(queen)
    assert not queen.validate_move("f6", boardCopy.board)

    # test dla figury bishop
    bishop = Bishop("b8", "white")
    boardCopy.set(bishop)
    assert not bishop.validate_move("h2", boardCopy.board)

    # test dla figury rook
    rook = Rook("g2", "white")
    boardCopy.set(rook)
    assert not rook.validate_move("c6", boardCopy.board)


def test_list_moves_after_first_pawn_move():
    boardCopy = copy.copy(board)
    pawn = Pawn("e7", "black")
    boardCopy.set(pawn)

    # po pierwszym ruchu pionek nie moze wykorzystac juz swojego specjalnego ruchu
    assert pawn.validate_move("e5", boardCopy.board)
    assert not pawn.validate_move("e3", boardCopy.board)
