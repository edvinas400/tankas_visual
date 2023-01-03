import pygame, pickle
from tankas import Tankas, math

pygame.init()
try:
    with open("rezultatai.pkl", "rb") as file:
        highscore = pickle.load(file)
except:
    highscore = 0

gamesizex = 800
gamesizey = 600
lastkey = None
screen = pygame.display.set_mode((gamesizex, gamesizey))

pygame.display.set_caption("Zaidimukas")
icon = pygame.image.load("tankas.png")
pygame.display.set_icon(icon)

a = pygame.image.load("tankas.png")
kulka = pygame.image.load("kulka.png")
enemy = pygame.image.load("enemy2.png")
fire = pygame.image.load("fire.png")
tekstas = pygame.font.Font("sketch.otf", 30)
tekstas2 = pygame.font.Font("sketch.otf", 100)

busena = "Laukia"

tankas = Tankas(gamesizex, gamesizey, a, kulka)

running = True
while running:
    screen.fill((50, 50, 70))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if busena == "Laukia":
                    busena = "Issauta"
                    boom = pygame.mixer.Sound("laser2.wav")
                    boom.play()
                    tankas.suvis()
                    kulka = tankas.kulka
            if event.key in (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s):
                lastkey = event.key
            match lastkey:
                case pygame.K_a:
                    tankas.kairen()
                case pygame.K_w:
                    tankas.pirmyn()
                case pygame.K_d:
                    tankas.desinen()
                case pygame.K_s:
                    tankas.atgal()
        if event.type == pygame.KEYUP:
            if event.key == lastkey:
                lastkey = None
        if event.type == pygame.QUIT:
            running = False

    tankas.stepx = -0.1 if lastkey == pygame.K_a else 0.1 if lastkey == pygame.K_d else 0
    tankas.stepy = -0.1 if lastkey == pygame.K_w else 0.1 if lastkey == pygame.K_s else 0

    if busena == "Issauta":
        screen.blit(kulka, (tankas.kulkax, tankas.kulkay))
        tankas.kulkax += tankas.stepkulkax
        tankas.kulkay += tankas.stepkulkay
        if tankas.kulkax < 0 or tankas.kulkay < 0 or tankas.kulkax > gamesizex or tankas.kulkay > gamesizey:
            busena = "Laukia"

    tankas.koordinates()
    screen.blit(tankas.pozicija, (tankas.x, tankas.y))
    screen.blit(tekstas.render("Your score: " + str(tankas.score), True, (145, 135, 225)), (2, 2))
    screen.blit(tekstas.render("Highscore: " + str(highscore), True, (5, 205, 205)), (2, 30))

    if tankas.boom():
        busena = "Laukia"
        hit = pygame.mixer.Sound("explosion2.wav")
        hit.play()
        tankas.taikinys()
        tankas.score += 1
    screen.blit(enemy, (tankas.enemyx, tankas.enemyy))

    tankas.ugnisx += tankas.ugnisstepx
    tankas.ugnisy += tankas.ugnisstepy

    if tankas.ugnisx < 0 or tankas.ugnisy < 0 or tankas.ugnisx > gamesizex or tankas.ugnisy > gamesizey:
        tankas.ugnis()
    dist = math.sqrt(math.pow(tankas.x - tankas.ugnisx + 24, 2) + math.pow(tankas.y - tankas.ugnisy + 24, 2))
    if dist < 32 or tankas.enemyx>1000:
        tankas.enemyx = 2000
        tankas.enemyy = 2000
        tankas.ugnisx = 2000
        tankas.ugnisy = 2000
        tankas.ugnisstepx = 0
        tankas.ugnisstepy = 0
        if tankas.score > highscore:
            with open("rezultatai.pkl", "wb") as file:
                pickle.dump(tankas.score, file)
                highscore = tankas.score
        screen.blit(tekstas2.render("GAME OVER", True, (165, 205, 25)), (220, 240))

    screen.blit(tankas.pozicija, (tankas.x, tankas.y))
    screen.blit(tekstas.render("Your score: " + str(tankas.score), True, (145, 135, 225)), (2, 2))
    screen.blit(tekstas.render("Highscore: " + str(highscore), True, (5, 205, 205)), (2, 30))
    screen.blit(fire, (tankas.ugnisx, tankas.ugnisy))

    pygame.display.update()

