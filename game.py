import pygame
from player import Player
from monster import Monster
#Classe jeu #
class Game:
    def __init__(self):
        #Génère notre joueur#
        self.player = Player()
        self.monster  = Monster()
        self.pressed = {}
        

#test
