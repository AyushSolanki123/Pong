import pygame
import random
pygame.init()
pygame.mixer.init()

#GAME VARIABLES
WIDTH = 800
HEIGHT = 600
FPS = 30

#COLORS    #R    #G    #B
RED     =  (255,   0,   0)
BLACK   =  (0  ,   0,   0)
WHITE   =  (255, 255, 255)
BLUE    =  (0  ,   0, 255)
ORANGE  =  (200, 128,   0)
RANDOM  =  (128, 128, 255)

#FONTS
GFONT = pygame.font.SysFont('Algerian', 30, True, True)
SFONT = pygame.font.SysFont('Cambria', 20, True)

#SETTING WINDOW
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PONG')
icon = pygame.image.load('ping-pong.png')
pygame.display.set_icon(icon)

#LOADING BACKGROUND
bg = pygame.image.load('background.png')
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT)).convert_alpha()

#SETTING CLOCK
clock = pygame.time.Clock()

#MUSICS
music = pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)
hitSound = pygame.mixer.Sound('hit.wav')

class player(object):
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vel = 10
        self.score = 0

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

class ball(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dirX = 10
        self.dirY = 10

    def draw(self, win):
        self.move()
        b1 = pygame.image.load('ball.png')
        win.blit(b1, (self.x, self.y))

    def move(self):
        self.x += self.dirX
        self.y += self.dirY
        if self.y >= HEIGHT:
            self.dirY *= -1
            self.y += self.dirY
        if self.y <= 0:
            self.y -= self.dirY
            self.dirY *= -1
            self.y -= self.dirY

def displayText(font, message, color, x, y):
    text = font.render(message, 1, color)
    win.blit(text, (x, y))

def redrawGameWindow():
    win.blit(bg, (0, 0))
    PADDLE1.draw(win)
    PADDLE2.draw(win)
    BALL.draw(win)
    displayText(SFONT, 'PLAYER 1 SCORE:' + str(PADDLE1.score), WHITE, 10, 10)
    displayText(SFONT, 'PLAYER 2 SCORE:' + str(PADDLE2.score), WHITE, 600, 10)
    if BALL.x >= WIDTH or BALL.x <= 20:
        displayText(GFONT, 'PRESS SPACE TO RESET BALL', ORANGE, 200, HEIGHT/2)
    if PADDLE1.score == 100:
        displayText(GFONT, 'PLAYER 1 WINS', RANDOM, 300, HEIGHT/2)
    if PADDLE2.score == 100:
        displayText(GFONT, 'PLAYER 2 WINS', RANDOM, 300, HEIGHT/2)
    pygame.display.update()

PADDLE1 = player(26, HEIGHT/2, 20, 100, BLUE)
PADDLE2 = player(753, HEIGHT/2, 20, 100, RED)
BALL = ball(WIDTH/2 - 16, HEIGHT/2, 32, 32)

def welcome():
    exit_game = False
    while not exit_game:
        win.fill(RANDOM)
        displayText(GFONT, "WELCOME TO PONG", BLACK, WIDTH/2 -150, HEIGHT/2)
        displayText(GFONT, "PRESS SPACE TO PLAY", BLACK, WIDTH/2 - 160, HEIGHT/2 + 40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()

        pygame.display.update()
        clock.tick(FPS)

def main():
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and PADDLE1.y > PADDLE1.vel:
            PADDLE1.y -= PADDLE1.vel
        if keys[pygame.K_s] and PADDLE1.y < HEIGHT - PADDLE1.vel - PADDLE1.height:
            PADDLE1.y += PADDLE1.vel
        if keys[pygame.K_UP] and PADDLE2.y > PADDLE2.vel:
            PADDLE2.y -= PADDLE2.vel
        if keys[pygame.K_DOWN] and PADDLE2.y < HEIGHT - PADDLE2.vel - PADDLE2.height:
            PADDLE2.y += PADDLE2.vel

        if BALL.x >= WIDTH or BALL.x <= 20:
            if keys[pygame.K_SPACE]:
                if BALL.x > WIDTH:
                    PADDLE1.score += 10
                if BALL.x < 20:
                    PADDLE2.score += 10
                BALL.x = random.randint(200, 600)
                BALL.y = random.randint(150, 450)
                BALL.dirX *= -1
                BALL.x += BALL.dirX

        if (BALL.x > 753 and BALL.x < 773) and (BALL.y > PADDLE2.y and BALL.y < PADDLE2.y + 100):
            hitSound.play()
            BALL.dirX *= -1
            BALL.x += BALL.dirX

        if (BALL.x > 26 and BALL.x < 46) and (BALL.y > PADDLE1.y and BALL.y < PADDLE1.y + 100):
            hitSound.play()
            BALL.dirX *= -1
            BALL.x += BALL.dirX

        if PADDLE1.score == 100 or PADDLE2.score == 100:
            run = False

        redrawGameWindow()

    pygame.quit()

welcome()
