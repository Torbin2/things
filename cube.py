import pygame as pg
import math

pg.init()
pg.display.set_caption("thing")
clock = pg.time.Clock()
#screen = pg.display.set_mode((3200, 1800))

screen = pg.display.set_mode((1600, 900))

player_pos = [0, 1, -200]

SCREEN_DIST  =300
POINTS = {1 : [-100, -100, -100]
         ,2 : [-100, -100, 100]
         ,3 : [-100, 100, -100]
         ,4 : [-100, 100, 100]
         ,5 : [100, -100, -100]
         ,6 : [100, -100, 100]
         ,7 : [100, 100, -100]
         ,8 : [100, 100, 100]}

projections = {}


# b = 0
# for x  in range(2):
#     for y in range(2):
#         for z in range(2):
#             print(f"{b} : [{1*x}, {1*y}, {1*z}]")
#             b+=1

def minimap(player_pos, points) -> None:
    pg.draw.circle(screen,"red", (player_pos[0] + 800, player_pos[2] + 450), 10)
    for point in points:
        pg.draw.circle(screen,"red", (POINTS[point][0]+ 800, POINTS[point][2]+ 450), 10)

def render_point(point) -> None:
    cords = POINTS[point] #x y z
    player_point_vect = [cords[0] - player_pos[0], cords[1] - player_pos[1], cords[2] - player_pos[2]]
    try: 
        scale = SCREEN_DIST / player_point_vect[2]
    except ZeroDivisionError: scale = 1000

    player_screen_vect = list(map(lambda x: x * scale, player_point_vect))
    #if int(player_point_vect[2]) != SCREEN_DIST: print(player_screen_vect)

    point_projection = (player_pos[0] + player_screen_vect[0] + 800, player_pos[1] + player_screen_vect[1] + 450)
    #point_projection = (player_screen_vect[0] + 800,player_screen_vect[1] + 450)
    
    pg.draw.circle(screen, (0, 20 * point, 0), point_projection, 10)

    projections[point] = point_projection
    
def draw_lines() -> None:
    for i in (2, 3, 5):
        pg.draw.line(screen, "black", projections[1], projections[i], 5)
    for i in (2, 3, 8):
        pg.draw.line(screen, "black", projections[4], projections[i], 5)
    for i in (2, 5, 8):
        pg.draw.line(screen, "black", projections[6], projections[i], 5)
    for i in (3, 5, 8):
        pg.draw.line(screen, "black", projections[7], projections[i], 5)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
            pg.quit()
    
    keys = pg.key.get_pressed()
    
    if keys[pg.K_w]: player_pos[2] += 3
    if keys[pg.K_s]: player_pos[2] -= 3

    if keys[pg.K_a]: player_pos[0] -= 10
    if keys[pg.K_d]: player_pos[0] += 10

    if keys[pg.K_SPACE]: player_pos[1] -= 10
    if keys[pg.K_LSHIFT]: player_pos[1] += 10


    screen.fill("black")
    pg.draw.rect(screen, (105, 255, 40), pg.Rect(0,player_pos[1] + screen.get_height() // 2, screen.get_width(), screen.get_height()))
    pg.draw.rect(screen, (55, 100, 250), pg.Rect(0,player_pos[1] - screen.get_height() // 2, screen.get_width(), screen.get_height()))

    for point in POINTS: render_point(point)
    draw_lines()
    minimap(player_pos, POINTS)

    pg.display.update()
    clock.tick(60)