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
    
    def make_move(self, start_bits: int, end_bits: int):
        if self.white_turn:
            if (start_bits, end_bits) in self.get_moves_white():
                new_WP = self.WP ^ (start_bits | end_bits)
                new_K = self.K | (new_WP & K_W_R)
                if self.K & start_bits:
                        new_K &= invert(start_bits)
                        new_K |= end_bits
                return GameState(new_WP, self.BP, new_K, not self.white_turn)
        else:
            if (start_bits, end_bits) in self.get_moves_black():
                new_BP = self.BP ^ (start_bits | end_bits)
                new_K = self.K | (new_BP & K_B_R)
                if self.K & start_bits:
                        new_K &= invert(start_bits)
                        new_K |= end_bits
                return GameState(self.WP, new_BP, new_K, not self.white_turn)
            
        print("Invalid")
        return None

    
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
    
    def get_captures_white_kings(self):
        free = self.get_free_spaces()
        moves = []
        WK = self.WP & self.K
        if WK:
            movers34 = (((free << 4) & self.BP & M_3) << 3) & WK
            moves += self.create_move_trip_right(movers34, 3, 4)
            movers43 = ((((free & M_3) << 3) & self.BP) << 4) & WK
            moves += self.create_move_trip_right(movers43, 4, 3)
            movers54 = (((free << 4) & self.BP & M_5) << 5) & WK
            moves += self.create_move_trip_right(movers54, 5, 4)
            movers45 = ((((free & M_5) << 5) & self.BP) << 4) & WK
            moves += self.create_move_trip_right(movers45, 4, 5)

        return moves

    def get_captures_white(self):
        free = self.get_free_spaces()
        moves = []
        movers34 = ((((free >> 4) & self.BP) >> 3) & M_3) & self.WP
        moves += self.create_move_trip_left(movers34, 3, 4)
        movers43 = (((free >> 3) & self.BP & M_3) >> 4) & self.WP
        moves += self.create_move_trip_left(movers43, 4, 3)
        movers54 = ((((free >> 4) & self.BP) >> 5) & M_5) & self.WP
        moves += self.create_move_trip_left(movers54, 5, 4)
        movers45 = (((free >> 5) & self.BP & M_5) >> 4) & self.WP
        moves += self.create_move_trip_left(movers45, 4, 5)

        return moves + self.get_captures_white_kings()
    
    def get_captures_black_kings(self):
        free = self.get_free_spaces()
        moves = []
        BK = self.BP & self.K
        if BK:
            movers34 = ((((free >> 4) & self.WP) >> 3) & M_3) & BK
            moves += self.create_move_trip_left(movers34, 3, 4)
            movers43 = (((free >> 3) & self.WP & M_3) >> 4) & BK
            moves += self.create_move_trip_left(movers43, 4, 3)
            movers54 = ((((free >> 4) & self.WP) >> 5) & M_5) & BK
            moves += self.create_move_trip_left(movers54, 5, 4)
            movers45 = (((free >> 5) & self.WP & M_5) >> 4) & BK
            moves += self.create_move_trip_left(movers45, 4, 5)

        return moves

    def get_captures_black(self):
        free = self.get_free_spaces()
        moves = []
        movers34 = (((free << 4) & self.WP & M_3) << 3) & self.BP
        moves += self.create_move_trip_right(movers34, 3, 4)
        movers43 = ((((free & M_3) << 3) & self.WP) << 4) & self.BP
        moves += self.create_move_trip_right(movers43, 4, 3)
        movers54 = (((free << 4) & self.WP & M_5) << 5) & self.BP
        moves += self.create_move_trip_right(movers54, 5, 4)
        movers45 = ((((free & M_5) << 5) & self.WP) << 4) & self.BP
        moves += self.create_move_trip_right(movers45, 4, 5)

        return moves + self.get_captures_black_kings()
    
    def get_captures(self):
        if self.white_turn:
            return self.get_captures_white()
        else: 
            return self.get_captures_black()

    def make_capture(self, start_bits, end_bits):
        if self.white_turn:
            moves = self.get_captures_white()
            for move in moves:
                if move[0] == start_bits and move[2] == end_bits:
                    new_WP = self.WP ^ (start_bits | end_bits)
                    new_BP = self.BP ^ move[1]
                    new_K = self.K | (new_WP & K_W_R)
                    if self.K & start_bits:
                        new_K &= invert(start_bits)
                        new_K |= end_bits
                        new_K &= invert(move[1])
                    return GameState(new_WP, new_BP, new_K, not self.white_turn)
        else:
            moves = self.get_captures_black()
            for move in moves:
                if move[0] == start_bits and move[2] == end_bits:
                    new_BP = self.BP ^ (start_bits | end_bits)
                    new_WP = self.WP ^ move[1]
                    new_K = self.K | (new_BP & K_B_R)
                    if self.K & start_bits:
                        new_K &= invert(start_bits)
                        new_K |= end_bits
                        new_K &= invert(move[1])
                    return GameState(new_WP, new_BP, new_K, not self.white_turn)
        
            
        print("Invalid")
        return None
    
    def make_move_capture(self, move):
        if len(move) == 3:
            return self.make_capture(move[0], move[2])
        else:
            return self.make_move(move[0], move[1])

    def player_move(self, start : int, end : int) -> bool:
        if start == end:
            print("start and end positions are the same")
            return False
        
        start_bits = indexes_to_bits([start])
        end_bits = indexes_to_bits([end])

        new_state = None
        if self.white_turn and self.get_captures_white() :
            new_state = self.make_capture(start_bits, end_bits)
        elif not self.white_turn and self.get_captures_black():
            new_state = self.make_capture(start_bits, end_bits)
        else:
            new_state = self.make_move(start_bits, end_bits)
        
        return new_state