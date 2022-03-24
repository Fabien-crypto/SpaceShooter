import pygame
from pygame import mixer
from random import randint
import sys


#Fonctions pour la sauvegarde#

def saveread(score):
    with open("scores.txt","r") as fichier:
        list = fichier.readlines()
        fichier.close()
    if score == "bestscore":
        return list[0].replace("\n","")
    elif score == "volume":
        return list[2].replace("\n","")
    elif score == "position":
        return list[3].replace("\n","")
    elif score == "volume2":
        return list[4].replace("\n","")
    elif score == "position2":
        return list[5]
    else:
        return list[1].replace("\n","")

def save(score,vol,pos,vol2,pos2):
    bestscore = saveread("bestscore")
    fichier = open("scores.txt","w+")
    if score > int(bestscore):
        fichier.write(str(score)+"\n"+str(score)+"\n"+str(vol)+"\n"+str(pos)+"\n"+str(vol2)+"\n"+str(pos2))
        fichier.close()
    elif score == -1:
        fichier.write(str(0)+"\n"+str(0)+"\n"+str(vol)+"\n"+str(pos)+"\n"+str(vol2)+"\n"+str(pos2))
        fichier.close()
    else:
        fichier.write(bestscore+"\n"+str(score)+"\n"+str(vol)+"\n"+str(pos)+"\n"+str(vol2)+"\n"+str(pos2))
        fichier.close()


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
        soundObj.set_volume(float(saveread("volume2")))
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
        soundObj.set_volume(float(saveread("volume2")))
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
        self.health = 50
        self.max_health = 50
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

#Initialisation du jeu#
pygame.init()
pygame.font.init()
pygame.init()

# Nom de la fenêtre #
pygame.display.set_caption("SpaceShoot")

#Définition de la police d'écriture #
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/menu/font.ttf", size)


#Icone jeu#
icon = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
pygame.display.set_icon(icon)

#Background des boutons#
buttonimg = pygame.image.load("assets/menu/button.png")
buttonimg = pygame.transform.scale(buttonimg,(150,50))
screen = pygame.display.set_mode((400, 600))

#Déclaration des variables de son#
volume = float(saveread("volume"))
position= int(saveread("position"))
position2= int(saveread("position2"))
volume2 = float(saveread("volume2"))

def options(menu):
    global volume,volume2
    global position,position2
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill("black")
        OPTIONS_TEXT = get_font(12).render("Choisir tes paramètres.", True, "white")
        OPTIONS_TEXT1 = get_font(12).render("Musique de fond", True, "white")
        OPTIONS_TEXT2 = get_font(12).render("Effets spéciaux ", True, "white")
        POURCENTAGE_FOND = get_font(12).render((str(int(200*(volume)))+"%"), True, "white")
        POURCENTAGE_FOND2 = get_font(12).render((str(int(200*(volume2)))+"%"), True, "white")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(200, 50))
        OPTIONS_RECT1 = OPTIONS_TEXT1.get_rect(center=(200, 150))
        OPTIONS_RECT2 = OPTIONS_TEXT1.get_rect(center=(200,300))
        OPTIONS_POURCENTAGE_FOND_RECT = POURCENTAGE_FOND.get_rect(center=(40, 205))
        OPTIONS_POURCENTAGE_FOND_RECT2 = POURCENTAGE_FOND.get_rect(center=(40, 355))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        screen.blit(OPTIONS_TEXT1, OPTIONS_RECT1)
        screen.blit(OPTIONS_TEXT2, OPTIONS_RECT2)
        screen.blit(POURCENTAGE_FOND,OPTIONS_POURCENTAGE_FOND_RECT)
        screen.blit(POURCENTAGE_FOND2,OPTIONS_POURCENTAGE_FOND_RECT2)

        RESET_BUTTON = Button(image=buttonimg, pos=(200, 460), text_input="Reset", font=get_font(12), base_color="White", hovering_color="Green")

        OPTIONS_BACK = Button(image=None, pos=(200, 550), 
                            text_input="BACK", font=get_font(12), base_color="white", hovering_color="Green")
        OPTIONS_MOINS = Button(image=None, pos=(350, 205),
                            text_input="-",font=get_font(12), base_color="white", hovering_color="Green")
        OPTIONS_PLUS = Button(image=None, pos=(380, 205),
                            text_input="+",font=get_font(12), base_color="white", hovering_color="Green")
        OPTIONS_MOINS2 = Button(image=None, pos=(350, 355),
                        text_input="-",font=get_font(12), base_color="white", hovering_color="Green")
        OPTIONS_PLUS2 = Button(image=None, pos=(380, 355),
                        text_input="+",font=get_font(12), base_color="white", hovering_color="Green")


        buttonlist = [OPTIONS_MOINS,OPTIONS_MOINS2,OPTIONS_PLUS,OPTIONS_PLUS2,OPTIONS_BACK,RESET_BUTTON]

        for button in buttonlist:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(screen)


        pygame.draw.rect(screen, (75,75,75), pygame.Rect(72, 197, 256, 16),3,5)
        pygame.draw.rect(screen, (140, 140, 140), pygame.Rect(75, 200, position, 10),0,2)
        pygame.draw.rect(screen, (75, 75, 75), pygame.Rect(72, 347, 256, 16),3,5)
        pygame.draw.rect(screen, (140, 140, 140), pygame.Rect(75, 350, position2, 10),0,2) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    if menu == "menu":
                        main_menu()
                    else:
                        screen.blit(background, (0, 0))
                        return 0

                if OPTIONS_PLUS.checkForInput(OPTIONS_MOUSE_POS):
                    if volume<0.5 and position <250: 
                        volume += 0.05
                        position += 25
                        volume = round(volume,2)
                        save(int(saveread("score")),volume,position,saveread("volume2"),saveread("position2"))

                    mixer.music.set_volume(float(saveread("volume")))

                if OPTIONS_MOINS.checkForInput(OPTIONS_MOUSE_POS):
                    if volume>0 and position >0: 
                        volume -= 0.05
                        position -= 25
                        volume = round(volume,2)
                        save(int(saveread("score")),volume,position,saveread("volume2"),saveread("position2"))

                    mixer.music.set_volume(float(saveread("volume")))

                if OPTIONS_PLUS2.checkForInput(OPTIONS_MOUSE_POS):
                    if volume2<0.5 and position2 <250: 
                        volume2 += 0.05
                        position2 += 25
                        volume2 = round(volume2,2)
                        save(int(saveread("score")),saveread("volume"),saveread("position"),volume2,position2)

                    mixer.music.set_volume(float(saveread("volume")))

                if OPTIONS_MOINS2.checkForInput(OPTIONS_MOUSE_POS):
                    if volume2>0 and position2 >0: 
                        volume2 -= 0.05
                        position2 -= 25
                        volume2 = round(volume2,2)
                        save(int(saveread("score")),saveread("volume"),saveread("position"),volume2,position2)

                    mixer.music.set_volume(float(saveread("volume")))
                
                if RESET_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    volume = 0.5
                    volume2 = 0.5
                    position = 250
                    position2 = 250
                    save(-1,volume,position,volume2,position2)


                mixer.music.set_volume(float(saveread("volume")))
                
        pygame.display.update()

def paused() :
    while True:
        PLAY_BUTTON = Button(image=buttonimg, pos=(200, 200), text_input="Reprendre", font=get_font(12), base_color="White", hovering_color="Green")
        OPTIONS_BUTTON = Button(image=buttonimg, pos=(200, 280), text_input="Options", font=get_font(12), base_color="White", hovering_color="Green")
        QUIT_BUTTON = Button(image=buttonimg, pos=(200, 360), text_input="Menu", font=get_font(12), base_color="White", hovering_color="Green")
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(screen)

        pygame.display.update() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN :
                if event.key==pygame.K_ESCAPE:
                    mixer.music.unpause()
                    return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    mixer.music.unpause()
                    return 0
                if OPTIONS_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    options("jeu")
                if QUIT_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    save(score,saveread("volume"),saveread("position"),saveread("volume2"),saveread("position2"))
                    mixer.music.unpause()
                    main_menu()
    


def over_menu():
    BG = pygame.image.load("assets/menu/Background.png")
    screen.blit(BG, (0, 0))
    MENU_TEXT = get_font(23).render("SpaceShooter", True, "#b68f40")
    MENU_RECT = MENU_TEXT.get_rect(center=(200, 80))
    OVER_TEXT = get_font(20).render("Game Over!", True, "white" )
    OVER_RECT = OVER_TEXT.get_rect(center=(200, 150))
    screen.blit(OVER_TEXT, OVER_RECT)
    best_score = pygame.image.load('assets/icon/best_score.png')
    best_score = pygame.transform.scale(best_score,(20,20))
    prec_score = pygame.image.load('assets/icon/prec_score.png')
    prec_score = pygame.transform.scale(prec_score,(20,20))
    Best_Score_TEXT = get_font(12).render("Meilleur Score: "+ saveread("bestscore"), True, "white")
    Best_Score_RECT = Best_Score_TEXT.get_rect(center=(215, 350))
    Prec_Score_TEXT = get_font(12).render(("Score Précédent: "+ saveread("prec")), True, "white")
    Prec_Score_RECT = Prec_Score_TEXT.get_rect(center=(215, 400))
    screen.blit(MENU_TEXT, MENU_RECT)
    screen.blit(Best_Score_TEXT, Best_Score_RECT)
    screen.blit(Prec_Score_TEXT, Prec_Score_RECT)
    screen.blit(best_score,(55,338))
    screen.blit(prec_score,(55,388))
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        BACK_MENU_BUTTON = Button(image=buttonimg, pos=(200, 250), text_input="Menu", font=get_font(12), base_color="White", hovering_color="Green")
        for button in [BACK_MENU_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
        pygame.display.update()

def main_menu(): 
    mixer.music.load('sounds/01_Title-Screen.wav')
    mixer.music.set_volume(volume)
    mixer.music.play()
    while True:
        BG = pygame.image.load("assets/menu/Background.png")
        best_score = pygame.image.load('assets/icon/best_score.png')
        best_score = pygame.transform.scale(best_score,(20,20))
        prec_score = pygame.image.load('assets/icon/prec_score.png')
        prec_score = pygame.transform.scale(prec_score,(20,20))
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(23).render("SpaceShooter", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(200, 80))
        PLAY_BUTTON = Button(image=buttonimg, pos=(200, 200), 
                            text_input="PLAY", font=get_font(12), base_color="White", hovering_color="Green")
        OPTIONS_BUTTON = Button(image=buttonimg, pos=(200, 280), 
                            text_input="OPTIONS", font=get_font(12), base_color="White", hovering_color="Green")
        QUIT_BUTTON = Button(image=buttonimg, pos=(200, 360), 
                            text_input="QUIT", font=get_font(12), base_color="White", hovering_color="Green")
        Best_Score_TEXT = get_font(12).render("Meilleur Score : "+ saveread("bestscore"), True, "white")
        Best_Score_RECT = Best_Score_TEXT.get_rect(topleft=(100, 442))
        Prec_Score_TEXT = get_font(12).render(("Score Précédent : "+ saveread("prec")), True, "white")
        Prec_Score_RECT = Prec_Score_TEXT.get_rect(topleft=(100, 493))
        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(Best_Score_TEXT, Best_Score_RECT)
        screen.blit(Prec_Score_TEXT, Prec_Score_RECT)
        screen.blit(best_score,(55,438))
        screen.blit(prec_score,(55,488))

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    jeu()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options("menu")
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
            
        pygame.display.update()


def jeu():
    global score
    #Musique de fond#    
    mixer.music.load('sounds/10 Drummed vaus.mp3')
    mixer.music.play()

    #Temps du jeu #
    clock = pygame.time.Clock()
    # Générer une fenêtre de jeu #
    pygame.display.set_caption("SpaceShoot")

    #background# 
    global background
    background = pygame.image.load('assets/fond/frameBackground.png')
    background = pygame.transform.scale(background,(400,600))
    y_background = 0
    #Chargement de notre jeu#
    game = Game()


    best_score = pygame.image.load('assets/icon/best_score.png')
    prec_score = pygame.image.load('assets/icon/prec_score.png')
    bestscore_TEXT = get_font(13).render(saveread("bestscore"), True, "white" )
    screen.blit(prec_score,(55,488))
    
    # Boucle jeu #
    running = True
    pygame.key.set_repeat()
    while running :
        #appliquer arrière plan et défilement#
        y_background += 1/2
        if y_background < 600 :
            screen.blit(background,(0,y_background))
            screen.blit(background, (0, y_background-600))
        else :
            y_background = 0
            screen.blit(background, (0, y_background))

        #Appliquer image de notre joueur#
        screen.blit(game.player.image, game.player.rect)
        clock.tick(60)
        
        #Appliquer l'ensemble de mon grp de projectiles en les dessinant#
        game.explosion_group.update()
        game.player.all_projectiles.draw(screen)
        game.all_monsters.draw(screen)
        game.explosion_group.draw(screen)

        if game.player.health <= 0:
            soundObj = pygame.mixer.Sound('sounds/game_over.wav')
            soundObj.set_volume(1)
            soundObj.play()
            pygame.mixer.music.stop()
            over_menu()

        #Affichage du score #
        best_score = pygame.transform.scale(best_score,(20,20))
        prec_score = pygame.transform.scale(prec_score,(20,20))
        Score_TEXT = get_font(13).render((str(game.player.score)), True, "white" )
        Score_RECT = Score_TEXT.get_rect(topleft=(60, 50))
        bestscore_RECT = best_score.get_rect(topleft=(60, 18))

        screen.blit(prec_score,(20,45))
        screen.blit(best_score,(20,15))
        screen.blit(Score_TEXT, Score_RECT)
        screen.blit(bestscore_TEXT, bestscore_RECT)

        #récupérer tout les projectiles du joueur #
        for projectile in game.player.all_projectiles :
            projectile.move()

        for monster in game.all_monsters :
            monster.forward()
        
        game.player.update_health_bar(screen)
        game.spawn_monster()

        # vérifier si le joueur souhaite bouger ou tirer#
        if game.pressed.get(pygame.K_SPACE):
            game.player.launch_projectile()
        if (game.pressed.get(pygame.K_DOWN) or game.pressed.get(pygame.K_s)) and game.player.rect.y + (game.player.rect.height) < screen.get_height():
            game.player.move_down()
        if (game.pressed.get(pygame.K_UP) or game.pressed.get(pygame.K_z)) and game.player.rect.y > 0:
            game.player.move_up()
        if (game.pressed.get(pygame.K_RIGHT) or game.pressed.get(pygame.K_d)):
            game.player.move_right()
        if (game.pressed.get(pygame.K_LEFT) or game.pressed.get(pygame.K_q)):
            game.player.move_left()
        if not((game.pressed.get(pygame.K_DOWN) or game.pressed.get(pygame.K_s)) or  
            (game.pressed.get(pygame.K_UP) or game.pressed.get(pygame.K_z)) or 
            (game.pressed.get(pygame.K_RIGHT) or game.pressed.get(pygame.K_d)) or  
            (game.pressed.get(pygame.K_LEFT) or game.pressed.get(pygame.K_q)) ):
            game.player.no_move()
        if (game.player.rect.x) > screen.get_width():
            game.player.rect.x = 0 - game.player.rect.width 
        if (game.player.rect.x) < -(game.player.rect.width) :
            game.player.rect.x = screen.get_width()

        #mettre à jour l'écran  #
        pygame.display.flip()
        #fermeture du jeu#
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                running = False
                score = game.player.score
                save(score,saveread("volume"),saveread("position"),saveread("volume2"),saveread("position2"))
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN :
                game.pressed[event.key]=True
                if event.key==pygame.K_ESCAPE:
                    mixer.music.pause()
                    score = game.player.score
                    paused()
            elif event.type == pygame.KEYUP :
                game.pressed[event.key] = False

main_menu()