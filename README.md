# Ferdi

## A tiny, lovely, sweet and simple Discord bot.

It runs on Python, accepts '&gt;' as command prefix,
and currently has two commands:
---
&gt;roll: Rolls any combination of dice.

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

&gt;twss: Sends a random "That's what she said" GIF from The Office.