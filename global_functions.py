import itertools
import math, sys
from tqdm import tqdm
import random

# filters
# QUANTIDADE TOTAL DE UM CERTO TAMANHO
def get_quantity(size, row_comb):
    qt = 0
    for comb in row_comb:
        for s in comb:
            if s == size:
                qt += 1
        
    return qt

# RÉGUAS DE SUPORTE POR BAIXO DOS ALINHAMENTOS
def get_fixed_beams_for_alignment(combination, length):
    beams = [0]
    for row in combination:
        position = 0
        for size in row:
            position += size
            if position >= length:
                position = length
            
            beams.append(position)
    raw_beams = list(sorted(set(beams)))
    beams = []
    index = None
    for i in range(len(raw_beams) - 1):
        if i != index:
            if abs(raw_beams[i] - raw_beams[i+1]) <= 100:
                #print(raw_beams[i-1] + ((raw_beams[i+1] - raw_beams[i]) // 2))
                beams.append(raw_beams[i] + ((raw_beams[i+1] - raw_beams[i]) // 2))
                beams.append(raw_beams[i] + ((raw_beams[i+1] - raw_beams[i]) // 2))
                index = i+1
            else:
                beams.append(raw_beams[i])
    if length not in beams:
        beams.append(length)
    return beams

def check_for_alignments(combinations, length, rows):
    max_alignments = (length*2)//5000
    combs = []
    print("Filtering for alignments...")
    for i in tqdm(range(len(combinations) - 1)):
        alignments = 0
        stop = False
        beams = sorted(get_fixed_beams_for_alignment(combinations[i], length))
        # SE HOUVER DUAS RÉGUAS COM A MESMA COMBINAÇÃO RETIRA
        for index in range(len(combinations[i]) - 1):
            r = []
            count1 = 0
            for size in combinations[i][index]:
                count1 += size
                r.append(count1)
            count2 = 0
            for j in range(len(combinations[i][index+1])):
                count2 += combinations[i][index+1][j]
                if count2 in r:
                    stop = True
                    break
        # SE HOUVER DUAS RÉGUAS CUJA SOMA DOS DOIS PRIMEIROS ELEMENTOS É IGUAL RETIRA
        for j in range(1, len(combinations[i])):
            if combinations[i][0][0] + combinations[i][0][1] == combinations[i][j][0] + combinations[i][j][1]:
                stop = True
                break
        # SE HOUVER DUAS RÉGUAS NA MESMA POSIÇÃO EM FILAS DIFERENTES RETIRA
        for j in range(len(combinations[i])-1):
            if combinations[i][j][0] == combinations[i][j+1][0]:
                stop = True
                break
        for j in range(len(combinations[i])-1):
            if combinations[i][j][0] + combinations[i][j][1] == combinations[i][j+1][0] + combinations[i][j+1][1]:
                stop = True
                break
        # SE HOUVER DOIS ALINHAMENTOS A UMA DISTANCIA MENOR QUE 150 RETIRA
        for h in range(len(beams)-1):
            if beams[h+1] - beams[h] < 150:
                stop = True
                break
        # ADICIONA
        if not stop:
            for k in range(len(beams) - 1):
                if beams[k] != 5000:
                    if beams[k] == beams[k+1]:
                        alignments += 1
            # SE HOUVER UM NÚMERO DE ALINHAMENTOS MAIOR QUE O SUPOSTO RETIRA
            if alignments <= max_alignments:
                combs.append(combinations[i])

    combs = check_first_last(combs, rows)

    return combs

def check_first_last(combinations, rows, for_multiple_combinations=True):
    if for_multiple_combinations:
        new_comb = []
        for c in combinations:
            possible_combs = itertools.permutations(c, rows)
            for comb in possible_combs:
                count = [[0 for _ in range(len(comb[i]))] for i in range(len(comb))]
                for index, c in enumerate(comb):
                    for j in range(1, len(comb[index])):
                        if sum(c[:j]) < 5000:
                            count[index][j] = sum(c[:j])
                to_add = True
                for k in range(len(count[0])):
                    if k < len(count[-1]):
                        if count[0][k] != 0:
                            if count[0][k] == count[-1][k]:
                                to_add = False
                
                if to_add:
                    new_comb.append(comb)
                    break
        
        return new_comb
    else:
        count = [[0 for _ in range(len(combinations[i]))] for i in range(len(combinations))]
        for index, c in enumerate(combinations):
            for j in range(1, len(combinations[index])):
                if sum(c[:j]) < 5000:
                    count[index][j] = sum(c[:j])
        for k in range(len(count[0])):
            if k < len(count[-1]):
                if count[0][k] != 0:
                    if count[0][k] == count[-1][k]:
                        return False
        
        return True

def get_sum(comb):
    total = 0
    for row in comb:
        total += sum(row)
    
    return total

def fixed_beams(combination, length):
    beams = [0]
    for row in combination:
        position = 0
        for size in row:
            position += size
            if position >= length:
                position = length
            
            beams.append(position)
    raw_beams = list(sorted(set(beams)))
    beams = []
    index = None
    for i in range(len(raw_beams) - 1):
        if i != index:
            if abs(raw_beams[i] - raw_beams[i+1]) <= 40:
                #print(raw_beams[i-1] + ((raw_beams[i+1] - raw_beams[i]) // 2))
                beams.append(raw_beams[i] + ((raw_beams[i+1] - raw_beams[i]) // 2))
                index = i+1
            else:
                beams.append(raw_beams[i])
    if length not in beams:
        beams.append(length)
    return beams

def get_used_beams(combination, intervals, length):
    additional_beams = []
    raw_beams = fixed_beams(combination, length)
    
    for i in range(len(raw_beams) - 1):
        diff = raw_beams[i+1] - raw_beams[i]
        if diff > intervals:
            number_spaces_beams = math.ceil(diff/625)
            space_between_beams = math.ceil(diff/number_spaces_beams)
            for j in range(number_spaces_beams):
                additional_beams.append(raw_beams[i] + space_between_beams*j)
    beams = raw_beams + additional_beams
    beams = list(sorted(set(beams)))
    return beams

def check_alignments_for_less_beams(combination, intervals, length, rows):
    # ADAPTAR O "VERIFICAR ALINHAMENTOS" DE CIMA AQUI
    max_alignments = (length*2)//5000
    beams = get_used_beams(combination, intervals, length)
    fixed_beams_for_alignment = sorted(get_fixed_beams_for_alignment(combination, length))
    # SE HOUVER DUAS TÁBUAS IGUAIS SEGUIDAS
    for i in range(len(combination)-1):
        if combination[i][0] == combination[i+1][0]:
            return False
    # SE HOUVER DUAS VIGAS A MENOS DE 150MM
    for i in range(len(beams)-1):
        if beams[i+1] - beams[i] < 150:
            return False
    
    # SE HOUVER MAIS DE DOIS ALINHAMENTOS IGUAIS
    alignments = 0
    for i in range(len(fixed_beams_for_alignment)-1):
        if fixed_beams_for_alignment[i] == fixed_beams_for_alignment[i+1]:
            return False
    
    if not check_first_last(combination, rows, for_multiple_combinations=False):
        return False
    
    for index in range(len(combination) - 1):
        r = []
        count1 = 0
        for size in combination[index]:
            count1 += size
            r.append(count1)
        count2 = 0
        for j in range(len(combination[index+1])):
            count2 += combination[index+1][j]
            if count2 in r:
                return False

    return True

def get_less_beams(comb, intervals, length, rows):
    less_beams_comb = comb
    less_beams = len(get_used_beams(comb, intervals, length))
    n = 10000

    # RANDOM PORQUE CHEGA A UM PONTO EM QUE ESTAGNA NUM NÚMERO
    # NÚMERO DE ITERAÇÕES RECOMENDADO É DE 10000
    print("Getting combination with less support beams...")
    for _ in tqdm(range(n)):
        new_rows = [None for _ in range(len(comb))]
        used = []
        while len(used) < len(comb):
            for index, row in enumerate(comb):
                if new_rows[index] == None:
                    n_row = random.sample(list(row), len(row))
                    shuffled = sorted(n_row, key=lambda k: random.random())
                    if shuffled not in used:
                        new_rows[index] = tuple(shuffled)
                        used.append(shuffled)
        
        if check_alignments_for_less_beams(new_rows, intervals, length, rows):
            beams = len(get_used_beams(new_rows, intervals, length))
            if less_beams > beams:
                less_beams = beams
                less_beams_comb = new_rows


    return less_beams, less_beams_comb

