import random
import pygame
import pickle


class Tankas():
    def __init__(self, gamesizex, gamesizey, pozicija, kulka, taskai=10000000000000, score=0, stepx=0, stepy=0,
                 stepkulkax=0, stepkulkay =0):
        self.gamesizex = gamesizex
        self.gamesizey = gamesizey
        self.ogpozicija = pozicija
        self.ogkulka = kulka
        self.stepx = stepx
        self.stepy = stepy
        self.stepkulkax = stepkulkax
        self.stepkulkay = stepkulkay
        self.x = gamesizex / 2 - 32
        self.y = gamesizey - 64
        self.taskai = taskai
        self.score = score
        self.pozicija = pozicija
        self.kryptis = ""
        self.kulka = kulka
        self.kulkax = self.x
        self.kulkay = self.y
        self.taikinys()
        try:
            with open("rezultatai.pkl", "rb") as file:
                self.highscores = pickle.load(file)
        except:
            self.highscores = []
        self.info()

    def taskusekimas(self):
        if self.taskai <= 0:
            name = input(f"Zaidimas baigtas, jusu rezultatas: {self.score}, iveskite savo varda: ")
            with open("rezultatai.pkl", "wb") as file:
                add = f"{name}: {self.score}"
                self.highscores.append(add)
                pickle.dump(self.highscores, file)
            exit()

    def koordinates(self):
        self.x += self.stepx
        self.y += self.stepy
        self.ribos()

    def ribos(self):
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.y > self.gamesizey - 64:
            self.y = self.gamesizey - 64
        if self.x > self.gamesizex - 64:
            self.x = self.gamesizex - 64

    def pirmyn(self):
        self.pozicija = self.ogpozicija
        self.kulka = self.ogkulka
        self.kryptis = "North"
        self.taskai -= 10
        self.taskusekimas()
        self.info()

    def kairen(self):
        self.pozicija = pygame.transform.rotate(self.ogpozicija, 90)
        self.kulka = pygame.transform.rotate(self.ogkulka, 90)
        self.kryptis = "West"
        self.taskai -= 10
        self.taskusekimas()
        self.info()

    def atgal(self):
        self.pozicija = pygame.transform.rotate(self.ogpozicija, 180)
        self.kulka = pygame.transform.rotate(self.ogkulka, 180)
        self.kryptis = "South"
        self.taskai -= 10
        self.taskusekimas()
        self.info()

    def desinen(self):
        self.pozicija = pygame.transform.rotate(self.ogpozicija, -90)
        self.kulka = pygame.transform.rotate(self.ogkulka, -90)
        self.kryptis = "East"
        self.taskai -= 10
        self.taskusekimas()
        self.info()

    def suvis(self):
        match self.kryptis:
            case "North":
                self.kulkax = self.x + 24
                self.kulkay = self.y - 16
                self.stepkulkax = 0
                self.stepkulkay = -0.5
            case "South":
                self.kulkax = self.x + 24
                self.kulkay = self.y + 64
                self.stepkulkax = 0
                self.stepkulkay = 0.5
            case "West":
                self.kulkax = self.x - 16
                self.kulkay = self.y + 24
                self.stepkulkax = -0.5
                self.stepkulkay = 0
            case "East":
                self.kulkax = self.x + 64
                self.kulkay = self.y + 24
                self.stepkulkax = 0.5
                self.stepkulkay = 0


        print(self.ar_pataike())
        if self.ar_pataike() == "Pataikyta!":
            self.taskai += 50
            self.score += 1
            self.taikinys()
            print(f"Sukurtas naujas taikinys {self.taik}")
        self.info()

    def info(self):
        print(f"Turimi taskai: {self.taskai}, numusti taikiniai: {self.score}")
        print(f"Taikinio koordinates: {self.taik}")

    def taikinys(self):
        self.taik = (random.randint(-10, 10), random.randint(-10, 10))

    def ar_pataike(self):
        if self.x == self.taik[0] and self.y == self.taik[1]:
            return ("Uzvaziuota ant taikinio!!")
        elif self.x == self.taik[0]:
            if self.y < self.taik[1] and self.kryptis == "Siaure":
                return ("Pataikyta!")
            elif self.y > self.taik[1] and self.kryptis == "Pietus":
                return ("Pataikyta!")
            else:
                return ("Nepataikyta")
        elif self.y == self.taik[1]:
            if self.x < self.taik[0] and self.kryptis == "Rytai":
                return ("Pataikyta!")
            elif self.x > self.taik[0] and self.kryptis == "Vakarai":
                return ("Pataikyta!")
            else:
                return ("Nepataikyta")
        else:
            return ("Nepataikyta")
