import pygame
import random
import math
from pygame import mixer


pygame.init()
screen = pygame.display.set_mode((1330, 750))

background = pygame.image.load("pu.jpg")
# Title and logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("icon pic.png")
pygame.display.set_icon(icon)

# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

PlayerImg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 550
playerX_change = 0


enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num = 6

for i in range(num):
    enemyImg.append(pygame.image.load("alien (1).png"))
    enemyX.append(random.randint(0, 1266))
    enemyY.append(random.randint(50, 100))
    enemyX_change.append(10)
    enemyY_change.append(60)

bulletImg = pygame.image.load("bullet (2).png")
bulletX = 0
bulletY = 550
bulletX_change = 0
bulletY_change = 55
bullet_state = "ready"

score_value = 0
s_font = pygame.font.Font("Cabaret Display.ttf", 32)
textX = 10
textY = 10

over_font = pygame.font.Font("Cabaret Display.ttf", 80)




textX1 = 1170
textY2 = 0

near_font = pygame.font.Font("Cabaret Display.ttf", 32)
textx = 475
texty = 0

play_font = pygame.font.Font("Cabaret Display.ttf", 55)

start_background = pygame.image.load("start.jpg")



def show_play():
    play_text = play_font.render("PLAY", True, (255, 255, 0))
    screen.blit(play_text, (585, 460))


def show_near(x, y):
    near_text = near_font.render("COMING NEARER!!!", True, (255, 0, 0))
    screen.blit(near_text, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (420, 330))

def show_score(x, y):
    Score = s_font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(Score, (x, y))

def player(x, y):
    screen.blit(PlayerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(bulletX, bulletY):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (bulletX + 49, bulletY + 80))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + ((math.pow(enemyY - bulletY,2))))

    if distance < 60:
        return True

    else:
        return False


running = True
def starting_page():

    while True:
        screen.fill((0, 0, 0))
        screen.blit(start_background, (0, 0))

        mx, my = pygame.mouse.get_pos()
        button1 = pygame.Rect(470, 455, 400, 100)
        show_play()
        pygame.draw.rect(screen, (255, 255, 0), button1, 6)

        if button1.collidepoint(mx, my):
            if click:
                return running
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True


        pygame.display.update()

starting_page()

# Game loop

while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -18
            if event.key == pygame.K_RIGHT:
                playerX_change = 18

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1266:
        playerX = 1266

    for i in range(num):

        if enemyY[i] >= 375:
            show_near(textx, texty)
            show_near(textx, texty)

        # GAME OVER
        if enemyY[i] > 495:
            for j in range(num):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 7
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 1266:
            enemyX_change[i] = -7
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 550
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 1266)
            enemyY[i] = random.randint(50, 100)
        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= -20:
        bulletY = 550
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()


