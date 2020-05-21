import pygame
import random
import math
from pygame import mixer

#Initialize the game
pygame.init()

#Create the screen
screen = pygame.display.set_mode((800,600))

#Background
background = pygame.image.load('galaxy2.jpg')
mixer.music.load("background.wav")
mixer.music.play(-1)

# score
score = 0
font = pygame.font.Font('freesansbold.ttf',28)
textX = 10
textY = 10
def show_score(x,y):
    scor = font.render("Score :" + str(score),True,(255,255,255))
    screen.blit(scor,(x,y))
font2 = pygame.font.Font('freesansbold.ttf',50)
def game_over():
    scor = font2.render("GAME OVER",True,(255,255,255))
    screen.blit(scor,(280,250))

# Title and icon
pygame.display.set_caption('Space Invader')
icon = pygame.image.load('racket.png')
pygame.display.set_icon(icon)

#Player
playerimg = pygame.image.load('spaceship.png')
playerX = 370.0
playerY = 480.0
playerX_change = 0
#Bullet
bulletimg = pygame.image.load('bullet.png')
bulletX = 370
bulletY = 490
bulletY_change = 10
bullet_state ='ready'
#Enemy
enemyimg =[]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
s =[]
num_enemies = 6
for i in range(num_enemies):
    enemyimg.append(pygame.image.load('robot.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0)
    enemyY_change.append(0)
    s.append(1)

def player(x,y):
    screen.blit(playerimg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    screen.blit(bulletimg,(x+16,y+10))
    bullet_state = 'fire'

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False
#Gaming loop
running = True
while running:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if keystoke is pressed check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key ==pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
                    bulletsound = mixer.Sound('laser.wav')
                    bulletsound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0

    playerX = playerX + playerX_change
    if playerX < 0:
        playerX = 0
    if playerX > 800-64:
        playerX = 800-64

    if bullet_state == 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY = bulletY - bulletY_change
        if bulletY <= -32:
            bullet_state = 'ready'
            bulletY = playerY
    for i in range(num_enemies):
        if enemyY[i] > 440:
            for j in range(num_enemies):
                enemyY[j] = 2000
                game_over()
        enemyX_change[i] = 4 * s[i]
        enemyY_change[i] = 0
        if enemyX[i] > 800-64:
            s[i] = -1
            enemyY_change[i] = 20
        if enemyX[i] < 0:
            s[i] = 1
            enemyY_change[i] = 20
        enemyX[i] = enemyX[i] + enemyX_change[i]
        enemyY[i] = enemyY[i] + enemyY_change[i]
        if isCollision(enemyX[i],enemyY[i],bulletX,bulletY) is True:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bullet_state = 'ready'
            bulletY = playerY
            score = score + 1
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,150)
            print(score)
        enemy(enemyX[i],enemyY[i],i)
    show_score(textX,textY)
    player(playerX,playerY)
    pygame.display.update()
