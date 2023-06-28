# board
#  n denotes size
#  list of lists nXn
#  placeholder on creation on 'blank'
# players
#  2 players
#  current player
# business logic
#  start of game
#  turn
#    player move
#      choose a column
#      check for vals and change appropriate color
#    check for win
#      iterate
#      check for horizontal, vertical, forward diagonal, and negative diagonal
#    switch curr player
#      unless board is full
# ui logic
class bcolors:
    black = '\x1b[0;97;40m'
    red = '\x1b[0;30;41m'
    empty = '\x1b[0;30;47m'
    end_of_string = '\x1b[0m'


class Board:
    def __init__(self, number_of_spaces):
        self.number_of_spaces = number_of_spaces
        self.gameboard = [['empty' for _ in range(number_of_spaces)] for _ in range(self.number_of_spaces)]    
    def add_token(self, column, current_player):
        for i, row  in enumerate(self.gameboard):
            value = row[column]
            if value != 'empty':
                if i-1 < 0:
                    print("That row is full")
                    return False
                else:
                    self.gameboard[i-1][column] = current_player.color
                    return True
            elif i == self.number_of_spaces-1 and value == 'empty':
                self.gameboard[i][column] = current_player.color
                return True
            
    def check_for_win(self, column_played, current_player):
        row_played = self.find_row_from_col(column_played)
        color = current_player.color
        # there is probably a way to do this better
        # vertical win
        vertical_count = 0
        vertical_win = False
        for row in self.gameboard:
            if row[column_played] == color:
                vertical_count += 1
                if vertical_count == 4:
                    vertical_win = True
            else:
                vertical_count = 0

        # horizontal win
        horizontal_count = 0
        horizontal_win = False
        for col in self.gameboard[row_played]:
            if col == color:
                horizontal_count += 1
                if horizontal_count == 4:
                    horizontal_win = True
            else:
                horizontal_count = 0
                
        down_diag_win = False
        up_diag_win = False
        down_diag_count = 0
        up_diag_count = 0    
        
        # diags
        col_offset = -3
        row_offset = 3
        for _ in range(7):
            try:
                if self.gameboard[row_played + col_offset][column_played + col_offset] == color:
                    down_diag_count += 1
                    if down_diag_count == 4:
                        down_diag_win = True
                else: 
                    down_diag_count = 0
            
                if self.gameboard[row_played + row_offset][column_played + col_offset] == color:
                    up_diag_count += 1
                    if up_diag_count == 4:
                        up_diag_win = True
                else: 
                    up_diag_count = 0
            except:
                continue
            finally:
                col_offset += 1
                row_offset -= 1
        
        return vertical_win or horizontal_win or down_diag_win or up_diag_win
    
    def print_board(self):
        for row in self.gameboard:
            for i in row:
                print(find_color(i), end=" "*(6-len(i)))
            print('\n')
            
    def find_row_from_col(self, last_col):
        for i, row in enumerate(self.gameboard):
            if row[last_col] != 'empty':
                return i
        
def find_color(i):
    if i == 'empty':
        return bcolors.empty + i + bcolors.end_of_string
    if i == 'black':
        return bcolors.black + i + bcolors.end_of_string
    if i == 'red':
        return bcolors.red + i + bcolors.end_of_string

class Player:
    def __init__(self):
        self.is_current_player = False
        self.color = ''
    def add_color(self, color):
        self.color = color
        
def switch_current_player(player1, player2):
    if player1.is_current_player:
        player1.is_current_player = False
        player2.is_current_player = True
    else:
        player1.is_current_player = True
        player2.is_current_player = False
        
    return player1, player2

def find_current_player(player1, player2):
    if player1.is_current_player:
        return player1
    else:
        return player2
    
def start_game():
    print("Welcome to Connect Four")
    board_size = input("Please enter the size board you would like to use as an integer: ")
    board = Board(int(board_size))
    player1_color = input("Player One, pick red or black by typing 'r' or 'b': ")
    player1 = Player()
    player2 = Player()
    if player1_color == 'r':
        player1.add_color('red')
        player2.add_color('black')
    else: 
        player1.add_color('black')
        player2.add_color('red')
    player1, player2 = switch_current_player(player1, player2)

    while True:
        current_player = find_current_player(player1, player2)
        board.print_board()
        column_chosen = input("Player " + find_color(current_player.color) + ", please enter a column number to drop your token: ")
        made_a_turn = board.add_token(int(column_chosen), current_player)
        # check for win
        if board.check_for_win(int(column_chosen), current_player):
            board.print_board()
            print("Player {color} wins!".format(color=current_player.color))
            return

        if made_a_turn:
            player1, player2 = switch_current_player(player1, player2)

# to play, `python connect_four.py` in terminal in the same directory
start_game()