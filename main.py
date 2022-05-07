import pygame as pg
from random import randrange
#from numba import prange, njit

RES = WIDTH, HEIGHT = 1200, 800
FPS = 60

pg.init ()
win = pg.display.set_mode(RES)
clock = pg.time.Clock()

m = 1
move = 1
ress = []
cages = []
cages_res = []
hungers= []
res_pos = randrange(100, 1100), randrange(100, 700)
gravity = 1

def create_sun(pos):
    sun = pg.draw.circle(win, (0, 255, 255), pos, 6)
    return sun

def create_cage(pos):
    cage = pg.draw.circle(win, (255, 0, 0), pos, 4)
    cage_res = 0
    cages.append(cage)
    cages_res.append(cage_res)
    hungers.append(0)

def create_res(kol):
    for i in range(kol):
        res = pg.draw.circle(win, (0, 255, 0), (randrange(400, 800), randrange(200, 600)), 2)
        ress.append(res)

def update_res():
    for i in range(len(ress)):
        ress[i] = pg.draw.circle(win, (0, 255, 0), (ress[i].x+2, ress[i].y+2), 2)


def create_res_in_pos(pos):
    res = pg.draw.circle(win, (0, 255, 0), pos, 2)
    ress.append(res)

def opt_x_and_y(x,y):
    opt_x, opt_y = ress[0].x, ress[0].y
    re = 0
    for r in range(len(ress)):
        res_x, res_y = ress[r].x, ress[r].y
        if abs(res_x - x) < abs(opt_x - x) and abs(res_y - y) < abs(opt_y - y):
            opt_x = res_x
            opt_y = res_y
            re = r
        #print('P:', x, y, 'R:', res_x, res_y, r, re, 'Opt:', opt_x, opt_y)
    return opt_x, opt_y, re

def update():
    global x, y, cage_res, sun_x, sun_y, res_x, res_y, opt_x, opt_y, move, hunger, m, delete_res, delete_cage
    if len(cages) > 0:
        delete_cage = []
        delete_res = []
        for i in range(len(cages)):
            x, y, cage_res, hunger = cages[i].x, cages[i].y, cages_res[i], hungers[i]
            opt_x, opt_y, re = opt_x_and_y(x, y)
            if m == 100:
                create_res(300)
                m = 0
            if hunger < 100:
                if cage_res == 1:
                    hungers[i] = 0
                    cages_res[i] = 0
                    print('Cage index:', i, 'eat res in position:', x, y)
                else:
                    if opt_x > x:
                        x += gravity
                    elif opt_x < x:
                        x += -gravity

                    if opt_y > y:
                        y += gravity
                    elif opt_y < y:
                        y += -gravity

                    if x < opt_x+5 and x > opt_x-5 and y > opt_y-5 and y < opt_y+5:
                        cages_res[i] = 1
                        print('Cage index:', i, 'take res in position:', opt_x, opt_y)
                        if ress[re] in delete_res:
                            pass
                        else:
                            print('DelR', re)
                            delete_res.append(re)

                    if x <= 0:
                        x = 1100
                    elif x >= 1200:
                        x = 100

                    if y <= 0:
                        y = 700
                    elif y >= 800:
                        y = 100
                hungers[i] += 1
                update_res()
            else:
                if cages[i] in delete_cage:
                    pass
                else:
                    print('DelC:', i)
                    delete_cage.append(i)
            print('Move:', move, 'Planet position:', i, x, y, cages_res[i], opt_x, opt_y)
            cages[i] = pg.draw.circle(win, (255, 0, 0), (x + 4, y + 4), 4)
        move += 1
        m += 1

        for i in range(len(delete_res)):
            print('D_r:', i)
            print(delete_res[i])
            try:
                ress.pop(delete_res[i])
            except IndexError:
                ress.pop()

        for i in range(len(delete_cage)):
            print('D_c:', i)
            print(delete_cage[i])
            try:
                cages.pop(delete_cage[i])
            except IndexError:
                cages.pop()

    else:
        print('Dead!')
        exit()

for i in range(20):
    create_cage((randrange(400, 800), randrange(200, 600)))

create_res(300)

while True:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                create_cage(i.pos)
            elif i.button == 2:
                create_res(10)
            elif i.button == 3:
                create_res_in_pos(i.pos)
        elif i.type == pg.K_1:
            FPS += 1
            print('FPS:', FPS)
        elif i.type == pg.K_2:
            FPS -= 1
            print('FPS:', FPS)
        elif i.type == pg.K_3:
            FPS += 10
            print('FPS:', FPS)
        elif i.type == pg.K_4:
            FPS -= 10
            print('FPS:', FPS)

    pg.display.set_caption(str(int(clock.get_fps())))
    win.fill((0,0,0))
    update()
    pg.display.update()
    clock.tick(FPS)
pg.quit