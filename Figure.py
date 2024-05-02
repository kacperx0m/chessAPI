class Figure:
    def __init__(self, currentField, color):
        self.currentField = currentField
        self.color = color

    def list_available_moves(self):
        pass

    def validate_move(self, dest_field, board):
        pass


class King(Figure):
    def __init__(self, position, color):
        super().__init__(position, color)

    def list_available_moves(self):
        # (x,y)
        moves = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
    def validate_move(self, dest_field, board):
        pass

    def __str__(self):
        print(self.currentField, self.color)


class Queen(Figure):
    def list_available_moves(self):
        # (x,y)
        moves = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
        longMove = 1


class Rook(Figure):
    def list_available_moves(self):
        # (x,y)
        moves = [(0,1),(1,0),(0,-1),(-1,0)]
        longMove = 1


class Bishop(Figure):
    def list_available_moves(self):
        # (x,y)
        moves = [(1,1),(1,-1),(-1,-1),(-1,1)]
        longMove = 1


class Knight(Figure):
    def list_available_moves(self):
        # (x,y)
        moves = [(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1)]


class Pawn(Figure):
    def __init__(self, position, color):
        super().__init__(position, color)
        if color == "white":
            # (x,y)
            self.moves = [(0,1)]
            if self.currentField[1] == "2":
                self.moves.append((0,2))
        elif color == "black":
            self.moves = [(0,-1)]
            if self.currentField[1] == "7":
                self.moves.append((0,-2))

    def list_available_moves(self):
        availableMoves = []
        start_col = ord(self.currentField[0]) #- ord('a')
        start_row = int(self.currentField[1]) - 1
        for move in self.moves:
            new_col = start_col + move[0]
            new_row = start_row + move[1]
            # 97 -ascii a 105 -ascii i
            if 97 <= new_col < 105 and 0 <= new_row < 8:
                availableMoves.append((chr(new_col), new_row+1))
        return availableMoves

    def validate_move(self, dest_field, board):
        temp1 = (ord(dest_field[0]) - ord('a'))
        temp2 = int(dest_field[1])
        moves = self.list_available_moves()
        if board[temp2-1][temp1-1] == None and (dest_field[0],int(dest_field[1])) in moves:
            # zakladamy ze walidacja zakonczona sukcesem = ruch
            self.moves.pop()
            return True
        return False

    def __str__(self):
        #return f"Pawn"
        return f"{self.currentField} {self.color}"


class Chessboard():
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]

    # def setChessboard(self):
    #     i=0
    #     for col in "abcdefgh":
    #         self.board[1][i] = Pawn(col+str(7),"black")
    #         self.board[6][i] = Pawn(col+str(2),"white")
    #         i+=1

    def setChessboard(self):
        i=0
        for col in "abcdefgh":
            # biale na dole (mniejsze indeksy) czarne na gorze (wyzsze indeksy)
            self.board[1][i] = Pawn(col+str(2),"white")
            self.board[6][i] = Pawn(col+str(7),"black")
            i+=1

    def printChessboard(self):
        # odwrotna kolejnosc do wyswietlania
        for row in self.board[::-1]:
            print(' '.join(str(piece) if piece else "None" for piece in row[::-1]))


chessboard = Chessboard()
chessboard.setChessboard()
chessboard.printChessboard()
piece = chessboard.board[1][1] # pole b2
print(piece.list_available_moves())
print(piece.validate_move("b3", chessboard.board))
#print(piece.validate_move("b4", chessboard.board))