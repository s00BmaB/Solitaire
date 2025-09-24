A solitaire project made as part of programming course in uni and then expanded after the course ended.  
=====

*My first project of a scale that big so the chance of things being broken is high due to maybe obvious reasons (still learning).*

Made possible by Python Arcade 2.6.17 page: ([https://api.arcade.academy/en/2.6.17/)](https://api.arcade.academy/en/2.6.17/))

# Installation Guide

## Prerequisites
- Made and tested with python 3.11.9 MAY work with versions close to this one ([https://www.python.org/downloads/)](https://www.python.org/downloads/))
- Make sure to check "Add Python to PATH" during installation (Windows)

## Quick Setup

1. **Download the project**
   ```bash
   # Download ZIP from the repo or clone with git
   git clone https://github.com/s00BmaB/Solitaire
   cd Solitaire
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create venv
   python -m venv venv
   
   # Activate it
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the game**
   ```bash
   python main.py
   ```

## Troubleshooting
- **"Python not recognized"**: Reinstall Python with "Add to PATH" checked
- **Module errors**: Make sure virtual environment is activated (you should see `(venv)` in terminal)
- **Game won't start**: Verify Python 3.11.9 with `python --version`

---
*Virtual environment must be activated each time you want to run the game*

Basic instructions and rules for people who never seen solitaire
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

github link:
https://github.com/s00BmaB/Solitaire

Signed:  
***BamB00s***
