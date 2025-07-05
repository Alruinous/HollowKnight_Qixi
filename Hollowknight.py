import sys

import pygame
import sys
import time
import os
from pygame.locals import *

pygame.init()

# 窗口设置
size = width, height = 1200, 725
screen = pygame.display.set_mode(size)
pygame.display.set_caption("空洞骑士 · 七夕")
# 图片加载
image_null = pygame.image.load("./assets/image_null.png")
background_place = (0, 25)

background = pygame.image.load("./assets/游戏背景/封面/主界面.png")

scene_bluelake = pygame.image.load("./assets/游戏背景/关卡/1蓝湖.png")
scene_mapseller = pygame.image.load("./assets/游戏背景/关卡/2关卡.png")
scene_crossroad = pygame.image.load("./assets/游戏背景/关卡/3关卡.png")
scene_beforelift = pygame.image.load("./assets/游戏背景/关卡/4电梯前走廊.png")
scene_liftup = pygame.image.load("./assets/游戏背景/关卡/5上电梯.png")
scene_liftdown = pygame.image.load("./assets/游戏背景/关卡/6下电梯.png")
scene_beforerain = pygame.image.load("./assets/游戏背景/关卡/7关卡.png")
scene_rainroad = pygame.image.load("./assets/游戏背景/关卡/8雨中走廊.png")
scene_beforeend = pygame.image.load("./assets/游戏背景/关卡/9小姐姐门前.png")
scene_end = pygame.image.load("./assets/游戏背景/关卡/10end.png")

# white_enemies
images_white_enemyl = []
images_white_enemyr = []
for i in range(1, 4):
    image_white_enemyl = pygame.image.load(f"./assets/enemys/white_enemies/white_enemy_0{i}.png")
    image_white_enemyr = pygame.transform.flip(image_white_enemyl, True, False)
    images_white_enemyl.append(image_white_enemyl)
    images_white_enemyr.append(image_white_enemyr)

#black_enemies
images_black_enemyl = []
images_black_enemyr = []
for i in range(1, 4):
    image_black_enemyl = pygame.image.load(f"./assets/enemys/black_enemies/black_enemy{i}.png")
    image_black_enemyr = pygame.transform.flip(image_black_enemyl, True, False)
    images_black_enemyl.append(image_black_enemyl)
    images_black_enemyr.append(image_black_enemyr)

#bigflies
images_bigfly_enemyl = []
images_bigfly_enemyr = []
for i in range(1, 5):
    image_bigfly_enemyl = pygame.image.load(f"./assets/enemys/bigflies/bigfly{i}.png")
    image_bigfly_enemyr = pygame.transform.flip(image_bigfly_enemyl, True, False)
    images_bigfly_enemyl.append(image_bigfly_enemyl)
    images_bigfly_enemyr.append(image_bigfly_enemyr)

#bigenemies
images_bigenemy_enemyl = []
images_bigenemy_enemyr = []
for i in range(1, 5):
    image_bigenemy_enemyl = pygame.image.load(f"./assets/enemys/big_enemies/big_enemy{i}.png")
    image_bigenemy_enemyr = pygame.transform.flip(image_bigenemy_enemyl, True, False)
    images_bigenemy_enemyl.append(image_bigenemy_enemyl)
    images_bigenemy_enemyr.append(image_bigenemy_enemyr)

life = [background]
life2 = [background]
for i in range(1,7):
    image = pygame.image.load(f"./assets/knight/life/life{i}.png")
    image2 = pygame.transform.flip(image, True, False)
    life.append(image)
    life2.append(image2)


image_stop_l = pygame.image.load("./assets/knight/stop/stop.PNG")
image_stop_r = pygame.transform.flip(image_stop_l, True, False)

#音乐加载
knight_walk = pygame.mixer.Sound("./assets/music/knight/walk.wav")
knight_walk.set_volume(0.1)
knight_jump = pygame.mixer.Sound("./assets/music/knight/jump.wav")
knight_jump.set_volume(0.4)
knight_land = pygame.mixer.Sound("./assets/music/knight/land_soft.wav")
knight_land.set_volume(0.2)
knight_harm = pygame.mixer.Sound("./assets/music/knight/harm.wav")
knight_harm.set_volume(1)
knight_sword = pygame.mixer.Sound("./assets/music/knight/sword_3.wav")
knight_sword.set_volume(0.2)
ui_load = pygame.mixer.Sound("./assets/music/ui_load.wav")
ui_load.set_volume(0.2)
ui_botton = pygame.mixer.Sound("./assets/music/ui_button_confirm.wav")
ui_botton.set_volume(0.8)
meeting = pygame.mixer.Sound("./assets/music/meeting.ogg")
meeting.set_volume(1)

greenland = pygame.mixer.Sound("./assets/music/greenland.ogg")
greenland.set_volume(1)

finghting = pygame.mixer.Sound("./assets/music/finghting.ogg")
finghting.set_volume(1)

# 帧率设置
FPS = 60
clock = pygame.time.Clock()

# 全局变量
barriers = []
barriers_sprite_group = pygame.sprite.Group()

enemies_sprite_group = pygame.sprite.Group()
enemies_sprite_group2 = pygame.sprite.Group()

vy_max = 20
vy_jump0 = -10  # vy_max 需要大于 vy_jump0
a_gravity = 1.5
flag_jumpdown = 0
jump_lastkey = pygame.K_k
jump_lastkey2 = pygame.K_2
flag_jumptime = 1
height_jumpbefore = 0
height_jumpbefore2 = 0
height_jumpmax = 200
last_attacktime = 0
last_harmtime = 0
last_walktime = 0
black = (0, 0, 0)


def between_anime(time):
    while True:
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        pygame.time.wait(time)
        return

class Videoplay(pygame.sprite.Sprite):
    def __init__(self):
        super(Videoplay, self).__init__()  # 调用父类的__init__方法初始化对象

        self.counter = 0
        self.page_now = 0
        self.images = [image_null]
        self.image = self.images[self.page_now]
        self.rect = (0, 25)
        self.speed = 7
        self.over = 0
    def update(self):
        self.counter += 1
        if self.counter >= self.speed and self.page_now < len(self.images) - 1:
            self.counter = 0
            self.page_now += 1
            self.image = self.images[self.page_now]
        if self.page_now >= len(self.images) - 1 and self.counter >= self.speed:
            self.page_now = 0
            self.counter = 0
            self.over = 1

class Barrier(pygame.sprite.Sprite):
    def __init__(self):
        super(Barrier, self).__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)


class Knife(pygame.sprite.Sprite):
    def __init__(self):
        super(Knife, self).__init__()
        self.counter = 0
        self.gif_speed = 5
        self.page_now = 0
        self.images = [image_stop_r]
        self.image = self.images[self.page_now]
        self.rect = self.image.get_rect(center = (0,0))
        self.images_attack_endl = []
        self.images_attack_endr = []
        self.images_attackup_endl = []
        self.images_attackup_endr = []

        # attack_end
        for i in range(1, 6):
            image_attack_endl = pygame.image.load(f"./assets/knight/attack/left/Attack_end{i}.PNG")
            image_attack_endr = pygame.transform.flip(image_attack_endl, True, False)
            self.images_attack_endl.append(image_attack_endl)
            self.images_attack_endr.append(image_attack_endr)

        for i in range(1, 6):
            image_attackup_endl = pygame.image.load(f"./assets/knight/attack/up/AttackTop_end{i}.PNG")
            image_attackup_endr = pygame.transform.flip(image_attackup_endl, True, False)
            self.images_attackup_endl.append(image_attackup_endl)
            self.images_attackup_endr.append(image_attackup_endr)

    def update(self, op, facing):
        if op==3 and facing==1:
            self.images = self.images_attack_endl
        elif op==3 and facing==2:
            self.images = self.images_attack_endr
        elif op==4 and facing==1:
            self.images = self.images_attackup_endl
        elif op==4 and facing==2:
            self.images = self.images_attackup_endr
        self.counter += 1
        self.image = self.images[self.page_now]
        if self.counter >= self.gif_speed and self.page_now < len(self.images) - 1:
            self.counter = 0
            self.page_now += 1
            self.image = self.images[self.page_now]
        if self.page_now >= len(self.images) - 1 and self.counter >= self.gif_speed:
            self.page_now = 0
            self.counter = 0
knife = Knife()
knife_group = pygame.sprite.Group(knife)

class Stick_enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Stick_enemy, self).__init__()  # 调用父类的__init__方法初始化对象
        self.image = pygame.image.load("./assets/enemys/stick.png")
        self.rect = self.image.get_rect(center = (0,0))

    def move(self):
        self.rect = self.rect.move_ip(0, 3)

class White_enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(White_enemy, self).__init__()  # 调用父类的__init__方法初始化对象
        self.life = 4
        self.facing = 2
        self.speed = 3

        self.counter = 0
        self.gif_speed = 8
        self.page_now = 0
        self.images = [image_white_enemyr]
        self.image = self.images[self.page_now]
        self.rect = self.image.get_rect(center=(20, 20))
        self.road_left = 0
        self.road_right = 0

    def move(self):
        if self.facing == 1:
            if self.rect.left <= self.road_left:
                self.facing = 2
            else:
                self.rect.move_ip(-self.speed, 0)
        elif self.facing == 2:
            if self.rect.right >= self.road_right:
                self.facing = 1
            else:
                self.rect.move_ip(self.speed, 0)
        self.update(self.facing)

    def update(self, facing):
        if facing == 1:
            self.images = images_white_enemyl
        elif facing == 2:
            self.images = images_white_enemyr

        self.counter += 1
        if self.counter >= self.gif_speed and self.page_now < len(self.images) - 1:
            self.counter = 0
            self.page_now += 1
            self.image = self.images[self.page_now]
        if self.page_now >= len(self.images) - 1 and self.counter >= self.gif_speed:
            self.page_now = 0
            self.counter = 0

class Black_enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Black_enemy, self).__init__()  # 调用父类的__init__方法初始化对象
        self.life = 3
        self.facing = 2
        self.speed = 2

        self.counter = 0
        self.gif_speed = 8
        self.page_now = 0
        self.images = [image_black_enemyr]
        self.image = self.images[self.page_now]
        self.rect = self.image.get_rect(center=(20, 20))
        self.road_left = 0
        self.road_right = 0

    def move(self):
        if self.facing == 1:
            if self.rect.left <= self.road_left:
                self.facing = 2
            else:
                self.rect.move_ip(-self.speed, 0)
        elif self.facing == 2:
            if self.rect.right >= self.road_right:
                self.facing = 1
            else:
                self.rect.move_ip(self.speed, 0)
        self.update(self.facing)

    def update(self, facing):
        if facing == 1:
            self.images = images_black_enemyl
        elif facing == 2:
            self.images = images_black_enemyr

        self.counter += 1
        if self.counter >= self.gif_speed and self.page_now < len(self.images) - 1:
            self.counter = 0
            self.page_now += 1
            self.image = self.images[self.page_now]
        if self.page_now >= len(self.images) - 1 and self.counter >= self.gif_speed:
            self.page_now = 0
            self.counter = 0

class Bigfly_enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Bigfly_enemy, self).__init__()  # 调用父类的__init__方法初始化对象
        self.life = 2
        self.facing = 2
        self.speed = 4

        self.counter = 0
        self.gif_speed = 8
        self.page_now = 0
        self.images = [image_bigfly_enemyl]
        self.image = self.images[self.page_now]
        self.rect = self.image.get_rect(center=(20, 20))
        self.road_left = 0
        self.road_up = 0
        self.width = 0
        self.height = 0
        self.flagup = 0
        self.vy = 5
    def move(self):
        if self.facing == 1:
            if self.rect.left <= self.road_left:
                self.facing = 2
            else:
                self.rect.move_ip(-self.speed, 0)
        elif self.facing == 2:
            if self.rect.right >= self.road_left + self.width:
                self.facing = 1
            else:
                self.rect.move_ip(self.speed, 0)

        if self.flagup == 0:
            self.rect.move_ip(0, self.vy)
        else:
            self.rect.move_ip(0, -self.vy)

        if self.rect.bottom >= self.road_up + self.height:
            self.flagup = 1
        elif self.rect.top <= self.road_up:
            self.flagup = 0

        self.update(self.facing)

    def update(self, facing):
        if facing == 1:
            self.images = images_bigfly_enemyl
        elif facing == 2:
            self.images = images_bigfly_enemyr

        self.counter += 1
        if self.counter >= self.gif_speed and self.page_now < len(self.images) - 1:
            self.counter = 0
            self.page_now += 1
            self.image = self.images[self.page_now]
        if self.page_now >= len(self.images) - 1 and self.counter >= self.gif_speed:
            self.page_now = 0
            self.counter = 0

class Big_enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Big_enemy, self).__init__()  # 调用父类的__init__方法初始化对象
        self.life = 6
        self.facing = 1
        self.speed = 7

        self.counter = 0
        self.gif_speed = 8
        self.page_now = 0
        self.images = [image_bigenemy_enemyl]
        self.image = self.images[self.page_now]
        self.rect = self.image.get_rect(center=(20, 20))
        self.road_left = 0
        self.road_right = 0

    def move(self):
        if self.facing == 1:
            if self.rect.left <= self.road_left:
                self.facing = 2
            else:
                self.rect.move_ip(-self.speed, 0)
        elif self.facing == 2:
            if self.rect.right >= self.road_right:
                self.facing = 1
            else:
                self.rect.move_ip(self.speed, 0)
        self.update(self.facing)

    def update(self, facing):
        if facing == 1:
            self.images = images_bigenemy_enemyl
        elif facing == 2:
            self.images = images_bigenemy_enemyr

        self.counter += 1
        if self.counter >= self.gif_speed and self.page_now < len(self.images) - 1:
            self.counter = 0
            self.page_now += 1
            self.image = self.images[self.page_now]
        if self.page_now >= len(self.images) - 1 and self.counter >= self.gif_speed:
            self.page_now = 0
            self.counter = 0


class Knight(pygame.sprite.Sprite):
    def __init__(self):
        super(Knight, self).__init__()  # 调用父类的__init__方法初始化对象

        # 小骑士基本属性
        self.life = 6
        self.walk_speed = 7
        self.harm_speed = 7
        self.harm = 1  #攻击力
        self.goldtime = 1500
        self.harm_move_time = 300
        self.harming = 0
        self.harm_moving = 0
        self.op = 0  # 小骑士行动状态: 0静止， 1走路， 2跳跃, 3左右攻击， 4上劈, 5受伤
        self.facing = 1  # 小骑士朝向：1左， 2右
        self.ontheground = 1  # 判断小骑士是否在地上，1在0不在
        self.attack_range = 120
        self.attack_cd = 600
        self.attacking = 0
        self.jumping = 0
        self.vy = 0
        self.images = [image_stop_r]
        self.images_attackend = []


        # walk图列表
        self.images_walk_l = []
        self.images_walk_r = []
        # jump图列表
        self.images_jump_l = []
        self.images_jump_r = []
        # attack图列表
        self.images_attackup_l = []
        self.images_attackup_r = []
        self.images_attack_l = []
        self.images_attack_r = []
        self.images_attack_endl = []
        self.images_attack_endr = []
        self.images_attackup_endl = []
        self.images_attackup_endr = []
        # 将图片导入动图列表
        for i in range(1, 5):  # walk
            image_walk_l = pygame.image.load(f"./assets/knight/walk/Walk_{i}.PNG")
            image_walk_r = pygame.transform.flip(image_walk_l, True, False)
            self.images_walk_l.append(image_walk_l)
            self.images_walk_r.append(image_walk_r)
        for i in range(1, 16):  # jump
            image_jump_l = pygame.image.load(f"./assets/knight/jump/Jump_{i}.PNG")
            image_jump_r = pygame.transform.flip(image_jump_l, True, False)
            self.images_jump_l.append(image_jump_l)
            self.images_jump_r.append(image_jump_r)
        for i in range(1, 6):  # attack
            image_attack_l = pygame.image.load(f"./assets/knight/attack/left/Attack_{i}.PNG")
            image_attack_r = pygame.transform.flip(image_attack_l, True, False)
            self.images_attack_l.append(image_attack_l)
            self.images_attack_r.append(image_attack_r)
        for i in range(1, 6):  # attackup
            image_attackup_l = pygame.image.load(f"./assets/knight/attack/up/AttackTop_{i}.PNG")
            image_attackup_r = pygame.transform.flip(image_attackup_l, True, False)
            self.images_attackup_l.append(image_attackup_l)
            self.images_attackup_r.append(image_attackup_r)
        self.page_now = 0
        self.image = self.images[self.page_now]
        self.rect = self.image.get_rect(center=(0, 0))
        self.counter = 0

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        flag_stop = 0
        global jump_lastkey, height_jumpbefore, height_jumpmax, last_harmtime, last_attacktime, last_walktime
        if pygame.time.get_ticks() - last_attacktime >= self.attack_cd:
            self.attacking = 0
        if pygame.time.get_ticks() - last_harmtime >= self.goldtime:
            self.harming = 0

        if pygame.time.get_ticks() - last_harmtime <= self.harm_move_time:
            self.harm_moving = 1
        else:
            self.harm_moving = 0

        if self.harm_moving == 1:
            self.harm_move(self.facing)
            return

        # 左右行走
        if pressed_keys[K_a]:
            if self.attacking != 1:
                self.op = 1
                self.facing = 1
            self.rect.move_ip(-self.walk_speed, 0)
            flag_stop = 1
            if pygame.sprite.spritecollide(self, barriers_sprite_group, False):
                self.rect.move_ip(self.walk_speed, 0)
                flag_stop = 1
        elif pressed_keys[K_d]:
            if self.attacking != 1:
                self.op = 1
                self.facing = 2
            self.rect.move_ip(self.walk_speed, 0)
            flag_stop = 1
            if pygame.sprite.spritecollide(self, barriers_sprite_group, False):
                self.rect.move_ip(-self.walk_speed, 0)
                flag_stop = 1
        # 确保一次攻击
        if self.attacking == 1:
            gravity_move(self)
            self.update(self.op, self.facing)
            if self.op == 1:
                knight_walk.play()
            return

        # 跳跃
        if (height_jumpbefore - self.rect.bottom) <= height_jumpmax:
            if pressed_keys[K_k]:
                if (self.rect.bottom - find_barrier_max_h(self)) == 0 or (jump_lastkey == pygame.K_k):
                    if self.rect.bottom - find_barrier_max_h(self) == 0:
                        knight_jump.play()
                    self.op = 2
                    self.vy = vy_jump0
                    flag_stop = 1
            if (self.rect.bottom - find_barrier_max_h(self)) != 0 and not pressed_keys[K_k]:  # 代表k未连续按下
                jump_lastkey = pygame.K_0
        else:
            jump_lastkey = pygame.K_0

        # 攻击
        # if self.attacking == 0:
        if pygame.time.get_ticks() - last_attacktime >= self.attack_cd:
            if pressed_keys[K_j] and pressed_keys[K_w]:
                self.op = 4
                flag_stop = 1
                self.attacking = 1
            elif pressed_keys[K_j]:
                self.op = 3
                flag_stop = 1
                self.attacking = 1

            if self.op == 3:
                (x, y) = self.rect.left, self.rect.top
                if self.facing == 1:
                    knife.rect.left, knife.rect.top = x - self.attack_range, y
                elif self.facing == 2:
                    knife.rect.left, knife.rect.top = x + self.attack_range, y
            elif self.op == 4:
                (x, y) = self.rect.left, self.rect.top
                knife.rect.left, knife.rect.top = x, y - self.attack_range

            if pressed_keys[K_j]:
                last_attacktime = pygame.time.get_ticks()
                knight_sword.play()

                enemy = pygame.sprite.spritecollideany(knife, enemies_sprite_group)
                if enemy:
                    enemy.life -= knight.harm
                    print(enemy.life)
                    if enemy.life <= 0:
                        enemy.kill()

        # 重力向下
        gravity_move(self)

        #受伤
        if self.harming == 0:
            if pygame.sprite.spritecollide(self, enemies_sprite_group, False):
                self.life -= 1
                self.harming = 1
                self.op = 5
                flag_stop = 0
                last_harmtime = pygame.time.get_ticks()
                knight_harm.play()

                self.harm_move(self.facing)

        if (self.rect.bottom - find_barrier_max_h(self)) == 0:  # 判断是否回到地面，刷新跳跃的前一键
            jump_lastkey = pygame.K_k
            height_jumpbefore = self.rect.bottom
        if flag_stop == 0:
            self.op = 0
            return

        #放音效
        if self.op == 1 and pygame.time.get_ticks() - last_walktime >= knight_walk.get_length():
            knight_walk.play()
            last_walktime = pygame.time.get_ticks()
        self.update(self.op, self.facing)


    def harm_move(self, facing):
        if facing == 1:
            self.rect.move_ip(self.harm_speed, 0)
            if pygame.sprite.spritecollide(self, barriers_sprite_group, False):
                self.rect.move_ip(-self.harm_speed, 0)
        elif facing == 2:
            self.rect.move_ip(-self.harm_speed, 0)
            if pygame.sprite.spritecollide(self, barriers_sprite_group, False):
                self.rect.move_ip(self.harm_speed, 0)
        gravity_move(self)

    def update(self, op, facing):
        global last_attacktime
        # attack
        if (op == 3 and facing == 1):
            self.images = self.images_attack_l
        elif (op == 3 and facing == 2):
            self.images = self.images_attack_r
        elif (op == 4 and facing == 1):
            self.images = self.images_attackup_l
        elif (op == 4 and facing == 2):
            self.images = self.images_attackup_r
        # jump
        elif (op == 2 and facing == 1):
            self.images = self.images_jump_l
        elif (op == 2 and facing == 2):
            self.images = self.images_jump_r
        # walk
        elif (op == 1 and facing == 1):
            self.images = self.images_walk_l
        elif (op == 1 and facing == 2):
            self.images = self.images_walk_r

        gif_speed = [0, 3.5, 2, 3, 3]  # 1走路， 2跳跃, 3左右攻击， 4上劈

        self.counter += 1


        if self.counter >= gif_speed[op] and self.page_now < len(self.images) - 1:
            self.counter = 0
            self.page_now += 1
            self.image = self.images[self.page_now]
            if op == 3:
                (x, y) = self.rect.left, self.rect.top
                if facing == 1:
                    knife.rect.left, knife.rect.top = x - self.attack_range, y
                elif facing == 2:
                    knife.rect.left, knife.rect.top = x + self.attack_range, y
            elif op == 4:
                (x, y) = self.rect.left, self.rect.top
                knife.rect.left, knife.rect.top = x, y - self.attack_range

        if self.page_now >= len(self.images) - 1 and self.counter >= gif_speed[op]:
            self.page_now = 0
            self.counter = 0
            self.attacking = 0

        knife.update(op, facing)

def find_barrier_max_h(knight):  #查询knight下方最近障碍物的y
    barrier_max_h = 10000
    for barrier in barriers:
        if knight.rect.bottom <= barrier.rect.top:
            if barrier.rect.right > knight.rect.left and not barrier.rect.left > knight.rect.right:
                if barrier.rect.top < barrier_max_h:
                    barrier_max_h = barrier.rect.top
    return barrier_max_h

def find_barrier_min_h(knight):  #查询knight上方最近障碍物的y
    barrier_min_h = -100
    for barrier in barriers:
        if knight.rect.top >= barrier.rect.bottom:
            if barrier.rect.right > knight.rect.left and not barrier.rect.left > knight.rect.right:
                if barrier.rect.bottom > barrier_min_h:
                    barrier_min_h = barrier.rect.bottom
    return barrier_min_h


def gravity_move(knight):
    barrier_max_h = find_barrier_max_h(knight)
    barrier_min_h = find_barrier_min_h(knight)
    h = knight.vy + a_gravity / 2
    if knight.vy > 0 and knight.vy < vy_max:
        if knight.vy + a_gravity > vy_max:
            h = (vy_max - knight.vy) / a_gravity * (knight.vy + vy_max) / 2 + (1 - (vy_max - knight.vy) / a_gravity) * vy_max  # 如果半路加到vy_max

    if knight.rect.bottom + h > barrier_max_h:
        knight.rect.bottom = barrier_max_h
        knight.vy = 0

    elif knight.rect.top + h < barrier_min_h:
        knight.rect.top = barrier_min_h
        knight.vy = 0
    else:
            knight.rect.bottom += h
            if knight.vy + a_gravity > vy_max:
                knight.vy = vy_max
            else:
                knight.vy = knight.vy + a_gravity



# 游戏开始
knight = Knight()

def video_flower():
    video_flower_images = []
    for i in range(1, 28):
        image = pygame.image.load(f"./assets/其他/娇嫩的花/{i}.png")
        video_flower_images.append(image)

    video_flower = Videoplay()
    video_flower_group = pygame.sprite.Group(video_flower)
    video_flower.images = video_flower_images
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        video_flower.update()
        video_flower_group.draw(screen)
        pygame.display.update()
        clock.tick(FPS)
        if video_flower.over == 1:
            return

def video_lift():
    liftsound = pygame.mixer.Sound("./assets/music/liftsound.ogg")
    liftsound.set_volume(0.2)

    video_lift_images = []
    for i in range(0, 92):
        image = pygame.image.load(f"./assets/其他/电梯下降/电梯下降{i}.png")
        video_lift_images.append(image)

    video_lift = Videoplay()
    video_lift.speed = 3
    video_lift_group = pygame.sprite.Group(video_lift)
    video_lift.images = video_lift_images
    liftsound.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        video_lift.update()
        video_lift_group.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

        if video_lift.over == 1:
            return


def video_getflower():
    video_getflower_images = []
    for i in range(1, 25):
        image = pygame.image.load(f"./assets/其他/花已送/{i}.png")
        video_getflower_images.append(image)

    video_getflower = Videoplay()
    video_getflower.speed = 8
    video_getflower_group = pygame.sprite.Group(video_getflower)
    video_getflower.images = video_getflower_images
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        video_getflower.update()
        video_getflower_group.draw(screen)
        pygame.display.update()
        clock.tick(FPS)
        if video_getflower.over == 1:
            return

def video_waiting1():
    video_waiting1_images = []
    for i in range(1, 11):
        img = pygame.image.load(f"./assets/游戏背景/敬请期待/敬请期待1/{i}.png")
        video_waiting1_images.append(img)

    video_waiting1 = Videoplay()
    video_waiting1_group = pygame.sprite.Group(video_waiting1)
    video_waiting1.images = video_waiting1_images
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        video_waiting1.update()
        video_waiting1_group.draw(screen)
        pygame.display.update()
        clock.tick(FPS)
        if video_waiting1.over == 1:
            return

def video_waiting2():
    video_waiting2_images = []
    for i in range(1, 14):
        img = pygame.image.load(f"./assets/游戏背景/敬请期待/敬请期待2/{i}.png")
        video_waiting2_images.append(img)

    video_waiting2 = Videoplay()
    video_waiting2_group = pygame.sprite.Group(video_waiting2)
    video_waiting2.images = video_waiting2_images
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        video_waiting2.update()
        video_waiting2_group.draw(screen)
        pygame.display.update()
        clock.tick(FPS)
        if video_waiting2.over == 1:
            return

def video_beforegame1():
    font = pygame.font.SysFont("华文楷体", 25)
    txt = font.render("Press space to skip", True, (255, 255, 255))
    txt_rect = txt.get_rect()
    txt_rect.center = (1000, 600)

    video_beforegame1_images = []
    for i in range(1, 61):
        img = pygame.image.load(f"./assets/游戏背景/game1剧情/beforegame1_1/{i}.png")
        video_beforegame1_images.append(img)
    for i in range(1, 61):
        img = pygame.image.load(f"./assets/游戏背景/game1剧情/beforegame1_2/{i}.png")
        video_beforegame1_images.append(img)
    for i in range(1, 61):
        img = pygame.image.load(f"./assets/游戏背景/game1剧情/beforegame1_3/{i}.png")
        video_beforegame1_images.append(img)
    for i in range(1, 44):
        img = pygame.image.load(f"./assets/游戏背景/game1剧情/beforegame1_4/{i}.png")
        video_beforegame1_images.append(img)

    video_beforegame1 = Videoplay()
    video_beforegame1_group = pygame.sprite.Group(video_beforegame1)
    video_beforegame1.images = video_beforegame1_images
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
        video_beforegame1.update()
        video_beforegame1_group.draw(screen)
        screen.blit(txt, txt_rect.center)
        pygame.display.update()
        clock.tick(FPS)
        if video_beforegame1.over == 1:
            return

def menu_window():
    meeting.play()

    font = pygame.font.SysFont("华文楷体", 25)
    txt = font.render("made by lorian", True, (255, 255, 255))
    txt_rect = txt.get_rect()
    txt_rect.center = (1000, 660)

    font_menu1 = pygame.font.SysFont("华文楷体", 80)
    font_menu2 = pygame.font.SysFont("华文楷体", 40)
    txt_menu1 = font_menu1.render("单人主线", True, (255, 255, 255))
    txt_menu2 = font_menu1.render("双人对战", True, (255, 255, 255))
    txt_menu1_rect = txt_menu1.get_rect()
    txt_menu2_rect = txt_menu2.get_rect()
    txt_menu1_rect.center = (650, 355)
    txt_menu2_rect.center = (650, 495)
    txt_menu11 = font_menu2.render("Press 1", True, (255, 255, 255))
    txt_menu21 = font_menu2.render("Press 2", True, (255, 255, 255))
    txt_menu11_rect = txt_menu11.get_rect()
    txt_menu21_rect = txt_menu21.get_rect()
    txt_menu11_rect.center = (1010, 395)
    txt_menu21_rect.center = (1010, 535)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                ui_botton.play()
                meeting.fadeout(1000)
                return 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                ui_botton.play()
                meeting.fadeout(1000)
                return 2

        screen.blit(background, background_place)
        screen.blit(txt_menu1, txt_menu1_rect.center)
        screen.blit(txt_menu2, txt_menu2_rect.center)
        screen.blit(txt_menu11, txt_menu11_rect.center)
        screen.blit(txt_menu21, txt_menu21_rect.center)
        screen.blit(txt, txt_rect.center)
        rect1 = pygame.Rect(0, 0, 1200, 25)
        rect2 = pygame.Rect(0, 700, 1200, 25)
        pygame.draw.rect(screen, black, rect1)
        pygame.draw.rect(screen, black, rect2)
        pygame.display.update()
        clock.tick(FPS)


def game_window1_1():
    knight.rect.center = (550, 400)
    knight.facing = 2
    height_jumpbefore = knight.rect.bottom
    knight_group = pygame.sprite.Group(knight)

    barrier_ground = Barrier()
    barrier_ground.rect = pygame.Rect(330, 530, width, 30)
    barriers.append(barrier_ground)
    barriers_sprite_group.add(barrier_ground)

    while True:
        screen.blit(scene_bluelake, background_place)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        knight.move()
        if knight.op != 0:
            knight_group.draw(screen)
            if knight.op==3 or knight.op==4:
                knife_group.draw(screen)
        elif (knight.op == 0 and knight.facing == 1):
            screen.blit(image_stop_l, knight.rect)
        elif (knight.op == 0 and knight.facing == 2):
            screen.blit(image_stop_r, knight.rect)
        rect1 = pygame.Rect(0, 0, 1200, 25)
        rect2 = pygame.Rect(0, 700, 1200, 25)
        pygame.draw.rect(screen, black, rect1)
        pygame.draw.rect(screen, black, rect2)
        if knight.rect.bottom > 710:  #掉河里
            knight.life -= 1
            knight_harm.play()
            knight.rect.center = (350, 400)
            between_anime(200)

        screen.blit(life[knight.life], background_place)
        pygame.display.update()
        clock.tick(FPS)

        if knight.rect.left > 1170 and 400 < knight.rect.top < 500:
            between_anime(500)
            barriers_sprite_group.empty()
            barriers.clear()
            return


def game_window1_2():
    knight.rect.center = (20, 580)
    knight.facing = 2
    height_jumpbefore = knight.rect.bottom
    knight_group = pygame.sprite.Group(knight)

    barrier_ground1 = Barrier()
    barrier_ground1.rect = pygame.Rect(-200, 630, 790, 30)
    barriers.append(barrier_ground1)
    barriers_sprite_group.add(barrier_ground1)

    barrier_ground2 = Barrier()
    barrier_ground2.rect = pygame.Rect(930, 630, 790, 30)
    barriers.append(barrier_ground2)
    barriers_sprite_group.add(barrier_ground2)

    step = pygame.image.load("./assets/游戏背景/关卡/2关卡台阶.png")
    step_rect = (800, 420)
    barrier_step = Barrier()
    barrier_step.rect = pygame.Rect(810, 425, 80, 80)
    barriers.append(barrier_step)
    barriers_sprite_group.add(barrier_step)

    barrier_1 = Barrier()
    barrier_1.rect = pygame.Rect(511, 420, 85, 80)
    barriers.append(barrier_1)
    barriers_sprite_group.add(barrier_1)

    barrier_2 = Barrier()
    barrier_2.rect = pygame.Rect(640, 205, 85, 80)
    barriers.append(barrier_2)
    barriers_sprite_group.add(barrier_2)

    barrier_wall = Barrier()
    barrier_wall.rect = pygame.Rect(1200, 0, 30, height)
    barriers.append(barrier_wall)
    barriers_sprite_group.add(barrier_wall)

    barrier_wall2 = Barrier()
    barrier_wall2.rect = pygame.Rect(-50, 0, 50, height)
    barriers.append(barrier_wall2)
    barriers_sprite_group.add(barrier_wall2)

    enemy1 = White_enemy()
    enemy1.rect.center = (900, 600)
    enemy1.road_left, enemy1.road_right = 900, 1200
    enemies_sprite_group.add(enemy1)

    while True:
        screen.blit(scene_mapseller, background_place)
        screen.blit(step, step_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        knight.move()
        enemy1.move()
        # for enemy in enemies_sprite_group:
        #     enemy.move()
        if knight.op != 0:
            knight_group.draw(screen)
            if knight.op == 3 or knight.op == 4:
                knife_group.draw(screen)
        elif (knight.op == 0 and knight.facing == 1):
            screen.blit(image_stop_l, knight.rect)
        elif (knight.op == 0 and knight.facing == 2):
            screen.blit(image_stop_r, knight.rect)

        rect1 = pygame.Rect(0, 0, 1200, 25)
        rect2 = pygame.Rect(0, 700, 1200, 25)
        pygame.draw.rect(screen, black, rect1)
        pygame.draw.rect(screen, black, rect2)
        if knight.rect.bottom > 710:  #掉下去
            knight.life -= 1
            knight_harm.play()
            knight.rect.center = (950, 540)
            between_anime(200)

        screen.blit(life[knight.life], background_place)
        enemies_sprite_group.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

        if knight.rect.bottom < 30 and 610 < knight.rect.left < 750:
            between_anime(500)
            barriers_sprite_group.empty()
            barriers.clear()
            enemies_sprite_group.empty()
            return

def game_window1_3():
    knight.rect.center = (940, 490)
    knight.facing = 2
    height_jumpbefore = knight.rect.bottom
    knight_group = pygame.sprite.Group(knight)

    barrier_ground1 = Barrier()
    barrier_ground1.rect = pygame.Rect(-200, 585, 930, 30)
    barriers.append(barrier_ground1)
    barriers_sprite_group.add(barrier_ground1)

    barrier_ground2 = Barrier()
    barrier_ground2.rect = pygame.Rect(915, 585, width, 30)
    barriers.append(barrier_ground2)
    barriers_sprite_group.add(barrier_ground2)

    barrier_wall1 = Barrier()
    barrier_wall1.rect = pygame.Rect(-100, 295, 260, 800)
    barriers.append(barrier_wall1)
    barriers_sprite_group.add(barrier_wall1)

    barrier_wall2 = Barrier()
    barrier_wall2.rect = pygame.Rect(-100, 160, 310, 135)
    barriers.append(barrier_wall2)
    barriers_sprite_group.add(barrier_wall2)

    barrier_wall3 = Barrier()
    barrier_wall3.rect = pygame.Rect(1200, 0, 30, height)
    barriers.append(barrier_wall3)
    barriers_sprite_group.add(barrier_wall3)

    barrier_1 = Barrier()
    barrier_1.rect = pygame.Rect(355, 400, 170, 30)
    barriers.append(barrier_1)
    barriers_sprite_group.add(barrier_1)

    barrier_2 = Barrier()
    barrier_2.rect = pygame.Rect(650, 295, 250, 30)
    barriers.append(barrier_2)
    barriers_sprite_group.add(barrier_2)

    crossingroad_step = pygame.image.load("./assets/游戏背景/关卡/crossing road 台阶.png")
    crossingroad_step_rect = (380, 110)
    barrier_3 = Barrier()
    barrier_3.rect = pygame.Rect(400, 110, 170, 30)
    barriers.append(barrier_3)
    barriers_sprite_group.add(barrier_3)

    enemy1 = White_enemy()
    enemy1.rect.center = (400, 560)
    enemy1.road_left, enemy1.road_right = 180, 730
    enemies_sprite_group.add(enemy1)

    enemy2 = Black_enemy()
    enemy2.rect.center = (750, 260)
    enemy2.road_left, enemy2.road_right = 630, 920
    enemies_sprite_group.add(enemy2)

    # stick = Stick_enemy()
    # stick.rect.center = (600, 300)
    # sticks = pygame.sprite.Group()
    # sticks.add(stick)


    while True:
        screen.blit(scene_crossroad, background_place)
        screen.blit(crossingroad_step, crossingroad_step_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        knight.move()
        # if knight.rect.bottom < 500 and knight.rect.left > 600:
            # stick.move()
        for enemy in enemies_sprite_group:
            enemy.move()
        if knight.op != 0:
            knight_group.draw(screen)
            if knight.op==3 or knight.op==4:
                knife_group.draw(screen)
        elif (knight.op == 0 and knight.facing == 1):
            screen.blit(image_stop_l, knight.rect)
        elif (knight.op == 0 and knight.facing == 2):
            screen.blit(image_stop_r, knight.rect)

        rect1 = pygame.Rect(0, 0, 1200, 25)
        rect2 = pygame.Rect(0, 700, 1200, 25)
        pygame.draw.rect(screen, black, rect1)
        pygame.draw.rect(screen, black, rect2)
        # sticks.draw(screen)
        # if pygame.sprite.spritecollide(knight, sticks, True):
        #     knight.life -= 1
        #     knight_harm.play()
        #     knight.harm_move()
        #     between_anime(200)
        if knight.rect.bottom > 710:  #掉下去
            knight.life -= 1
            knight_harm.play()
            knight.rect.center = (950, 500)
            between_anime(200)

        screen.blit(life[knight.life], background_place)
        enemies_sprite_group.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

        if knight.rect.left < 50 and 50 < knight.rect.bottom < 170:
            between_anime(500)
            barriers_sprite_group.empty()
            barriers.clear()
            enemies_sprite_group.empty()
            return

def game_window1_4():
    knight.rect.center = (1170, 500)
    knight.facing = 1
    height_jumpbefore = knight.rect.bottom
    knight_group = pygame.sprite.Group(knight)

    barrier_ground = Barrier()
    barrier_ground.rect = pygame.Rect(0, 550, width, 30)
    barriers.append(barrier_ground)
    barriers_sprite_group.add(barrier_ground)

    barrier_wall = Barrier()
    barrier_wall.rect = pygame.Rect(1200, 0, 30, height)
    barriers.append(barrier_wall)
    barriers_sprite_group.add(barrier_wall)

    enemy1 = Black_enemy()
    enemy1.rect.center = (400, 520)
    enemy1.road_left, enemy1.road_right = 180, 1100
    enemies_sprite_group.add(enemy1)

    enemy2 = White_enemy()
    enemy2.rect.center = (800, 520)
    enemy2.facing = 1
    enemy2.road_left, enemy2.road_right = 180, 1100
    enemies_sprite_group.add(enemy2)

    enemy3 = Bigfly_enemy()
    enemy3.rect.center = (800, 300)
    enemy3.road_left, enemy3.road_up = 100, 40
    enemy3.width, enemy3.height = 700, 500
    enemies_sprite_group.add(enemy3)

    while True:
        screen.blit(scene_beforelift, background_place)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        knight.move()
        for enemy in enemies_sprite_group:
            enemy.move()
        if knight.op != 0:
            knight_group.draw(screen)
            if knight.op==3 or knight.op==4:
                knife_group.draw(screen)
        elif (knight.op == 0 and knight.facing == 1):
            screen.blit(image_stop_l, knight.rect)
        elif (knight.op == 0 and knight.facing == 2):
            screen.blit(image_stop_r, knight.rect)

        rect1 = pygame.Rect(0, 0, 1200, 25)
        rect2 = pygame.Rect(0, 700, 1200, 25)
        pygame.draw.rect(screen, black, rect1)
        pygame.draw.rect(screen, black, rect2)
        screen.blit(life[knight.life], background_place)
        enemies_sprite_group.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

        if knight.rect.right < 30 and 450 < knight.rect.bottom < 560:
            between_anime(500)
            barriers_sprite_group.empty()
            barriers.clear()
            enemies_sprite_group.empty()
            return

def game_window1_5():
    lifts = pygame.sprite.Group()

    knight.rect.center = (1180, 370)
    knight.facing = 1
    height_jumpbefore = knight.rect.bottom
    knight_group = pygame.sprite.Group(knight)

    barrier_ground = Barrier()
    barrier_ground.rect = pygame.Rect(0, 420, width, 30)
    barriers.append(barrier_ground)
    barriers_sprite_group.add(barrier_ground)

    barrier_wall1 = Barrier()
    barrier_wall1.rect = pygame.Rect(1200, 0, 30, height)
    barriers.append(barrier_wall1)
    barriers_sprite_group.add(barrier_wall1)

    barrier_wall2 = Barrier()
    barrier_wall2.rect = pygame.Rect(150, 0, 30, height)
    barriers.append(barrier_wall2)
    barriers_sprite_group.add(barrier_wall2)

    barrier_lift = Barrier()
    barrier_lift.rect = pygame.Rect(430, 225, 50, 50)
    lifts.add(barrier_lift)

    while True:
        screen.blit(scene_liftup, background_place)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        knight.move()
        for enemy in enemies_sprite_group:
            enemy.move()
        if knight.op != 0:
            knight_group.draw(screen)
            if knight.op==3 or knight.op==4:
                knife_group.draw(screen)
        elif (knight.op == 0 and knight.facing == 1):
            screen.blit(image_stop_l, knight.rect)
        elif (knight.op == 0 and knight.facing == 2):
            screen.blit(image_stop_r, knight.rect)

        rect1 = pygame.Rect(0, 0, 1200, 25)
        rect2 = pygame.Rect(0, 700, 1200, 25)
        pygame.draw.rect(screen, black, rect1)
        pygame.draw.rect(screen, black, rect2)
        screen.blit(life[knight.life], background_place)
        enemies_sprite_group.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

        if pygame.sprite.spritecollide(knife, lifts, False):
            between_anime(500)
            barriers_sprite_group.empty()
            barriers.clear()
            enemies_sprite_group.empty()
            return

def game_window1_6():
    knight.rect.center = (465, 490)
    knight.facing = 2
    height_jumpbefore = knight.rect.bottom
    knight_group = pygame.sprite.Group(knight)



    barrier_ground = Barrier()
    barrier_ground.rect = pygame.Rect(0, 540, width, 30)
    barriers.append(barrier_ground)
    barriers_sprite_group.add(barrier_ground)

    barrier_ground2 = Barrier()
    barrier_ground2.rect = pygame.Rect(995, 460, 800, 80)
    barriers.append(barrier_ground2)
    barriers_sprite_group.add(barrier_ground2)

    barrier_wall = Barrier()
    barrier_wall.rect = pygame.Rect(-30, 0, 30, height)
    barriers.append(barrier_wall)
    barriers_sprite_group.add(barrier_wall)

    while True:
        screen.blit(scene_liftdown, background_place)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        knight.move()
        for enemy in enemies_sprite_group:
            enemy.move()
        if knight.op != 0:
            knight_group.draw(screen)
            if knight.op==3 or knight.op==4:
                knife_group.draw(screen)
        elif (knight.op == 0 and knight.facing == 1):
            screen.blit(image_stop_l, knight.rect)
        elif (knight.op == 0 and knight.facing == 2):
            screen.blit(image_stop_r, knight.rect)

        rect1 = pygame.Rect(0, 0, 1200, 25)
        rect2 = pygame.Rect(0, 700, 1200, 25)
        pygame.draw.rect(screen, black, rect1)
        pygame.draw.rect(screen, black, rect2)
        screen.blit(life[knight.life], background_place)
        enemies_sprite_group.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

        if knight.rect.left > 1170 and 430 < knight.rect.bottom < 470:
            between_anime(500)
            barriers_sprite_group.empty()
            barriers.clear()
            enemies_sprite_group.empty()
            return

def game_window1_7():
    knight.rect.center = (20, 490)
    knight.facing = 2
    height_jumpbefore = knight.rect.bottom
    knight_group = pygame.sprite.Group(knight)

    barrier_ground3 = Barrier()
    barrier_ground3.rect = pygame.Rect(0, 625, width, 30)
    barriers.append(barrier_ground3)
    barriers_sprite_group.add(barrier_ground3)

    barrier_ground = Barrier()
    barrier_ground.rect = pygame.Rect(420, 540, width, 30)
    barriers.append(barrier_ground)
    barriers_sprite_group.add(barrier_ground)

    barrier_ground2 = Barrier()
    barrier_ground2.rect = pygame.Rect(600, 460, 800, 80)
    barriers.append(barrier_ground2)
    barriers_sprite_group.add(barrier_ground2)

    barrier_wall = Barrier()
    barrier_wall.rect = pygame.Rect(0, 100, 560, 160)
    barriers.append(barrier_wall)
    barriers_sprite_group.add(barrier_wall)

    barrier_wall2 = Barrier()
    barrier_wall2.rect = pygame.Rect(-30, 0, 30, height)
    barriers.append(barrier_wall2)
    barriers_sprite_group.add(barrier_wall2)

    enemy1 = Black_enemy()
    enemy1.rect.center = (400, 90)
    enemy1.road_left, enemy1.road_right = 100, 500
    enemies_sprite_group.add(enemy1)

    enemy2 = Bigfly_enemy()
    enemy2.rect.center = (800, 300)
    enemy2.road_left, enemy2.road_up = 690, 40
    enemy2.width, enemy2.height = 500, 360
    enemies_sprite_group.add(enemy2)

    enemy3 = White_enemy()
    enemy3.facing = 1
    enemy3.rect.center = (750, 420)
    enemy3.road_left, enemy3.road_right = 600, 1170
    enemies_sprite_group.add(enemy3)

    while True:
        screen.blit(scene_beforerain, background_place)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        knight.move()
        for enemy in enemies_sprite_group:
            enemy.move()
        if knight.op != 0:
            knight_group.draw(screen)
            if knight.op==3 or knight.op==4:
                knife_group.draw(screen)
        elif (knight.op == 0 and knight.facing == 1):
            screen.blit(image_stop_l, knight.rect)
        elif (knight.op == 0 and knight.facing == 2):
            screen.blit(image_stop_r, knight.rect)

        rect1 = pygame.Rect(0, 0, 1200, 25)
        rect2 = pygame.Rect(0, 700, 1200, 25)
        pygame.draw.rect(screen, black, rect1)
        pygame.draw.rect(screen, black, rect2)
        enemies_sprite_group.draw(screen)
        screen.blit(life[knight.life], background_place)

        pygame.display.update()
        clock.tick(FPS)

        if knight.rect.left > 1170 and 440 < knight.rect.bottom < 470:
            between_anime(500)
            barriers_sprite_group.empty()
            barriers.clear()
            enemies_sprite_group.empty()
            return

def game_window1_8():
    knight.rect.center = (20, 480)
    knight.facing = 2
    height_jumpbefore = knight.rect.bottom
    knight_group = pygame.sprite.Group(knight)

    barrier_ground = Barrier()
    barrier_ground.rect = pygame.Rect(0, 530, width, 30)
    barriers.append(barrier_ground)
    barriers_sprite_group.add(barrier_ground)

    barrier_wall2 = Barrier()
    barrier_wall2.rect = pygame.Rect(-30, 0, 30, height)
    barriers.append(barrier_wall2)
    barriers_sprite_group.add(barrier_wall2)

    enemy1 = Big_enemy()
    enemy1.rect.center = (700, 460)
    enemy1.road_left, enemy1.road_right = 0, width
    enemies_sprite_group.add(enemy1)

    enemy2 = Bigfly_enemy()
    enemy2.rect.center = (300, 430)
    enemy2.facing = 2
    enemy2.road_left, enemy2.road_up = 100, 40
    enemy2.width, enemy2.height = 1000, 500
    enemies_sprite_group.add(enemy2)

    enemy3 = Bigfly_enemy()
    enemy3.rect.center = (900, 200)
    enemy3.facing = 1
    enemy3.road_left, enemy2.road_up = 100, 40
    enemy3.width, enemy3.height = 1000, 500
    enemies_sprite_group.add(enemy3)

    while True:
        screen.blit(scene_rainroad, background_place)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        knight.move()
        for enemy in enemies_sprite_group:
            enemy.move()
        if knight.op != 0:
            knight_group.draw(screen)
            if knight.op==3 or knight.op==4:
                knife_group.draw(screen)
        elif (knight.op == 0 and knight.facing == 1):
            screen.blit(image_stop_l, knight.rect)
        elif (knight.op == 0 and knight.facing == 2):
            screen.blit(image_stop_r, knight.rect)

        rect1 = pygame.Rect(0, 0, 1200, 25)
        rect2 = pygame.Rect(0, 700, 1200, 25)
        pygame.draw.rect(screen, black, rect1)
        pygame.draw.rect(screen, black, rect2)
        screen.blit(life[knight.life], background_place)
        enemies_sprite_group.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

        if knight.rect.left > 1170 and 490 < knight.rect.bottom < 540:
            between_anime(500)
            barriers_sprite_group.empty()
            barriers.clear()
            enemies_sprite_group.empty()
            return

def game_window1_9():
    knight.rect.center = (20, 480)
    knight.facing = 2
    height_jumpbefore = knight.rect.bottom
    knight_group = pygame.sprite.Group(knight)

    barrier_ground = Barrier()
    barrier_ground.rect = pygame.Rect(0, 530, width, 30)
    barriers.append(barrier_ground)
    barriers_sprite_group.add(barrier_ground)

    barrier_wall = Barrier()
    barrier_wall.rect = pygame.Rect(1200, 0, 30, height)
    barriers.append(barrier_wall)
    barriers_sprite_group.add(barrier_wall)

    barrier_wall2 = Barrier()
    barrier_wall2.rect = pygame.Rect(-30, 0, 30, height)
    barriers.append(barrier_wall2)
    barriers_sprite_group.add(barrier_wall2)
    while True:
        screen.blit(scene_beforeend, background_place)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        knight.move()
        for enemy in enemies_sprite_group:
            enemy.move()
        if knight.op != 0:
            knight_group.draw(screen)
            if knight.op == 3 or knight.op == 4:
                knife_group.draw(screen)
        elif (knight.op == 0 and knight.facing == 1):
            screen.blit(image_stop_l, knight.rect)
        elif (knight.op == 0 and knight.facing == 2):
            screen.blit(image_stop_r, knight.rect)

        rect1 = pygame.Rect(0, 0, 1200, 25)
        rect2 = pygame.Rect(0, 700, 1200, 25)
        pygame.draw.rect(screen, black, rect1)
        pygame.draw.rect(screen, black, rect2)
        screen.blit(life[knight.life], background_place)
        enemies_sprite_group.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

        if knight.rect.left > 870 and knight.rect.left < 950 and 490 < knight.rect.bottom < 540:
            between_anime(500)
            barriers_sprite_group.empty()
            barriers.clear()
            enemies_sprite_group.empty()
            return

def game_window1_10():
    image_lover = pygame.image.load("./assets/小姐姐.png")
    lovers = pygame.sprite.Group()
    lover = Barrier()
    lover.rect = pygame.Rect(575, 450, 100, 100)
    lovers.add(lover)

    knight.rect.center = (220, 580)
    knight.facing = 2
    height_jumpbefore = knight.rect.bottom
    knight_group = pygame.sprite.Group(knight)

    barrier_ground = Barrier()
    barrier_ground.rect = pygame.Rect(0, 630, width, 30)
    barriers.append(barrier_ground)
    barriers_sprite_group.add(barrier_ground)

    barrier_wall = Barrier()
    barrier_wall.rect = pygame.Rect(1000, 0, 30, height)
    barriers.append(barrier_wall)
    barriers_sprite_group.add(barrier_wall)

    arrow_images = []
    for i in range(0, 9):
        image = pygame.image.load(f"./assets/其他/箭头/bottom_fleur000{i}.png")
        arrow_images.append(image)

    video_arrow = Videoplay()
    video_arrow.rect = (595, 420)
    video_arrow.speed = 6
    video_arrow_group = pygame.sprite.Group(video_arrow)
    video_arrow.images = arrow_images

    font1 = pygame.font.SysFont("华文楷体", 35)
    font2 = pygame.font.SysFont("华文楷体", 25)
    txt1 = font1.render("送花", True, (255, 255, 255))
    txt2 = font2.render("Press w", True, (255, 255, 255))
    txt1_rect = txt1.get_rect()
    txt2_rect = txt2.get_rect()
    txt1_rect = (610, 375)
    txt2_rect = (700, 385)

    while True:
        screen.blit(scene_end, background_place)
        screen.blit(image_lover, lover.rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        knight.move()
        if knight.op != 0:
            knight_group.draw(screen)
            if knight.op == 3 or knight.op == 4:
                knife_group.draw(screen)
        elif (knight.op == 0 and knight.facing == 1):
            screen.blit(image_stop_l, knight.rect)
        elif (knight.op == 0 and knight.facing == 2):
            screen.blit(image_stop_r, knight.rect)

        rect1 = pygame.Rect(0, 0, 1200, 25)
        rect2 = pygame.Rect(0, 700, 1200, 25)
        pygame.draw.rect(screen, black, rect1)
        pygame.draw.rect(screen, black, rect2)
        screen.blit(life[knight.life], background_place)
        if pygame.sprite.spritecollide(knight, lovers, False) and knight.facing == 2:
            video_arrow.update()
            video_arrow_group.draw(screen)
            screen.blit(txt1, txt1_rect)
            screen.blit(txt2, txt2_rect)

        pygame.display.update()
        clock.tick(FPS)
        pressed_keys = pygame.key.get_pressed()
        if pygame.sprite.spritecollide(knight, lovers, False) and knight.facing == 2 and pressed_keys[K_w]:
            video_getflower()
            between_anime(500)
            barriers_sprite_group.empty()
            barriers.clear()
            enemies_sprite_group.empty()
            return

def photo_play(photo, photo_rect, angle):


    photo = pygame.transform.rotate(photo, angle)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(photo, (photo_rect.left, photo_rect.top))
        pygame.display.update()
        return

def end1_window():
    # font = pygame.font.SysFont("华文楷体", 25)
    # txt = font.render("Press space to skip", True, (255, 255, 255))
    # txt_rect = txt.get_rect()
    # txt_rect.center = (1000, 600)

    for i in range(1, 7):
        photo = pygame.image.load(f"./assets/游戏背景/封面/双人封面{i}.png")
        photo_rect = photo.get_rect(center = (600, 362.5))
        photo_play(photo, photo_rect, 0)
        # screen.blit(txt, txt_rect.center)
        # pygame.display.update()
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #         return
        pygame.time.wait(1700)
    return


class Knight2(pygame.sprite.Sprite):
    def __init__(self):
        super(Knight2, self).__init__()  # 调用父类的__init__方法初始化对象

        # 小骑士基本属性
        self.life = 6
        self.walk_speed = 7
        self.harm_speed = 7
        self.harm = 1  # 攻击力
        self.goldtime = 1500
        self.harm_move_time = 300
        self.harming = 0
        self.harm_moving = 0
        self.op = 0  # 小骑士行动状态: 0静止， 1走路， 2跳跃, 3左右攻击， 4上劈, 5受伤
        self.facing = 1  # 小骑士朝向：1左， 2右
        self.ontheground = 1  # 判断小骑士是否在地上，1在0不在
        self.attack_range = 120
        self.attack_cd = 600
        self.attacking = 0
        self.jumping = 0
        self.images = [image_stop_r]
        self.images_attackend = []

        # walk图列表
        self.images_walk_l = []
        self.images_walk_r = []
        # jump图列表
        self.images_jump_l = []
        self.images_jump_r = []
        # attack图列表
        self.images_attackup_l = []
        self.images_attackup_r = []
        self.images_attack_l = []
        self.images_attack_r = []
        self.images_attack_endl = []
        self.images_attack_endr = []
        self.images_attackup_endl = []
        self.images_attackup_endr = []
        # 将图片导入动图列表
        for i in range(1, 5):  # walk
            image_walk_l = pygame.image.load(f"./assets/knight/walk/Walk_{i}.PNG")
            image_walk_r = pygame.transform.flip(image_walk_l, True, False)
            self.images_walk_l.append(image_walk_l)
            self.images_walk_r.append(image_walk_r)
        for i in range(1, 16):  # jump
            image_jump_l = pygame.image.load(f"./assets/knight/jump/Jump_{i}.PNG")
            image_jump_r = pygame.transform.flip(image_jump_l, True, False)
            self.images_jump_l.append(image_jump_l)
            self.images_jump_r.append(image_jump_r)
        for i in range(1, 6):  # attack
            image_attack_l = pygame.image.load(f"./assets/knight/attack/left/Attack_{i}.PNG")
            image_attack_r = pygame.transform.flip(image_attack_l, True, False)
            self.images_attack_l.append(image_attack_l)
            self.images_attack_r.append(image_attack_r)
        for i in range(1, 6):  # attackup
            image_attackup_l = pygame.image.load(f"./assets/knight/attack/up/AttackTop_{i}.PNG")
            image_attackup_r = pygame.transform.flip(image_attackup_l, True, False)
            self.images_attackup_l.append(image_attackup_l)
            self.images_attackup_r.append(image_attackup_r)
        self.page_now = 0
        self.image = self.images[self.page_now]
        self.rect = self.image.get_rect(center=(0, 0))
        self.counter = 0

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        flag_stop = 0
        global jump_lastkey2, height_jumpbefore2, height_jumpmax, last_harmtime, last_attacktime, last_walktime
        if pygame.time.get_ticks() - last_attacktime >= self.attack_cd:
            self.attacking = 0
        if pygame.time.get_ticks() - last_harmtime >= self.goldtime:
            self.harming = 0

        if pygame.time.get_ticks() - last_harmtime <= self.harm_move_time:
            self.harm_moving = 1
        else:
            self.harm_moving = 0

        if self.harm_moving == 1:
            self.harm_move(self.facing)
            return

        # 左右行走
        if pressed_keys[K_LEFT]:
            if self.attacking != 1:
                self.op = 1
                self.facing = 1
            self.rect.move_ip(-self.walk_speed, 0)
            flag_stop = 1
            if pygame.sprite.spritecollide(self, barriers_sprite_group, False):
                self.rect.move_ip(self.walk_speed, 0)
                flag_stop = 1
        elif pressed_keys[K_RIGHT]:
            if self.attacking != 1:
                self.op = 1
                self.facing = 2
            self.rect.move_ip(self.walk_speed, 0)
            flag_stop = 1
            if pygame.sprite.spritecollide(self, barriers_sprite_group, False):
                self.rect.move_ip(-self.walk_speed, 0)
                flag_stop = 1
        # 确保一次攻击
        if self.attacking == 1:
            gravity_move(self)
            self.update(self.op, self.facing)
            if self.op == 1:
                knight_walk.play()
            return

        # 跳跃
        if ( height_jumpbefore2- self.rect.bottom) <= height_jumpmax:
            if pressed_keys[K_2]:
                if (self.rect.bottom - find_barrier_max_h(self)) == 0 or (jump_lastkey2 == pygame.K_2):
                    if self.rect.bottom - find_barrier_max_h(self) == 0:
                        knight_jump.play()
                    self.op = 2
                    self.vy = vy_jump0
                    flag_stop = 1
            if (self.rect.bottom - find_barrier_max_h(self)) != 0 and not pressed_keys[K_2]:  # 代表k未连续按下
                jump_lastkey2 = pygame.K_0
        else:
            jump_lastkey2 = pygame.K_0

        # 攻击
        # if self.attacking == 0:
        if pygame.time.get_ticks() - last_attacktime >= self.attack_cd:
            if pressed_keys[K_1] and pressed_keys[K_UP]:
                self.op = 4
                flag_stop = 1
                self.attacking = 1
            elif pressed_keys[K_1]:
                self.op = 3
                flag_stop = 1
                self.attacking = 1

            if self.op == 3:
                (x, y) = self.rect.left, self.rect.top
                if self.facing == 1:
                    knife.rect.left, knife.rect.top = x - self.attack_range, y
                elif self.facing == 2:
                    knife.rect.left, knife.rect.top = x + self.attack_range, y
            elif self.op == 4:
                (x, y) = self.rect.left, self.rect.top
                knife.rect.left, knife.rect.top = x, y - self.attack_range

            if pressed_keys[K_1]:
                last_attacktime = pygame.time.get_ticks()
                knight_sword.play()

                enemy = pygame.sprite.spritecollideany(knife, enemies_sprite_group2)
                if enemy:
                    enemy.life -= knight.harm
                    print(enemy.life)
                    if enemy.life <= 0:
                        enemy.kill()

        # 重力向下
        gravity_move(self)

        # 受伤
        if self.harming == 0:
            if pygame.sprite.spritecollide(self, enemies_sprite_group2, False):
                self.life -= 1
                self.harming = 1
                self.op = 5
                flag_stop = 0
                last_harmtime = pygame.time.get_ticks()
                knight_harm.play()

                self.harm_move(self.facing)

        if (self.rect.bottom - find_barrier_max_h(self)) == 0:  # 判断是否回到地面，刷新跳跃的前一键
            jump_lastkey2 = pygame.K_2
            height_jumpbefore2 = self.rect.bottom
        if flag_stop == 0:
            self.op = 0
            return

        # 放音效
        if self.op == 1 and pygame.time.get_ticks() - last_walktime >= knight_walk.get_length():
            knight_walk.play()
            last_walktime = pygame.time.get_ticks()
        self.update(self.op, self.facing)

    def harm_move(self, facing):
        if facing == 1:
            self.rect.move_ip(self.harm_speed, 0)
            if pygame.sprite.spritecollide(self, barriers_sprite_group, False):
                self.rect.move_ip(-self.harm_speed, 0)
        elif facing == 2:
            self.rect.move_ip(-self.harm_speed, 0)
            if pygame.sprite.spritecollide(self, barriers_sprite_group, False):
                self.rect.move_ip(self.harm_speed, 0)
        gravity_move(self)

    def update(self, op, facing):
        global last_attacktime
        # attack
        if (op == 3 and facing == 1):
            self.images = self.images_attack_l
        elif (op == 3 and facing == 2):
            self.images = self.images_attack_r
        elif (op == 4 and facing == 1):
            self.images = self.images_attackup_l
        elif (op == 4 and facing == 2):
            self.images = self.images_attackup_r
        # jump
        elif (op == 2 and facing == 1):
            self.images = self.images_jump_l
        elif (op == 2 and facing == 2):
            self.images = self.images_jump_r
        # walk
        elif (op == 1 and facing == 1):
            self.images = self.images_walk_l
        elif (op == 1 and facing == 2):
            self.images = self.images_walk_r

        gif_speed = [0, 3.5, 2, 3, 3]  # 1走路， 2跳跃, 3左右攻击， 4上劈

        self.counter += 1
        if self.counter >= gif_speed[op] and self.page_now < len(self.images) - 1:
            self.counter = 0
            self.page_now += 1
            self.image = self.images[self.page_now]
            if op == 3:
                (x, y) = self.rect.left, self.rect.top
                if facing == 1:
                    knife.rect.left, knife.rect.top = x - self.attack_range, y
                elif facing == 2:
                    knife.rect.left, knife.rect.top = x + self.attack_range, y
            elif op == 4:
                (x, y) = self.rect.left, self.rect.top
                knife.rect.left, knife.rect.top = x, y - self.attack_range

        if self.page_now >= len(self.images) - 1 and self.counter >= gif_speed[op]:
            self.page_now = 0
            self.counter = 0
            self.attacking = 0

        knife.update(op, facing)

knight2 = Knight2()

def game_window2():
    enemies_sprite_group.empty()
    enemies_sprite_group2.empty()

    knight.rect.center = (20, 480)
    knight.facing = 2
    height_jumpbefore = knight.rect.bottom
    knight_group = pygame.sprite.Group(knight)
    enemies_sprite_group2.add(knight)

    knight2.rect.center = (1150, 480)
    knight2.facing = 1
    height_jumpbefore2 = knight2.rect.bottom
    knight2_group = pygame.sprite.Group(knight2)
    enemies_sprite_group.add(knight2)

    barrier_ground = Barrier()
    barrier_ground.rect = pygame.Rect(0, 530, width, 30)
    barriers.append(barrier_ground)
    barriers_sprite_group.add(barrier_ground)

    barrier_wall = Barrier()
    barrier_wall.rect = pygame.Rect(1200, 0, 30, height)
    barriers.append(barrier_wall)
    barriers_sprite_group.add(barrier_wall)

    barrier_wall2 = Barrier()
    barrier_wall2.rect = pygame.Rect(-30, 0, 30, height)
    barriers.append(barrier_wall2)
    barriers_sprite_group.add(barrier_wall2)

    while True:
        screen.blit(scene_rainroad, background_place)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        knight.move()
        knight2.move()

        if knight.op != 0:
            knight_group.draw(screen)
            if knight.op == 3 or knight.op == 4:
                knife_group.draw(screen)
        elif (knight.op == 0 and knight.facing == 1):
            screen.blit(image_stop_l, knight.rect)
        elif (knight.op == 0 and knight.facing == 2):
            screen.blit(image_stop_r, knight.rect)

        if knight2.op != 0:
            knight2_group.draw(screen)
            if knight2.op == 3 or knight2.op == 4:
                knife_group.draw(screen)
        elif (knight2.op == 0 and knight2.facing == 1):
            screen.blit(image_stop_l, knight2.rect)
        elif (knight2.op == 0 and knight2.facing == 2):
            screen.blit(image_stop_r, knight2.rect)

        rect1 = pygame.Rect(0, 0, 1200, 25)
        rect2 = pygame.Rect(0, 700, 1200, 25)
        pygame.draw.rect(screen, black, rect1)
        pygame.draw.rect(screen, black, rect2)
        screen.blit(life[knight.life], background_place)
        screen.blit(life2[knight2.life], background_place)
        pygame.display.update()
        clock.tick(FPS)

        if knight.life == 0:
            return 2
        elif knight2.life == 0:
            return 1

def end2_window(winner):
    # video_waiting1()
    #
    # video_waiting = pygame.image.load("./assets/游戏背景/敬请期待/敬请期待2.5.png")
    # screen.blit(video_waiting, (0, 25))
    # pygame.time.wait(1000)
    #
    # video_waiting2()

    font = pygame.font.SysFont("华文楷体", 100)
    txt = font.render("Player 1 is winner!", True, (255, 255, 255))
    txt_rect = txt.get_rect()
    txt_rect.center = (600, 362.5)

    txt2 = font.render("Player 2 is winner!", True, (255, 255, 255))
    txt2_rect = txt2.get_rect()
    txt2_rect.center = (600, 362.5)

    if winner == 1:
        screen.fill(black)
        screen.blit(txt, txt_rect)
        pygame.display.update()
        pygame.time.wait(2000)

    elif winner == 2:
        screen.fill(black)
        screen.blit(txt2, txt2_rect)
        pygame.display.update()
        pygame.time.wait(2000)

    return

def main():
    while True:
        game_type = menu_window()  # 主菜单
        if game_type == 1:
            pygame.mixer.music.load("./assets/music/泪城bgm.ogg")
            pygame.mixer.music.set_volume(0.07)

            greenland.play()
            video_beforegame1()
            video_flower()
            ui_load.play()
            greenland.stop()
            pygame.time.wait(1500)

            pygame.mixer.music.play()

            game_window1_1()
            game_window1_2()
            game_window1_3()
            game_window1_4()
            game_window1_5()
            pygame.mixer.music.pause()
            video_lift()
            pygame.mixer.music.unpause()
            game_window1_6()
            game_window1_7()
            game_window1_8()
            pygame.mixer.music.stop()
            meeting.play()
            game_window1_9()
            game_window1_10()
            end1_window()
            between_anime(1700)
            meeting.stop()

        elif game_type == 2:
            finghting.play()
            winner = game_window2()
            finghting.stop()
            end2_window(winner)

main()