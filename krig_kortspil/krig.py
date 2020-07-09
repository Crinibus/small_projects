import random
from dataclasses import dataclass


@dataclass
class Kortspil:
    antal_kort: int
    unikke_kort: dict
    antal_mulige_kort: dict
    antal_taget_kort: dict

    

kortspil = Kortspil(52, 
                    {"1": "1", 
                     "2": "2", 
                     "3": "3",
                     "4": "4",
                     "5": "5",
                     "6": "6",
                     "7": "7",
                     "8": "8",
                     "9": "9",
                     "10": "10",
                     "11": "11",
                     "12": "12",
                     "13": "13"},
                    {"1": 4,
                     "2": 4, 
                     "3": 4,
                     "4": 4,
                     "5": 4,
                     "6": 4,
                     "7": 4,
                     "8": 4,
                     "9": 4,
                     "10": 4,
                     "11": 4,
                     "12": 4,
                     "13": 4},
                    {"1": 0,
                     "2": 0, 
                     "3": 0,
                     "4": 0,
                     "5": 0,
                     "6": 0,
                     "7": 0,
                     "8": 0,
                     "9": 0,
                     "10": 0,
                     "11": 0,
                     "12": 0,
                     "13": 0})


class Spiller:
    def __init__(self, navn, antal_kort):
        self.navn = navn
        self.antal_kort = int(antal_kort)
        self.taget_kort = {"1": 0,
                           "2": 0, 
                           "3": 0,
                           "4": 0,
                           "5": 0,
                           "6": 0,
                           "7": 0,
                           "8": 0,
                           "9": 0,
                           "10": 0,
                           "11": 0,
                           "12": 0,
                           "13": 0}
        self.uddel_kort()

    def vælg_tilfældigt_kort(self):
        '''Returnere et tilfældigt kort som ikke er taget 4 gange (der er f.eks. kun 4 konger)'''
        tilfældigt_kort = kortspil.unikke_kort[f'{random.randint(1, 13)}']
        while kortspil.antal_mulige_kort[tilfældigt_kort] == 0:
            tilfældigt_kort = kortspil.unikke_kort[f'{random.randint(1, 13)}']
        return tilfældigt_kort

    def uddel_kort(self):
        for _ in range(int(self.antal_kort)):
            tilfældigt_kort = self.vælg_tilfældigt_kort()
            self.taget_kort[tilfældigt_kort] += 1
            kortspil.antal_mulige_kort[tilfældigt_kort] -= 1


def duel(list_spillere):
    checked_0 = []
    kort_0 = random.choice(list(list_spillere[0].taget_kort.keys()))
    while list_spillere[0].taget_kort[kort_0] == 0:
        #print(f'vælger nyt kort for {list_spillere[0].navn}')
        kort_0 = random.choice(list(list_spillere[0].taget_kort.keys()))
        if kort_0 not in checked_0:
            checked_0.append(kort_0)
        if len(checked_0) == 13:
            break
    list_spillere[0].taget_kort[kort_0] -= 1 # tag det valgte kort ud af bunken
    list_spillere[0].antal_kort -= 1 # tag det valgte kort ud af bunken

    checked_1 = []
    kort_1 = random.choice(list(list_spillere[1].taget_kort.keys()))
    while list_spillere[1].taget_kort[kort_1] == 0:
        #print(f'vælger nyt kort for {list_spillere[1].navn}')
        kort_1 = random.choice(list(list_spillere[1].taget_kort.keys()))
        if kort_1 not in checked_1:
            checked_1.append(kort_1)
        if len(checked_1) == 13:
            break
    list_spillere[1].taget_kort[kort_1] -= 1 # tag det valgte kort ud af bunken
    list_spillere[1].antal_kort -= 1 # tag det valgte kort ud af bunken

    if int(kort_0) > int(kort_1):
        list_spillere[0].taget_kort[kort_0] += 1
        list_spillere[0].taget_kort[kort_1] += 1
        list_spillere[0].antal_kort += 2
        print(f'{list_spillere[1].navn} har tabt et kort')
        print(f'{list_spillere[0].navn} har nu {list_spillere[0].antal_kort} kort')
        print(f'{list_spillere[1].navn} har nu {list_spillere[1].antal_kort} kort\n')
    elif int(kort_0) < int(kort_1):
        list_spillere[1].taget_kort[kort_0] += 1
        list_spillere[1].taget_kort[kort_1] += 1
        list_spillere[1].antal_kort += 2
        print(f'{list_spillere[0].navn} har tabt et kort')
        print(f'{list_spillere[0].navn} har nu {list_spillere[0].antal_kort} kort')
        print(f'{list_spillere[1].navn} har nu {list_spillere[1].antal_kort} kort\n')
    else:
        print('oh shit, krig!')
        krig(kort_0, kort_1, list_spillere)

    

def krig(kort_0, kort_1, list_spillere):
    if list_spillere[0].antal_kort >= 3 and list_spillere[1].antal_kort >= 3:
        antal_kort_krig = 3
    # else:
    #     antal_kort_krig = int(min([list_spillere[0].antal_kort, list_spillere[1].antal_kort]))
    elif list_spillere[0].antal_kort >= 1 and list_spillere[1].antal_kort >= 1:
        antal_kort_krig = int(min([list_spillere[0].antal_kort, list_spillere[1].antal_kort]))
    else:
        return

    kort_0_3 = [vælg_tilfældigt_kort(list_spillere[0]) for _ in range(antal_kort_krig)]
    kort_1_3 = [vælg_tilfældigt_kort(list_spillere[1]) for _ in range(antal_kort_krig)]
    
    for kort in kort_0_3:
        #list_spillere[0].taget_kort[kort] -= 1
        list_spillere[0].antal_kort -= 1
    for kort in kort_1_3:
        #list_spillere[1].taget_kort[kort] -= 1
        list_spillere[1].antal_kort -= 1

    point_0 = 0
    point_1 = 0
    if int(kort_0_3[0]) > int(kort_1_3[0]):
        point_0 += 1
    elif int(kort_0_3[0]) < int(kort_1_3[0]):
        point_1 += 1
    
    if int(min([list_spillere[0].antal_kort, list_spillere[1].antal_kort])) >= 2:
        if int(kort_0_3[1]) > int(kort_1_3[1]):
            point_0 += 1
        elif int(kort_0_3[1]) < int(kort_1_3[1]):
            point_1 += 1

        if int(min([list_spillere[0].antal_kort, list_spillere[1].antal_kort])) >= 3:
            if int(kort_0_3[2]) > int(kort_1_3[2]):
                point_0 += 1
            elif int(kort_0_3[2]) < int(kort_1_3[2]):
                point_1 += 1

    if point_0 > point_1:
        print(f'{list_spillere[0].navn} har vundet krig')
        for kort in kort_0_3:
            list_spillere[0].taget_kort[kort] += 1
        for kort in kort_1_3:
            list_spillere[0].taget_kort[kort] += 1
        list_spillere[0].antal_kort += 8
        #return list_spillere[0]
    elif point_0 < point_1:
        print(f'{list_spillere[1].navn} har vundet krig')
        for kort in kort_0_3:
            list_spillere[1].taget_kort[kort] += 1
        for kort in kort_1_3:
            list_spillere[1].taget_kort[kort] += 1
        list_spillere[1].antal_kort += 8
        #return list_spillere[1]
    else:
        tilfældig_spiller = random.choice(list(list_spillere))
        print(f'{tilfældig_spiller.navn} har vundet krig (tilfældigt)')
        for kort in kort_0_3:
            tilfældig_spiller.taget_kort[kort] += 1
        for kort in kort_1_3:
            tilfældig_spiller.taget_kort[kort] += 1
        tilfældig_spiller.antal_kort += 8
        #return random.choice(list(list_spillere))


def vælg_tilfældigt_kort(spiller):
    checked = []
    kort = random.choice(list(list_spillere[0].taget_kort.keys()))
    while spiller.taget_kort[kort] == 0:
        kort = random.choice(list(list_spillere[0].taget_kort.keys()))
        if kort not in checked:
            checked.append(kort)
        if len(checked) == 13:
            break
    spiller.taget_kort[kort] -= 1
    return kort

#Nikolaj = Spiller('Nikolaj', kortspil.antal_kort/2)
#Mikael = Spiller('Mikael', kortspil.antal_kort/2)

#uddel_kort([Nikolaj, Mikael])

# print('Nikolaj:')
# for kort in sorted(Nikolaj.taget_kort):
#     print(f'{kort}: {Nikolaj.taget_kort[kort]}, ', end='')
# print('\nMikael:')
# for kort in sorted(Mikael.taget_kort):
#     print(f'{kort}: {Mikael.taget_kort[kort]}, ', end='')
# print()

if __name__ == '__main__':
    antal_spillere = int(input('Hvor mange vil spille?\n> '))
    list_spillere = []
    for _ in range(antal_spillere):
        spiller_navn = input('Indtast navn: ')
        list_spillere.append(Spiller(spiller_navn, kortspil.antal_kort/antal_spillere))
    while list_spillere[0].antal_kort > 0 and list_spillere[1].antal_kort > 0:
        duel(list_spillere)
    print(f'antal kort for {list_spillere[0].navn}: {list_spillere[0].antal_kort}')
    print(f'antal kort for {list_spillere[1].navn}: {list_spillere[1].antal_kort}')

