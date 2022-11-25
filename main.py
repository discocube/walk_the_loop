"""
Main for playing platonic ham.
"""

from game.walk_the_loop import WalkTheLoop


def main(numbered=None):
    """
    Run Icosian Game.
    """
    game = WalkTheLoop(numbered=numbered)
    game.walk()


if __name__ == '__main__':
    main(numbered=True)
