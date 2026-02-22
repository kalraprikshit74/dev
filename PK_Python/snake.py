import pygame
import sys
import random
import os

UP = 'UP'
RIGHT = 'RIGHT'
DOWN = 'DOWN'
LEFT = 'LEFT'

class SnakeGame:
    def __init__(self):
        pygame.init()
        # Get screen resolution
        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h
        self.display = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.font = pygame.font.Font(None, 75)
        self.clock = pygame.time.Clock()
        self.high_score = 0
        self.touch_start = None  # Initialize touch control
        self.button_width = 300
        self.button_height = 150
        self.exit_button_rect = pygame.Rect(
            self.width - self.button_width - 20,  # 20px margin from the right
            self.height - self.button_height - 20,  # 20px margin from the bottom
            self.button_width,
            self.button_height,
            )
        self.reset()


    def reset(self):
        self.high_score = max(self.high_score, len(self.snake) if hasattr(self, "snake") else 0)
        self.direction = RIGHT
        self.snake = [(120, 100), (140, 100), (160, 100)]
        self.apple = self.set_new_apple()

    def set_new_apple(self):
        while True:
            x = random.randint(0, (self.width // 20) - 1) * 20
            y = random.randint(0, (self.height // 20) - 1) * 20
            if (x, y) not in self.snake:
                return x, y

    def draw(self):
        self.display.fill((0, 255, 0))
        for i, (x,y) in enumerate(self.snake):
            if i == len(self.snake) - 1:
                pygame.draw.circle(self.display ,(0, 0, 255), (x +20, y+20), 22)
                eye_offset_x = 8 if self.direction in (LEFT, RIGHT) else 0
                eye_offset_y = 8 if self.direction in (UP, DOWN) else 0
                pygame.draw.circle(self.display, (255, 255, 255), (x + 12 + eye_offset_x, y+12 + eye_offset_y),4)
                pygame.draw.circle(self.display, (255, 255, 255), (x + 28 - eye_offset_x, y+12 + eye_offset_y), 4)
            else:
                pygame.draw.circle(self.display, (0, 0, 139), (x + 20, y+20), 18)
        pygame.draw.circle(self.display, (255, 0, 0), (self.apple[0] + 20, self.apple[1] + 20), 20 )

        score_text = self.font.render(f"Score: {len(self.snake)}", True, (0, 0, 0))
        self.display.blit(score_text, (20, 20))

        pygame.display.flip()



    def draw(self):
        self.display.fill((0, 255, 0))  # Green background
        for i, (x, y) in enumerate(self.snake):
            if i == len(self.snake)-1:
                pygame.draw.circle(self.display, (0, 0, 255), (x + 20, y + 20), 20)
            else:
                width = max(10, 40 - i * 5)  # Gradually reduce width
                pygame.draw.rect(self.display, (0, 0, 255), (x, y, width, 40))
        pygame.draw.rect(self.display, (255, 0, 0), (*self.apple, 40, 40))
        score_text = self.font.render(f"Score: {len(self.snake)}", True, (0, 0, 0))
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, (0, 0, 0))
        self.display.blit(score_text, (20, 20))
        self.display.blit(high_score_text, (20, 100))

        pygame.draw.rect(self.display, (255, 0, 0), self.exit_button_rect)  # Red button
        exit_text = self.font.render("Exit", True, (255, 255, 255))
        text_rect = exit_text.get_rect(center=self.exit_button_rect.center)  # Center the text
        self.display.blit(exit_text, text_rect)

        pygame.display.flip()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.exit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                self.touch_start = event.pos
            elif event.type == pygame.MOUSEMOTION and self.touch_start:
                touch_end = event.pos
                dx, dy = touch_end[0] - self.touch_start[0], touch_end[1] - self.touch_start[1]
                if abs(dx) > abs(dy):
                    if dx > 0 and self.direction != LEFT:
                        self.direction = RIGHT
                    elif dx < 0 and self.direction != RIGHT:
                        self.direction = LEFT
                else:
                    if dy > 0 and self.direction != UP:
                        self.direction = DOWN
                    elif dy < 0 and self.direction != DOWN:
                        self.direction = UP
                self.touch_start = None
        #Horizontal Movement (dx):
        #Positive dx: Swipe to the right.
        #Negative dx: Swipe to the left.
        #Vertical Movement (dy):
        #Positive dy: Swipe down.
        #Negative dy: Swipe up
        head = self.snake[-1] #(160,100)
        if self.direction == UP:
            new_head = (head[0], head[1] - 20)
        elif self.direction == DOWN:
            new_head = (head[0], head[1] + 20)
        elif self.direction == LEFT:
            new_head = (head[0] - 20, head[1])
        elif self.direction == RIGHT:
            new_head = (head[0] + 20, head[1])

        if (new_head[0] < 0 or new_head[0] >= self.width or
                new_head[1] < 0 or new_head[1] >= self.height or
                new_head in self.snake[:-1]):
            self.reset()
        elif new_head == self.apple:
            self.snake.append(new_head)
            self.apple = self.set_new_apple()
        else:
            self.snake.append(new_head)
            self.snake.pop(0)

    def run(self):
        while True:
            self.update()
            self.draw()
            self.clock.tick(10)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
