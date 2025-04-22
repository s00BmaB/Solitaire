A solitaire project made as part of programming course in uni.  
=====

*My first project of a scale that big so things are broken.  
Lost access to uni repo after course finished so made new one and things may have broken even more during the moving process.(I can't use git properly yet, etc.).*  
*Also probably got bad gitignore.*  
*works on python arcade 2.6.17*

Basic instructions/rules if someone gets here
======

|                  **Action**                   | **KeyBind** |
|:---------------------------------------------:|:-----------:|
|                     Pause                     |     Esc     |
|                     Reset                     |      R      |
| Auto move a card to done pile in classic mode | CTRL + LMB  | 

## CLASSIC
- **Objective:**  
    - Move all cards to the four foundation piles, arranged in ascending order (Ace to King) by suit.

- **Rules:** 
  - Played with **regular deck(52 cards)**.
  - Build tableau columns in descending order, alternating colors.
  - Only a King or a sequence starting with a King can be moved to an empty column.
  - Draw cards from the stockpile when no moves are available.
  - The game is won when all foundation piles are complete.  
 
## SPIDER
- **Objective:**  
    - Arrange all cards in descending order (King to Ace) within the tableau and remove completed sequences.

- **Rules:**
  - Played with **two decks (104 cards)** of a single color.
  - Build sequences in descending order within a column.
  - Only completed sequences of the same suit (King to Ace) are removed automatically.
  - Empty columns can be filled with any card or sequence.
  - Draw from the stockpile when no moves are available.
  - To draw from a stockpile at least one card in each column is needed.

### After finishing Your time can be saved into the respective score list with the name you give  
*bug warning (can't see what is typed) don't know how to fix*  
*score list is a simple .txt file with no ordering*

gitfront link:
https://gitfront.io/r/BamB00s/gbLDKUuU9CFw/Solitaire/

Signed:  
***BamB00s***
