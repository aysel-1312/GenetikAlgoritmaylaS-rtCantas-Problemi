
from collections import namedtuple
from random import choices, randint, randrange, random
from typing import List, Optional, Callable, Tuple
from functools import partial

Genler = List[int]
population = List[Genler]
FitnessFunc = Callable[[Genler], int]
Func = Callable[[], population]
secilenFunc = Callable[[population, FitnessFunc], Tuple[Genler, Genler]]
CrossoverFunc = Callable[[Genler, Genler], Tuple[Genler, Genler]]
mutasyonFunc = Callable[[Genler], Genler]


Nesne = namedtuple('Nesne', ['esya', 'Fayda', 'agirlik'])


tablo = [
    Nesne('1', 5, 7),
    Nesne('2', 8, 8),
    Nesne('3', 3, 4),
    Nesne('4', 2, 10),
    Nesne('5', 7, 4),
    Nesne('6', 9, 6),
    Nesne('7', 4, 4),
]

def gen_olusturma(length: int) -> Genler: #//0 ve 1 lerden gen oluşturma
    return choices([0,1], k=length)


def nesil_populasyon(size: int, gen_lenght: int) -> population: #//population olusturma
    return [gen_olusturma(gen_lenght) for _ in range(size)]

def fitness(genler: Genler, tablo: [Nesne], agirlik_limit: int) -> int: #//fitness fonksiyonu
    if len(genler) != len(tablo):
        raise ValueError("Genler aynı uzunluklukta olmalı")

    agirlik = 0
    Fayda = 0

    for i, Nesne in enumerate(tablo):
        if genler[i] == 1:
            agirlik += Nesne.agirlik
            Fayda += Nesne.Fayda

        if agirlik > agirlik_limit:
            return 0

    return Fayda

def secilen_cift(population: population, fitness_func: FitnessFunc) -> population:
    return choices(
        population=population,
        weights=[fitness_func(genler) for genler in population],
        k=2
    )

def crossover(a: Genler, b: Genler) -> Tuple[Genler, Genler]:
    if len(a) != len(b):
        raise ValueError("Genler aynı uzunlukta olmalı")

    lenght = len(a)
    if lenght <2:
        return a,b

    p = randint(1, lenght-1)
    return a[0:p] + b[p:], b[0:p] + a[p:]

def mutasyon(genler: Genler, num: int =1, probability: float = 0.5) -> Genler:
    for _ in range(num):
        index = randrange(len(genler))
        genler[index] = genler[index] if random() > probability else abs(genler[index] - 1)
    return genler

def evrim_basla(
    func: Func,
    fitness_func: FitnessFunc,
    fitness_limit: int,
    secilen_func: secilenFunc = secilen_cift,
    crossover_func: CrossoverFunc = crossover,
    mutasyon_func: mutasyonFunc = mutasyon,
    nesil_limit: int = 100
) -> Tuple[population, int]:
    population = func()

    for i in range(nesil_limit):
        population = sorted(
            population,
            key=lambda genler: fitness_func(genler),
            reverse=True
        )

        if fitness_func(population[0]) >=fitness_limit:
            break

        yeni_nesil = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = secilen_func(population, fitness_func)
            cocuk_a,cocuk_b = crossover_func(parents[0], parents[1])
            cocuk_a = mutasyon_func(cocuk_a)
            cocuk_b = mutasyon_func(cocuk_b)
            yeni_nesil += [cocuk_a,cocuk_b]

        population = yeni_nesil

    population = sorted(
            population,
            key=lambda genler: fitness_func(genler),
            reverse=True
    )

    return population, i

population, nesiller = evrim_basla(
    func=partial(
        nesil_populasyon, size=10, gen_lenght=len(tablo)
    ),
    fitness_func=partial(
        fitness, tablo=tablo, agirlik_limit=22
    ),
    fitness_limit=200,
    nesil_limit=50
)

def gen_tablo(genler: Genler, tablo: [Nesne]) -> [Nesne]:
    result = []
    for i, Nesne in enumerate(tablo):
        if genler[i] == 1:
            result += [Nesne.esya]
    
    return result

print(f"jenerasyon sayısı: {nesiller}")
print(f"En iyi esyalar: {gen_tablo(population[0], tablo)}")
