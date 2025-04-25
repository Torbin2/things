import pygame as pg
import math

pg.init()
pg.display.set_caption("thing")
clock = pg.time.Clock()
#screen = pg.display.set_mode((3200, 1800))

screen = pg.display.set_mode((1600, 900))
pg.mouse.set_visible(False)
print("press esc to exit")
SCREEN_DIST = 10

player_pos = [0, 0, 0] #x, y, z
rotation = 0


class Box:
    def __init__(self, start_point: tuple[int, int, int]):
        self.POINTS = {1 : [start_point[0], start_point[1], start_point[2]] ,
                       2 : [start_point[0], start_point[1], start_point[2]+200] ,
                       3 : [start_point[0], start_point[1]+200, start_point[2]] ,
                       4 : [start_point[0]+200, start_point[1], start_point[2]] ,
                       5 : [start_point[0], start_point[1]+200, start_point[2]+200] ,
                       6 : [start_point[0]+200, start_point[1], start_point[2]+200] ,
                       7 : [start_point[0]+200, start_point[1]+200, start_point[2]] ,
                       8 : [start_point[0]+200, start_point[1]+200, start_point[2]+200]}
        
    def find_projecton(self, point):
        pass

def input(player_pos, rotation):
    keys = pg.key.get_pressed()
    
    if keys[pg.K_w]: player_pos[1] -= 10
    if keys[pg.K_s]: player_pos[1] += 10

    if keys[pg.K_a]: player_pos[0] -= 10
    if keys[pg.K_d]: player_pos[0] += 10

    if keys[pg.K_SPACE]: player_pos[2] += 10
    if keys[pg.K_LSHIFT]: player_pos[2] -= 10

    if keys[pg.K_ESCAPE]:
        exit()
        pg.quit()

    mouse_pos = pg.mouse.get_pos()
    rotation = (rotation + ((mouse_pos[0] - screen.width // 2) / 200)) % math.tau
    pg.mouse.set_pos((screen.width // 2, screen.height // 2))
    print(mouse_pos, rotation)

    return player_pos, rotation

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
            pg.quit()
    screen.fill("black")
    
    player_pos, rotation = input(player_pos, rotation)

    pg.draw.circle(screen, "white", (player_pos[0], player_pos[1]), 10)
    pg.draw.line(screen, "red", (player_pos[0], player_pos[1]), (player_pos[0] + math.cos(rotation) * 100, player_pos[1] + math.sin(rotation)*100))

    

    pg.display.update()
    clock.tick(60)