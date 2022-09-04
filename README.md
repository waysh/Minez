# Minez
#### Description:

##### General Overview:
Minesweeper but worse. + dark mode. Uncover all the squares that arent mines and you win :D. Uncover a mine and you lose :(.
Written in python with the pygame library.

##### Menu:

When app.py is run the menu is initiated. The menu allows you to choose the dimensions of the play field and the number of mines.


##### Main:

##### Reducing guesses

The position of the mines is randomly generated. The entire point of the game is to deduce the position of each mine using L O G I C skills! WOW! But wait. What about the very first square you uncover? How could you know if it's a mine or not? GREAT QUESTION! You can't. So I added a feature that marks one square that isn't a mine for you to uncover. 
But but but- you say. How would that help? what if it just says 1 after i uncover it? how am i supposed to D E D U C E which of the surrounding 8 squares is ZE MINE? Brozzer asks a very good question. So i made it so that it marks a square whomst's'er surrounding squares are also not mines, this way it ensures that you start with at least more information than one square. Ofc that doesnt gaurantee that it's solvable, it just increase the likelihood that it is. kekw. This ALGORITHM starts at the center square and does the rolley polley until it finds a square that meets said conditions and it marks it. OK. Thats it. Thats all i did to reduce GUESSING. Theres minesweeper clones online that have a no guessing mode which ensures every board is solvable without guessing. But. uhhh. idk. i havent gotten around to that yet and i dont think i will. In truth. I shamefully admit that i lack the necessary brain cells to implement such a system.

##### Clearing nearby mines

wow recursion! 

##### BOOM

uhhh. 
