from typing import List
import math

'''
Board representation:
   28  29  30  31
 24  25  26  27
   20  21  22  23
 16  17  18  19
   12  13  14  15
 08  09  10  11
   04  05  06  07
 00  01  02  03
'''

def invert(n : int) -> int:
    #inverts the bits given an integer I wanted to use ~ but that
    #operator doesn't work for this purpose as it uses negatives
    return n ^ 4294967295

def bits_to_indexes(n : int) -> List[int]:
    #gets the board positions given a bitwise representation

    indexes = []
    while n > 0:
        LSB = ((n ^ (n - 1)) + 1) >> 1
        indexes.append(round(math.log2(LSB)))
        n = n ^ LSB
    return indexes

def get_single_bits(n):
    bits = []
    while n > 0:
        LSB = ((n ^ (n - 1)) + 1) >> 1
        bits.append(LSB)
        n = n ^ LSB
    return bits


def indexes_to_bits(indexes : List[int]) -> int:
    #gets the bitwise representation given the board positions
    out = 0
    for index in indexes:
        out += 2**index
    return out

def output_moves(self, moves):
    for move in moves:
        self.output_move(move)

def output_move(self, move):
    out = []
    for item in move:
        out += bits_to_indexes(item)
    print(out)

#M_3 and M_5 show the positions from which adding 3 or 5 to its index
#gives you a valid move. For example, in the representation, going from
#1 to 4 is valid but 5 to 8 is invalid
M_3 = indexes_to_bits([1,2,3,9,10,11,17,18,19,25,26,27])
M_5 = indexes_to_bits([4,5,6,12,13,14,20,21,22])
K_W_R = indexes_to_bits([28,29,30,31])
K_B_R = indexes_to_bits([0,1,2,3])

class GameState:
    def __init__(self, WP : int = 4095, BP :int = 4293918720, K : int = 0, white_turn : bool = True):
        self.WP = WP
        self.BP = BP
        self.K = K
        self.white_turn = white_turn

    def display(self) -> None:
        board = []
        for i in range(8):
            row = [0] * 8
            for j in range(i % 2, 8, 2):
                index = (i * 4 + j // 2)
                position = 2**(index)
                if position & self.WP:
                    if position & self.K:
                        row[j] = 3
                    else:
                        row[j] = 1
                elif position & self.BP:
                    if position & self.K:
                        row[j] = 4
                    else:
                        row[j] = 2
            board.append(row)

        board.reverse()
        for row in board:
            print(row)
        print()

    def get_free_spaces(self) -> int:
        occupied = (self.BP | self.WP)
        return invert(occupied)


    def create_move_pairs_left(self, starts, offset):
        move_pairs = []
        for position in get_single_bits(starts):
            move_pairs.append((position, position << offset))
        return move_pairs

    def create_move_pairs_right(self, starts, offset):
        move_pairs = []
        for position in get_single_bits(starts):
            move_pairs.append((position, position >> offset))
        return move_pairs

    def get_moves_white_kings(self):
        free = self.get_free_spaces()
        WK = self.WP & self.K
        moves = []
        if WK:
            moves4 = (free << 4 & WK)
            moves3 = ((free & M_3) << 3 & WK)
            moves5 = ((free & M_5) << 5 & WK)
            moves += self.create_move_pairs_right(moves4, 4)
            moves += self.create_move_pairs_right(moves3, 3)
            moves += self.create_move_pairs_right(moves5, 5)
        return moves

    def get_moves_white(self):
        free = self.get_free_spaces()
        moves4 = (free >> 4 & self.WP)
        moves3 = (free >> 3 & self.WP & M_3)
        moves5 = (free >> 5 & self.WP & M_5)
        moves = []
        moves += self.create_move_pairs_left(moves4, 4)
        moves += self.create_move_pairs_left(moves3, 3)
        moves += self.create_move_pairs_left(moves5, 5)
        return moves + self.get_moves_white_kings()

    def get_moves_black_kings(self):
        free = self.get_free_spaces()
        BK = self.BP & self.K
        moves = []
        if BK:
            moves4 = (free >> 4 & BK)
            moves3 = (free >> 3 & BK & M_3)
            moves5 = (free >> 5 & BK & M_5)
            moves += self.create_move_pairs_left(moves4, 4)
            moves += self.create_move_pairs_left(moves3, 3)
            moves += self.create_move_pairs_left(moves5, 5)
        return moves

    def get_moves_black(self):
        free = self.get_free_spaces()
        moves4 = (free << 4 & self.BP)
        moves3 = ((free & M_3) << 3 & self.BP)
        moves5 = ((free & M_5) << 5 & self.BP)
        moves = []
        moves += self.create_move_pairs_right(moves4, 4)
        moves += self.create_move_pairs_right(moves3, 3)
        moves += self.create_move_pairs_right(moves5, 5)
        return moves + self.get_moves_black_kings()


    def create_move_trip_right(self, starts, offset1, offset2):
        move_pairs = []
        for position in get_single_bits(starts):
            move_pairs.append((position, position >> offset1, position >> (offset1 + offset2)))
        return move_pairs

    def create_move_trip_left(self, starts, offset1, offset2):
        move_pairs = []
        for position in get_single_bits(starts):
            move_pairs.append((position, position << offset1, position << (offset1 + offset2)))
        return move_pairs

    def get_captures_white(self, start_positions = None, kings = None, previous_start_positions = None):
        if start_positions == None:
            start_positions = self.WP
        if kings == None:
            kings = self.K
        start_kings = start_positions & kings

        free = self.get_free_spaces()
        moves = []
        movers34 = ((((free >> 4) & self.BP) >> 3) & M_3) & start_positions
        movers43 = (((free >> 3) & self.BP & M_3) >> 4) & start_positions
        movers54 = ((((free >> 4) & self.BP) >> 5) & M_5) & start_positions
        movers45 = (((free >> 5) & self.BP & M_5) >> 4) & start_positions
        moves += self.create_move_trip_left(movers34, 3, 4)
        moves += self.create_move_trip_left(movers43, 4, 3)
        moves += self.create_move_trip_left(movers54, 5, 4)
        moves += self.create_move_trip_left(movers45, 4, 5)

        end_positions = (movers43 | movers34) << 7
        new_kings = ((movers43 | movers34) & kings) << 7
        end_positions |= (movers54 | movers45) << 9
        new_kings |= ((movers54 | movers45) & kings) << 9

        if start_kings:
            movers34 = (((free << 4) & self.BP & M_3) << 3) & start_kings
            movers43 = ((((free & M_3) << 3) & self.BP) << 4) & start_kings
            movers54 = (((free << 4) & self.BP & M_5) << 5) & start_kings
            movers45 = ((((free & M_5) << 5) & self.BP) << 4) & start_kings
            moves += self.create_move_trip_right(movers34, 3, 4)
            moves += self.create_move_trip_right(movers43, 4, 3)
            moves += self.create_move_trip_right(movers54, 5, 4)
            moves += self.create_move_trip_right(movers45, 4, 5)
            end_positions |= (movers43 | movers34) >> 7
            new_kings |= ((movers43 | movers34) & kings) >> 7
            end_positions |= (movers54 | movers45) >> 9
            new_kings |= ((movers54 | movers45) & kings) >> 9

        if previous_start_positions != None:
            end_positions &= invert(previous_start_positions)
            moves = [move for move in moves if not (move[-1] & previous_start_positions)]

        new_moves = []
        if end_positions:
            new_captures_kings = self.get_captures_white(end_positions & new_kings, new_kings, start_positions)
            new_captures_minus_kings = self.get_captures_white(end_positions, 0 , start_positions)
            new_moves = [move + new_move[1:]
                         for move in moves for new_move in new_captures_minus_kings
                         if move[-1] == new_move[0]]
            new_moves += [move + new_move[1:]
                         for move in moves for new_move in new_captures_kings
                         if move[-1] == new_move[0] and move[0] & kings]

            moves += new_moves
            new_moves = []
            for move1 in moves:
                smaller = False
                for move2 in moves:
                    if move1 == move2[:len(move1)] and move1 != move2:
                        smaller = True
                        break
                if not smaller:
                    new_moves.append(move1)
            moves = new_moves

        return moves


    def get_captures_black(self, start_positions = None, kings = None, previous_start_positions = None):
        if start_positions == None:
            start_positions = self.BP
        if kings == None:
            kings = self.K
        start_kings = start_positions & kings
    
        free = self.get_free_spaces()
        moves = []
        movers34 = (((free << 4) & self.WP & M_3) << 3) & start_positions
        moves += self.create_move_trip_right(movers34, 3, 4)
        movers43 = ((((free & M_3) << 3) & self.WP) << 4) & start_positions
        moves += self.create_move_trip_right(movers43, 4, 3)
        movers54 = (((free << 4) & self.WP & M_5) << 5) & start_positions
        moves += self.create_move_trip_right(movers54, 5, 4)
        movers45 = ((((free & M_5) << 5) & self.WP) << 4) & start_positions
        moves += self.create_move_trip_right(movers45, 4, 5)

        end_positions = (movers43 | movers34) >> 7
        new_kings = ((movers43 | movers34) & kings) >> 7
        end_positions |= (movers54 | movers45) >> 9
        new_kings |= ((movers54 | movers45) & kings) >> 9

        if start_kings:
            movers34 = ((((free >> 4) & self.WP) >> 3) & M_3) & start_kings
            moves += self.create_move_trip_left(movers34, 3, 4)
            movers43 = (((free >> 3) & self.WP & M_3) >> 4) & start_kings
            moves += self.create_move_trip_left(movers43, 4, 3)
            movers54 = ((((free >> 4) & self.WP) >> 5) & M_5) & start_kings
            moves += self.create_move_trip_left(movers54, 5, 4)
            movers45 = (((free >> 5) & self.WP & M_5) >> 4) & start_kings
            moves += self.create_move_trip_left(movers45, 4, 5)
            end_positions |= (movers43 | movers34) << 7
            new_kings |= ((movers43 | movers34) & kings) << 7
            end_positions |= (movers54 | movers45) << 9
            new_kings |= ((movers54 | movers45) & kings) << 9

        if previous_start_positions != None:
            end_positions &= invert(previous_start_positions)
            moves = [move for move in moves if not (move[-1] & previous_start_positions)]

        new_moves = []
        if end_positions:
            new_captures_kings = self.get_captures_black(end_positions & new_kings, new_kings, start_positions)
            new_captures_minus_kings = self.get_captures_black(end_positions, 0 , start_positions)
            new_moves = [move + new_move[1:]
                         for move in moves for new_move in new_captures_minus_kings
                         if move[-1] == new_move[0]]
            new_moves += [move + new_move[1:]
                         for move in moves for new_move in new_captures_kings
                         if move[-1] == new_move[0] and move[0] & kings]

            moves += new_moves
            new_moves = []
            for move1 in moves:
                smaller = False
                for move2 in moves:
                    if move1 == move2[:len(move1)] and move1 != move2:
                        smaller = True
                        break
                if not smaller:
                    new_moves.append(move1)
            moves = new_moves

        return moves

    def get_captures(self):
        if self.white_turn:
            return self.get_captures_white()
        else:
            return self.get_captures_black()

    def make_move(self, start_bits, end_bits):
        if self.white_turn:
            moves = self.get_captures_white()
            if moves == []:
                moves = self.get_moves_white()

            moves = [move for move in moves
                    if move[0] == start_bits and move[-1] == end_bits]
            
            if moves == []:
                print("Invalid move")
                return None
        
            move = moves[0]
        
            new_WP = self.WP ^ (start_bits | end_bits)
            new_K = self.K | (new_WP & K_W_R)
            new_BP = self.BP

            for i in range(1, len(move) - 1, 2):
                new_BP = new_BP ^ move[i]
                new_K &= invert(move[i])

            if self.K & start_bits:
                new_K &= invert(start_bits)
                new_K |= end_bits
                
            return GameState(new_WP, new_BP, new_K, not self.white_turn)
        else:
            moves = self.get_captures_black()
            if moves == []:
                moves = self.get_moves_black()

            moves = [move for move in moves
                    if move[0] == start_bits and move[-1] == end_bits]
            
            if moves == []:
                print("Invalid move")
                return None
            
            move = moves[0]
            
            new_BP = self.BP ^ (start_bits | end_bits)
            new_K = self.K | (new_BP & K_B_R)
            new_WP = self.WP
            
            for i in range(1, len(move) - 1, 2):
                new_WP = new_WP ^ move[i]
                new_K &= invert(move[i])

            if self.K & start_bits:
                new_K &= invert(start_bits)
                new_K |= end_bits
            return GameState(new_WP, new_BP, new_K, not self.white_turn)


        print("Invalid")
        return None

    def player_move(self, start : int, end : int) -> bool:
        if start == end:
            print("start and end positions are the same")
            return False

        start_bits = indexes_to_bits([start])
        end_bits = indexes_to_bits([end])

        new_state = None
        new_state = self.make_move(start_bits, end_bits)

        return new_state