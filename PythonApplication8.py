import pygame
import random
import time

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (50, 150, 255)
YELLOW = (255, 220, 0)
RED = (255, 50, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Подземный Бур")
font_small = pygame.font.SysFont("Arial", 20)
font_big = pygame.font.SysFont("Arial", 36)

class Drill:
    def __init__(self, x, y):
        self.size = 30
        self.x = x
        self.y = y
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_UP] and self.y > 50:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.size:
            self.y += self.speed
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.size:
            self.x += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, self.size, self.size))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)


class Crystal:
    def __init__(self):
        self.radius = 8
        self.x = random.randint(20, WIDTH - 20)
        self.y = random.randint(80, HEIGHT - 20)

    def draw(self, surface):
        pygame.draw.circle(surface, YELLOW, (self.x, self.y), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)


class GameApp:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.current_tab = 1  
        self.crystal_count = 5 
        self.game_started = False
        self.drill = None
        self.crystals = []
        self.score = 0
        self.start_time = 0
        self.total_time = 0
        self.game_over = False

    def check_buttons(self, pos):
        if pygame.Rect(10, 10, 120, 30).collidepoint(pos):
            self.current_tab = 1
        if pygame.Rect(140, 10, 120, 30).collidepoint(pos):
            self.current_tab = 2

        if self.current_tab == 1:
            if pygame.Rect(260, 100, 30, 30).collidepoint(pos):
                if self.crystal_count < 15:
                    self.crystal_count += 1
            if pygame.Rect(120, 100, 30, 30).collidepoint(pos):
                if self.crystal_count > 5:
                    self.crystal_count -= 1
            if pygame.Rect(120, 160, 200, 40).collidepoint(pos):
                self.generate_mine()

    def generate_mine(self):
        self.drill = Drill(WIDTH // 2, HEIGHT // 2)
        self.crystals = [Crystal() for _ in range(self.crystal_count)]
        self.score = 0
        self.start_time = time.time()
        self.game_started = True
        self.game_over = False
        self.current_tab = 2 

    def update_game(self):
        if not self.game_started or self.game_over:
            return

        keys = pygame.key.get_pressed()
        self.drill.move(keys)

        drill_rect = self.drill.get_rect()
        for crystal in self.crystals[:]:
            if drill_rect.colliderect(crystal.get_rect()):
                self.crystals.remove(crystal)
                self.score += 1

        if len(self.crystals) == 0:
            self.game_over = True
            self.total_time = round(time.time() - self.start_time, 2)
            self.save_result_to_file()

    def save_result_to_file(self):
        with open("game_results.txt", "a", encoding="utf-8") as file:
            file.write(f"Собрано кристаллов: {self.crystal_count}, Время: {self.total_time} сек.\n")

    def draw_interface(self):
        screen.fill(BLACK)

        tab1_color = BLUE if self.current_tab == 1 else DARK_GRAY
        tab2_color = BLUE if self.current_tab == 2 else DARK_GRAY
        
        pygame.draw.rect(screen, tab1_color, (10, 10, 120, 30))
        pygame.draw.rect(screen, tab2_color, (140, 10, 120, 30))
        
        screen.blit(font_small.render("Настройки", True, WHITE), (25, 15))
        screen.blit(font_small.render("Шахта (Игра)", True, WHITE), (150, 15))

        pygame.draw.line(screen, WHITE, (0, 50), (WIDTH, 50), 2)

        if self.current_tab == 1:
            screen.blit(font_small.render("Количество кристаллов:", True, WHITE), (120, 75))
            
            pygame.draw.rect(screen, DARK_GRAY, (120, 100, 30, 30)) 
            pygame.draw.rect(screen, WHITE, (160, 100, 90, 30))     
            pygame.draw.rect(screen, DARK_GRAY, (260, 100, 30, 30)) 
            
            screen.blit(font_small.render("-", True, WHITE), (131, 102))
            screen.blit(font_small.render(str(self.crystal_count), True, BLACK), (200, 102))
            screen.blit(font_small.render("+", True, WHITE), (270, 102))

            pygame.draw.rect(screen, BLUE, (120, 160, 200, 40))
            screen.blit(font_small.render("Генерировать шахту", True, WHITE), (135, 168))

        elif self.current_tab == 2:
            if self.game_started:
                for crystal in self.crystals:
                    crystal.draw(screen)
                self.drill.draw(screen)

                score_text = font_small.render(f"Собрано: {self.score} / {self.crystal_count}", True, WHITE)
                screen.blit(score_text, (WIDTH - 180, 15))

                if self.game_over:
                    win_text = font_big.render("Уровень пройден!", True, YELLOW)
                    time_text = font_small.render(f"Время сохранения: {self.total_time} сек.", True, WHITE)
                    screen.blit(win_text, (WIDTH // 2 - 130, HEIGHT // 2 - 50))
                    screen.blit(time_text, (WIDTH // 2 - 110, HEIGHT // 2 + 10))
            else:
                no_game_text = font_small.render("Шахта не создана. Перейдите во вкладку 'Настройки' и нажмите 'Генерировать шахту'", True, GRAY)
                screen.blit(no_game_text, (80, HEIGHT // 2))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.check_buttons(event.pos)

            self.update_game()
            self.draw_interface()

        pygame.quit()

if __name__ == "__main__":
    app = GameApp()
    app.run()
