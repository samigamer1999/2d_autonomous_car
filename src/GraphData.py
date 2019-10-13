import matplotlib.pyplot as plt

f = open("savefile.txt", "r")
gen = [[], [], []]
fit = [[], [], []]
for line in f:
    temp = line.split(',')
    gen[int(temp[2])] += [int(temp[0])]
    fit[int(temp[2])] += [float(temp[1])]
f.close()
plt.title("Pour 30 voitures")
plt.xlabel("Generation")
plt.ylabel("Max_fitness")
plt.plot(gen[0], fit[0], label='10%')
plt.plot(gen[1], fit[1], label='20%')
plt.plot(gen[2], fit[2], label='30%')
plt.legend(loc='upper left')
plt.show()
