import pygame as pg
from random import randrange
import random

RES = WIDTH, HEIGHT = 1200, 800
FPS = 60

pg.init()
win = pg.display.set_mode(RES)
clock = pg.time.Clock()

f1 = pg.font.Font(None, 36)

m = 1
move = 1
ress = []
cages = []
cages_res = []
hungers = []

klan_1 = 0
klan_2 = 0
klan_3 = 0

predator_kol = 2
predators = []
predators_res = []
predators_hungers = []
gens = []

clear = 0

hunger_koll = 100
predator_hunger_koll = 100
clear_koll = 500
m_koll = 100
res_kol = 100
res_kol1 = 50
cage_kol = 20
res_pos = randrange(100, 1100), randrange(100, 700)
cage_speed = 1
predator_speed = 2
game_speed = 1

gen = [[60, 30, 5], [40, 10, 3], [30, 5, 2]]


def pause():
    pauses = input('Press to continue...')


def slow():
    global cage_speed, predator_speed, hunger_koll, clear_koll, m_koll, predator_hunger_koll
    if cage_speed == 2 and predator_speed == 3:
        cage_speed = cage_speed//2
        predator_speed = predator_speed//2
        hunger_koll = hunger_koll*2
        predator_hunger_koll = predator_hunger_koll*2
        clear_koll = clear_koll*2
        m_koll = m_koll*2
        print('Slow is active')
        print(cage_speed, predator_speed, hunger_koll, clear_koll, m_koll, predator_hunger_koll)
    else:
        cage_speed = 2
        predator_speed = 3
        hunger_koll = 100
        clear_koll = 500
        m_koll = 100
        print('Slow is deactivate')


def create_sun(pos):
    sun = pg.draw.circle(win, (0, 255, 255), pos, 6)
    return sun


def create_cage(pos, kol):
    for i in range(kol):
        cage = pg.draw.circle(win, (255, 0, 0), pos, 4)
        cages.append(cage)
        cages_res.append(0)
        hungers.append(0)
        gens.append(gen[random.randint(0, len(gen) - 1)])


def create_cage_with_gen(pos, gen):
    cage = pg.draw.circle(win, (255, 0, 0), pos, 4)
    cages.append(cage)
    cages_res.append(0)
    hungers.append(0)
    gens.append(gen)


def create_predators(pos, kol):
    for i in range(kol):
        predator = pg.draw.circle(win, (255, 255, 255), pos, 6)
        predators.append(predator)
        predators_res.append(0)
        predators_hungers.append(0)


def create_res(kol):
    for i in range(kol):
        res = pg.draw.circle(win, (0, 255, 0), (randrange(400, 800), randrange(200, 600)), 2)
        ress.append(res)


def update_res():
    for i in range(len(ress)):
        ress[i] = pg.draw.circle(win, (0, 255, 0), (ress[i].x + 2, ress[i].y + 2), 2)


def clear_f():
    global ress, delete_cage, predators, res_kol1, res_kol
    ress = []
    res_kol = res_kol1
    predators = []
    for i in range(len(cages) // 2):
        try:
            cages.pop((random.randint(0, len(cages) - 1)))
        except IndexError:
            cages.pop()


def create_res_in_pos(pos):
    res = pg.draw.circle(win, (0, 255, 0), pos, 2)
    ress.append(res)


def opt_x_and_y(x, y):
    opt_x, opt_y = ress[0].x, ress[0].y
    re = 0
    for r in range(len(ress)):
        res_x, res_y = ress[r].x, ress[r].y
        if abs(res_x - x) < abs(opt_x - x) and abs(res_y - y) < abs(opt_y - y):
            opt_x = res_x
            opt_y = res_y
            re = r
    return opt_x, opt_y, re


def predator_opt_x_and_y(x, y):
    opt_x, opt_y = cages[0].x, cages[0].y
    re = 0
    for r in range(len(cages)):
        cage_x, cage_y = cages[r].x, cages[r].y
        if abs(cage_x - x) < abs(opt_x - x) and abs(cage_y - y) < abs(opt_y - y):
            opt_x = cage_x
            opt_y = cage_y
            re = r
    return opt_x, opt_y, re


def danger_x_and_y(x, y):
    danger_x, danger_y = predators[0].x, predators[0].y
    d = 0
    for r in range(len(predators)):
        pre_x, pre_y = predators[r].x, predators[r].y
        if abs(pre_x - x) < abs(danger_x - x) and abs(pre_y - y) < abs(danger_y - y):
            danger_x = pre_x
            danger_y = pre_y
            d = r
    return danger_x, danger_y, d


def gens_klan():
    global klan_1, klan_2, klan_3
    klan_1, klan_2, klan_3 = 0, 0, 0
    for i in range(len(gens)):
        if gen[0] == gens[i]:
            klan_1 += 1
        elif gen[1] == gens[i]:
            klan_2 += 1
        elif gen[2] == gens[i]:
            klan_3 += 1
    Gen1 = f1.render(f'Gen_1, {klan_1}', True, (255, 0, 0))
    Gen2 = f1.render(f'Gen_2, {klan_2}', True, (0, 255, 0))
    Gen3 = f1.render(f'Gen_3, {klan_3}', True, (0, 0, 255))
    win.blit(Gen1, (10, 10))
    win.blit(Gen2, (10, 40))
    win.blit(Gen3, (10, 70))


def cage_update():
    global x, y, cage_res, res_x, res_y, opt_x, opt_y, move, hunger, m, delete_res, delete_cage, delete_gens, clear, hunger_koll, clear_koll, m_koll, res_kol
    if len(cages) > 0:
        delete_cage = []
        delete_res = []
        #delete_gens = []
        for i in range(len(cages)):
            x, y, cage_res, hunger, cage_gen = cages[i].x, cages[i].y, cages_res[i], hungers[i], gens[i]
            eat_gen, danger_gen, create_gen = cage_gen
            if len(ress) > 0:
                opt_x, opt_y, re = opt_x_and_y(x, y)
            else:
                create_res(1)
                opt_x, opt_y, re = opt_x_and_y(x, y)
            if len(predators) > 0:
                danger_x, danger_y, d = danger_x_and_y(x, y)
            else:
                danger_x, danger_y, d = 1300, 900, 0

            '''if clear == clear_koll:
                clear_f()
                create_res(res_kol)
                create_predators((randrange(400, 800), randrange(200, 600)), predator_kol)
                m = 0
                break'''
            if m == m_koll:
                create_res(res_kol)
                m = 0
            if hunger < hunger_koll:
                if cage_res == 1:
                    Chance = random.randint(1, create_gen)
                    mutation_chance = random.randint(1, 5)
                    predator_chans =  random.randint(1, 50)
                    # print('Chance create cage:', Chance)
                    if Chance == 1:
                        if mutation_chance == 1:
                            create_cage((x + random.randint(-10, 10), y + random.randint(-10, 10)), 1)
                        else:
                        #res_kol += 1
                            if predator_chans == 1:
                                create_predators((x + random.randint(-10, 10), y + random.randint(-10, 10)), 1)
                            else:
                                create_cage_with_gen((x + random.randint(-10, 10), y + random.randint(-10, 10)), cage_gen)
                    else:
                        hungers[i] = 0
                        cages_res[i] = 0
                else:
                    if abs(danger_x - x) > danger_gen and abs(danger_y - y) > danger_gen:
                        if abs(opt_x-x) <= eat_gen and abs(opt_y-y) <= eat_gen:
                            if opt_x > x:
                                x += cage_speed
                            elif opt_x < x:
                                x += -cage_speed

                            if opt_y > y:
                                y += cage_speed
                            elif opt_y < y:
                                y += -cage_speed

                            if x < opt_x + 5 and x > opt_x - 5 and y > opt_y - 5 and y < opt_y + 5:
                                cages_res[i] = 1
                                if ress[re] in delete_res:
                                    pass
                                else:
                                    delete_res.append(re)
                        else:
                            move_chance = random.randint(1, 4)
                            if move_chance == 1:
                                x += cage_speed
                            elif move_chance == 2:
                                x += -cage_speed
                            if move_chance == 3:
                                y += cage_speed
                            elif move_chance == 4:
                                y += -cage_speed
                    else:
                        if danger_x > x:
                            x += -cage_speed
                        elif danger_x < x:
                            x += cage_speed

                        if danger_y > y:
                            y += -cage_speed
                        elif danger_y < y:
                            y += cage_speed

                    if x <= 0:
                        x = 1100
                    elif x >= 1200:
                        x = 100

                    if y <= 0:
                        y = 700
                    elif y >= 800:
                        y = 100
                hungers[i] += 1
                gens_klan()
                update_res()
            else:
                if cages[i] in delete_cage:
                    pass
                else:
                    delete_cage.append(i)

                '''if gens[i] in delete_gens:
                    pass
                else:
                    delete_gens.append(i)'''
            if cage_gen == gen[0]:
                cages[i] = pg.draw.circle(win, (255, 0, 0), (x + 4, y + 4), 4)
            elif cage_gen == gen[1]:
                cages[i] = pg.draw.circle(win, (0, 255, 0), (x + 4, y + 4), 4)
            elif cage_gen == gen[2]:
                cages[i] = pg.draw.circle(win, (0, 0, 255), (x + 4, y + 4), 4)
        move += 1
        m += 1
        clear += 1

        for i in range(len(delete_res)):
            try:
                ress.pop(delete_res[i])
            except IndexError:
                try:
                    ress.pop()
                except Exception:
                    continue

        '''for i in range(len(delete_gens)):
            try:
                gens.pop(delete_gens[i])
            except IndexError:
                try:
                    gens.pop()
                except Exception:
                    continue'''

        for i in range(len(delete_cage)):
            try:
                try:
                    cages.pop(delete_cage[i])
                except IndexError:
                    cages.pop()
            except Exception:
                continue

            try:
                try:
                    cages_res.pop(delete_cage[i])
                except IndexError:
                    cages_res.pop()
            except Exception:
                continue

            try:
                try:
                    hungers.pop(delete_cage[i])
                except IndexError:
                    hungers.pop()
            except Exception:
                continue

            try:
                try:
                    gens.pop(delete_cage[i])
                except IndexError:
                    gens.pop()
            except Exception:
                continue

    else:
        return False


def predator_update():
    global predator_x, predator_y, predator_res, res_x, res_y, predator_opt_x, predator_opt_y, predator_hunger, delete_res, delete_cage, delete_predator, predator_hunger_koll
    if len(predators) > 0:
        delete_cage = []
        delete_predator = []
        delete_res = []
        for i in range(len(predators)):
            predator_x, predator_y, predator_res, predator_hunger = predators[i].x, predators[i].y, predators_res[i], \
                                                                    predators_hungers[i]
            if len(cages) > 0:
                predator_opt_x, predator_opt_y, re = predator_opt_x_and_y(predator_x, predator_y)
            else:
                break
            if predator_hunger < predator_hunger_koll:
                if predator_res == 1:
                    Chance = random.randint(1, 10)
                    if Chance == 5:
                        create_predators((x + random.randint(-10, 10), y + random.randint(-10, 10)), 1)
                    else:
                        predators_hungers[i] = 0
                        predators_res[i] = 0
                else:
                    if predator_opt_x > predator_x:
                        predator_x += predator_speed
                    elif predator_opt_x < predator_x:
                        predator_x += -predator_speed

                    if predator_opt_y > predator_y:
                        predator_y += predator_speed
                    elif predator_opt_y < predator_y:
                        predator_y += -predator_speed

                    if predator_x < predator_opt_x + 10 and predator_x > predator_opt_x - 10 and predator_y > predator_opt_y - 10 and predator_y < predator_opt_y + 10:
                        predators_res[i] = 1
                        if cages[re] in delete_cage:
                            pass
                        else:
                            delete_cage.append(re)

                    if predator_x <= 0:
                        predator_x = 1100
                    elif predator_x >= 1200:
                        predator_x = 100

                    if predator_y <= 0:
                        predator_y = 700
                    elif predator_y >= 800:
                        predator_y = 100
                predators_hungers[i] += 1
            else:
                if predators[i] in delete_predator:
                    pass
                else:
                    delete_predator.append(i)
            predators[i] = pg.draw.circle(win, (255, 255, 255), (predator_x + 4, predator_y + 4), 4)

        for i in range(len(delete_predator)):
            try:
                try:
                    predators.pop(delete_predator[i])
                except IndexError:
                    predators.pop()
                try:
                    predators_res.pop(delete_predator[i])
                except IndexError:
                    predators_res.pop()
                try:
                    predators_hungers.pop(delete_predator[i])
                except IndexError:
                    predators_hungers.pop()
            except Exception:
                continue

        for i in range(len(delete_cage)):
            try:
                try:
                    cages.pop(delete_cage[i])
                except IndexError:
                    cages.pop()
                try:
                    cages_res.pop(delete_cage[i])
                except IndexError:
                    cages_res.pop()
                try:
                    hungers.pop(delete_cage[i])
                except IndexError:
                    hungers.pop()
            except Exception:
                continue

    else:
        return False

for i in range(cage_kol):
    create_cage((randrange(400, 800), randrange(200, 600)), 1)

for i in range(predator_kol):
    create_predators((randrange(400, 800), randrange(200, 600)), 1)

create_res(res_kol)

while True:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                create_cage(i.pos, 1)
                print("Cage has be create in position:", i.pos)
            elif i.button == 2:
                create_predators(i.pos, 1)
            elif i.button == 3:
                res_kol -= 100
                print('Res_kol:', res_kol)
        elif i.type == pg.KEYDOWN:
            if i.key == pg.K_1:
                FPS += 1
                print('FPS:', FPS)
            elif i.key == pg.K_2:
                if FPS > 1:
                    FPS -= 1
                    print('FPS:', FPS)
            elif i.key == pg.K_3:
                FPS += 10
                print('FPS:', FPS)
            elif i.key == pg.K_4:
                if FPS > 10:
                    FPS -= 10
                    print('FPS:', FPS)
            elif i.key == pg.K_5:
                res_kol += 10
                print('Res_kol:', res_kol)
            elif i.key == pg.K_6:
                if res_kol > 10:
                    res_kol -= 10
                    print('Res_kol:', res_kol)
            elif i.key == pg.K_7:
                slow()
            elif i.key == pg.K_9:
                for i in range(10):
                    create_predators((randrange(400, 800), randrange(200, 600)), 1)
            elif i.key == pg.K_0:
                pause()

    pg.display.set_caption(str(int(clock.get_fps())))
    win.fill((0, 0, 0))
    cage_update()
    predator_update()
    pg.display.update()
    clock.tick(FPS)
pg.quit
