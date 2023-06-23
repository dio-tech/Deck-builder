from tqdm import tqdm
import math
from global_functions import *
from combinations import get_combinations, get_percentage_combinations
from graphics import Graphics

'''sizes = [940, 1240, 1550, 1820, 2150]
length = 5000'''

def main(sizes, length, width, pretended_combs, first_elements, beam_defined_pos, _rows, intervals, percentages=[]):
    def fixed_beams(combination):
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

        print(beams)
        return beams

    def get_used_beams(combination):
        additional_beams = []
        raw_beams = fixed_beams(combination)
        if len(beam_defined_pos) == 3:
            raw_beams.append(beam_defined_pos[0])
            raw_beams.append(beam_defined_pos[1])
            raw_beams.append(beam_defined_pos[2])

        raw_beams = sorted(raw_beams)
        
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

    def get_waste(combination):
        waste_additional_wood = 0
        for row in combination:
            waste_additional_wood += (sum(row) - length)

        return waste_additional_wood

    def total_waste(waste):
        return n_sets * waste

    if len(percentages) == 0:
        row_combs = get_combinations(sizes, length, _rows)
    else:
        row_combs = get_percentage_combinations(percentages, sizes, length, _rows, pretended_combs, first_elements)

    # replacing last beam
    final_comb = []
    print("Replacing...")
    for combination in tqdm(list(row_combs)):
        combinations = []
        for row in list(combination):
            last = row[-1]
            index_size_last = sizes.index(last)
            subtract = index_size_last
            new_row = list(row)
            # PEGA NO TAMANHO IMEDIATAMENTE ANTES E VERIFICA SE A SUA UTILIZAÇÃO NA ÚLTIMA RÉGUA PERMITE CHEGAR AO COMPRIMENTO DO DECK
            if index_size_last != 0:
                new_row[-1] = 0
                while sum(new_row) < length:
                    new_index = index_size_last - subtract
                    new_row[-1] = sizes[new_index]
                    subtract -= 1
                if new_row[-1] == 0:
                    new_row = list(row)
            combinations.append(tuple(new_row))
        if len(combinations) == len(set(combinations)):
            final_comb.append(combinations)
    
    row_combs = final_comb

    new_comb = check_for_alignments(row_combs, length, _rows)

    final = tuple(map(tuple, new_comb))
    final_comb = list(sorted(set(final), key=get_waste))

    combinations = []
    beams_combinations = []
    waste = []

    beam_width = 95
    spacing = 5

    n_sets = width // ((beam_width+spacing) * _rows)

    print(f"Existem no total {len(final_comb)} combinações!")

    if len(final_comb) > 0:
                
        print('----------------------------------------------------------------------------------------------------------------')
        for combination in final_comb[:5]:
            # GETS THE COMBINATION WITH LESS BEAMS
            num_beams, comb = get_less_beams(combination, intervals, length, _rows)
            beams = get_used_beams(comb)
            beams_combinations.append(beams)
            combinations.append(comb)
            wood_waste = total_waste(get_waste(comb))
            waste.append(wood_waste)
            print("Combination: " + str(comb))
            print("Used beams: " + str(num_beams))
            print("Used beams position: " + str(beams))
            print("Waste: " + str(wood_waste))
            print('----------------------------------------------------------------------------------------------------------------')

        graphics = Graphics(_rows, length, width, n_sets, (beam_width+spacing))
        graphics.run(beams_combinations, combinations, waste, sizes, intervals)
    else:
        if _rows - 1 == 1:
            print("Não foram encontradas soluções!\nAumentar número de combinações de filas!")
        else:
            print(f"Não foram encontradas soluções para {_rows} filas!\nA tentar com {_rows - 1} filas!")
            main(sizes, length, width, pretended_combs, first_elements, beam_defined_pos, _rows - 1, intervals, percentages)

#main(sizes, length, 4500)

