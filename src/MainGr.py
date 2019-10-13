import os
import pygame
from src.Car import Car
from src.reseau import ReseauNeurone
import math
import numpy as np

class Game:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont(" ", 20)
        pygame.init()
        pygame.display.set_caption("TIPE")
        pygame.font.init()
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.updates = 10

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # initialisation circuit
        circuit = pygame.image.load("track.png").convert_alpha()
        track_mask = pygame.mask.from_surface(circuit)
        given_brain = ReseauNeurone(3, 6, 2)
        given_brain.E_C_matrice = [[-8.97733451e-02, 3.88300394e-01, -4.33225819e-01],
                                   [-5.60947796e-01, -3.44441383e-01, 2.26400017e-01],
                                   [-4.05719496e-01, -8.51709163e-01, 7.65198411e-01],
                                   [-2.52344199e-01, 2.92995343e-01, 3.26502978e-04],
                                   [-2.92018717e-01, -5.59915332e-01, 4.38344407e-01],
                                   [4.77456562e-01, 7.88640334e-01, -4.51291827e-01]]
        given_brain.C_S_matrice = [[0.35782455, 0.09804306, 0.04327138, -0.41764635, -0.41508099, 0.53154817],
                                   [0.51327193, 0.33521452, 0.36453928, -0.43719057, 0.7806659, 0.31162904]]
        given_brain.E_C_biais = [-0.11689981, -0.14345427, 0.45680658, 0.1483759, 0.10124425, -0.1142477]
        given_brain.C_S_biais = [0.02099482, 0.80842289]
        car = Car(0, 0)
        car.brain.E_C_biais = [-0.11689981, -0.14345427, 0.45680658, 0.1483759, 0.10124425, -0.1142477]
        car.brain.C_S_biais = [0.02099482, 0.80842289]
        times = 0
        error = 1000
        rate = 1
        while not self.exit:
            dt = self.clock.get_time() / 1000
            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                if self.updates < 1000:
                    self.updates += 1

            if pressed[pygame.K_DOWN]:
                if self.updates > 1:
                    self.updates -= 1
            max_fitness = 0
            last_pos = (car.position.x, car.position.y)
            for i in range(self.updates):
                if car.fitness > 7000:
                    print("Done")
                # Logic
                errorx = car.update(dt, given_brain, rate)

                # Drawing
                self.screen.fill((0, 0, 0))
                self.screen.blit(circuit, (-500, -300) - car.car_position())
                car.display(self.screen)
                if car.fitness > max_fitness:
                    max_fitness = car.fitness
                car.fitness += math.sqrt((car.position.x - last_pos[0])**2 + (car.position.y - last_pos[1])**2)
                last_pos = (car.position.x, car.position.y)
                # Collision detection
                offset = (-(int(-500 - car.position.x * 32 - 640 + car.rect.width/2)), -(int(-300 - car.position.y * 32 - 360 + car.rect.height/2)))
                result = track_mask.overlap(car.mask, offset)
                if result or car.velocity.x < 0:
                    temp_error = math.sqrt(np.dot(errorx, errorx))
                    temp_matrice = [car.brain.E_C_matrice, car.brain.C_S_matrice]
                    if temp_error <= error:
                        error = temp_error
                        rate *= 1.05
                    else:
                        car.brain.E_C_matrice = temp_matrice[0]
                        car.brain.C_S_matrice = temp_matrice[1]
                        rate *= 0.95
                    times+=1
                    f = open("savefile.txt", "a")
                    f.write(str(times) + " " + str(error))
                    f.write("\n")
                    f.close
                    car.reset()
                text = [self.clock.get_fps(),
                           car.angle,
                           car.velocity,
                        self.updates]
                for y in range(len(text)):
                    self.screen.blit(self.font.render(str(text[y]), True, (0, 255, 0)), (10, 10 + (10 * y)))
                pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
