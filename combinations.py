import itertools
import math
import numpy as np
from tqdm import tqdm
from global_functions import *

def get_percentage_combinations(percentage, sizes, length, rows, pretended_combs, first_elements):
    combs = []
    # ADICIONA À LISTA TODAS AS COMBINAÇÕES CUJO TAMANHO SEJA IGUAL AO SUPERIOR AO COMPRIMENTO DO DECK SENDO O DESPERDÍCIO MENOR QUE 10% DO COMPRIMENTO
    for i in range(math.ceil(length/sizes[-1]), math.ceil(length/(sizes[0]) + 1)):
        lst = list(itertools.combinations_with_replacement(sizes, i))
        for combination in lst:
            if sum(combination) >= length:
                combs.append(tuple(sorted(combination)))

    # ITERA ENTRE OS PRIMEIROS N ELEMENTOS
    row_combs = list(itertools.combinations(combs[:first_elements], rows))
    final_comb = []

    value_to_add = 0

    print("Filtering acording to percentages...")
    # VÊ SE AS PERCENTAGES DA COMBINAÇÃO CORRESPONDE AO PRETENDIDO
    # SE NÃO HOUVER COMBINAÇÕES SUFICIENTES AUMENTA A MARGEM DE ERRO
    first = True
    while len(final_comb) < pretended_combs:
        if not first:
            print(f"Increasing margin to {np.round(sorted(percentage)[0] + value_to_add, decimals=2) * 100}%")
        f_comb = []
        for row_comb in tqdm(row_combs):
            total_length = 0
            deck_percentage = []
            for_comb = True
            for row in row_comb:
                for _ in row:
                    total_length += 1
            for size in sizes:
                qt = get_quantity(size, row_comb)
                percent = np.round(np.array(qt / total_length), decimals=2)
                deck_percentage.append(percent)
            for i in range(len(deck_percentage)):
                if abs(deck_percentage[i] - percentage[i]) >= sorted(percentage)[0] + value_to_add:
                    for_comb = False
                    break
            if for_comb:
                f_comb.append(row_comb)

        if len(f_comb) >= pretended_combs:
            final_comb = f_comb
        value_to_add += 0.01
        first = False
    
    # alignement
    # PARA AUMENTAR AS COMBINAÇÕES:
    # SEMPRE QUE TEM ALINHAMENTOS A COINCIDIR TROCA A TÁBUA INICIAL PELA PENÚLTIMA
    f = final_comb
    f = []
    for comb in final_comb:
        row = []
        for i in range(len(comb) - 1):
            if i == 0:
                row.append(comb[i])
            if comb[i][0] == comb[i+1][0]:
                r = [comb[i+1][j] for j in range(len(comb[i+1]))]
                last = r[-2]
                r[-2] = r[0]
                r[0] = last
                row.append(tuple(r))
            else:
                row.append(comb[i+1])
        f.append(row)
    return f

def get_combinations(sizes, length, rows):
    combs = []
    # ADICIONA À LISTA TODAS AS COMBINAÇÕES CUJO TAMANHO SEJA IGUAL AO SUPERIOR AO COMPRIMENTO DO DECK SENDO O DESPERDÍCIO MENOR QUE 10% DO COMPRIMENTO
    for i in range(math.ceil(length/sizes[-1]), math.ceil(length/(sizes[0]) + 1)):
        lst = list(itertools.combinations_with_replacement(sizes, i))
        for combination in lst:
            if sum(combination) >= length:
                if sum(combination[:len(combination) - 1]) >= length:
                    combs.append(tuple(sorted(combination[:len(combination) - 1])))
                else:
                    combs.append(tuple(sorted(combination)))
    
    # PEGA NAS PRIMEIRAS 70 COMBINAÇÕES DE FILAS E ITERA ENTRE TODAS
    combs = list(itertools.combinations(combs[:70], rows))

    # ORDENA CONSOANTE O DESPERDÍCIO
    combs = sorted(combs, key=get_sum)

    return combs

#get_percentage_combinations([0.4, 0.3, 0.13, 0.1, 0.08], [940, 1240, 1550, 1820, 2150], 5000, 4, 50, 50)
#get_combinations([940, 1240, 1550, 1820, 2150], 5000, 4)