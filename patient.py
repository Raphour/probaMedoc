import random

proba_medicament = {
    "med1": 0.05,
    "med2": 0.15,
    "med3": 0.25,
    "med4": 0.35,
    "med5": 0.45,
    "med6": 0.55,
    "med7": 0.65,
    "med8": 0.75,
    "med9": 0.85,
    "med10": 0.95
}


def resultat_medicament(medicament):
    pi = proba_medicament[medicament]
    if pi >= random.random():
        return True
    return False
