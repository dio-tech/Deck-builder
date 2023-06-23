from main import *
import numpy as np


class Deck:
    def __init__(self):
        self.n_sizes = None
        self.sizes = []
        self.length = None
        self.width = None
        self.error = "\nSelecionar um número válido!"
        self.stock = None
        self.pretended_comb = None
        self.num_combs = None
        self.beam_position = None
        self.pos = []
        self.num_rows = None
        self.spacing = None
    
    def n_get_sizes(self):
        while type(self.n_sizes) != int and len(self.sizes) == 0:
            print("Quantos tamanhos diferentes existem?")
            try:
                self.n_sizes = int(input(":"))
            except:
                print(self.error)
    
    def get_spacing(self):
        while type(self.spacing) != int:
            try:
                print("\nQual o espaçamento máximo entre réguas?")
                response = input(":")
                self.spacing = int(response)
            except:
                print(self.error)

    def get_rows(self):
        while type(self.num_rows) != int:
            try:
                print("\nQual o número de filas pretendidas? (Clicar Enter para ignorar parâmetro)")
                print("(Predefinição: 4) Quanto maior o número maior o número de réguas")
                response = input(":")
                try:
                    self.num_rows = int(response.replace(' ', ''))
                except:
                    self.num_rows = 4
            except:
                print(self.error)

    def get_beam_position(self):
        while type(self.beam_position) != int:
            print("\nQuer definir as posições da primeira, segunda e penúltima régua?")
            print("1 - SIM\n2 - NÃO")
            try:
                beam_pos = int(input(":"))
                if beam_pos == 1 or beam_pos == 2:
                    self.beam_position = beam_pos
                else:
                    print("Escolher entre 1 e 2!")
            except:
                print(self.error)
        if self.beam_position == 1:
            self.beam_pos()
    
    def beam_pos(self):
        pos_s = ['primeira', 'segunda', 'penúltima']
        index = 0
        while len(self.pos) < len(pos_s):
            p = input(f"Posição da {pos_s[index]} viga: ")

            try:
                self.pos.append(int(p))
            except:
                print(self.error)

            index += 1
            if index > len(pos_s) - 1:
                index = 0
        self.pos = sorted(self.pos)

    def get_pretended_comb(self):
        while type(self.pretended_comb) != int:
            try:
                print("\nQual o número de pré combinações desejado? (Clicar Enter para ignorar parâmetro)")
                print("(Predefinição: 50) >50 menos precisão; <50 possibilidade de não encontrar soluções")
                response = input(":")
                try:
                    self.pretended_comb = int(response.replace(' ', ''))
                except:
                    self.pretended_comb = 50
            except:
                print(self.error)
    
    def get_pretended_num_comb(self):
        while type(self.num_combs) != int and self.num_combs != 50:
            try:
                print("\nQual o número de combinações de réguas? (Clicar Enter para ignorar parâmetro)")
                print("(Predefinição: 70) >70 - mais preciso e mais lento")
                response = input(":")
                try:
                    if int(response.replace(' ', '')) > 100:
                        print("Máximo de combinações é 100")
                        #self.num_combs = 100
                    else:
                        self.num_combs = int(response.replace(' ', ''))
                except:
                    self.num_combs = 70
            except:
                print(self.error)

    def get_different_sizes(self):
        while len(self.sizes) != self.n_sizes:
            size = int(input("Tamanho: "))
            try:
                self.sizes.append(int(size))
            except:
                print(self.error)
        
        self.sizes = sorted(self.sizes)
        self.quantities = self.percentages = [0 for _ in range(len(self.sizes))]
        self.quantity_chosen = [False for _ in range(len(self.sizes))]
    
    def get_deck_length(self):
        while type(self.length) != int:
            try:
                print("\nQual o comprimento do deck?")
                self.length = int(input(":"))
            except:
                print(self.error)
    
    def get_deck_width(self):
        while type(self.width) != int:
            try:
                print("\nQual a largura do deck?")
                self.width = int(input(": "))
            except:
                print(self.error)
    
    def run_without_stock(self):
        main(self.sizes, self.length, self.width, self.pretended_comb, self.num_combs, self.pos, self.num_rows, self.spacing)
    
    def run_with_stock(self):
        while False in self.quantity_chosen:
            for index, size in enumerate(self.sizes):
                if not self.quantity_chosen[index]:
                    qt = input(f"Quantidade de {size}: ")
                    try:
                        qt = int(qt)
                        self.quantity_chosen[index] = True
                        self.quantities[index] = qt
                    except:
                        print(self.error)
        p = self.get_percentages_stock()
        lst = np.array(p)
        percentages = np.around(lst, decimals=2)
        self.get_pretended_comb()
        self.get_pretended_num_comb()
        main(sorted(self.sizes), self.length, self.width, self.pretended_comb, self.num_combs, self.pos, self.num_rows, self.spacing, percentages=percentages)
    
    def get_percentages_stock(self):
        p = []
        for qt in self.quantities:
            percentage = qt/sum(sorted(self.quantities))
            p.append(percentage)
        return p
    
    def get_stock(self):
        while type(self.stock) != int:
            print("\nO stock é importante?")
            print("1 - SIM\n2 - NÃO")
            try:
                stock = int(input(":"))
                if stock == 1 or stock == 2:
                    self.stock = stock
                else:
                    print("Escolher entre 1 e 2!")
            except:
                print(self.error)
    
    def questions(self):
        self.n_get_sizes()
        self.get_different_sizes()
        self.get_deck_length()
        self.get_deck_width()
        self.get_rows()
        self.get_spacing()
        self.get_beam_position()
        self.get_stock()
        print('')
    
    def run(self):
        while True:
            sizes = self.sizes
            n_sizes = self.n_sizes
            self.__init__()
            self.n_sizes = n_sizes
            self.sizes = sizes
            self.questions()
            if int(self.stock) == 1:
                self.run_with_stock()
            else:
                self.run_without_stock()

deck = Deck()
deck.run()
