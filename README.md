# Buttons Game

This project takes inspiration from the Reaction Game exhibited at the National Museum of Scotland and incorporates ideas from the [pico-button-game-keypad](https://github.com/jcabrerizo/pico-button-game-keypad).

## How to Play

To start the game, execute the script [run.py](./run.py). The display will show the remaining game time at the top and indicate the color corresponding to the button you need to press. Although multiple LEDs may be illuminated, only one matches the displayed color, making it the correct choice.

During gameplay, the display will update to show both the remaining time and the count of correctly pressed buttons. At the end of the game, the display will provide a summary, including the total number of incorrect presses and the percentage of correct responses.

## Development Environment

- **IDE**: Visual Studio Code with the official [Raspberry Pi Pico extension](https://marketplace.visualstudio.com/items?itemName=raspberry-pi.raspberry-pi-pico).  
- **Setup**: Since the project consists of multiple files, the entire project must be uploaded to the device before running the `main.py` script.

## Planned Enhancements

1. **User Experience Improvements**  
   - [ ] Additional lighting effects.  

2. **Customizable Game Duration**  
   - [ ] Allow players to adjust the game timer.  

3. **Multiplayer Features**  
   - [ ] Add Wi-Fi support for multiplayer modes.  
   - [ ] Implement score storage and leaderboards.  
