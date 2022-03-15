import pygame
from player import Player
from monster import Monster
import time
#Classe jeu #
class Game:
    def __init__(self):
        #Génère notre joueur#
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        self.explosion_group = pygame.sprite.Group()
        self.all_monsters = pygame.sprite.Group()
        self.monster  = Monster(self)
        self.pressed = {}
        self.delay_spawn = 900
        self.last_monster = pygame.time.get_ticks()

    def check_collision(self, sprite, group) :
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_monster(self):
        now = pygame.time.get_ticks()
        monster = Monster(self)
        if now - self.last_monster > self.delay_spawn :
            self.all_monsters.add(monster)
            self.last_monster = now

    