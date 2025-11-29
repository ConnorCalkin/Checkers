# Checkers
This is the capstone project for the pre-learning for Sigma Labs
In this project, I will create a command line version of checkers and hopefully create an AI that can play it too.

This implementation will be made using a bitwise representation of the board. Each bit will represent a position on the board in the following configuration:

Board representation:
   28  29  30  31 
 24  25  26  27
   20  21  22  23
 16  17  18  19
   12  13  14  15
 08  09  10  11  
   04  05  06  07 
 00  01  02  03  

 There will be three numbers. One representing the positions of the white pieces, one for the black pieces and one for the kings.

 For example, if there are white pieces on position 0 and 2, then the number for the white pieces would be 000101, or 5.

 The reason why this implementation is useful is because it allows us to use bitwise operations to do a lot of the logic that we need for the game. For example, if you wanted to know where the white kings were, you could simply do an AND operation with the white pieces and the kings. These operations make finding movable checkers or checkers that can capture go very quickly, which can be useful when creating an AI.

##How to play:
Because we are using the command line, making moves means choosing a starting position on the board and choosing an end position. These position