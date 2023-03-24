class TicTacToe:
    def __init__(self):
        self.player_x = 0b0000000000000000
        self.player_o = 0b0000000000000000
        self.winning_masks = [
            0b111000000, 0b000111000, 0b000000111,  # rows
            0b100100100, 0b010010010, 0b001001001,  # columns
            0b100010001, 0b001010100  # diagonals
        ]
        self.possible_positions = set(range(9))

    def get_board(self):
        board = ""
        for i in range(9):
            board += "|"
            mask = 1 << i
            if self.player_x & mask:
                board += "X"
            elif self.player_o & mask:
                board += "O"
            else:
                board += " "
            if i % 3 == 2:
                board += "\n"
            
        return board

    def make_move(self, player, position: int):
        if position in self.possible_positions:
            if player == "X":
                self.player_x |= 1 << position
            else:
                self.player_o |= 1 << position
            
            self.possible_positions.remove(position)

    def has_winner(self):
        for mask in self.winning_masks:
            if self.player_x & mask == mask:
                return "X"
            elif self.player_o & mask == mask:
                return "O"
        return None

def play_game():
    game = TicTacToe()
    current_player = "X"
    positions_taken = set()
    while True:
        print(game.get_board())
        print(f"It's {current_player}'s turn.")
        while True:
            position = int(input("Enter a position (0-8): "))
            if position in positions_taken:
                print("That position has already been taken. Please choose a different one.")
            else:
                positions_taken.add(position)
                break
        game.make_move(current_player, position)
        winner = game.has_winner()
        if winner:
            print(game.get_board())
            print(f"{winner} wins!")
            break
        elif game.player_x | game.player_o == 0b111111111:
            print(game.get_board())
            print("It's a tie!")
            break
        else:
            current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    play_game()
