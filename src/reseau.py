import numpy as np
import random as rd


class ReseauNeurone:



    def __init__(self, n_entree, n_cachee, n_sortie, brain=None):
        if brain is None:
            self.n_entree = n_entree
            self.n_cachee = n_cachee
            self.n_sortie = n_sortie
            self.E_C_matrice = np.random.rand(n_cachee, n_entree) - np.random.rand(n_cachee, n_entree)
            self.C_S_matrice = np.random.rand(n_sortie, n_cachee) - np.random.rand(n_sortie, n_cachee)
            self.E_C_biais = np.random.rand(n_cachee) - np.random.rand(n_cachee)
            self.C_S_biais = np.random.rand(n_sortie) - np.random.rand(n_sortie)
        else:
            self.E_C_matrice = self.mutate(brain.E_C_matrice.copy())
            self.C_S_matrice = self.mutate(brain.C_S_matrice.copy())
            self.E_C_biais = self.mutate_b(brain.E_C_biais.copy())
            self.C_S_biais = self.mutate_b(brain.C_S_biais.copy())


    def __str__(self):
        s =  """"Matrice poids Entree --> Cachee \n
{} \n
Matrice poids Cachee --> Sortie \n
{} \n
Vecteur biais Entree --> Cachee \n
{} \n
Vecteur biais Cachee --> Sortie \n
{} \n""".format(self.E_C_matrice, self.C_S_matrice, self.E_C_biais, self.C_S_biais)
        return s



    #Les fonctions
    def sigmoid(self, vecteur):
        return 1/(1 + np.exp(-vecteur))

    def sigmoid_prime(self, z):
        return self.sigmoid(z) * (1 - self.sigmoid(z))


    # Alg. propagation en avant

    def propagation_avant(self, entree):
        self.entree2 = self.sigmoid(np.dot(self.E_C_matrice, entree) - self.E_C_biais)
        return self.sigmoid(np.dot(self.C_S_matrice, self.entree2) - self.C_S_biais) - 0.5


    #Correction DG

    def corriger(self, Y, S, E, rate):
        propa = rate * np.multiply((S - Y), self.sigmoid_prime(np.dot(self.C_S_matrice, self.entree2) - self.C_S_biais))
        self.C_S_matrice -= np.dot(propa.reshape((-1, 1)), self.entree2.reshape(1, 6))
        temp = np.dot(np.transpose(propa), self.C_S_matrice)
        self.E_C_matrice -= np.dot(np.multiply(temp, self.sigmoid_prime(np.dot(self.E_C_matrice, E) - self.E_C_biais)).reshape(-1, 1), np.array(E).reshape(1, 3))


    # Les mutations
    def mutate(self, x):
        res = []
        for i in range(len(x)):
            temp = []
            for j in range(len(x[0])):
                if rd.random() < 0.2:
                    temp.append(x[i][j] + (rd.random() - 0.5) / 5)
                else:
                    temp.append(x[i][j])
            res.append(temp)
        return np.array(res)

    def mutate_b(self, x):
        res = []
        for i in range(len(x)):
            if rd.random() < 0.2:
                res.append(x[i] + (rd.random() - 0.5) / 5)
            else:
                res.append(x[i])
        return np.array(res)



