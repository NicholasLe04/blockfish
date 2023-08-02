# Blockfish
stockfish if it was written by someone REALLY dumb

# How Blockfish blockfishes
Like most basic chess engines, it uses the minimax algorithm ([Epic video by Sebastian Lague](https://www.youtube.com/watch?v=l-hh51ncgDI))
Basically, it assumes both players will choose the best move for themselves. Using that, it searches through every possible position to a given depth assuming white will choose the move with the greatest evaluation and black will choose the move with the least evaluation. It then chooses the move which will result in the best material evaluation.

## Optimizations 
### Completed
- Alpha-Beta Pruning - Essentially, while traversing the possible positions, if the algorithm encounters a position from which it is guaranteed a worse evaluation than
  what has already been searched (for example: it finds a position with <=1 evaluation when it has found another position with a <= 5 evaluation) it will prune that part of the tree,
  reducing the amount of searches.
- Move Ordering - In order to prune as much as possible, it is important to search the best moves first. A very simple approach Blockfish takes is by placing captures ahead of quiet moves in the move ordering.
- Zobrist Hashing - Use Zobrist Hashing to store the current state of a board in a bitstring. This allows easier unmoves by easily loading previous states.
- Transposition Table / Memoization - The algorithm can store a position's evaluation and best move, using its Zobrist Hash as a key, in a transposition table so that if it runs into that position again, it can simply search it in the table.


### To-Do
- Better move ordering (MVV-LVA)
- Instead of having 12 different bitboard variables that need to be scanned through each time, create a dictionary for easy bitboard lookup.
