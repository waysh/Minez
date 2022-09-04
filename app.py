# M I N E S W E E P E R
from ctypes.wintypes import HACCEL
from re import S
from tkinter import W
import pygame
import numpy as np
import random
import time
from configure_mines import *
from sys import exit
import sys

sys.setrecursionlimit(3000)

def menu():
    #load data
    W, H, n_mines = [int(i) for i in read_settings()]

    #initializes pygame, loads up and draws some surfaces
    pygame.init()
    screen = pygame.display.set_mode((400, 284))
    clock = pygame.time.Clock()
    pygame.display.set_caption('MINEZ - Menu')

    bg_surface = pygame.image.load(f'menu/menu.png').convert()
    screen.blit(bg_surface, (0,0))
    slider = pygame.image.load('menu/slider.png').convert_alpha()
    screen.blit(slider, (136,104))
    play = pygame.image.load('menu/play.png').convert_alpha()
    play_down = pygame.image.load('menu/play_pressed.png').convert_alpha()
    play_grey = pygame.image.load('menu/play_greyed.png').convert_alpha()
    image_icon = pygame.image.load('numbers/sqr.png').convert()
    pygame.display.set_icon(image_icon)

    #coordinate points for sliders areas
    width_area = ((143, 104), (317, 133))
    height_area = ((143, 145), (316, 174))
    mines_area = ((143, 189), (317, 221))
    play_area = ((151,230), (249,264))

    #max and mins for config
    width_limit = (8, 30)
    height_limit = (8, 30)
    mines_limit = (1, 300)

    #some booleans
    mouse_down = False
    play_mdown = False
    unplayable = True

    #more surfaces
    font = pygame.font.Font('font/OpenSans-Bold.ttf', 14)
    mine_fail = pygame.image.load('menu/mine_fail.png').convert_alpha()

    #sets starting values based on variables from config.txt
    values = {
        'width': W,
        'height': H,
        'mines': n_mines
    }

    #sets the starting slider positions based on values (inverse of the coord_to_value func)
    sliders = {
        'width': ((W - width_limit[0])/ (width_limit[1] - width_limit[0])) * (width_area[1][0] - width_area[0][0]) + width_area[0][0] - 7,
        'height': ((H - height_limit[0])/ (height_limit[1] - height_limit[0])) * (height_area[1][0] - height_area[0][0]) + height_area[0][0] - 7,
        'mines': ((n_mines - mines_limit[0])/ (mines_limit[1] - mines_limit[0])) * (mines_area[1][0] - mines_area[0][0]) + mines_area[0][0] - 7
    }

    #checks if mouse positions is within area coordinates
    def slider_magic(pos, area):
        if pos[0] >= area[0][0] and pos[0] <= area[1][0] and pos[1] >= area[0][1] and pos[1] <= area[1][1]:
            return True
        return False

    #converts coordinate position of slider to respective value
    def coord_to_value(x_pos, area, limit):
        percent = (x_pos - area[0][0]) / (area[1][0] - area[0][0])
        value = int(percent * (limit[1] - limit[0]) + limit[0])

        return value

    #basic function to draw text for value trackers
    def draw_text(val, coord):
        val = font.render(str(val).rjust(3, ' '), True, 'White')
        screen.blit(val, coord)
        return

    #main loop for menu
    while True:
        #draws initial background surface
        screen.blit(bg_surface, (0, 0))

        #checks if n_mines is playable
        if values['width'] * values['height'] > values['mines']:
            unplayable = False
        else:
            unplayable = True

        #iterates over the events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            #mouse button up
            if event.type == pygame.MOUSEBUTTONUP:
                
                #cheks if play button is effectively clicked, commits the values to the config.txt and calls main with the values
                pos = pygame.mouse.get_pos()
                if pos[0] >= play_area[0][0] and pos[0] <= play_area[1][0] and pos[1] >= play_area[0][1] and pos[1] <= play_area[1][1] and play_mdown:
                    vals = (values['width'], values['height'], values['mines'])
                    commit(vals)
                    main(vals)

                #otherwise set mouse_down booleans to False
                mouse_down = False
                play_mdown = False

            #initial mousebutton down or mouse already down using the mouse down booleans
            if event.type == pygame.MOUSEBUTTONDOWN or mouse_down or play_mdown:
                
                #mouse down on the play button
                pos = pygame.mouse.get_pos()
                if pos[0] >= play_area[0][0] and pos[0] <= play_area[1][0] and pos[1] >= play_area[0][1] and pos[1] <= play_area[1][1] and not(unplayable):
                    mouse_down = False
                    play_mdown = True
                else:
                    play_mdown = False
                
                #skips slider interaction if play button is still being pressed down
                if play_mdown:
                    continue

                #boolean for mouse down to go through this part again if the mouse is still held down 
                mouse_down = True

                #checks if mouse pos is within each slider area and respectively moves the slider pointer to that position if it is, and changes the value
                #i named it magic because i initially thought i was gna implement it in a different way which i thought was interesting
                if slider_magic(pos, width_area): 
                    sliders['width'] = pos[0] - 7
                    values['width'] = coord_to_value(pos[0], width_area, width_limit)

                if slider_magic(pos, height_area): 
                    sliders['height'] = pos[0] - 7
                    values['height'] = coord_to_value(pos[0], height_area, height_limit)

                if slider_magic(pos, mines_area): 
                    sliders['mines'] = pos[0] - 7
                    values['mines'] = coord_to_value(pos[0], mines_area, mines_limit)

        #draws the slider pointers
        screen.blit(slider, (sliders['width'], width_area[0][1]))
        screen.blit(slider, (sliders['height'], height_area[0][1]))
        screen.blit(slider, (sliders['mines'], mines_area[0][1]))
        
        #if theres more mines than squares, grey out the button. If it's pressed drawn, draw the pressed version, else draw the normal play button.
        if unplayable:
            screen.blit(mine_fail, (325, 189))
            screen.blit(play_grey, (149, 228))
        elif play_mdown:
            screen.blit(play_down, (149, 228))
        else:
            screen.blit(play, (149, 228))
            
        #draws the tracker text for each value in it's respective position
        draw_text(values['width'], (331, 108))
        draw_text(values['height'], (331, 149))
        draw_text(values['mines'], (332, 193))
        
        #fps for pygame
        clock.tick(60)

        #updates the display with all the newly drawn surfaces
        pygame.display.update()
    return

def main(vals):
    W, H, n_mines = vals

    def coord_to_index(pos):
        pos = (pos[1] - border - menu_height, pos[0] - border)
        pos = (pos[1] // (spacing + size), pos[0] // (spacing + size))
        return pos

    #takes in index of square and the field, returns number of nearby mines
    def nearby(clicked, true_field):
        total = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                n_y = clicked[1] + i
                n_x = clicked[0] + j

                if (n_x < 0) or (n_x >= W) or (n_y < 0) or (n_y >= H): continue
                if true_field[n_y][n_x] == 'MINE':
                    total += 1
        return total

    def clear_nearby(clicked, true_field):
        for i in range(-1, 2):
            for j in range(-1, 2):
                n_y = clicked[1] + i
                n_x = clicked[0] + j


                if (n_x < 0) or (n_x >= W) or (n_y < 0) or (n_y >= H) or (i == 0 and j == 0) or ((n_x, n_y) in uncovered) or ((n_x, n_y) in flagz): continue
                if true_field[n_y][n_x] == 'EMPTY':
                    n_close = nearby((n_x, n_y), true_field)
                    if n_close == 0:
                        seen = set()
                        clear_rest(0, (n_x, n_y), seen)
                        pass
                    else:
                        found.add((n_x, n_y))
                        uncovered.add((n_x, n_y))
                        draw = pygame.image.load(f'numbers/{n_close}.png').convert()
                        screen.blit(draw, coords_field[n_y][n_x])
                elif true_field[n_y][n_x] == 'MINE':
                    winnable.append(False)
                    screen.blit(mine, coords_field[n_y][n_x])
                    uncovered.add((n_x, n_y))

        return        


    def clear_rest(n, clicked, seen):
        if n > 0:
            draw = pygame.image.load(f'numbers/{n}.png').convert()
            screen.blit(draw, coords_field[clicked[1]][clicked[0]])
            uncovered.add(clicked)
            found.add(clicked)
            return
        else:
            draw = pygame.image.load('numbers/0.png').convert()
            screen.blit(draw, coords_field[clicked[1]][clicked[0]])
            uncovered.add(clicked)
            found.add(clicked)
            for i in range(-1, 2):
                for j in range(-1, 2):
                    n_y = clicked[1] + i
                    n_x = clicked[0] + j
                    if (n_x, n_y) == clicked: continue
                    if (n_x < 0) or (n_x >= W) or (n_y < 0) or (n_y >= H): continue
                    if (n_x, n_y) in seen: continue
                    seen.add((n_x, n_y))
                    if true_field[n_y][n_x] == 'EMPTY':
                        clear_rest(nearby((n_x, n_y), true_field), (n_x, n_y), seen)


    #Initial game logic
    spacing = -1
    size = 25
    border = 2
    uncovered = set()
    flagz = []
    won = False
    current = None
    previous = None
    hovered = None
    found = set()
    menu_height = 37 + border
    reset_hovered = False
    config_hovered = False
    lose = False




    raw_field = ['MINE'] * n_mines + ['EMPTY'] * (W * H - n_mines)
    random.shuffle(raw_field) 
    true_field = np.reshape(raw_field, (H, W))
    coords_field = np.empty((H, W), dtype = tuple)

    x,y = spacing + border, spacing + border + menu_height

    for i in range(H):
        for j in range(W):
            coords_field[i][j] = (x, y)
            x += size + spacing
        x = border + spacing
        y += size + spacing



    pygame.init()
    screen = pygame.display.set_mode((W* (size + spacing) + spacing + 2 * border, H * (size + spacing) + spacing + 2 * border + menu_height))

    pygame.display.set_caption('MINEZ')

    clock = pygame.time.Clock()


    window_width = W*(size + spacing) + spacing + 2 * border
    window_height = H * (size + spacing) + spacing + 2 * border + menu_height
    #top menu
    top_bg = pygame.image.load('top/bg.png').convert()
    screen.blit(top_bg, (border, border))
    #cut right side
    cut_black = pygame.Surface((1000, 1000))
    cut_black.fill('Black')
    screen.blit(cut_black, (window_width - border, 0))
    screen.blit(cut_black, (0, menu_height))
    #middle button
    reset_button = pygame.image.load('top/reset.png').convert_alpha()
    

    #coordinates for timer + mine counter
    
    s_passed = 0
    timer_start = False
    mine_counter_coords = (window_width // 2 - 31 // 2 + 31 + 8, menu_height // 2 - 31 // 2 + 8)
    timer_width = 50
    timer_coords = (window_width // 2 - 31 // 2 - timer_width + 3, menu_height // 2 - 31 // 2 + 8)
    font = pygame.font.Font('font/Pixeltype.ttf', 36)
    n_mines_surface = font.render(str(n_mines).rjust(3, '0'), False, 'White')
    timer_surface = font.render(str(s_passed).rjust(3, '0'), False, 'White')


    timer_bg = pygame.image.load('top/timer_bg.png').convert_alpha()

    #Draw
    screen.blit(timer_bg, (timer_coords[0] - 7, timer_coords[1] - 4))
    screen.blit(reset_button, (window_width // 2 - 31 // 2, menu_height // 2 - 31 // 2 + 1))
    screen.blit(n_mines_surface, mine_counter_coords)
    screen.blit(timer_surface, timer_coords)

    #config/menu button
    config_surface = pygame.image.load('top/config.png').convert_alpha()
    config_surface_down = pygame.image.load('top/config_down.png').convert_alpha()

    config_coords = (window_width - 31 - border - 3, menu_height // 2 - 31 // 2 + 1)

    screen.blit(config_surface, config_coords)




    bg_for_winlose = pygame.Surface((80, 31))
    bg_for_winlose.fill((40,40,40))
    bg_outline = pygame.Surface((84, 35))
    bg_outline.fill((2,2,2))





    #initial drawing stage
    square = pygame.image.load('numbers/sqr.png').convert()
    held = pygame.image.load('numbers/sqr2.png').convert()
    mine = pygame.image.load('numbers/mine.png').convert()

    for i in coords_field:
        for j in i:
            screen.blit(square, j)

    #find square that has empty nearby to mark it for the player
    distance = 1
    counter = 0
    right = True
    moves = []
    sign = 1
    target = (W//2, H//2)
    found_empty = False
    winnable = [True]

    while True:
        if right:
            direction = (0, distance)
            right = False
        else:
            direction = (distance, 0)
            right = True
        
        if direction[0] == 0:
            move = (0, int(direction[1] * sign / direction[1]))
        else:
            move = (int(direction[0] * sign / direction[0]), 0)
        
        for i in range(abs(distance)):
            #execute
            
            target = (target[0] + move[0], target[1] + move[1])
            if nearby(target, true_field) == 0:
                x_spot = pygame.image.load('numbers/x.png').convert()
                screen.blit(x_spot, coords_field[target[1]][target[0]])
                found_empty = True
                break
            

        counter += 1
        if counter % 2 == 0:
            if distance < 0:
                distance -= 1
            else:
                distance += 1
            distance *= -1
            sign *= -1


        if (abs(distance) > W // 1.4 - 1) or (abs(distance) > H // 1.4 - 1): 
            break
        if found_empty:
            break

        

    #Game Loop
    while True:

        if timer_start and won == False:
            screen.blit(timer_bg, (timer_coords[0] - 7, timer_coords[1] - 4))

            time_passed = int(time.time() - timer_start_time)
            if time_passed > 999:
                time_passed = 999
            timer_surface = font.render(str(time_passed).rjust(3, '0'), False, 'White')
            screen.blit(timer_surface, timer_coords)

            n_mines_surface = font.render(str(n_mines - len(flagz)).rjust(3, '0'), False, 'White')
            screen.blit(n_mines_surface, mine_counter_coords)

            if reset_hovered:
                screen.blit(reset_button_down, (window_width // 2 - 31 // 2, menu_height // 2 - 31 // 2 + 1))
            else:
                screen.blit(reset_button, (window_width // 2 - 31 // 2, menu_height // 2 - 31 // 2 + 1))
            
            if config_hovered:
                screen.blit(config_surface_down, config_coords)
            else:
                screen.blit(config_surface, config_coords)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            #mouse down in menu region
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()

                #its in menu region
                if pos[1] <= menu_height:
                    #highlight the button if its within the button
                    if (pos[0] >= window_width // 2 - 31 // 2) and (pos[0] <= window_width // 2 - 31 // 2 + 31) and (pos[1] >= menu_height // 2 - 31 // 2 + 1) and (pos[1] <= menu_height // 2 - 31 // 2 + 1 + 31):
                        reset_hovered = True
                        reset_button_down = pygame.image.load('top/reset_down.png').convert_alpha()
                        screen.blit(reset_button_down, (window_width // 2 - 31 // 2, menu_height // 2 - 31 // 2 + 1))
                        continue
                    #else if its in config button region
                    elif (pos[0] >= config_coords[0]) and (pos[0] <= config_coords[0] + 31) and (pos[1] >= config_coords[1]) and (pos[1] <= config_coords[1] + 31):
                        config_hovered = True
                        screen.blit(config_surface_down, config_coords)
                    else:
                        continue
                        
            #mouse up in menu region
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()


                #its in menu region
                if pos[1] <= menu_height:
                    #highlight the button if its within the button
                    if (pos[0] >= window_width // 2 - 31 // 2) and (pos[0] <= window_width // 2 - 31 // 2 + 31) and (pos[1] >= menu_height // 2 - 31 // 2 + 1) and (pos[1] <= menu_height // 2 - 31 // 2 + 1 + 31):
                        main(vals)

                    elif (pos[0] >= config_coords[0]) and (pos[0] <= config_coords[0] + 31) and (pos[1] >= config_coords[1]) and (pos[1] <= config_coords[1] + 31):
                        menu()
                    else:
                        continue
            
            #final check to skip the top region
            pos = pygame.mouse.get_pos()

            if reset_hovered and ((pos[0] >= window_width // 2 - 31 // 2) and (pos[0] <= window_width // 2 - 31 // 2 + 31) and (pos[1] >= menu_height // 2 - 31 // 2 + 1) and (pos[1] <= menu_height // 2 - 31 // 2 + 1 + 31)) != True:
                reset_hovered = False
                screen.blit(reset_button, (window_width // 2 - 31 // 2, menu_height // 2 - 31 // 2 + 1))

            if config_hovered and ((pos[0] >= config_coords[0]) and (pos[0] <= config_coords[0] + 31) and (pos[1] >= config_coords[1]) and (pos[1] <= config_coords[1] + 31)) != True:
                config_hovered = False
                screen.blit(config_surface, config_coords)           


            if (pos[0] <= border) or (pos[0] >= window_width - 1) or (pos[1] <= 0) or (pos[1] >= window_height - border) or (pos[1] <= menu_height + border):
                if hovered not in uncovered and hovered != None:
                    screen.blit(square, coords_field[hovered[1]][hovered[0]])
                continue
            
            if won:
                continue


            #mouse down
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if timer_start == False:
                    timer_start = True
                    timer_start_time = time.time()

                pos = pygame.mouse.get_pos()


                clicked = coord_to_index(pos)
                if clicked in uncovered or clicked in flagz:
                    pass
                else:
                    screen.blit(held, coords_field[clicked[1]][clicked[0]])
                    hovered = clicked

            #square is clicked?
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked = coord_to_index(pos)
                if event.button == 1 and clicked not in flagz:
                    clicked_on = true_field[clicked[1]][clicked[0]]
                    if hovered not in uncovered and hovered != None:
                        screen.blit(square, coords_field[hovered[1]][hovered[0]])
                    if clicked != hovered and hovered != None and clicked not in uncovered: continue
                    if clicked in uncovered and clicked_on != 'MINE':
                        clear_nearby(clicked, true_field)
                    elif clicked_on == 'MINE':
                        screen.blit(mine, coords_field[clicked[1]][clicked[0]])
                        lose = True
                        uncovered.add(clicked)
                        winnable.append(False)

                    elif clicked_on == 'EMPTY':
                        uncovered.add(clicked)
                        found.add(clicked)
                        near = nearby(clicked, true_field)
                        if near == 0:
                            seen = set()
                            clear_rest(0, clicked, seen)
                        else: 
                            draw = pygame.image.load(f'numbers/{near}.png').convert()
                            screen.blit(draw, coords_field[clicked[1]][clicked[0]])
                    else:
                        pass
                    if hovered not in uncovered and hovered != None:
                        screen.blit(square, coords_field[hovered[1]][hovered[0]])
        
                if event.button == 3:
                    if clicked in uncovered:
                        pass
                    elif clicked in flagz:
                        draw = pygame.image.load('numbers/sqr.png').convert()
                        screen.blit(draw, coords_field[clicked[1]][clicked[0]])
                        flagz.remove(clicked)

                    else:
                        draw = pygame.image.load('numbers/flag.png').convert()
                        screen.blit(draw, coords_field[clicked[1]][clicked[0]])
                        flagz.append(clicked)

        if len(found) == W * H - n_mines and won == False:
            won = True
            if winnable[-1]:
                screen.blit(bg_outline, (window_width // 2 - 80 // 2 - 2, menu_height // 2 - 31 // 2 + 57 - 2))
                bg_for_winlose.fill((15, 55, 5))
                screen.blit(bg_for_winlose, (window_width // 2 - 80 // 2, menu_height // 2 - 31 // 2 + 57))
                font2 = pygame.font.Font('font/OpenSans-Bold.ttf', 18)
                win_text = font.render('W I N !', True, 'White')
                screen.blit(win_text, (window_width // 2 - 54 // 2, menu_height // 2 - 31 // 2 + 64))
            #else:
                #print('You wouldve won if you didnt uncover a mine')
        if won == False and winnable[-1] == False:
            won = True
            screen.blit(bg_outline, (window_width // 2 - 80 // 2 - 2 - 2, menu_height // 2 - 31 // 2 + 57 - 2))
            bg_for_winlose.fill((75, 15, 0))
            screen.blit(bg_for_winlose, (window_width // 2 - 80 // 2 - 2, menu_height // 2 - 31 // 2 + 57))
            font2 = pygame.font.Font('font/OpenSans-Bold.ttf', 18)
            win_text = font.render('BOOM!', True, 'White')
            screen.blit(win_text, (window_width // 2 - 54 // 2 - 4, menu_height // 2 - 31 // 2 + 64))
        clock.tick(60)
        pygame.display.update()


menu()
