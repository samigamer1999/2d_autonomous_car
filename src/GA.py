import random

def calculate_fitness(voitures_sauve):
    somme = 0
    for car in voitures_sauve:
        somme += car.fitness

    for car in voitures_sauve:
        car.fitness = car.fitness / somme


def nouvelle_gen(voitures_sauves):
    calculate_fitness(voitures_sauves)
    return generate(voitures_sauves)


def selection(voitures_sauves):

    index = 0

    r = random.random()

    while r > 0:
        r-= voitures_sauves[index].fitness
        index += 1
    index -= 1
    return voitures_sauves[index].get_Child()


def generate(voitures_sauve):
    nv_gen = []
    index = 0
    fitmax = 0
    for i in range(len(voitures_sauve)):
        if voitures_sauve[i].fitness > fitmax:
            index = i
            fitmax = voitures_sauve[i].fitness
    nv_gen.append(voitures_sauve[index].getIt())
    for i in range(7):
        nv_gen.append(selection(voitures_sauve))
    nv_gen[0].fitness = 0
    return nv_gen

