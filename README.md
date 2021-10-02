# Virtual drag-and-drop jigsaw using OpenCV

## About
Jigsaw puzzles were always fun to solve. This project was aimed at recreating the explerience virtually, using Computer Vision. The game can be played by dragging constituent square-shaped pieces of an image virtually, to complete the correct order of arrangement as per the original image. 

_src_ contains a README on how to use this project.

*add preview**

## Project Structure

```bash
├── input images            # Sample images that were used.
│   ├── i1.jpg        
│   ├── i2.jpg   
├── src                     # Source code used in this project.
    ├── create_jigsaw.py    # Creates the jigsaw out of the input image.
    ├── images.py           # Describes the characteristics of each constituent piece.
    ├── main.py             # Executes the project.
    ├── run.py              # Contains utility functions needed once the game has begun. 
    ├── README.md               # Set of instructions on how to use this project and play the game.
├── README.md               # A top-level README about this project.
```

## Required
Python 3.7 | OpenCV 4.5.2.54 | Mediapipe 0.8.5
