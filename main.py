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
hunger = 0
ress = []
cages = []
cages_res = []
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

def create_res(kol):
    for i in range(kol):
        res = pg.draw.circle(win, (0, 255, 0), (randrange(400, 800), randrange(200, 600)), 2)
        ress.append(res)

def update_res():
    for i in range(len(ress)):
        ress[i] = pg.draw.circle(win, (0, 255, 0), (randrange(500, 700), randrange(300, 500)), 2)


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
    print(len(cages))
    if len(cages) > 0:
        for i in range(len(cages)):
            delete_cage = []
            for r in range(len(ress)):
                delete_res = []
                sun_x, sun_y, r1, r2 = create_sun((WIDTH // 2, HEIGHT // 2))
                x, y, cage_res = cages[i].x, cages[i].y, cages_res[i]
                res_x, res_y = ress[r].x, ress[r].y
                opt_x, opt_y, re = opt_x_and_y(x, y)
                if m == 1000:
                    create_res(100)
                    m = 0
                if hunger < 10000:
                    if cage_res == 1:
                        '''
                        if sun_x > x:
                            x += gravity
                        elif sun_x < x:
                            x += -gravity
        
                        if sun_y > y:
                            y += gravity
                        elif sun_y < y:
                            y += -gravity
        
                        if x < sun_x + 5 and x > sun_x - 5 and y > sun_y - 5 and y < sun_y + 5:
                            cages_res[i] = 0
                            print('Cage index:', i, 'put res.')
        
                        if x <= 0:
                            x = 1100
                        elif x >= 1200:
                            x = 100
        
                        if y <= 0:
                            y = 700
                        elif y >= 800:
                            y = 100
                        #ress[r] = pg.draw.circle(win, (0, 255, 0), (res_x + 2, res_y + 2), 2)
                        '''
                        hunger = 0
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
                            if ress[re] in delete_res:
                                pass
                            else:
                                delete_res.append(re)
                            #ress[re] = pg.draw.circle(win, (0, 255, 0), (randrange(100, 1100), randrange(100, 700)), 2)
                            print('Cage index:', i, 'take res in position:', opt_x, opt_y)
                        #else:
                            #ress[r] = pg.draw.circle(win, (0, 255, 0), (res_x+2, res_y+2), 2)

                        if x <= 0:
                            x = 1100
                        elif x >= 1200:
                            x = 100

                        if y <= 0:
                            y = 700
                        elif y >= 800:
                            y = 100
                        #hunger += 1
                    ress[r] = pg.draw.circle(win, (0, 255, 0), (res_x+2, res_y+2), 2)
                else:
                    if cages[i] in delete_cage:
                        pass
                    else:
                        delete_cage.append(i)
                #print(ress)
            #print(i)
                #print('Res position:', res_x, res_y, 'P:', x, y, 'And opt:', opt_x, opt_y)
            #print('Planet_index:', planet_index)
            print('Move:', move, 'Planet position:', i, x, y, cages_res[i], opt_x, opt_y)
            #print('Sun position:', sun_x, str(sun_y) + ', Res position:', res_x, res_y, 'And planet position:', x, y, cages_res[i])
            #print('Gravity:', gravity)
            #print('Planets:', planets[i])
            cages[i] = pg.draw.circle(win, (255, 0, 0), (x + 4, y + 4), 4)
            move += 1
            m += 1
            #print('Planets:', planets[i])

        for i in range(len(delete_res)):
            print('D_r:', i)
            ress.pop(delete_res[i])

        for i in range(len(delete_cage)):
            print('D_c:', i)
            cages.pop(delete_cage[i])

    else:
        print('Dead!')
        exit()

for i in range(10):
    create_cage((randrange(100, 1100), randrange(100, 700)))

create_res(100)

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