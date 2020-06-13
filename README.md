# **🚗python AI for solving parking puzzles🚗**

This is an Object-Oriented AI designed to solve those little puzzles where you have to move cars horizontally or vertically to make way for a specific car and exit the parking. It uses a recursive function to dig deep into the possible steps and states and find the minimum number of moves required to solve the puzzle.

## All you need to know/do

- You need the following libraries in your environment to run the script:
  - numpy
  - copy
  - itertools
  - threading
  - time
  - os
  - sys

- 🚨 Since inputting lists in python has its difficulties, the script is designed to have the input data in itself, so **before you run it, modify the input list according to your own puzzle**.

    🚨 The details on how to modify are commented in the code.

- The optimization method used for this script is A-Star. Not directly implemented, but it prioritizes reviewing states and moves that move the main car closer to the exit. This logic might not necessarily result in a faster calculation since some complex puzzles require you to move the main car back and forth, but it's better than no optimization.

- After finding a way to solve with _n_ moves required, it will skip going deeper than _n_ moves and only search for shorter paths to success.

- The output is only the minimum number of moves required to solve the puzzle.

- There have been fixes to bugs like overlapping cars, and puzzles that can't be solved in any way, or error in the input list.

- If there are problems that make this code seem amateur, well sorry, this was a project done last minute and the base structure is definitely not as optimal as it should be 🤷‍♂️.

## future plans

- [ ] Implementing an input method with ease of usage ⌨
- [ ] Further improvement in computation time and state reviewing prioritization 🕖
- [x] Memory optimization 💾
- [ ] Code optimization 📜
