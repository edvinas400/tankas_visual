import random
import pygame
import math


class Tankas():
    def __init__(self, gamesizex, gamesizey, pozicija, kulka, score=0, stepx=0, stepy=0,
                 stepkulkax=0, stepkulkay=0):
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
        self.score = score
        self.pozicija = pozicija
        self.kryptis = "North"
        self.kulka = kulka
        self.kulkax = self.x
        self.kulkay = self.y
        self.taikinys()

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

    def kairen(self):
        self.pozicija = pygame.transform.rotate(self.ogpozicija, 90)
        self.kulka = pygame.transform.rotate(self.ogkulka, 90)
        self.kryptis = "West"

    def atgal(self):
        self.pozicija = pygame.transform.rotate(self.ogpozicija, 180)
        self.kulka = pygame.transform.rotate(self.ogkulka, 180)
        self.kryptis = "South"

    def desinen(self):
        self.pozicija = pygame.transform.rotate(self.ogpozicija, -90)
        self.kulka = pygame.transform.rotate(self.ogkulka, -90)
        self.kryptis = "East"

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

    def taikinys(self):
        self.enemyx = random.randint(0, 736)
        self.enemyy = random.randint(0, 536)
        self.ugnis()

    def ugnis(self):
        self.ugnisx = self.enemyx + 28
        self.ugnisy = self.enemyy + 28
        # Calculate the vector from the enemy to the object
        vector_x = self.x - self.enemyx
        vector_y = self.y - self.enemyy
        # Calculate the angle between the enemy and the object
        angle = math.atan2(vector_y, vector_x)
        self.ugnisstepx = math.cos(angle) * 0.25
        self.ugnisstepy = math.sin(angle) * 0.25

    def boom(self):
        dist = math.sqrt(math.pow(self.enemyx - self.kulkax + 24, 2) + math.pow(self.enemyy - self.kulkay + 25, 2))
        if dist < 32:
            return True
        else:
            return False
