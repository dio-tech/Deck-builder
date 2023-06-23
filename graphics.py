from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import numpy as np
from global_functions import *
pygame.font.init()
pygame.init()

class Graphics:
    def __init__(self, rows, length, width, n_sets, spacing):
        self.spacing = spacing
        self.n_sets = n_sets
        self.deck_width = width
        self.start_pos_x = 50
        self.start_pos_y = 70
        self.line_offset = 10
        self.rows = rows
        self.length = length
        self.width = self.start_pos_x + self.length//10 + 430
        self.height = self.start_pos_y + self.rows*self.start_pos_y + 50
        if self.height < 470:
            self.height = 470
        self.win = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.fixed_width = self.width

    def get_squared_waste(self, waste):
        return np.round((waste/1000) * (self.spacing/1000), decimals=2)

    def get_total_beams(self, beams):
        return self.n_sets * beams

    def draw_support_beams(self, combination):
        for index, pos in enumerate(combination):
            pygame.draw.line(self.win, (255, 0, 0), (self.start_pos_x + pos//10, 30), (self.start_pos_x + pos//10, self.start_pos_y * self.rows + 80), 5)

            try: 
                diff = (combination[index+1] - combination[index]) // 10
                font = pygame.font.SysFont('arial', 17)
                text = font.render(str(diff*10), True, (0, 255, 0))
                textRect = text.get_rect()
                textRect.center = (self.start_pos_x + pos//10 + (diff//2), self.start_pos_y * self.rows + 80)

                self.win.blit(text, textRect)
            except:
                pass
        
        font = pygame.font.SysFont('arial', 20)
        text = font.render("Posição das réguas: " + str(combination), True, (255, 255, 255))
        self.win.blit(text, (self.start_pos_x, self.start_pos_y * self.rows + 150))

    def beams(self, combination):
        for index, comb in enumerate(combination):
            start_pos_x = 50
            for size in comb:
                self.draw_beam(size, index+1, start_pos_x)
                start_pos_x = start_pos_x + size//10

    def draw_final(self, length):
        pygame.draw.line(self.win, (0, 0, 255), (self.start_pos_x + length//10, 30), (self.start_pos_x + length//10, self.start_pos_y * self.rows + 40), 5)

    def get_percentage(self, combinations, size1, sizes):
        total = 0
        for size in sizes:
            total += self.get_total_beams(get_quantity(size, combinations))
        for size in sizes:
            if size1 == size:
                return np.round((self.get_total_beams(get_quantity(size1, combinations))/total) * 100, decimals=2)

    def draw_beam(self, size, row, start):
        pygame.draw.line(self.win, (255, 255, 255), (start, row*self.start_pos_y), (start + size//10, row*self.start_pos_y), 3)
        pygame.draw.line(self.win, (255, 255, 255), (start, row*self.start_pos_y - self.line_offset), (start, row*self.start_pos_y + self.line_offset), 3)
        pygame.draw.line(self.win, (255, 255, 255), (start + size//10, row*self.start_pos_y - self.line_offset), (start + size//10, row*self.start_pos_y + self.line_offset), 3)

        font = pygame.font.SysFont('arial', 22)
        text = font.render(str(size), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (start + (size//20), row*self.start_pos_y + 20)

        self.win.blit(text, textRect)

    def ranking(self, index):
        font = pygame.font.SysFont('arial', 40)
        text = font.render("#" + str(index+1), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (self.width - 40, self.height - 40)

        self.win.blit(text, textRect)

    def info(self, beams_comb, combinations, waste, sizes, max_spacing):

        font = pygame.font.SysFont('arial', 30)
        text = ["Quantidades: "]

        for size in sizes:
            text.append(f"{size}: {self.get_total_beams(get_quantity(size, combinations))} un. ({self.get_percentage(combinations, size, sizes)}%)")
                        
        y = 50
        for index, txt in enumerate(text):
            if index == 0:
                text = font.render(txt, True, (255, 255, 255))
                textRect = text.get_rect()
                textRect.center = (self.start_pos_x + self.length//10 + 200, y)
            else:
                text = font.render(txt, False, (255, 255, 255))
                textRect = text.get_rect()
                textRect.center = (self.start_pos_x + self.length//10 + 200, y)
            
            y += 27

            self.win.blit(text, textRect)
        
        waste_txt = f"Desperdício linear: {waste}"
        waste_text = font.render(waste_txt, True, (255, 255, 255))
        textRect1 = waste_text.get_rect()
        textRect1.center = (self.start_pos_x + self.length//10 + 210, y+20)
        self.win.blit(waste_text, textRect1)

        waste_txt = f"Desperdício (m2): {self.get_squared_waste(waste)}"
        waste_text = font.render(waste_txt, True, (255, 255, 255))
        textRect1 = waste_text.get_rect()
        textRect1.center = (self.start_pos_x + self.length//10 + 210, y+45)

        self.win.blit(waste_text, textRect1)

        beams_txt = f"Suporte: {str(len(beams_comb))} réguas"
        beams_text = font.render(beams_txt, True, (255, 255, 255))
        textRect2 = beams_text.get_rect()
        textRect2.center = (self.start_pos_x + self.length//10 + 210, y+80)

        self.win.blit(beams_text, textRect2)

        space_txt = f"Espaçamento máximo: {max_spacing}"
        space_text = font.render(space_txt, True, (255, 255, 255))
        textRect3 = space_text.get_rect()
        textRect3.center = (self.start_pos_x + self.length//10 + 210, y+120)

        self.win.blit(space_text, textRect3)

    def redraw_window(self, beams_comb, comb, waste, index, sizes, max_spacing):
        self.win.fill((0, 0, 0))
        self.draw_support_beams(beams_comb[index])
        self.beams(comb[index])
        self.draw_final(self.length)
        self.ranking(index)
        self.info(beams_comb[index], comb[index], waste[index], sizes, max_spacing)

    def run(self, beams_comb, comb, waste, sizes, max_spacing):
        index = 0
        pygame.font.init()
        pygame.init()
        while self.running:
            self.redraw_window(beams_comb, comb, waste, index, sizes, max_spacing)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.display.quit()
                    pygame.quit()
                
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_RIGHT]:
                        index += 1

                        if index > (len(comb[:5]) - 1):
                            index = 0
                    if keys[pygame.K_LEFT]:
                        index -= 1

                        if index < 0:
                            index = len(comb[:5]) - 1
            if self.running:
                pygame.display.update()
