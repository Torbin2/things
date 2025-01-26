import pygame as pg
import math


pg.init()
pg.display.set_caption("thing")
clock = pg.time.Clock()
#screen = pg.display.set_mode((3200, 1800))
screen = pg.display.set_mode((1600, 900))


#changable
circles = [(400, 300), (415, 300), (430, 300), (445, 300), (445, 300), (445, 300), (445, 300), (445, 300),(445, 300),(445, 300)]
sizes = [40, 30, 25, 20, 18, 15, 13, 10, 10, 10,]


EYE_DIST = 20
EYE_SIZE = 10


SCALE = 2


COLOUR = ["#485844", "#8ead86", "#020302"]
#backg, snake, eyes


#===============================
eyesballs = [(), ()]


def calc_eyeballs(head_cent, mouse_pos):
    eyes = [(), ()]


    angle = math.atan2(mouse_pos[1] - head_cent[1], mouse_pos[0] - head_cent[0])
    turns_angle = (angle - 0.25 * math.pi, angle + 0.25 * math.pi) #sos cas toa, s = 5
    
    vect = ((EYE_DIST * math.cos(turns_angle[0]), EYE_DIST * math.sin(turns_angle[0])), #eye 1
            (EYE_DIST * math.cos(turns_angle[1]), EYE_DIST * math.sin(turns_angle[1])) #eye 2
                )
        
    eyes[0] = ((head_cent[0] + vect[0][0]) * SCALE, (head_cent[1] + vect[0][1])* SCALE)
    eyes[1] = ((head_cent[0] + vect[1][0]) * SCALE, (head_cent[1] + vect[1][1])* SCALE)


    return eyes


    


def draw_eyes(eyes):
    for i in range(2):
        pg.draw.circle(screen, (COLOUR[2]), eyes[i], EYE_SIZE * SCALE)


def update_circle(circle_num, circle_pos, prev_pos):
    global eyesballs
    if circle_num == 0:
        mouse_pos = (pg.mouse.get_pos()[0] / SCALE, pg.mouse.get_pos()[1] / SCALE)
        if circle_pos != mouse_pos:
            eyesballs = calc_eyeballs(circle_pos, mouse_pos)
        return mouse_pos




    dist_to_prev = math.sqrt((circle_pos[0] - prev_pos[0])**2 + (circle_pos[1] - prev_pos[1])**2)
    if dist_to_prev > sizes[circle_num] + sizes[circle_num - 1]:
        vect_new_to_prev_edge = (circle_pos[0] - prev_pos[0], circle_pos[1] - prev_pos[1])
        scale = (sizes[circle_num]+ sizes[circle_num - 1]) / dist_to_prev
        scaled_vect = (vect_new_to_prev_edge[0] * scale, vect_new_to_prev_edge[1] * scale)


        return (prev_pos[0] + scaled_vect[0], prev_pos[1] + scaled_vect[1])


    return circle_pos
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
            pg.quit()


    screen.fill(COLOUR[0])


    for num in range(len(circles)):
        pg.draw.circle(screen, (COLOUR[1]), (int(circles[num][0]) * SCALE, int(circles[num][1]) * SCALE), sizes[num] * SCALE)
        circles[num] = update_circle(num, circles[num], circles[num - 1] if num > 0 else (0, 0))
        
    draw_eyes(eyesballs)


    pg.display.update()
    clock.tick(60)