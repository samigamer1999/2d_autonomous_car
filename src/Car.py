from math import tan, radians, degrees, copysign, sin, cos
from pygame.math import Vector2
import pygame
from src.reseau import ReseauNeurone
import numpy as np

class Car:
    def __init__(self, x, y, brain=0, angle=0.0, length=4, max_steering=30, max_acceleration=5.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 20
        self.brake_deceleration = 10
        self.free_deceleration = 2

        self.acceleration = 0.0
        self.steering = 0.0

        self.car_image = pygame.image.load("car.png").convert_alpha()
        self.rect = pygame.transform.rotate(self.car_image, self.angle).get_rect()
        self.mask = pygame.mask.from_surface(self.car_image)

        # brain
        if brain == 0:
            self.brain = ReseauNeurone(3, 6, 2)
        else:
            self.brain = ReseauNeurone(0, 0, 0, brain)
        self.sensors = [0, 0, 0]
        self.fitness = 0

    def update(self, dt, given_brain, rate):
        self.velocity = (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / tan(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

        # Brain deciding
        temp = 0
        for n in self.sensors:
            temp +=n
        if temp == 0:
            temp = 1
        for i in range(len(self.sensors)):
            self.sensors[i] /= temp
        output = self.brain.propagation_avant(np.array(self.sensors))
        self.acceleration = output[0] * 5
        self.steering = output[1] * 60
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

        # Brain correction
        Y = given_brain.propagation_avant(np.array(self.sensors))
        self.brain.corriger(Y, output, self.sensors, rate)
        return Y - output


    def display(self, screen, voiture_pos=Vector2(0.0, 0.0)):
        dist = 350
        sensors = ["0", "1", "2"]
        rotated = pygame.transform.rotate(self.car_image, self.angle)
        self.rect = rotated.get_rect()

        for i in range(0, dist, 3):
            if "0" in sensors:
                if screen.get_at((int(640 + i * cos(radians(-self.angle))),  int(360 + i * sin(radians(-self.angle))))) == (136, 136, 136):
                    sensors.remove("0")
                    self.sensors[0] = i
                pygame.draw.line(screen, (255, 255, 255), (640, 360),
                                 (640 + i * cos(radians(-self.angle)), 360 + i * sin(radians(-self.angle))))

            if "1" in sensors:
                if screen.get_at((int(640 + i * sin(radians(self.angle + 30))),  int(360 + i * cos(radians(self.angle + 30))))) == (136, 136, 136):
                    sensors.remove("1")
                    self.sensors[1] = i
                pygame.draw.line(screen, (255, 255, 255), (640, 360),
                                 (640 + i * sin(radians(self.angle + 30)), 360 + i * cos(radians(self.angle + 30))))

            if "2" in sensors:
                if screen.get_at((int(640 + i * sin(-radians(self.angle - 30))),  int(360 + i * -cos(radians(self.angle - 30))))) == (136, 136, 136):
                    sensors.remove("2")
                    self.sensors[2] = i
                pygame.draw.line(screen, (255, 255, 255), (640, 360),
                                 (640 + i * sin(-radians(self.angle - 30)), 360 + i * -cos(radians(self.angle - 30))))

        screen.blit(rotated, (640 - self.rect.width / 2, 360 - self.rect.height / 2) )


    def car_position(self):
        return self.position * 32

    def reset(self):
        self.position.x = 0
        self.position.y = 0
        self.acceleration = 0
        self.velocity = Vector2(0.0, 0.0)
        self.fitness = 0
        self.angle = 0

    def setMask(self, mask):
        self.mask = mask

    def get_Child(self):
        return Car(0, 0, self.brain)

    def getIt(self):
        self.position = Vector2(0, 0)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = 0

        self.acceleration = 0.0
        self.steering = 0.0


        return self

    def save_neural(self):
        f = open("savefile.txt", "a")
        f.write("/n")
        f.write(str(self.brain.E_C_matrice))
        f.write(str(self.brain.C_S_matrice))
        f.write(str(self.brain.E_C_biais))
        f.write(str(self.brain.C_S_biais))
        f.close()

    def savegen(self, gen, fit, nbr):
        f = open("savefile.txt", "a")
        f.write(str(gen)+","+str(fit)+','+str(nbr))
        f.write("\n")
        f.close()








