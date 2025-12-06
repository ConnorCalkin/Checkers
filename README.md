# Checkers
This is the capstone project for the pre-learning for Sigma Labs

In this project, I have created an application that allows you to play checkers against an AI.

## How to run the program

After cloning the repository, navigate to the file.

To play checkers against an AI, run the following command
```console
python3 main.py
```

If you would like to use the board generator to get bitwise representation of different boards, then run this command instead:
```console
python3 board_generator.py
```

## How to play:

Moves can be made by clicking the piece you intend to move and then clicking the space you want to move to. The AI opponent will automatically make a move against you after.

## Checkers Implementation

This implementation will be made using a bitwise representation of the board. Each bit will represent a position on the board in the following configuration:

Board representation:
|    | 28 |    | 29 |    | 30 |    | 31 |
|----|----|----|----|----|----|----|----|
| 24 |    | 25 |    | 26 |    | 27 |    |
|    | 20 |    | 21 |    | 22 |    | 23 |
| 16 |    | 17 |    | 18 |    | 19 |    |
|    | 12 |    | 13 |    | 14 |    | 15 |
| 8  |    | 9  |    | 10 |    | 11 |    |
|    | 4  |    | 5  |    | 6  |    | 7  |
| 0  |    | 1  |    | 2  |    | 3  |    |

 There will be three numbers. One representing the positions of the white pieces, one for the black pieces and one for the kings.

 For example, if there are white pieces on position 0 and 2, then the number for the white pieces would be 000101, or 5.

 The reason why this implementation is useful is because it allows us to use bitwise operations to do a lot of the logic that we need for the game. For example, if you wanted to know where the white kings were, you could simply do an AND operation with the white pieces and the kings. These operations make finding movable checkers or checkers that can capture go very quickly, which can be useful when creating an AI.

## AI implementation

The AI has been implemented using the minimax algorithm. I have also added alpha-beta pruning that has allowed the depth to improve significantly.

The current evaluation function calculates the difference between the counts of the pieces between black and white. This seems to work pretty well, as the AI is better than me, but I'm not very good at checkers. It may still be better to add kings to the evaluation function or to

## References

I got the idea for using checkers bitboards from this website:
https://3dkingdoms.com/checkers/bitboards.htm

I learned about minimax and alpha-beta pruning from:
https://www.geeksforgeeks.org/dsa/minimax-algorithm-in-game-theory-set-1-introduction/