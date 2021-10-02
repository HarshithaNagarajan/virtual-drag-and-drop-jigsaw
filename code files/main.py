from run import start_game

def main():
    """
    name: name of the image for creating the puzzle
    parts: Number of pieces in the puzzle
           Note: Must be a whole number square eg: 4, 9, 16, 25, 36...
                 Preferably an odd number
    path: path of the folder to store cropped pieces of the puzzle
    """

    name = "i2.jpg"
    parts = 4
    path = 'cropped'
    start_game(name, parts, path)


if __name__ == '__main__':
    main()
