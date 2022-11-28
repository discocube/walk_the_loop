"""
Platonian Game.
"""
import random
from itertools import cycle
import pygame.transform
from pygame.locals import MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE, QUIT, K_r, K_RIGHT, K_SPACE

from src.game.pieces.edge import Edge
from src.game.pieces.icons import ActionIcon, DrawnIcon, ToggleIcon
from src.game.pieces.node import Node
from src.game.pieces.players import Players
from src.game.settings import COLORS, G_TYPES, G_POLYHEDRA
from src.game.utils import time, walk, walker


class WalkTheLoop:
    """
    Icosian Game
    """
    screen, buttons = None, {}
    edges, nodes, players, clock = [None] * 4
    update, running = [None] * 2
    G, V, E, A, ORD = [None] * 5
    walker = None

    def __init__(self, screen_size=(800, 800), numbered=True, graph_type=None, animate=False):
        self.new = False
        self.winning, self.losing = False, False
        self.animate = animate
        self.screen_rect = screen_size
        self.screen_scale = self.screen_rect[0] / 1000
        self.numbered = numbered
        self.graph_type = graph_type

        self.all_sprites_grp, self.edges_grp, self.nodes_grp, self.buttons_grp = (pygame.sprite.Group() for _ in range(4))
        self.graph_iter = cycle(G_TYPES)

        self.init_screen_clock()
        self.reset_game(graph_type=self.graph_type)

    @property
    def player(self):
        """
        Player object.
        """
        return self.players.current

    @property
    def path(self):
        """
        Path of player.
        """
        return self.player.path

    def init_screen_clock(self):
        """
        Init game at the beginning.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_rect)
        self.clock = pygame.time.Clock()
        self.clock.tick(30)

    def reset_game(self, graph_type=None):
        """
        Create new containers.
        """
        self.set_graph(graph_type=graph_type)
        self.walker = walker(self.A)
        self.edges = {frozenset(edge): None for edge in self.E}
        self.nodes = {node: None for node in self.A.keys()}
        self.players = Players(self.G, nodes=self.nodes)
        self.make_sprite_grps()
        self.reset_board()
        self.reset_flags()

    def set_graph(self, graph_type=None):
        """
        Initialize game with new graph.
        """
        if graph_type:
            while next(self.graph_iter) != graph_type:
                pass
            self.graph_type = graph_type
        else:
            self.graph_type = next(self.graph_iter)
        self.G = G_POLYHEDRA[self.graph_type]
        self.V, self.E, self.A = self.G['V'], self.G['E'], self.G['A']
        self.ORD = len(self.V)

    def make_sprite_grps(self):
        """
        Make groups for sprites.
        """
        self.all_sprites_grp, self.edges_grp, self.nodes_grp, self.buttons_grp = (pygame.sprite.Group() for _ in range(4))

    def reset_board(self):
        """
        Initialize pygame, draw board.
        """
        self.players.add_player()
        self.add_nodes_edges()
        self.add_buttons()
        self.draw_sprites()
        self.renew_sprites()

    def add_nodes_edges(self):
        """
        Add edges & nodes.
        """
        for e in self.E:
            self.add_sprite_to_grps(
                Edge(
                    scale=self.screen_scale,
                    group=self.edges_grp,
                    data=e,
                    pm=self.V[e[0]],
                    pn=self.V[e[1]],
                    screen_rect=self.screen_rect
                ),
                edge=e
            )
        for idx, vert in enumerate(self.V):
            self.add_sprite_to_grps(
                Node(
                    A=self.A,
                    scale=self.screen_scale,
                    center=vert,
                    group=self.nodes_grp,
                    data=idx,
                    numbered=self.numbered,
                    screen=self.screen,
                    players=self.players,
                    paths=self,
                    screen_rect=self.screen_rect
                ), node=idx
            )

    def add_buttons(self):
        """
        Add/Set buttons.
        """
        self.buttons = {
            G_TYPES[i]:
                self.add_sprite_to_grps(
                    sprite=ActionIcon(
                        scale=self.screen_scale,
                        center=(250 + i * 100, 900),
                        name=G_TYPES[i],
                        current_graph_type=self.graph_type,
                        group=self.buttons_grp
                    ),
                    button_name=G_TYPES[i])
            for i in range(6)
        }
        self.buttons['drawn_icon'] = self.add_sprite_to_grps(
            DrawnIcon(
                name=self.graph_type,
                group=self.buttons_grp,
                center=[point * self.screen_scale for point in (900, 100)],
                path_obj=self.path
            )
        )
        self.buttons['play&pause'] = self.add_sprite_to_grps(
            ToggleIcon(
                center=(500, 750),
                scale=self.screen_scale,
                name='play&pause',
                group=self.buttons_grp,
                animate_state=self.animate
            )
        )
        self.buttons['reset'] = self.add_sprite_to_grps(
            ActionIcon(
                screen_rect=(50, 50),
                scale=self.screen_scale,
                center=(400, 750),
                name='reset',
                group=self.buttons_grp
            )
        )
        self.buttons['next'] = self.add_sprite_to_grps(
            ActionIcon(
                screen_rect=(50, 50),
                scale=self.screen_scale,
                center=(600, 750),
                name='next',
                group=self.buttons_grp
            )
        )

    def draw_sprites(self):
        """
        Draw sprites in all sprites.
        """
        self.screen.fill(COLORS['BLACK'])
        for entity in self.all_sprites_grp:
            self.screen.blit(entity.surface, entity.rect)
        pygame.display.flip()

    def reset_flags(self):
        """
        Reset flags to default values.
        """
        self.update, self.running, self.animate, self.winning = False, True, False, False

    def add_sprite_to_grps(self, sprite, node=None, edge=None, button_name=None):
        """
        Add given sprite, node or edge to all sprites and respective group.
        """
        if node is not None:
            self.nodes[node] = sprite
            self.nodes_grp.add(sprite)
        elif edge:
            self.edges[frozenset(edge)] = sprite
            self.edges_grp.add(sprite)
        elif button_name:
            self.buttons['button_name'] = sprite
            self.buttons_grp.add(sprite)
        self.all_sprites_grp.add(sprite)
        return sprite

    def play(self):
        """
        Player play.
        """
        self.update = True
        self.animate, self.new = [False] * 2
        while self.running:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    self.parse_click()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    elif event.key == K_RIGHT:
                        self.animate = not self.animate
                    elif event.key == K_r:
                        self.reset_game(graph_type=self.graph_type)
                    elif event.key == K_SPACE:
                        self.animate = not self.animate
                        self.buttons['play&pause'].switch()
                elif event.type == QUIT:
                    self.running = False

            self.animate_path()
            self.check_status()
            self.renew_sprites()
            self.draw_sprites()
            self.check_reset()

        pygame.quit()

    def animate_path(self):
        """
        Animate path
        """
        if self.animate:
            try:
                self.path.data[:] = next(self.walker)
            except StopIteration:
                self.animate = False
                self.start_walker()
            self.running = True
        else:
            self.start_walker()

    def start_walker(self):
        """
        Start walker iterator according to current path.
        """
        data = self.path.data[:-1] if len(self.path.data) > 1 else [random.randint(0, self.ORD + 1)] if not self.path.data else self.path.data
        self.walker = walker(self.A, s=data)

    def check_status(self):
        """
        Check if a loop has been found.
        """
        if self.player.found_solution:
            self.show_status('winning')
            self.new = not self.animate
        else:
            self.update = True

    def check_reset(self):
        """
        Check if game needs resetting.
        """
        if self.winning:
            self.reset_game(self.graph_type)
        if self.new:
            time.sleep(.5)
            self.reset_game()
            return self.play()

    def parse_click(self):
        """
        Process mouse click.
        """
        self.update = True
        for button in self.buttons_grp:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                if isinstance(button, ToggleIcon):
                    self.animate = not self.animate
                    return button.switch()
                elif button.name == 'reset':
                    self.screen.fill(COLORS['BLACK'])
                    self.animate = False
                    return self.reset_game(self.graph_type)
                elif button.name == 'next':
                    self.screen.fill(COLORS['BLACK'])
                    return self.reset_game(next(self.graph_iter))
                elif button.name in G_TYPES:
                    self.screen.fill(COLORS['BLACK'])
                    self.animate = False
                    return self.reset_game(button.name)
        for n, node in self.nodes.items():
            if node.rect.collidepoint(pygame.mouse.get_pos()):
                self.animate = False
                if self.player.is_new:
                    return self.player.step(n)
                elif n == self.player.butt and len(self.path) > 2:
                    return self.player.switch_head()
                elif n in self.player.path:
                    return self.path.rewind(n)
                elif n not in self.player.path:
                    if node.is_adjacent(self.player.head):
                        return self.player.step(n)
                    return self.run(n)

    def set_node_edge(self, node=None, edge=None, style='active'):
        """
        Set edge style.
        """
        if node is not None:
            (node_obj := self.nodes[node]).set_color(style=style)
            if style == 'active':
                node_obj.player_id = self.player.id
        if edge:
            (edge_obj := self.edges[frozenset(edge)]).set_color(style=style)
            if style == 'active':
                edge_obj.player_id = self.player.id

    def show_status(self, status='winning'):
        """
        Set flags for winning, resulting in winning COLORS (GREEN).
        """
        self.screen.fill(COLORS['GREEN'])
        self.update = False
        frozen_edges = {frozenset(edge) for edge in self.path.edges}
        for n in range(self.ORD):
            if n in self.path:
                self.set_node_edge(node=n, style=status)
            else:
                self.set_node_edge(node=n, style='inactive')
        for edge in self.edges.keys():
            if edge in frozen_edges:
                self.set_node_edge(edge=edge, style=status)
            else:
                self.set_node_edge(edge=edge, style='inactive')

    def run(self, n):
        """
        Random run to goal n.
        """
        if solution := walk(self.A, start=self.path[-1], goal=n, walked=self.players.stepped.difference(self.path[-1:]), prune=len(self.path) > 1):
            self.path.data.extend(solution[1:])
        else:
            print('no solution')

    def renew_sprites(self):
        """
        Renew (deactivate and color) edges and nodes.
        """
        if self.update:
            if self.players.stepped:
                self.renew_nodes()
                self.renew_edges()

    def renew_nodes(self):
        """
        Gray out nodes then recolor.
        """
        for node in self.nodes.values():
            node.set_color('inactive')
        for player in self.players.data.values():
            for n in player.path:
                self.set_node_edge(node=n, style='active')
            if player.path:
                self.renew_ends(player)

    def renew_edges(self):
        """
        Gray out nodes then recolor.
        Assign player_id to each node.
        """
        for edge in self.E:
            self.set_node_edge(edge=edge, style='inactive')
        for player in self.players.data.values():
            path = player.path
            if path.has_edge:
                for e in path.edges:
                    self.set_node_edge(edge=e, style='active')

    def renew_ends(self, player):
        """
        Refresh head or origin.
        """
        for idx, style in enumerate(('head', 'origin')):
            self.set_node_edge(node=player.ends[idx], style=style)
