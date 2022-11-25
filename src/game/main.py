"""
Main for playing platonic ham.
"""

from walk_the_loop import WalkTheLoop


def main(numbered=True):
    """
    Run Icosian Game.
    """
    game = WalkTheLoop(numbered=numbered)
    game.play()


if __name__ == '__main__':
    main(numbered=False)
