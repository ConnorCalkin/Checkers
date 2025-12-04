from board import GameState, bits_to_indexes
import random

class AI:
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

    def minimax(self, gamestate, max_depth, depth = 0):
        
        
        possible_moves = self.get_possible_moves(gamestate)
        if depth == max_depth or possible_moves == []:
            return None, self.evaluate(gamestate)

        isMax = not gamestate.white_turn
        best_move = None
        best_score = None
        for move in possible_moves:
            new_state = gamestate.make_move_capture(move)
            _, score = self.minimax(new_state, max_depth, depth + 1)
            try:
                if (best_score == None or 
                    (isMax and best_score < score) or 
                    (not isMax and best_score > score)):
                    best_score = score
                    best_move = new_state
            except:
                new_state.display()
                best_move.display()
                print(best_score)
                print(score)

        return best_move, best_score


    def evaluate(self, gamestate):
        num_BP = len(bits_to_indexes(gamestate.BP))        
        num_WP = len(bits_to_indexes(gamestate.WP))
        return num_BP - num_WP
    