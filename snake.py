import pygame
from pygame.locals import *
import random

class Square(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Square, self).__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 200, 255))
        self.rect = self.image.get_rect(topleft=(x, y))

class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Food, self).__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

pygame.init()

screen = pygame.display.set_mode((800, 600))

snake = Square(40, 40)
food = Food(random.randint(0, 780), random.randint(0, 580))

snake_group = pygame.sprite.Group()
snake_group.add(snake)

food_group = pygame.sprite.Group()
food_group.add(food)

snake_direction = 'RIGHT'
snake_body = [snake]
score = 0
food_eaten = 0
speed = 10



gameOn = True
while gameOn:
    
    pygame.time.Clock().tick(speed)
    for event in pygame.event.get():
        if event.type == QUIT:
            gameOn = False
        if event.type == KEYDOWN:
            if event.key == K_UP and snake_direction!= 'DOWN':
                snake_direction = 'UP'
            if event.key == K_DOWN and snake_direction!= 'UP':
                snake_direction = 'DOWN'
            if event.key == K_LEFT and snake_direction!= 'RIGHT':
                snake_direction = 'LEFT'
            if event.key == K_RIGHT and snake_direction!= 'LEFT':
                snake_direction = 'RIGHT'

# to manually quit the game
    keys = pygame.key.get_pressed()
    if keys[K_q]:
        gameOn = False

# determinng the position of snake's new head
    if snake_direction == 'UP':
        new_head = Square(snake_body[-1].rect.x, (snake_body[-1].rect.y - 20)%600)
    if snake_direction == 'DOWN':
        new_head = Square(snake_body[-1].rect.x, (snake_body[-1].rect.y + 20)%600)
    if snake_direction == 'LEFT':
        new_head = Square((snake_body[-1].rect.x - 20)%800, snake_body[-1].rect.y)
    if snake_direction == 'RIGHT':
        new_head = Square((snake_body[-1].rect.x + 20)%800, snake_body[-1].rect.y)

# adding new head to front of snake
    snake_body.append(new_head)
    snake_group.add(new_head)


# spawn new food if snake eat food
    if pygame.sprite.spritecollideany(new_head, food_group):
        food.rect.x = random.randint(0, 780)
        food.rect.y = random.randint(0, 580)
        score += 10
        food_eaten += 1
        # increase speed whenever food is eaten 5 times
        if food_eaten % 5 == 0:
            speed += 5
    else:
        # to remove old square
        snake_group.remove(snake_body[0])
        snake_body.pop(0)

    # if snake head touch its body game is over
    for body_part in snake_body[:-1]:
        if new_head.rect.colliderect(body_part.rect):
            gameOn = False
            break

# instead of blit;draw is used to show snake and food
    screen.fill((0, 0, 0))
    snake_group.draw(screen)
    food_group.draw(screen)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

# display final score
game_over_text = font.render('Game Over!', True, (255, 255, 255))
screen.blit(game_over_text, (350, 250))
score_text = font.render(f'Final Score: {score}', True, (255, 255, 255))
screen.blit(score_text, (350, 300))
pygame.display.flip()
pygame.time.wait(2000)
pygame.quit()