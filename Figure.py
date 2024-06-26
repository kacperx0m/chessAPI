class Figure:
    def __init__(self, currentField, color):
        self.currentField = currentField
        self.color = color

    """
    zwraca liste dostepnych ruchow dla figury w oparciu o aktualna pozycje
    np ['a3']
    nie uwzglednia sekwencji bicia
    """

    def list_available_moves(self, board):
        availableMoves = []
        start_col = ord(self.currentField[0]) - ord("a")
        start_row = int(self.currentField[1])
        # move (x,y)
        for move in self.moves:
            for i in range(1, 8 if self.longMove else 2):
                new_col = start_col + move[0] * i
                new_row = start_row + move[1] * i
                transformed = chr(new_col + ord("a")) + str(new_row)
                if 0 <= new_col < 8 and 0 < new_row <= 8:
                    if board.get(transformed) is not None:
                        break
                    availableMoves.append(f"{transformed}")
        return availableMoves

    """
    zwraca True albo False w zaleznosci od tego czy ruch moze byc wykonany
    bazuje na tym czy pole jest puste (None) i czy ruch znajduje sie w
    liscie ruchow
    """

    def validate_move(self, dest_field, board):
        moves = self.list_available_moves(board)
        if board.get(dest_field) is None \
                and f"{dest_field[0]}{dest_field[1]}" in moves:
            return True
        return False

    def __str__(self):
        return f"{self.currentField} {self.color} {self.__class__.__name__}"


class King(Figure):
    def __init__(self, position, color):
        super().__init__(position, color)
        # (x,y)
        self.moves = [
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
            (-1, 0),
            (-1, 1),
        ]
        self.longMove = 0
        self.castling = True
        if color == "white":
            if self.currentField == "e1":
                self.moves.append((2, 0))
        elif color == "black":
            if self.currentField == "e8":
                self.moves.append((-2, 0))

    def validate_move(self, dest_field, board):
        moves = self.list_available_moves(board)
        if board.get(dest_field) is None \
                and f"{dest_field[0]}{dest_field[1]}" in moves:
            # zakladamy ze walidacja zakonczona sukcesem = ruch
            if self.castling is True:
                self.moves.pop()
                self.castling = False
            return True
        return False


class Queen(Figure):
    def __init__(self, position, color):
        super().__init__(position, color)
        # (x,y)
        self.moves = [
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
            (-1, 0),
            (-1, 1),
        ]
        self.longMove = 1


class Rook(Figure):
    def __init__(self, position, color):
        super().__init__(position, color)
        # (x,y)
        self.moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.longMove = 1


class Bishop(Figure):
    def __init__(self, position, color):
        super().__init__(position, color)
        # (x,y)
        self.moves = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        self.longMove = 1


class Knight(Figure):
    def __init__(self, position, color):
        super().__init__(position, color)
        # (x,y)
        self.moves = [
            (-1, 2),
            (1, 2),
            (2, 1),
            (2, -1),
            (1, -2),
            (-1, -2),
            (-2, -1),
            (-2, 1),
        ]
        self.longMove = 0


class Pawn(Figure):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.firstMove = True
        self.longMove = 0
        if color == "white":
            # (x,y)
            self.moves = [(0, 1)]
            if self.currentField[1] == "2":
                self.moves.append((0, 2))
        elif color == "black":
            self.moves = [(0, -1)]
            if self.currentField[1] == "7":
                self.moves.append((0, -2))

    """
    nadpisana funkcja z klasy abstrakcyjnej Figure
    zapewnie mozliwosc wykonania specjalnego ruchu tylko raz
    """

    def validate_move(self, dest_field, board):
        moves = self.list_available_moves(board)
        if board.get(dest_field) is None \
                and f"{dest_field[0]}{dest_field[1]}" in moves:
            # zakladamy ze walidacja zakonczona sukcesem = ruch
            if self.firstMove is True:
                self.moves.pop()
                self.firstMove = False
            return True
        return False


class Chessboard:
    """
    klasa reprezentujaca plansze do gry w szachy
    posiada funkcje do generowania oraz wyswietlania planszy
    """

    def __init__(self, arrangement=None):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        # plansza 8x8
        # biale na dole (wyzsze indeksy) czarne na gorze (mniejsze indeksy)
        if arrangement is None:
            self.arrangement = """
                rkbqKbkr
                pppppppp
                nnnnnnnn
                nnnnnnnn
                nnnnnnnn
                nnnnnnnn
                pppppppp
                rkbqKbkr
                """
        elif arrangement == "clear":
            self.arrangement = """
                            nnnnnnnn
                            nnnnnnnn
                            nnnnnnnn
                            nnnnnnnn
                            nnnnnnnn
                            nnnnnnnn
                            nnnnnnnn
                            nnnnnnnn
                            """
        else:
            self.arrangement = arrangement
        self.setChessboard()

    def setChessboard(self):
        # litery reprezentujace poszczegolne klasy figur
        figureDict = {
            "r": Rook,
            "k": Knight,
            "b": Bishop,
            "q": Queen,
            "K": King,
            "p": Pawn,
            "n": None,
        }

        # iteruje po arrangement i ustawia figury na planszy
        i = 0
        for line in self.arrangement.strip().split("\n"):
            line = line.strip()
            for j, char in enumerate(line):
                piece = figureDict[char]
                if piece is not None:
                    self.board[7 - i][j] = piece(
                        f'{chr(j+ord("a"))}{8-i}',
                        "black" if 0 <= i < 2 else "white"
                    )
                else:
                    continue
            i += 1

    # przyjmuje figure np Pawn(...) i ustawia figure pod tym polem
    def set(self, piece):
        col = ord(piece.currentField[0]) - ord("a")
        row = int(piece.currentField[1]) - 1
        self.board[row][col] = piece

    # przyjmuje pole o wartosci string np "b1" i zwraca figure pod tym polem
    def get(self, currentField):
        col = ord(currentField[0]) - ord("a")
        row = int(currentField[1]) - 1
        return self.board[row][col]

    def printChessboardObjects(self):
        for row in self.board[::-1]:
            print(row)

    def printChessboard(self):
        # odwrotna kolejnosc do wyswietlania
        for row in self.board[::-1]:
            print(" | ".join(str(piece) if piece else "None" for piece in row))


# """
# proste testy nie licząc oddzielego pliku do testów

chessboard = Chessboard(
    arrangement="""
    nnnnqnnn
    nbnnnnKp
    nnnnnppn
    nprqnknn
    pnnnnnnn
    nnnpnppn
    pnnknnnp
    nrnnrnKn
    """
)
# chessboard.setChessboard()
# chessboard.printChessboardObjects()
# pawn = Pawn("e7", "black")
# chessboard.board[6][4] = pawn
# pawn2 = Pawn("e2", "white")
# chessboard.set(pawn2)
# knight1 = Knight("d4", "white")
# knight2 = Knight("f3", "white")
# chessboard.set(knight1)
# chessboard.set(knight2)
# chessboard.printChessboard()
# chessboard.set(Rook("c6", "white"))
piece = chessboard.get("b7")
chessboard.printChessboard()
temp = piece.list_available_moves(chessboard)
print(piece.list_available_moves(chessboard))
print(piece.validate_move("e6", chessboard))
# print(piece.validate_move("g1", chessboard.board))

# """
