import random
import sys
import mcts
import argparse


from tictactoe import TicTacToe

class MCTSTestError(Exception):
    pass
        

def random_choice(position):
    moves = position.get_actions()
    return random.choice(moves)


def compare_policies(game, p1, p2, games, prob):
    p1_wins = 0
    p2_wins = 0
    p1_score = 0

    for i in range(games):
        # start with fresh copies of the policy functions
        p1_policy = p1()
        p2_policy = p2()
        position = game.initial_state()
        copy = position
        
        while not position.is_terminal():
            if random.random() < prob:
                if position.actor() == i % 2:
                    move = p1_policy(position)
                else:
                    move = p2_policy(position)
            else:
                move = random_choice(position)
            
            position = position.successor(move)

        p1_score += position.payoff() * (1 if i % 2 == 0 else -1)
        if position.payoff() == 0:
            p1_wins += 0.5
            p2_wins += 0.5
        elif (position.payoff() > 0 and i % 2 == 0) or (position.payoff() < 0 and i % 2 == 1):
            p1_wins += 1
        else:
            p2_wins += 1

    return p1_score / games, p1_wins / games


def test_game(game, count, p_random, p1_policy_fxn, p2_policy_fxn):
    ''' Tests a search policy through a series of complete games of Kalah.
        The test passes if the search wins at least the given percentage of
        games and calls its heuristic function at most the given proportion of times
        relative to Minimax.  Writes the winning percentage of the second
        policy to standard output.

        game -- a game
        count -- a positive integer
        p_random -- the probability of making a random move instead of the suggested move
        p1_policy_fxn -- a function that takes no arguments and returns
                         a function that takes a position and returns the
                       suggested move
        p2_policy_fxn -- a function that takes no arguments and returns
                         a function that takes a position and returns the
                       suggested move
                      
    '''
    margin, wins = compare_policies(game, p1_policy_fxn, p2_policy_fxn, count, 1.0 - p_random)

    print("NET: ", margin, "; WINS: ", wins, sep="")

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test MCTS agent")
    parser.add_argument('--count', dest='count', type=int, action="store", default=2, help='number of games to play (default=2')
    parser.add_argument('--time', dest='time', type=float, action="store", default=0.1, help='time for MCTS per move')
    args = parser.parse_args()

    try:
        if args.count < 1:
            raise MCTSTestError("count must be positive")
        if args.time <= 0:
            raise MCTSTestError("time must be positive")

        game = TicTacToe()
    
        test_game(game,
                  args.count,
                  0.0,
                  lambda: mcts.mcts_policy(args.time),
                  lambda: mcts.mcts_policy(.005))
        sys.exit(0)
    except MCTSTestError as err:
        print(sys.argv[0] + ":", str(err))
        sys.exit(1)
    
