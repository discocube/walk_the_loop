"""
Main for playing platonic ham.
"""

from src.game.walk_the_loop import WalkTheLoop


def main(screen_size=(1000, 1000), numbered=True):
    """
    Run Icosian Game.
    """
    game = WalkTheLoop(screen_size=screen_size, numbered=numbered)
    game.play()


if __name__ == '__main__':
    main(screen_size=(1000, 1000), numbered=False)


"""
Implement a snake version and a loop version:

loop version starts from a starting point
snake version starts from a starting point with an end point.
-petersen graph has a ham path.

A graph that contains a Hamiltonian path is called a traceable graph. A graph is Hamiltonian-connected if for every pair of vertices there is a Hamiltonian path between the two vertices. A Hamiltonian cycle, Hamiltonian circuit, vertex tour or graph cycle is a cycle that visits each vertex exactly once.

drawing a star 

"""