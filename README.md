# tetrisrl
 Tetris built in Python for reinforcement learning
## Installation
Install the required packages listed in [requirements.txt](requirements.txt)
## Description
The goal was to make a fully playable version of Tetris (T-spins included) that adhered to the Tetris Guideline. I also wanted to create a Tetris environment using the OpenAi gym framework.
## Usage
Run the [game.py](game.py) file in order to play Tetris using the WASD and arrow keys. 
```bash
python game.py
```
You can optionally change the key bindings in this file.
* W = hard drop
* A = move left
* S = soft drop
* D = move right
* up arrow key = hold
* left arrow key = rotate counter-clockwise
* right arrow key = rotate clockwise

Run the [t.py](t.py) file in order to run the simulation in order to train the neural network.
```bash
python t.py
```
## Features
This version of modern Tetris features the SRS rotation system, both mini and regular t-spins and a combo system. There is also an implementation of back to back difficult clears which awards more points. There is a hold mechanism and the game shows the next 7 pieces to be dropped. The drop order is determined using a 7 piece bag after which they are then put into the queue.

The neural network takes in a state that contains the board, what piece is being held and currently controlled as well as the next 7 pieces in the queue. Also the position and rotation of the current piece is taken into account.

The actions taken at each state resemble what an actual human does as it can move left and right and perform any of the seven actions listed in the controls above.

## License
[MIT](https://choosealicense.com/licenses/mit/)
