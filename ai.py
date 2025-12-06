from board import GameState, bits_to_indexes
import random

class AI:
    MAX = 1000
    MIN = -1000
    

    def random_move(self, gamestate):
        possible_moves = self.get_possible_moves(gamestate)
        random_move = random.choice(possible_moves)
        for move in possible_moves:
            moveD = []
            for item in move:
                moveD += bits_to_indexes(item)
            print(moveD)
        return gamestate.make_move_capture(random_move)
    
    def get_possible_moves(self, gamestate):
        possible_moves = []
        if gamestate.white_turn:
            captures = gamestate.get_captures_white()
            if captures != []:
                possible_moves = captures
            else:
                possible_moves = gamestate.get_moves_white()
        else:
            captures = gamestate.get_captures_black()
            if captures != []:
                possible_moves = captures
            else:
                possible_moves = gamestate.get_moves_black()
        return possible_moves

    def minimax(self, gamestate, max_depth, depth = 0, alpha = MIN, beta = MAX):
        possible_moves = self.get_possible_moves(gamestate)
        if depth == max_depth or possible_moves == []:
            return None, self.evaluate(gamestate)

        isMax = not gamestate.white_turn
        best_move = None
        best_score = None

        if isMax:
            for move in possible_moves:
                new_state = gamestate.make_move(move[0] , move[-1])
                _, score = self.minimax(new_state, max_depth, depth + 1, alpha, beta)
                if (best_score == None or best_score < score):
                    best_score = score
                    best_move = new_state
                    alpha = max(best_score, alpha)
                    if alpha >= beta:
                        break
        if not isMax:
            for move in possible_moves:
                new_state = gamestate.make_move(move[0] , move[-1])
                _, score = self.minimax(new_state, max_depth, depth + 1, alpha, beta)
                if (best_score == None or best_score > score):
                    best_score = score
                    best_move = new_state
                    beta = min(best_score, beta)
                    if alpha >= beta:
                        break
                    
        return best_move, best_score


    def evaluate(self, gamestate):
        num_BP = len(bits_to_indexes(gamestate.BP))        
        num_WP = len(bits_to_indexes(gamestate.WP))
        return num_BP - num_WP
    