from asyncio.format_helpers import _format_args_and_kwargs
from turtle import delay, forward
import pygame
from pygame import mixer
from random import randint
import sys
from PIL import Image, ImageFilter


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


    def remove(self):
        self.monster.all_laser.remove(self)
    #classe mouvement du laser #
    def move(self, time):
        self.rect.y += self.velocity * time
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
        self.velocity = 1
        self.all_laser = pygame.sprite.Group()
        self.image = pygame.image.load("assets/vaisseaux/ennemies/enemy-01/nomove_1.png")
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect()
        self.rect.x = randint(-15,360)
        self.rect.y = -10
        self.delay = 90
        self.delay_spawn = 1000
 
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


    def velocityUp(self, x) :
        self.velocity += x

    def freeze(self):
        self.rect.y += 0
        if self.game.check_collision(self,self.game.all_players) :
            self.game.player.damage(self.attack)
            self.game.all_monsters.remove(self)
        if self.rect.y > 590 :
            self.game.all_monsters.remove(self)
            self.game.player.damage(self.attack)

    def HealthUp(self, x) :
        self.health += x
        self.max_health += x
        

#classe projectile de notre vaisseau #
class Projectile(pygame.sprite.Sprite) :
    # Définir le constructeur de cette classe #
    def __init__(self, player):
        super().__init__()
        soundObj = pygame.mixer.Sound('sounds/player_shoot.wav')
        soundObj.set_volume(float(saveread("volume2")))
        soundObj.play()
        self.velocity = 450
        self.player = player
        self.image = pygame.image.load('assets/missiles/PlayProjectile.png')
        self.image = pygame.transform.scale(self.image, (20,20))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + (player.rect.width)/2 - self.image.get_width()/2
        self.rect.y = player.rect.y

    def remove(self):
        self.player.all_projectiles.remove(self)

    def move(self,time):
        for monster in self.player.game.check_collision(self, self.player.game.all_monsters) :
            self.remove()
            monster.damage(self.player.attack)
        if self.rect.y < -10 :
            self.remove()
        self.rect.y -= self.velocity * time

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 15
        self.velocity = 440
        self.score = 0
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))
        self.rect = self.image.get_rect()
        self.rect.x = 160
        self.rect.y = 500
        self.shoot_delay = 250
        self.last_shoot =  pygame.time.get_ticks()
        self.clock = pygame.time.get_ticks()

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

    def HealthUp(self, x) :
        self.health += x
        self.max_health += x

    def ShootUp(self, x) :
        self.shoot_delay -= x

    def move_right(self, time):
        self.rect.x += self.velocity * time
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/right.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
    def move_left(self, time):
        self.rect.x -= self.velocity * time
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/left.png')
        self.image = pygame.transform.scale(self.image, (80,80))
    def move_up(self, time):
        self.rect.y -= self.velocity * time
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))
    def move_down(self, time):
        self.rect.y += self.velocity * time
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
        self.delay_spawn = 1000
        self.last_monster = pygame.time.get_ticks()

    def check_collision(self, sprite, group) :
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def SpawnUp(self, x):
        self.delay_spawn -= x

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
flake = pygame.image.load("assets/icon/flake.png")
flake = pygame.transform.scale(flake,(50,50))
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
        OPTIONS_POURCENTAGE_FOND_RECT2 = POURCENTAGE_FOND2.get_rect(center=(40, 355))
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
            if event.type == pygame.KEYDOWN :
                if event.key==pygame.K_ESCAPE:
                    if menu == "menu":
                        return 0
                    else :
                        BG2 = pygame.image.load("assets/menu/blurrybg.jpg")
                        screen.blit(BG2, (0, 0))
                        return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    if menu == "menu":
                        return 0
                    else:
                        BG2 = pygame.image.load("assets/menu/blurrybg.jpg")
                        screen.blit(BG2, (0, 0))
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
                    if warning()==1:
                        volume = 0.5
                        volume2 = 0.5
                        position = 250
                        position2 = 250
                        save(-1,volume,position,volume2,position2)
                        mixer.music.set_volume(float(saveread("volume")))
    
        pygame.display.update()


def warning() :
    screen.fill("black")
    buttonimg1 = pygame.image.load("assets/menu/button.png")
    buttonimg1 = pygame.transform.scale(buttonimg1,(100,30))  
    while True:
        color = (131, 136, 143)

        pygame.draw.rect(screen, color, pygame.Rect(10, 175, 380, 130))

        warning_TEXT = get_font(9).render("Etes-vous sûr de vouloir réinitialiser ?", True, "white")
        warning_RECT = warning_TEXT.get_rect(topleft=(20, 200))
        warning_TEXT2 =  get_font(9).render("(cela inclut le score)", True, "white")
        warning_RECT2 = warning_TEXT.get_rect(topleft=(100, 220))
        screen.blit(warning_TEXT, warning_RECT)
        screen.blit(warning_TEXT2, warning_RECT2)

        YES_BUTTON = Button(image=buttonimg1, pos=(130, 270), text_input="Oui", font=get_font(8), base_color="White", hovering_color="Green")
        QUIT_BUTTON = Button(image=buttonimg1, pos=(260, 270), text_input="Quitter", font=get_font(8), base_color="White", hovering_color="Green")   
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        for button in [YES_BUTTON,QUIT_BUTTON]:
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
                if QUIT_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    return 0
                if YES_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    return 1



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
                    color="White"
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
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    jeu()
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
    global color
    global score
    color="White"
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

    #Chargement image pour score et bestscore#
    prec_score = pygame.image.load('assets/icon/prec_score.png')
    
    # Boucle jeu #
    running = True

    #Vague d'ennemis#
    vague = 1

    last_seconde = pygame.time.get_ticks()
    delai = 1000
    count = 0
    freeze = 0
    last_seconde2 = pygame.time.get_ticks()


    freeze_BUTTON = Button(image=flake, pos=(50, 560), text_input="      ", font=get_font(12), base_color="White", hovering_color="Green")

    while running :
        #appliquer arrière plan et défilement#

        dt = clock.tick(120)
        time = dt/1000
        print(clock.get_fps())
        if freeze != 1:
            y_background += 0.25
        if y_background < 600 :
            screen.blit(background,(0,y_background))
            screen.blit(background, (0, y_background-600))
        else :
            y_background = 0
            screen.blit(background, (0, y_background))

        #Appliquer image de notre joueur#
        screen.blit(game.player.image, game.player.rect)

        MOUSE_POS = pygame.mouse.get_pos()

        for button in [freeze_BUTTON]:
            button.changeColor(MOUSE_POS)
            button.update(screen)

        #Appliquer l'ensemble de mon grp de projectiles en les dessinant#
        game.explosion_group.update()
        game.player.all_projectiles.draw(screen)
        game.all_monsters.draw(screen)
        game.explosion_group.draw(screen)

        if game.player.health <= 0:
            soundObj = pygame.mixer.Sound('sounds/game_over.wav')
            soundObj.set_volume(volume)
            soundObj.play()
            pygame.mixer.music.stop()
            over_menu()

        #Affichage du score #
        prec_score = pygame.transform.scale(prec_score,(20,20))
        Score_TEXT = get_font(13).render((str(game.player.score)), True, color )
        Score_RECT = Score_TEXT.get_rect(topleft=(60, 18))

        #Affichage du score #
        Vague_TEXT = get_font(13).render(("Vague "+str(vague)), True, color )
        Vague_RECT = Vague_TEXT.get_rect(bottomright=(380, 590))

        
        if game.player.score > int(saveread("bestscore")):
            color="Red"
            Record_TEXT = get_font(8).render("Nouveau record !",True,"Red")
            Record_RECT = Record_TEXT.get_rect(topleft=(20, 45))
            screen.blit(Record_TEXT,Record_RECT)

        screen.blit(prec_score,(20,15))
        screen.blit(Score_TEXT, Score_RECT)
        screen.blit(Vague_TEXT, Vague_RECT)
        

        #récupérer tout les projectiles du joueur #
        for projectile in game.player.all_projectiles :
            projectile.move(time)

        game.player.update_health_bar(screen)

        #################################################################################
        ################################# VAGUE ENNEMIS #################################
        #################################################################################
        now = pygame.time.get_ticks()

        if (now - last_seconde > delai) and count<15 :
            count +=1 
            last_seconde = now
        if count<15 :
            game.spawn_monster()
        if count==15 and len(game.all_monsters)==0:
            VagueFinish_TEXT = get_font(20).render(("Vague "+str(vague)+" Terminée"), True, color )
            VagueFinish_RECT = VagueFinish_TEXT.get_rect(center=(200,300 ))
            screen.blit(VagueFinish_TEXT, VagueFinish_RECT)
            if now - last_seconde > 15000:
                count = 0
                last_seconde = now
                vague +=1
                game.SpawnUp(300)

        #################################################################################


        # vérifier si le joueur souhaite bouger ou tirer#
        if game.pressed.get(pygame.K_SPACE):
            game.player.launch_projectile()
        if (game.pressed.get(pygame.K_DOWN) or game.pressed.get(pygame.K_s)) and game.player.rect.y + (game.player.rect.height) < screen.get_height():
            game.player.move_down(time)
        if (game.pressed.get(pygame.K_UP) or game.pressed.get(pygame.K_z)) and game.player.rect.y > 0:
            game.player.move_up(time)
        if (game.pressed.get(pygame.K_RIGHT) or game.pressed.get(pygame.K_d)):
            game.player.move_right(time)
        if (game.pressed.get(pygame.K_LEFT) or game.pressed.get(pygame.K_q)):
            game.player.move_left(time)
        if not((game.pressed.get(pygame.K_DOWN) or game.pressed.get(pygame.K_s)) or  
            (game.pressed.get(pygame.K_UP) or game.pressed.get(pygame.K_z)) or 
            (game.pressed.get(pygame.K_RIGHT) or game.pressed.get(pygame.K_d)) or  
            (game.pressed.get(pygame.K_LEFT) or game.pressed.get(pygame.K_q)) ):
            game.player.no_move()
        if (game.player.rect.x) > screen.get_width():
            game.player.rect.x = 0 - game.player.rect.width 
        if (game.player.rect.x) < -(game.player.rect.width) :
            game.player.rect.x = screen.get_width()


        for monster in game.all_monsters :
            if freeze == 0:
                monster.forward()
            else:
                monster.freeze()


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
                    pygame.image.save(screen,"assets/menu/currentbg.jpg")
                    OriImage = Image.open('assets/menu/currentbg.jpg')
                    blurImage = OriImage.filter(ImageFilter.BLUR)
                    blurImage.save('assets/menu/blurrybg.jpg')
                    BG2 = pygame.image.load('assets/menu/blurrybg.jpg')
                    screen.blit(BG2, (0, 0))

                    listkeys = [pygame.K_DOWN,pygame.K_UP,pygame.K_RIGHT,pygame.K_SPACE,pygame.K_LEFT,pygame.K_s,pygame.K_z,pygame.K_q,pygame.K_d]

                    for key in listkeys:
                        game.pressed[key] = False
                    paused()
            if event.type == pygame.KEYUP :
                game.pressed[event.key] = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if freeze_BUTTON.checkForInput(MOUSE_POS):
                    freeze = 1
                    last_seconde2 = pygame.time.get_ticks()

            now2 = pygame.time.get_ticks()
            if now2 - last_seconde2 >= 5000:
                freeze = 0
            
            



main_menu()