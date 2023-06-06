import random
import math
import patient
from matplotlib import pyplot as plt


class Medicaments:
    def __init__(self, nom):
        self.nom = nom
        self.nb_succes = 0
        self.nb_test = 0

    def succes(self):
        self.nb_succes += 1

    def test(self):
        self.nb_test += 1

    def clear(self):
        self.nb_succes = 0
        self.nb_test = 0


medicaments = [Medicaments("med{}".format(i)) for i in range(1, 11)]


def somme_test():
    somme = 0
    for i in range(10):
        somme += medicaments[i].nb_test
    return somme


def clear_medic():
    for medic in medicaments:
        medic.clear()


def somme_succes():
    somme = 0
    for i in range(10):
        somme += medicaments[i].nb_succes
    return somme


def test_est_fini():
    somme = 0
    for i in range(10):
        somme += medicaments[i].nb_test
    return somme >= 100


def test_10_fois_chacun():
    nb_succes = 0
    for med in medicaments:
        for i in range(10):
            med.test()
            if patient.resultat_medicament(med.nom):
                med.succes()
    for i in range(10):
        nb_succes += medicaments[i].nb_succes
    return nb_succes


def test_x_jours(nbjours: int, precision: float):
    nb_test = round(nbjours / 10)
    for _ in range(nb_test):
        for med in medicaments:
            med.test()
            if patient.resultat_medicament(med.nom):
                med.succes()

        # 20 Jours
    liste_succes = [medicaments[i].nb_succes / medicaments[i].nb_test for i
                    in range(10)]

    liste_med_reussi = [medicaments[i] for i in range(10) if
                        medicaments[i].nb_succes / medicaments[i].nb_test >= 0.5]

    i = 0
    while not (test_est_fini()):
        temp = max(liste_med_reussi, key=lambda item: item.nb_succes)
        liste_med_reussi = [liste_med_reussi[i] for i in range(len(liste_med_reussi)) if
                            liste_med_reussi[i].nb_succes / liste_med_reussi[i].nb_test >= 0.5 + precision * i]
        if len(liste_med_reussi) == 0:
            liste_med_reussi.append(temp)

        for med in liste_med_reussi:
            if test_est_fini():
                return liste_succes, liste_med_reussi, somme_succes()
            else:

                med.test()
                if patient.resultat_medicament(med.nom):
                    med.succes()

        liste_succes = [liste_med_reussi[i].nb_succes / liste_med_reussi[i].nb_test for i in
                        range(len(liste_med_reussi))]
        i += 1

    return liste_succes, liste_med_reussi, somme_succes()

# clear_medic()
# test = test_x_jours(50,10)
# succes = test[2]
# print(succes)
# meds = test[1]
# print(meds[0].nom)


def test_efficacite():
    result = {}
    for i in range(10, 51):

        for j in range(10, 100,2):

            result_tuple = []
            for _ in range(10):
                clear_medic()
                result_tuple.append((test_x_jours(i, 1 / j)[2]))

            result[(i, j)] = sum(result_tuple) / len(result_tuple)
    return result


def plot_dict(dictionary):
    keys = [str(key) for key in dictionary.keys()]
    values = list(dictionary.values())

    plt.scatter(keys, values)
    plt.xlabel('Clés')
    plt.ylabel('Valeurs')
    plt.title('Graphique des clés et des valeurs')
    plt.show()


# plot_dict(test_efficacite())

# 2eme solution

def choisir_medicament(medicaments):
    total_tests = sum(m.nb_test for m in medicaments)
    if total_tests == 0:
        return random.choice(medicaments)

    # Calculer les scores UCB (Upper Confidence Bound) pour chaque médicament
    scores_ucb = []
    for medicament in medicaments:
        if medicament.nb_test == 0:
            scores_ucb.append(float('inf'))
        else:
            mean = medicament.nb_succes / medicament.nb_test
            exploration_term = math.sqrt(2 * math.log(total_tests) / medicament.nb_test)
            score = mean + exploration_term
            scores_ucb.append(score)

    # Choisir le médicament avec le score UCB le plus élevé
    max_score = max(scores_ucb)
    best_medicaments = [medicament for medicament, score in zip(medicaments, scores_ucb) if score == max_score]
    return random.choice(best_medicaments)

for i in range(50):
    nombre_jours = 100
    nombre_patients_soignes = 0
    clear_medic()
    for jour in range(nombre_jours):
        medicament_choisi = choisir_medicament(medicaments)
        # Effectuer le test du médicament sur un patient (résultat binaire)
        resultat_test = patient.resultat_medicament(medicament_choisi.nom)
        if resultat_test:
            medicament_choisi.succes()
            nombre_patients_soignes += 1
        medicament_choisi.test()

    print("Nombre de patients soignés :", nombre_patients_soignes)