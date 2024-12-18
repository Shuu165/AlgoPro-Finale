import pygame # for ofc. pygame
import sys # to be able to exit the program cleanly
import time # for the timer

pygame.init()
pygame.display.set_caption("Towers of Hanoi") # Title
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

game_done = False
framerate = 60

steps = 0 # players moves
n_disks = 3
disks = []
towers_midx = [120, 320, 520] # 3 rods coordinates
pointing_at = 0 # tracks which tower player selects
floating = False # indicates if disks being moved
floater = 0 # stores index. (when disk is picked up. floater stores the index as "picked up")
start_time = 0
stars = 0
time_limit = 300  # 5 minutes

#RGB Values for the colors in the pygame
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gold = (239, 229, 51)
blue = (78, 162, 196)
grey = (170, 170, 170)
green = (77, 206, 145)

def blit_text(screen, text, midtop, aa=True, font=None, font_name=None, size=None, color=(255, 0, 0)):
    if font is None:
        font = pygame.font.SysFont(font_name, size)
    font_surface = font.render(text, aa, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop
    screen.blit(font_surface, font_rect)

def menu_screen():
    global screen, n_disks, game_done, start_time
    menu_done = False
    while not menu_done:
        screen.fill(white)
        blit_text(screen, 'Towers of Hanoi', (320, 120), font_name='sans serif', size=90, color=gold)
        blit_text(screen, 'Select difficulty:', (320, 220), font_name='sans serif', size=30, color=black)
        blit_text(screen, str(n_disks), (320, 260), font_name='sans serif', size=40, color=blue)
        blit_text(screen, 'Press ENTER to continue', (320, 320), font_name='sans serif', size=30, color=black)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                # Press "Q"
                if event.key == pygame.K_q:
                    menu_done = True # Exit menu
                    game_done = True # Exit Game
                
                # Press "Enter"
                if event.key == pygame.K_RETURN:
                    menu_done = True # Exit Menu, Start Game
                    start_time = time.time()  # Start the timer

                # Change Difficulties            
                if event.key in [pygame.K_RIGHT, pygame.K_UP]: 
                    n_disks += 1
                    if n_disks > 6:
                        n_disks = 6
                if event.key in [pygame.K_LEFT, pygame.K_DOWN]:
                    n_disks -= 1
                    if n_disks < 1:
                        n_disks = 1

            if event.type == pygame.QUIT:
                menu_done = True
                game_done = True
        pygame.display.flip() # If changes happen, updates the screen
        clock.tick(60) # Frames

def game_over():
    global steps, stars, start_time
    screen.fill(white)
    min_steps = 2**n_disks - 1 # Tower of Hanoi Algorithm
    elapsed_time = time.time() - start_time

    # Title
    blit_text(screen, 'You Won!', (320, 150), font_name='sans serif', size=72, color=gold)

    # Star Ratings
    stars = 1  # Completing the game
    if steps == min_steps:
        stars += 1
    if elapsed_time <= time_limit:
        stars += 1

    # Display steps and time
    blit_text(screen, f'Steps: {steps}', (320, 250), font_name='mono', size=30, color=black)
    blit_text(screen, f'Minimum Steps: {min_steps}', (320, 280), font_name='mono', size=30, color=red)
    blit_text(screen, f'Time Taken: {int(elapsed_time)}s', (320, 310), font_name='mono', size=30, color=blue)

    # Display stars
    for i in range(3):  # Draw stars
        color = gold if i < stars else grey
        pygame.draw.circle(screen, color, (260 + i * 40, 360), 15)  # spacing between stars

    # Update the display
    pygame.display.flip()
    time.sleep(5)  # Pause for 5 seconds
    pygame.quit()
    sys.exit()

def draw_towers(): # Displays the towers
    for xpos in range(40, 460+1, 200):
        pygame.draw.rect(screen, green, pygame.Rect(xpos, 400, 160, 20))
        pygame.draw.rect(screen, grey, pygame.Rect(xpos+75, 200, 10, 200))
    blit_text(screen, 'Start', (towers_midx[0], 403), font_name='mono', size=14, color=black)
    blit_text(screen, 'Finish', (towers_midx[2], 403), font_name='mono', size=14, color=black)

def make_disks():
    global n_disks, disks
    disks = [] # to reset the disks
    height = 20
    ypos = 397 - height # it stacks from the bottom
    width = n_disks * 23 # disk size, largest to smallest
    for i in range(n_disks):
        disk = {}
        disk['rect'] = pygame.Rect(0, 0, width, height) # makes the largest at the bottom and smaller above it
        disk['rect'].midtop = (120, ypos)
        disk['val'] = n_disks-i # make the size not too big yet not too small
        disk['tower'] = 0 # placing the disks on the first tower
        disks.append(disk)
        ypos -= height + 3
        width -= 23

def draw_disks(): # Displays the Disks
    for disk in disks:
        pygame.draw.rect(screen, blue, disk['rect'])

def draw_ptr(): # displays a red arrow indicating selected tower
    ptr_points = [(towers_midx[pointing_at]-7, 440), (towers_midx[pointing_at]+7, 440), (towers_midx[pointing_at], 433)]
    pygame.draw.polygon(screen, red, ptr_points)

def check_won(): # checks if all disks are at the last tower
    global disks
    over = True
    for disk in disks:
        if disk['tower'] != 2:
            over = False
    if over:
        time.sleep(0.2)
        game_over()

def reset(): # reset back to menu
    global steps, pointing_at, floating, floater
    steps = 0
    pointing_at = 0
    floating = False
    floater = 0
    menu_screen()
    make_disks()

menu_screen()
make_disks()

while not game_done: # Main Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Exit Game when window is closed
            game_done = True
        if event.type == pygame.KEYDOWN: # key inputs
            if event.key == pygame.K_ESCAPE: # resets the game when press "esc"
                reset()
            if event.key == pygame.K_q: # quits the game when press "Q"
                game_done = True

            if event.key == pygame.K_RIGHT: # Move disk to the right
                pointing_at = (pointing_at+1) % 3 # go through 3 towers
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at

            if event.key == pygame.K_LEFT: # Move disk to the left
                pointing_at = (pointing_at-1) % 3
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at

            if event.key == pygame.K_UP and not floating: # make disk float/go up
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at:
                        floating = True
                        floater = disks.index(disk)
                        disk['rect'].midtop = (towers_midx[pointing_at], 100)
                        break

            if event.key == pygame.K_DOWN and floating: # make disk go down
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at and disks.index(disk) != floater:
                        if disk['val'] > disks[floater]['val']:
                            floating = False
                            disks[floater]['rect'].midtop = (towers_midx[pointing_at], disk['rect'].top-23)
                            steps += 1
                        break
                else:
                    floating = False
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 400-23)
                    steps += 1 # adds into number of steps done

    screen.fill(white)
    draw_towers()
    draw_disks()
    draw_ptr()
    blit_text(screen, 'Steps: '+str(steps), (320, 20), font_name='mono', size=30, color=black)
    pygame.display.flip()
    if not floating:
        check_won()
    clock.tick(framerate)
