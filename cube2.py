import pygame as pg
import math

pg.init()
pg.display.set_caption("thing")
clock = pg.time.Clock()
#screen = pg.display.set_mode((3200, 1800))

screen = pg.display.set_mode((1600, 900))
pg.mouse.set_visible(False)
print("press esc to exit")
SCREEN_DIST = 100

global player_pos
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
        cords: tuple[int, int, int] = self.POINTS[point]
        
        pg.draw.circle(screen, "white", (cords[0], cords[1]), 10)
        player_point_vect = (cords[0] - player_pos[0]) , (cords[1] - player_pos[1])
        line_of_sight_vect = (math.cos(rotation), math.sin(rotation))
        angle = math.atan2(line_of_sight_vect[1], line_of_sight_vect[0]) - math.atan2(player_point_vect[1], player_point_vect[0])
        
        # if abs(angle) > math.pi/2:
        #     print("behind")
        #     return
        try:
            lenght_LOS_vect = math.sqrt(line_of_sight_vect[0]**2 + line_of_sight_vect[1]**2)
            rc = (line_of_sight_vect[0] / lenght_LOS_vect, line_of_sight_vect[1] / lenght_LOS_vect) #richtingscoefiecent zichtlijn
            c = rc[0] * player_pos[0] +  rc[1] * player_pos[1] #c = ax + by
            
            if abs(angle) < math.pi/2: d_line_point = (abs(rc[0] * cords[0] + rc[1] * cords[1] - c)) / (math.sqrt(rc[0]**2 + rc[1]**2))
            else: d_line_point = math.sqrt((player_pos[0] - cords[0])**2 + (player_pos[1] - cords[1])**2)
            
            d_player_point = math.sqrt((player_pos[0] - cords[0])**2 + (player_pos[1] - cords[1])**2)
            print(angle, d_line_point, 1 - 2* (angle < 0))
            side = 1 - 2* (angle < 0)
            angle_triangle = math.asin(d_line_point / d_player_point)
            
            projected_x = SCREEN_DIST * math.tan(angle_triangle) * side #player -> screen * tan(angle) * left/right
            pg.draw.circle(screen, "red", (projected_x + 800, 450), 10)
            pg.draw.line(screen, "orange", (cords[0] + math.sin(rotation) * d_line_point, cords[1] - math.cos(rotation)*d_line_point), (cords[0] - math.sin(rotation) * d_line_point, cords[1] + math.cos(rotation)*d_line_point))
        except ZeroDivisionError: print("on point")
        

    def update(self):
        # for num in self.POINTS:
        #     self.find_projecton(num)
        self.find_projecton(8)

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
    rotation = (rotation + ((mouse_pos[0] - screen.width // 2) / 300)) % math.tau
    pg.mouse.set_pos((screen.width // 2, screen.height // 2))
    #print(mouse_pos, rotation)

    return player_pos, rotation
    
box = Box((0, 0, 0))

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
            pg.quit()
    screen.fill("black")
    
    player_pos, rotation = input(player_pos, rotation)

    pg.draw.circle(screen, "white", (player_pos[0], player_pos[1]), 10)
    pg.draw.line(screen, "red", (player_pos[0] + math.cos(rotation) * -1000, player_pos[1] + math.sin(rotation)*-1000), (player_pos[0] + math.cos(rotation) * 1000, player_pos[1] + math.sin(rotation)*1000))

    box.update()

    pg.display.update()
    clock.tick(60)