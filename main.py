from typing import List

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
    return (1 << len(format(n,'08b'))) - 1 - n

def bits_to_indexes(n : int) -> List[int]:
    #gets the board positions given a bitwise representation

    #TODO:: implement this as a generator that pops off the least
    #significant bit. I think it would be more efficient.
    bits = format(n, "08b")
    bits = bits[::-1]
    return [i for i, x in enumerate(bits) if not x == "0"]

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

class GameState:
    def __init__(self, WP : int = 4095, BP :int = 4293918720):
        self.WP = WP
        self.BP = BP

    def display(self) -> None:
        board = []
        for i in range(8):
            row = [0] * 8
            for j in range(i % 2, 8, 2):
                index = (i * 4 + j // 2)
                if (2**(index)) & self.WP:
                    row[j] = 1
                elif (2**(index)) & self.BP:
                    row[j] = 2                
            board.append(row)
        
        board.reverse()
        for row in board:
            print(row)
        print()

    def get_free_spaces(self) -> int:
        occupied = (self.BP | self.WP)
        return invert(occupied)

    def get_captures_white(self):
        '''
            returns all of the white pieces that can capture a black piece
        '''
        free = self.get_free_spaces()
        #move back 4 then 3
        #I think of the logic as: we move back 4, then check if its a 
        #black piece, then we move 3 and check that that is a spot you
        #can move 3 from and that it is a white piece. If it is, that
        #white piece can capture
        movers = ((((free >> 4) & self.BP) >> 3) & M_3) & self.WP
        #move back 4 then 5
        movers |= ((((free >> 4) & self.BP) >> 5) & M_5) & self.WP
        #move back 3 then 4
        movers |= (((free >> 3) & self.BP & M_3) >> 4) & self.WP
        #move back 5 then 4
        movers |= (((free >> 5) & self.BP & M_5) >> 4) & self.WP
        return movers
    
    def check_valid_move_white(self, start_bits: int, end_bits: int) -> bool:
        return ((end_bits >> 4 & start_bits) |
            (end_bits >> 3 & start_bits & M_3) | 
            (end_bits >> 5 & start_bits & M_5))

    def check_valid_move_black(self, start_bits: int, end_bits: int) -> bool:
        return ((start_bits >> 4 & end_bits) |
            (start_bits >> 3 & end_bits & M_3) | 
            (start_bits >> 5 & end_bits & M_5))
        
    def check_valid_move(self, start_bits: int, end_bits: int, white: bool) -> bool:
        if not (end_bits & self.get_free_spaces()):
            print("end space is occupied")
            return False

        if white:
            #check that start tile is white
            if not (start_bits & self.WP):
                print("start space does not have a piece owned by you")
                return False
            
            if not self.check_valid_move_white(start_bits, end_bits):
                print("Invalid Move")
                return False
        else:
            #check that start tile is black
            if not (start_bits & self.BP):
                print("start space does not have a piece owned by you")
                return False
            
            if not self.check_valid_move_black(start_bits, end_bits):
                print("Invalid Move")
                return False
            
        return True

        


    def player_move(self, start : int, end : int, white_turn : bool) -> bool:
        '''
            updates board based on player move. Returns true if valid move
            was played, returns false if invalid move was played
        '''
        
        if start == end:
            print("start and end positions are the same")
            return False
        
        start_bits = indexes_to_bits([start])
        end_bits = indexes_to_bits([end])
        joint_bits = start_bits + end_bits

        if not self.check_valid_move(start_bits, end_bits, white_turn):
            return False
        
        if white_turn == True:
            self.WP = self.WP ^ joint_bits
        else:
            self.BP = self.BP ^ joint_bits

        print(bits_to_indexes(self.get_free_spaces()))
        print(bits_to_indexes(self.get_captures_white()))
        return True
    

    


board = GameState()
board.display()
white_turn = True

while True:
    start = int(input("start: "))
    end = int(input("end: "))
    if (board.player_move(start, end, white_turn)):
        board.display()
        white_turn = not white_turn
    





