import matplotlib.pyplot as plt

f = open("savefile.txt", "r")
hit = []
fit = []

for line in f:
    temp = line.split(' ')
    hit.append(int(temp[0]))
    fit.append(float(temp[1]))
plt.plot(hit, fit)
plt.show()