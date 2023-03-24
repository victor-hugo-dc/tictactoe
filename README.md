### **Tic-Tac-Toe Monte Carlo Tree Search**

The following code is an adaptation from my *CPSC 474: Computational Intelligence for Games* Monte Carlo Search Tree for use on a Tic Tac Toe game implemented using bitboards.

**The Logic**

Both players are represented as two 16-bit integers, of which we'll only be using nine bits. 
```{python}
self.player_x = 0b0000000000000000
self.player_o = 0b0000000000000000
```

Given a position (a value between 0-8 inclusive) we can update the value of the board by updating the player's integer by shifting to the position and oring it with 1.
```{python}
self.player_x |= 1 << position
```
In this way, we can check for winning positions using certain bit masks and a for loop of fixed size.
```{python}
winning_masks = [
                0b111000000, 0b000111000, 0b000000111,
                0b100100100, 0b010010010, 0b001001001,
                0b100010001, 0b001010100 
            ]

for mask in winning_masks:
    if self.player_x & mask == mask:
        return 1
                
    elif self.player_o & mask == mask:
        return -1
            
    if self.player_x | self.player_o == 0b111111111:
        return 0
```
