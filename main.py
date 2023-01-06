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
endgame = False
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
startas = True

tankas = Tankas(gamesizex, gamesizey, a, kulka)

running = True
while running:
    screen.fill((50, 50, 70))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                startas = False
            if event.key == pygame.K_x:
                endgame = False
                tankas.taikinys()
                tankas.ugnis()
                tankas.score = 0
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
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
    if startas:
        screen.blit(tekstas2.render("WELCOME!", True, (165, 205, 25)), (240, 200))
        screen.blit(tekstas.render("Press 'P' to play", True, (165, 205, 25)), (300, 300))
    else:
        tankas.stepx = -0.1 if lastkey == pygame.K_a else 0.1 if lastkey == pygame.K_d else 0
        tankas.stepy = -0.1 if lastkey == pygame.K_w else 0.1 if lastkey == pygame.K_s else 0

        if busena == "Issauta":
            screen.blit(kulka, (tankas.kulkax, tankas.kulkay))
            tankas.kulkax += tankas.stepkulkax
            tankas.kulkay += tankas.stepkulkay
            if tankas.kulkax < 0 or tankas.kulkay < 0 or tankas.kulkax > gamesizex or tankas.kulkay > gamesizey:
                busena = "Laukia"

        tankas.koordinates()

        if tankas.boom():
            busena = "Laukia"
            hit = pygame.mixer.Sound("explosion2.wav")
            hit.play()
            tankas.taikinys()
            tankas.score += 1

        tankas.ugnisx += tankas.ugnisstepx
        tankas.ugnisy += tankas.ugnisstepy

        if tankas.ugnisx < 0 or tankas.ugnisy < 0 or tankas.ugnisx > gamesizex or tankas.ugnisy > gamesizey:
            tankas.ugnis()
        dist = math.sqrt(math.pow(tankas.x - tankas.ugnisx + 25, 2) + math.pow(tankas.y - tankas.ugnisy + 25, 2))
        if dist < 34:
            endgame = True
            if tankas.score > highscore and highscore != tankas.score:
                with open("rezultatai.pkl", "wb") as file:
                    pickle.dump(tankas.score, file)
                    highscore = tankas.score
        if endgame:
            screen.blit(tekstas2.render("GAME OVER", True, (165, 205, 25)), (220, 240))
            screen.blit(tekstas.render("Press 'X' to play again", True, (165, 205, 25)), (280, 340))

        screen.blit(tankas.pozicija, (tankas.x, tankas.y))
        screen.blit(tekstas.render("Your score: " + str(tankas.score), True, (145, 135, 225)), (2, 2))
        screen.blit(tekstas.render("Highscore: " + str(highscore), True, (5, 205, 205)), (2, 30))
        if endgame == False:
            screen.blit(enemy, (tankas.enemyx, tankas.enemyy))
            screen.blit(fire, (tankas.ugnisx, tankas.ugnisy))
    pygame.display.update()
