import os
import pygame
from src.Car import Car
import src.GA
import math


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
        voitures = []
        voitures_sauve = []
        max_fitness = 0
        generation = 1
        nbr_voit=[10, 20, 30]
        # initialisation circuit
        circuit = pygame.image.load("track.png").convert_alpha()
        track_mask = pygame.mask.from_surface(circuit)

        # initialisation generation voitures
        nbr = 0
        for i in range(nbr_voit[nbr]):
            voitures.append(Car(0, 0))
        car = voitures[0]

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

            last_pos = (car.position.x, car.position.y)
            for i in range(self.updates):
                if car.fitness > 7000:
                    car.save_neural()
                    voitures_sauve = []
                    nbr += 1
                    generation = 1
                    max_fitness = 0
                    for _ in range(nbr_voit[nbr]):
                        voitures.append(Car(0, 0))
                    car = voitures[0]
                if len(voitures) == 0:
                    if generation > 250:
                        print("gen")
                        voitures_sauve = []
                        nbr += 1
                        generation = 1
                        max_fitness = 0
                        for _ in range(nbr_voit[nbr]):
                            voitures.append(Car(0, 0))
                    else:
                        car.savegen(generation, max_fitness, nbr)
                        generation += 1
                        voitures = src.GA.nouvelle_gen(voitures_sauve)
                        voitures_sauve = []
                        voitures.append(Car(0, 0))
                        voitures.append(Car(0, 0))
                car = voitures[0]
                # Logic
                car.update(dt, pressed)

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
                    voitures_sauve.append(voitures.pop(0))
                text = [self.clock.get_fps(),
                           "Generation :" + str(generation),
                           "Genome:" + str(len(voitures_sauve)+1),
                           car.angle,
                           car.velocity,
                           car.fitness,
                        "Max fit:" + str(max_fitness),
                        self.updates]
                for y in range(len(text)):
                    self.screen.blit(self.font.render(str(text[y]), True, (0, 255, 0)), (10, 10 + (10 * y)))
                pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
