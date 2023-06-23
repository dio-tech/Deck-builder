import pygame, sys
pygame.font.init()

class Graphics:
    def __init__(self, rows, length, width, n_sets):
        self.n_sets = n_sets
        self.deck_width = width
        self.start_pos_x = 50
        self.start_pos_y = 70
        self.line_offset = 10
        self.rows = rows
        self.length = length
        self.width = self.start_pos_x + self.length//10 + 430
        self.height = self.start_pos_y + self.rows*self.start_pos_y + 50
        self.win = pygame.display.set_mode((self.width, self.height))
    
    def get_quantity(self, size, row_comb):
        qt = 0
        for comb in row_comb:
            for s in comb:
                if s == size:
                    qt += 1
        
        return qt

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

    def beams(self, combination):
        for index, comb in enumerate(combination):
            start_pos_x = 50
            for size in comb:
                self.draw_beam(size, index+1, start_pos_x)
                start_pos_x = start_pos_x + size//10

    def draw_final(self, length):
        pygame.draw.line(self.win, (0, 0, 255), (self.start_pos_x + length//10, 30), (self.start_pos_x + length//10, self.start_pos_y * self.rows + 40), 5)

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

    def info(self, beams_comb, combinations, waste, sizes):

        font = pygame.font.SysFont('arial', 30)
        text = ["Quantidades: "]

        for size in sizes:
            text.append(f"{size}: {self.get_total_beams(self.get_quantity(size, combinations))} un.")
                        
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
        
        waste_txt = f"Desperdício: {waste}"
        waste_text = font.render(waste_txt, True, (255, 255, 255))
        textRect1 = waste_text.get_rect()
        textRect1.center = (self.start_pos_x + self.length//10 + 210, y+20)

        self.win.blit(waste_text, textRect1)

        beams_txt = f"Suporte: {str(len(beams_comb))} varas"
        beams_text = font.render(beams_txt, True, (255, 255, 255))
        textRect2 = beams_text.get_rect()
        textRect2.center = (self.start_pos_x + self.length//10 + 210, y+70)

        self.win.blit(beams_text, textRect2)

        space_txt = f"Espaçamento máximo: 625"
        space_text = font.render(space_txt, True, (255, 255, 255))
        textRect3 = space_text.get_rect()
        textRect3.center = (self.start_pos_x + self.length//10 + 210, y+120)

        self.win.blit(space_text, textRect3)

    def redraw_window(self, beams_comb, comb, waste, index, sizes):
        self.win.fill((0, 0, 0))
        self.draw_support_beams(beams_comb[index])
        self.beams(comb[index])
        self.draw_final(self.length)
        self.ranking(index)
        self.info(beams_comb[index], comb[index], waste[index], sizes)

    def run(self, beams_comb, comb, waste, sizes):
        index = 0
        while True:
            self.redraw_window(beams_comb, comb, waste, index, sizes)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]:
                        index += 1

                        if index > 4:
                            index = 0
            
            pygame.display.update()
