# WALK THE LOOP

A simple 'learning by doing' game illustrating the concept of hamiltonian cycles by having the player find a hamiltonian cycle (a cycle that visits each node exactly once) in 6 graphs (gameboards), each consecutively more difficult than the last, with 5 derived from the skeleton of the 5 platonic solids and a sixth discocube graph derived from skeleton of a polycube of an octahedron (like using sugarcubes to form a diamond).

## Description

6 puzzles, each having more edges and nodes (game pieces) in its graph (gameboard) than the previous (from 4 nodes to 32 nodes) results in each proceeding graph being slightly more difficult than the last, demonstrating the idea of complexity, of the growth in complexity in solving a puzzle with let's say a thousand more nodes.
Once a puzzle is solved, the game will proceeds to the next puzzle. Clicking on one of the 6 icons below the gameboard will set that graph as the current game.
The gameboard consists of a visual representation of a graph, which is a collection of nodes and edges, where node represent objects and edges the connection / relationship between them. In this game the nodes are the steps and the edges are the lines connecting these steps.
The goal is to step (click) from node to node (if they are connected by an edge) until all nodes have been clicked and the last node is next to the start.

## GAMEPLAY
Starting:
Click on any node to begin. This is the origin. You will have to end up here to finish the game.

Stepping Forward:
Click on any node adjacent to the current step to take a step.
You can run by clicking on an unvisited node (grayed circle) not adjacent to the current step.

Stepping Backward:
Clicking on any visited node (colored node) will cause that to be the current step (purple circle with a ring), thereby erasing the previous moves.

Switching heads:
Clicking on the other end (the origin), will switch the origin to be the head (current step) and the head as the origin.

Choose another graph (non-sequential):
  The 6 puzzle icons below can be used to pick a particular graph.

Reset game: 
  The (r) key will reset the game

Quit:
  The (esc) key will quit the game.

## Getting Started

Just click. To pick a starting point. 

### Dependencies

* Hopefully none other than pygame.
* for mac and windows better is a web app.

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advice for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Rommelo Yu


## Version History


* 0.1
    * Initial Release

## License

This project is licensed under the [GNU AFFERO GENERAL PUBLIC LICENSE] License - see the LICENSE.md file for details

## Acknowledgments
