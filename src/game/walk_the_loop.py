"""
Platonian Game.
"""
from itertools import cycle
import pygame.transform
from pygame.locals import MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE, QUIT, K_r

from src.game.pieces.edge import Edge
from src.game.pieces.icons import GraphIcon, Icon
from src.game.pieces.node import Node
from src.game.pieces.players import Players
from src.game.settings import colors, G_TYPES, G_POLYHEDRA
from src.game.utils import time, walk


class WalkTheLoop:
    """
    Icosian Game
    """
    screen, buttons = None, {}
    edges, nodes, players, clock = [None] * 4
    update, running = [None] * 2
    G, V, E, A, ORD = [None] * 5

    def __init__(self, screen_rect=(1000, 1000), numbered=True, graph_type=None):
        self.screen_rect = screen_rect
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

    def reset_game(self, graph_type=None):
        """
        Create new containers.
        """
        self.set_graph(graph_type=graph_type)
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
        self.graph_type = graph_type or next(self.graph_iter)
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
        self.place_nodes_edges()
        self.place_buttons()
        self.draw_sprites()
        self.players.add_player()

    def place_nodes_edges(self):
        """
        Add edges & nodes.
        """
        for e in self.E:
            self.add_sprite_to_grps(Edge(group=self.edges_grp, data=e, pm=self.V[e[0]], pn=self.V[e[1]], screen_rect=self.screen_rect), edge=e)
        for idx, vert in enumerate(self.V):
            self.add_sprite_to_grps(
                Node(
                    A=self.A,
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

    def place_buttons(self):
        """
        Set buttons for other graph problems.
        """
        self.buttons = {G_TYPES[i]: self.add_sprite_to_grps(GraphIcon(center=(250 + i * 100, 900), name=G_TYPES[i], group=self.buttons_grp), button_name=G_TYPES[i]) for i in range(6)}
        self.buttons['s_icon'] = self.add_sprite_to_grps(Icon(name=self.graph_type, group=self.buttons_grp))

    def draw_sprites(self):
        """
        Draw sprites in all sprites.
        """
        self.screen.fill(colors['BLACK'])
        for entity in self.all_sprites_grp:
            self.screen.blit(entity.surface, entity.rect)
        pygame.display.flip()

    def reset_flags(self):
        """
        Reset flags to default values.
        """
        self.update, self.running = False, True

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
        new = False
        while self.running:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    self.parse_click()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    elif event.key == K_r:
                        self.reset_game(graph_type=self.graph_type)
                elif event.type == QUIT:
                    self.running = False
            if self.player.max_stepped:
                if self.path.is_loop:
                    self.running = False
                    self.show_winning()
                    new = True
                else:
                    self.show_losing()
            if self.update:
                if self.players.stepped:
                    self.renew_sprites()
            self.draw_sprites()
        if new:
            time.sleep(.5)
            self.reset_game()
            return self.play()
        pygame.quit()

    def parse_click(self):
        """
        Process mouse click.
        """
        self.update = True
        for g_type in self.buttons_grp:
            if g_type.rect.collidepoint(pygame.mouse.get_pos()):
                self.screen.fill(colors['BLACK'])
                return self.reset_game(g_type.name)
        for n, node in self.nodes.items():
            if node.rect.collidepoint(pygame.mouse.get_pos()):
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
            (node_obj := self.nodes[node]).set_color(style)
            if style == 'active':
                node_obj.player_id = self.player.id
        if edge:
            (edge_obj := self.edges[frozenset(edge)]).set_color(style)
            if style == 'active':
                edge_obj.player_id = self.player.id

    def show_winning(self):
        """
        Set flags for winning, resulting in winning colors (GREEN).
        """
        self.update = False
        for n in self.path:
            self.set_node_edge(node=n, style='winning')
        for e in self.path.edges:
            self.set_node_edge(edge=e, style='winning')

    def show_losing(self):
        """
        Set flags for winning, resulting in losing colors (RED)
        """
        self.update = False
        for n in self.path:
            self.set_node_edge(node=n, style='losing')
        for e in self.path.edges:
            self.set_node_edge(edge=e, style='losing')

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
            self.set_node_edge(node=player.ends[0], style=style)
