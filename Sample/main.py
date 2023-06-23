import itertools
from tqdm import tqdm
import math
import sys
from graphics import Graphics
import collections

sizes = [940, 1240, 1550, 1820, 2150]
length = 5000
intervals = 625

def main(sizes, length, width):

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

        return raw_beams

    def get_used_beams(combination):
        additional_beams = []
        raw_beams = fixed_beams(combination)
        
        for i in range(len(raw_beams) - 1):
            diff = raw_beams[i+1] - raw_beams[i]
            if diff > 625:
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

    def remove_repeated(combs):
        for index, comb in enumerate(combs):
            combs[index] = tuple(sorted(comb))
        
        possible_comb = list(set(combs))
        
        return possible_comb

    _rows = 4

    _POSSIBLE_COMB = list(itertools.permutations(sizes, math.ceil(length/(sum(sizes)/len(sizes)))))
    _POSSIBLE_COMBS = list(itertools.permutations(sizes, length//(sum(sizes)//len(sizes))))

    combs = []
    for comb in _POSSIBLE_COMBS:
        if sum(comb) >= length:
            _POSSIBLE_COMB.append(comb)
    for combination in _POSSIBLE_COMB:
        if sum(combination) >= length:
            combs.append(combination)
    
    possible_comb = remove_repeated(combs)

    combs = sorted([c for c in possible_comb], key=sum)
    row_combs = list(itertools.permutations(combs, _rows))

    print("Filtering for grooves...")
    new_comb = []
    for combination in tqdm(row_combs):
        stop = False
        for i in range(len(combination) - 1):
            if combination[i][0] == combination[i + 1][0]:
                stop = True
                break
        if not stop:
            new_comb.append(tuple(combination))
    
    _comb = []
    new_comb = list(sorted(new_comb, key=get_waste))
    for i in range(len(new_comb)-1):
        if collections.Counter(new_comb[i]) != collections.Counter(new_comb[i+1]):
            _comb.append(new_comb[i])

    new_comb = []
    for comb in _comb:
        rows = [0 for _ in comb]
        for index, row in enumerate(comb):
            if rows[0] != 0:
                if rows[0][0] == row[0] and rows[0][1] == row[1]:
                    pass
                else:
                    rows[index] = row
            else:
                rows[index] = row
        if not 0 in rows:
            new_comb.append(rows)

    # replacing last beam
    final_comb = []
    for combination in list(new_comb):
        combinations = []
        for index, row in enumerate(list(combination)):
            last = row[-1]
            index_size_last = sizes.index(last)
            subtract = index_size_last
            new_row = list(row)
            new_row[-1] = 0
            #print(index_size_last)
            if index_size_last != 0:
                while sum(new_row) < length:
                    new_index = index_size_last - subtract
                    new_row[-1] = sizes[new_index]
                    subtract -= 1
            combinations.append(tuple(new_row))
        final_comb.append(combinations)
    
    #final_comb = new_comb

    final = tuple(map(tuple, final_comb))
    final_comb = list(sorted(set(final), key=get_waste))

    combinations = []
    beams_combinations = []
    waste = []

    beam_width = 95
    spacing = 5

    print(len(final_comb))
    n_sets = width // ((beam_width+spacing) * _rows)
                
    print('----------------------------------------------------------------------------------------------------------------')
    for combination in final_comb[:5]:
        beams = get_used_beams(combination)
        beams_combinations.append(beams)
        combinations.append(combination)
        wood_waste = total_waste(get_waste(combination))
        waste.append(wood_waste)
        print("Combination: " + str(combination))
        print("Used beams: " + str(len(beams)))
        print("Used beams position: " + str(beams))
        print("Waste: " + str(wood_waste))
        print('----------------------------------------------------------------------------------------------------------------')

    graphics = Graphics(_rows, length, width, n_sets)
    graphics.run(beams_combinations, combinations, waste, sizes)

main(sizes, length, 4500)

