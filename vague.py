
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)



class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"assets/explosion/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (40, 40))
            if size == 2:
                img = pygame.transform.scale(img, (60, 60))
            if size == 3:
                img = pygame.transform.scale(img, (180, 180))
            #add the image to the list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0


    def update(self):
        explosion_speed = 3
        #update explosion animation
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        #if the animation is complete, delete explosion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


class Laser_ennemie(pygame.sprite.Sprite) :
    # Définir le constructeur de cette classe #
    def __init__(self, monster):
        super().__init__()
        self.velocity = 3.5
        self.monster = monster
        self.image = pygame.image.load('assets/missiles/ennemie.png')
        self.image = pygame.transform.scale(self.image, (80,80))
        self.rect = self.image.get_rect()
        self.rect.x = monster.rect.x + (monster.rect.width)/2 - self.image.get_width()/2
        self.rect.y = monster.rect.y
    def remove(self):
        self.monster.all_laser.remove(self)
    #classe mouvement du laser #
    def move(self):
        self.rect.y += self.velocity
        from main import screen
        if self.rect.y >  screen.get_height():
            self.remove()



#Classe du monstre#s
class Monster(pygame.sprite.Sprite):
    def __init__(self, game):
        global soundObj 
        super().__init__()
        self.game = game
        soundObj = pygame.mixer.Sound('sounds/ennemy_explosion.aiff')
        soundObj.set_volume(1)
        self.health = 30
        self.max_health = 30
        self.attack = 10
        self.velocity = 1.5
        self.all_laser = pygame.sprite.Group()
        self.image = pygame.image.load("assets/vaisseaux/ennemies/enemy-01/nomove_1.png")
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect()
        self.rect.x = randint(-15,360)
        self.rect.y = -10
        self.delay = 90
 
    def damage(self, amount) :
        self.health -= amount
        if self.health <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            soundObj.play()
            self.game.explosion_group.add(explosion)
            self.game.all_monsters.remove(self)
            self.game.player.score += 5

    def forward(self):
        self.rect.y += self.velocity
        if self.game.check_collision(self,self.game.all_players) :
            self.game.player.damage(self.attack)
            self.game.all_monsters.remove(self)
        if self.rect.y > 590 :
            self.game.all_monsters.remove(self)
            self.game.player.damage(self.attack)

            

    def launch_laser(self) :
        self.all_laser.add(Laser_ennemie(self))



#classe projectile de notre vaisseau #
class Projectile(pygame.sprite.Sprite) :
    # Définir le constructeur de cette classe #
    def __init__(self, player):
        super().__init__()
        soundObj = pygame.mixer.Sound('sounds/player_shoot.wav')
        soundObj.set_volume(1)
        soundObj.play()
        self.velocity = 9
        self.player = player
        self.image = pygame.image.load('assets/missiles/PlayProjectile.png')
        self.image = pygame.transform.scale(self.image, (20,20))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + (player.rect.width)/2 - self.image.get_width()/2
        self.rect.y = player.rect.y

    def remove(self):
        self.player.all_projectiles.remove(self)

    def move(self):
        for monster in self.player.game.check_collision(self, self.player.game.all_monsters) :
            self.remove()
            monster.damage(self.player.attack)
        if self.rect.y < -10 :
            self.remove()
        self.rect.y -= self.velocity
            




class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 15
        self.velocity = 7
        self.score = 0
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))
        self.rect = self.image.get_rect()
        self.rect.x = 160
        self.rect.y = 500
        self.shoot_delay = 250
        self.last_shoot =  pygame.time.get_ticks()

    def damage(self, amount) :
        if self.health < 0 :
            from main import main_menu
            main_menu()
        else :
            self.health -= amount

    def update_health_bar(self,surface):
        bar_color = (35, 188, 27)
        bar_position = [self.rect.x -10, self.rect.y + self.rect.height, self.health, 5]
        back_bar_color = (212, 63, 23)
        back_bar_position = [self.rect.x -10, self.rect.y + self.rect.height, self.max_health, 5]
        pygame.draw.rect(surface, back_bar_color, back_bar_position,0,3) #dessin barre de vie rouge #
        pygame.draw.rect(surface, bar_color, bar_position,0,3) #dessin barre de vie verte#

    def launch_projectile(self):
        #Création nouvelle instance du projectile et intervalle de temps#
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.all_projectiles.add(Projectile(self))
            self.last_shoot = now

    def move_right(self):
        self.rect.x += self.velocity
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/right.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
    def move_left(self):
        self.rect.x -= self.velocity
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/left.png')
        self.image = pygame.transform.scale(self.image, (80,80))
    def move_up(self):
        self.rect.y -= self.velocity
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))
    def move_down(self):
        self.rect.y += self.velocity
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))
    def no_move(self):
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))





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