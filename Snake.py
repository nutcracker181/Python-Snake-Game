import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
outline_color = (255, 255, 255)

dis_width = 600
dis_height = 400
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 30)

def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def draw_message(msg, color, size=50, position=(dis_width / 2, dis_height / 2)):
    font = pygame.font.SysFont(None, size)
    mesg = font.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=position)
    dis.blit(mesg, mesg_rect)

def draw_score(score):
    value = small_font.render(f"Score: {score}", True, black)
    dis.blit(value, [10, 10])

def draw_button(position, size, text, color=black):
    pygame.draw.rect(dis, color, [position[0], position[1], size[0], size[1]], 2)
    text_surf = small_font.render(text, True, black)
    text_rect = text_surf.get_rect(center=(position[0] + size[0] / 2, position[1] + size[1] / 2))
    dis.blit(text_surf, text_rect)

def start_screen():
    dis.fill(white)
    draw_message("Welcome to Snake Game!", black, size=50, position=(dis_width / 2, dis_height / 4))
    
    button_width, button_height = 150, 50
    start_button_pos = (dis_width / 2 - button_width / 2, dis_height / 2 - button_height / 2 - 10)
    quit_button_pos = (dis_width / 2 - button_width / 2, dis_height / 2 + button_height / 2 + 10)
    
    draw_button(start_button_pos, (button_width, button_height), "Start")
    draw_button(quit_button_pos, (button_width, button_height), "Quit")
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if (start_button_pos[0] <= mouse_pos[0] <= start_button_pos[0] + button_width and
                    start_button_pos[1] <= mouse_pos[1] <= start_button_pos[1] + button_height):
                    waiting = False
                elif (quit_button_pos[0] <= mouse_pos[0] <= quit_button_pos[0] + button_width and
                      quit_button_pos[1] <= mouse_pos[1] <= quit_button_pos[1] + button_height):
                    pygame.quit()
                    quit()

def generate_red_squares(num_squares):
    red_squares = []
    for _ in range(num_squares):
        x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        red_squares.append((x, y))
    return red_squares

def pause_screen():
    paused = True
    dis.fill(white)
    draw_message("Paused", black, size=50, position=(dis_width / 2, dis_height / 3))
    draw_message("Press P to Resume", black, size=30, position=(dis_width / 2, dis_height / 2))
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

def end_screen(score_value):
    dis.fill(white)
    draw_message("Game Over", black, size=50, position=(dis_width / 2, dis_height / 3))
    draw_message(f"Score: {score_value}", black, size=30, position=(dis_width / 2, dis_height / 2 - 30))
    
    button_width, button_height = 150, 50
    play_again_button_pos = (dis_width / 2 - button_width / 2, dis_height / 2)
    quit_button_pos = (dis_width / 2 - button_width / 2, dis_height / 2 + button_height + 10)

    draw_button(play_again_button_pos, (button_width, button_height), "Play Again", color=(0, 0, 0, 0))
    draw_button(quit_button_pos, (button_width, button_height), "Quit", color=(0, 0, 0, 0))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if (play_again_button_pos[0] <= mouse_pos[0] <= play_again_button_pos[0] + button_width and
                    play_again_button_pos[1] <= mouse_pos[1] <= play_again_button_pos[1] + button_height):
                    waiting = False
                    gameLoop()
                elif (quit_button_pos[0] <= mouse_pos[0] <= quit_button_pos[0] + button_width and
                      quit_button_pos[1] <= mouse_pos[1] <= quit_button_pos[1] + button_height):
                    pygame.quit()
                    quit()

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1
    score_value = 0

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    num_red_squares = 1
    red_squares = generate_red_squares(num_red_squares)

    while not game_over:
        while game_close:
            end_screen(score_value)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:
                    pause_screen()

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(white)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        for red_square in red_squares:
            pygame.draw.rect(dis, red, [red_square[0], red_square[1], snake_block, snake_block])
        
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        if snake_Head in snake_List[:-1]:
            game_close = True

        if any(x1 == rx and y1 == ry for rx, ry in red_squares):
            game_close = True

        draw_snake(snake_block, snake_List)
        draw_score(score_value)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score_value += 10
            num_red_squares += 1
            red_squares = generate_red_squares(num_red_squares)

        clock.tick(snake_speed)

    pygame.quit()
    quit()

start_screen()
gameLoop()
