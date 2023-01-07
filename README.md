# Ferdi

### A tiny, lovely, sweet Discord bot.

It runs on Python, accepts '&gt;' as command prefix,
and responds to the following commands (for now):

- &gt;roll: Rolls any combination of dice.
  ```
  Format: 'AdP+BdQ+...+CdR+X+...+Y' where A, B, C are numbers of dice,
                                  P, Q, R are die-faces, 
                                  X and Y are any integer.
          Any spaces in the expression prevents it from reading the afterwards.
          So *NO* spaces in between dice or modifiers.
          Dice number can be omitted if rolling only 1 die.

          It uses '+' signs in the string to parse it, 
          so put a '+' before the '-' for negative modifiers.
        
  Example: >roll 2d8+d6+3d20+5+-4
  Output:  (2, 1) | (2) | (14, 14, 10) | + (5) | + (-4) | Total: 44
  ```
- &gt;rollability: Rolls 6 sets of 4d6 and keeps highest 3 for each set.
        Used when creating D&D characters.
  ```
  Output: (1, 4, 4, 2)
          (5, 3, 4, 1)
          (4, 1, 2, 1)
          (6, 5, 5, 3)
          (4, 3, 5, 2)
          (6, 1, 3, 6)
  
          Results: 16, 15, 12, 12, 10, 7
  ```
- &gt;rollfate: Rolls Fate RPG dice.
  ```
  Example: >rollfate 2
  Output:  (  ) (  ) (+) (+) | Mod: 2 
           Result: 4
  
  OR
  
  Example: >rollfate
  Output:  (+) (-) (+) (  ) | Mod: 0 
           Result: 1
  ```
- &gt;twss: Sends a random "That's what she said" GIF from The Office.
- &gt;source: Sends the link to here.