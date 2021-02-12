import sys
import time
sys.path.append("../core/")
from board_patterns import *
from board import *
from chess import *
from piece_data import *
import pygame
import math

pygame.init()

font = pygame.font.Font('freesansbold.ttf', 32)
screen = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)

running = True

class TilePy(Tile):
    def __init__(self, color, pos):
        Tile.__init__(self, color, pos)

class BoardPy(Board):
    def get_board_dimensions(self):
        return screen.get_height()

    def set_sprite_size(self, size):
        size *= 1.171875
        self.sprite_size = math.floor(64 * size)
        self.light_sprite = pygame.transform.scale(self.light_sprite_og, (self.sprite_size, self.sprite_size))
        self.dark_sprite = pygame.transform.scale(self.dark_sprite_og, (self.sprite_size, self.sprite_size))

        for sprite in self.white_sprites:
            self.white_sprites[sprite] = pygame.transform.scale(self.white_sprites_og[sprite], (self.sprite_size, self.sprite_size))
        for sprite in self.black_sprites:
            self.black_sprites[sprite] = pygame.transform.scale(self.black_sprites_og[sprite], (self.sprite_size, self.sprite_size))

    def __init__(self, pattern):
        Board.__init__(self, pattern, TilePy)
        self.light_sprite = pygame.image.load("sprites/board/light.png")
        self.dark_sprite = pygame.image.load("sprites/board/dark.png")
        self.light_sprite_og = pygame.image.load("sprites/board/light.png")
        self.dark_sprite_og = pygame.image.load("sprites/board/dark.png")
        
        self.white_sprites = {}
        self.black_sprites = {}
        self.white_sprites_og = {}
        self.black_sprites_og = {}
        #piece sprites
        for piece in piece_dictionaries:
            self.white_sprites[piece] = pygame.image.load("sprites/white/"+str(piece)+".png")
            self.black_sprites[piece] = pygame.image.load("sprites/black/"+str(piece)+".png")
            self.white_sprites_og[piece] = pygame.image.load("sprites/white/"+str(piece)+".png")
            self.black_sprites_og[piece] = pygame.image.load("sprites/black/"+str(piece)+".png")

        self.sprite_size = 64
        self.set_sprite_size(1)

    def render_piece(self, piece, pos):
        location = (pos[0] * self.sprite_size, pos[1] * self.sprite_size)
        if piece.owner == "white":
            screen.blit(self.white_sprites[piece.piece_name], location)
        else:
            screen.blit(self.black_sprites[piece.piece_name], location)

    def render_tile(self, tile):
        location = (tile.pos[0] * self.sprite_size, tile.pos[1] * self.sprite_size)
        if tile.color == -1:
            screen.blit(self.light_sprite, location)
        else:
            screen.blit(self.dark_sprite, location)
        
        if tile.piece_slot != None:
            self.render_piece(tile.piece_slot, tile.pos)

    def draw_board(self):
        for row in self.tiles:
            for tile in row:
                self.render_tile(tile)

class BoardEditor:
    def __init__(self, board):
        self.board = board
        self.pieces = []
        for piece in piece_dictionaries:
            self.pieces.append(Piece(piece, "white"))
            self.pieces.append(Piece(piece, "black"))

    def handle_click(self, pos):
        pass

    def render_piece_selector(self):
        x = self.board.get_board_dimensions()
        y = 10
        for piece_index in range(len(self.pieces)//2 - 1):
            piece_index *= 2
            piece1 = self.pieces[piece_index]
            piece2 = self.pieces[piece_index+1]

            screen.blit(board.white_sprites[piece1.piece_name], (x, y))
            screen.blit(board.black_sprites[piece1.piece_name], (x + 256, y))

            text1 = font.render(piece1.piece_name, True, (255, 255, 255), (60, 60, 60))
            textRect1 = text1.get_rect()
            textRect1.center = (x + self.board.sprite_size + 32, y + 32)
            screen.blit(text1, textRect1)

            text2 = font.render(piece2.piece_name, True, (255, 255, 255), (60, 60, 60))
            textRect2 = text2.get_rect()
            textRect2.center = (x + self.board.sprite_size + 256 + 32, y + 32)
            screen.blit(text2, textRect2)

            y += 128


board = BoardPy("default")
editor = BoardEditor(board)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            board.set_sprite_size(screen.get_height()/600)
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if event.button == pygame.BUTTON_RIGHT:
                pos_in_board = (pos[0]//(screen.get_height()//8), pos[1]//(screen.get_height()//8))
                if pos[0] > 7 or pos[1] > 7 or pos[0] < 0 or pos[1] < 0:
                    editor.handle_click(pos)
                else:
                    board.kill(pos_in_board)

    screen.fill((60, 60, 60))
    board.draw_board()
    editor.render_piece_selector()
    pygame.display.update()