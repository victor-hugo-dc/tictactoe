import random
from math import log, sqrt
from game import State
import copy
from time import perf_counter

CONST = 2 * sqrt(2)

def mcts_policy(time_limit: float):
    def fxn(pos: State):
        t: Tree = Tree(pos)
        time_elapsed = 0.
        while time_elapsed < time_limit:
            start = perf_counter()
            node = t.traverse_tree()

            if node.state.is_terminal():
                reward = node.state.payoff()
                t.backprop_reward(node, reward)
            else:
                next = node.expand()
                t.simulate(next)
            
            end = perf_counter()
            time_elapsed += (end - start)

        return t.next_move()
    return fxn


class Node:
    
    def __init__(self, state: State, parent = None, move = None):
        self.state: State = state
        self.children: list = []
        self.unexpanded_children: list = state.get_actions()
        self.reward: float = 0
        self.visits: float = 0
        self.parent: Node = parent
        self.move = move

    def mean_reward(self) -> float:
        return self.reward / self.visits

    def ucb(self) -> float:
        if self.parent.state.actor() == 0:
            return self.mean_reward() + CONST * sqrt(2 * (log(self.parent.visits)) / self.visits)
        return self.mean_reward() - CONST * sqrt(2 * (log(self.parent.visits)) / self.visits)

    def add_child(self, move):
        next: Node = Node(self.state.successor(move), self, move)
        self.children.append(next)
        return next

    def expand(self):
        index: int = random.randint(0, len(self.unexpanded_children) - 1)
        move = self.unexpanded_children.pop(index)
        return self.add_child(move)

class Tree:
    def __init__(self, state: State):
        self.root: Node = Node(state = state)

    def next_move(self):
        mean_rewards = []
        for child in self.root.children:
            mean_rewards.append(child.mean_reward())

        opt_child: int = -1
        if(self.root.state.actor() == 0):
            opt_child = mean_rewards.index(max(mean_rewards))
        else:
            opt_child = mean_rewards.index(min(mean_rewards))
        return self.root.children[opt_child].move

    def traverse_tree(self):
        curr: Node = self.root
        while(not curr.state.is_terminal()):
            if(len(curr.unexpanded_children) != 0): break
            curr = self.select(curr)
        return curr

    '''Simulate the game until the end and then backprop the reward'''
    def simulate(self, node: Node):
        curr_state: State = node.state

        while(not curr_state.is_terminal()):
            possible_moves: list = curr_state.get_actions()
            next_move = random.choice(possible_moves)
            curr_state = curr_state.successor(next_move)

        reward = curr_state.payoff()
        self.backprop_reward(node, reward)

    '''Select the optimal child based on UCB values'''
    def select(self, node: Node):
        ucb_values: list = []
        for child in node.children:
            ucb_values.append(child.ucb())
        next_idx: int = -1
        if(node.state.actor() == 0):
            next_idx = ucb_values.index(max(ucb_values))
        else:
            next_idx = ucb_values.index(min(ucb_values))
        return node.children[next_idx]

    '''Backpropagate the reward and number of visits upward'''
    def backprop_reward(self, node: Node, reward: float):
        curr: Node = node
        while(curr != None):
            curr.visits += 1
            curr.reward += reward
            curr = curr.parent
