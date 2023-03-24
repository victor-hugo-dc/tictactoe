from game import Game, State


class TicTacToe(Game):
    def __init__(self):
        """ Initializes the player positions

        """
        self.player_x = 0b0000000000000000
        self.player_o = 0b0000000000000000


    def initial_state(self):
        
        return TicTacToe.State(self.player_x, self.player_o)


    class State(State):
        """ A state in a Tic Tac Toe game.
        """
        def __init__(self, x, o, positions: set = None):
            self._x = x
            self._o = o
            if positions is None:
                self._positions = set(range(9))
            else:
                self._positions = positions

            self._turn = 0


        def __hash__(self):
            return hash((self._x, self._o, frozenset(self._positions)))


        def __eq__(self, other):
            return (self._x == other._x
                    and self._o == other._o)


        def __repr__(self):
            return f"X: {self._x}\nO: {self._o}"
        
        
        def is_terminal(self):
            return len(self._positions) == 0 or (self._x | self._o == 0b111111111)


        def payoff(self):

            if not self.is_terminal():
                return None
            
            winning_masks = [
                0b111000000, 0b000111000, 0b000000111,  # rows
                0b100100100, 0b010010010, 0b001001001,  # columns
                0b100010001, 0b001010100  # diagonals
            ]
            for mask in winning_masks:

                if self._x & mask == mask:
                    return 1
                
                elif self._o & mask == mask:
                    return -1
            
            if self._x | self._o == 0b111111111:
                return 0


        def actor(self):
            return self._turn


        def get_actions(self):
            return list(self._positions)

            
        def is_legal(self, position):
            return position in self._positions


        def successor(self, action: int):

            next_x = self._x
            next_o = self._o

            if self._turn % 2 == 0: # player x
                next_x |= 1 << action
            else:
                next_o |= 1 << action
            
            next_positions = {c for c in self._positions if (c != action)}
            succ = TicTacToe.State(next_x, next_o, next_positions)
            succ._turn = 1 - self._turn

            return succ

