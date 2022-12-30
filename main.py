import pygame
from tankas import Tankas, pickle

pygame.init()

gamesizex = 800
gamesizey = 600
lastkey = None
screen = pygame.display.set_mode((gamesizex, gamesizey))

pygame.display.set_caption("Zaidimukas")
icon = pygame.image.load("tankas.png")
pygame.display.set_icon(icon)

a = pygame.image.load("tankas.png")
kulka = pygame.image.load("kulka.png")
suvis = "Laukia"

tankas = Tankas(gamesizex, gamesizey, a, kulka)

running = True
while running:
    screen.fill((50, 50, 70))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                suvis = "Issauta"
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
    tankas.koordinates()
    if suvis == "Issauta":
        screen.blit(kulka, (tankas.kulkax, tankas.kulkay))
        tankas.kulkax += tankas.stepkulkax
        tankas.kulkay +=tankas.stepkulkay

    screen.blit(tankas.pozicija, (tankas.x, tankas.y))
    pygame.display.update()

# while True:
#     choice1 = input("z - naujas zaidimas\nt - rezultatai\nv - isvalyti rezultatus\ni - iseiti\n")
#     match choice1:
#         case "t":
#             try:
#                 with open("rezultatai.pkl", "rb") as file:
#                     highscores = pickle.load(file)
#                     for x in highscores:
#                         print(x)
#             except:
#                 print("Sarasas tuscias")
#
#         case "v":
#             with open("rezultatai.pkl", "wb") as file:
#                 a = []
#                 pickle.dump(a, file)
#         case "i":
#             break
#         case _:
#             print("Neteisingai pasirinktas veiksmas")
