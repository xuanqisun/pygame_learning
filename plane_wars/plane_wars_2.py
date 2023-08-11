import random
import pygame
from pygame.locals import *
import time


class HeroPlane(object):
    def __init__(self, screen):
        self.player = pygame.image.load("./plane_2.png")  # 玩家的飞机 https://www.shejihz.com/archives/84716/
        self.x = 200
        self.y = 680
        self.speed = 3  # 飞机速度
        self.screen = screen  # 记录当前的窗口对象
        self.bullets = []  # 装子弹到列表

    def key_control(self):
        # 监听键盘事件
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_z] or key_pressed[K_UP]:
            self.y -= self.speed
        if key_pressed[K_q] or key_pressed[K_LEFT]:
            self.x -= self.speed
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            self.x += self.speed
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            self.y += self.speed
        if key_pressed[K_SPACE]:  # 发射子弹
            bullet = Bullet(self.screen, self.x, self.y)
            # 把子弹放到列表中
            self.bullets.append(bullet)

    def display(self):  # 显示玩家飞机和所有子弹
        self.screen.blit(self.player, (self.x, self.y))
        for bullet in self.bullets:  # 遍历所有子弹
            bullet.auto_move()  # 修改子弹的y坐标
            bullet.display()


class Bullet(object):
    def __init__(self, screen, x, y):
        self.x = x + 25
        self.y = y - 45
        self.image = pygame.image.load("./bullet_2.png")  # http://47.100.44.116/sucai/vn2i05k0v.html
        self.screen = screen
        self.speed = 10  # 子弹速度

    def display(self):  # 显示子弹到窗口上
        self.screen.blit(self.image, (self.x, self.y))

    def auto_move(self):  # 子弹飞
        self.y -= self.speed


class EnemyPlane(object):
    def __init__(self, screen):
        self.player = pygame.image.load("./EnemyPlane_1.png")  # 50*53
        # 敌方飞机 https://img95.699pic.com/xsj/17/a7/9f.jpg!/fw/700/watermark/url/L3hzai93YXRlcl9kZXRhaWwyLnBuZw/align/southeast
        self.x = 0
        self.y = 0
        self.speed = 4  # 飞机速度
        self.screen = screen  # 窗口对象
        self.bullets = []  # 装子弹到列表
        self.direction = 'right'  # 敌机移动方向

    def display(self):
        self.screen.blit(self.player, (self.x, self.y))
        for bullet in self.bullets:
            bullet.auto_move()
            bullet.display()

    def auto_move(self):
        if self.direction == 'right':  # 向右移动
            self.x += self.speed
        elif self.direction == 'left':  # 向左移动
            self.x -= self.speed

        if self.x > 480 - 50:
            self.direction = 'left'
        elif self.x <= 0:
            self.direction = 'right'

    def auto_fire(self):  # 创建子弹对象，添加进列表
        random_num = random.randint(1, 20)
        if random_num == 8:  # 随便一个数字，用于缩概率
            bullet = EnemyBullet(self.screen, self.x, self.y)
            self.bullets.append(bullet)


class EnemyBullet(object):
    def __init__(self, screen, x, y):
        self.x = x + 21
        self.y = y + 10
        self.image = pygame.image.load("./Enemy_bullet.png")  # https://www.shejihz.com/archives/148580/
        self.screen = screen
        self.speed = 8  # 子弹速度

    def display(self):  # 显示子弹到窗口上
        self.screen.blit(self.image, (self.x, self.y))

    def auto_move(self):  # 子弹飞
        self.y += self.speed

class GameSound(object):
    def __init__(self):
        pygame.mixer.init() # 音乐模块初始化
        pygame.mixer.music.load('./bgm.mp3')
        pygame.mixer.music.set_volume(0.5)  # 声音大小

    def playBackgroundMusic(self):
        pygame.mixer.music.play(-1)  # -1无限循环播放音乐

def main():
    """完成整个程序的控制"""
    sound = GameSound()
    sound.playBackgroundMusic()

    screen = pygame.display.set_mode((480, 800), 0, 32)

    background = pygame.image.load(
        "./background_2.jpg")  # 背景图片 https://t1.tp88.net/uploads/allimg/2004/co200410152946-3.jpg
    player = HeroPlane(screen)
    enemy = EnemyPlane(screen)
    # enemy.auto_move()

    while True:

        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        player.key_control()  # 执行飞机的键盘监听
        player.display()  # 显示飞机

        enemy.auto_move()  # 移动的东西放主循环中
        enemy.display()  # 显示敌方飞机
        enemy.auto_fire()  # 自动开火
        pygame.display.update()
        time.sleep(0.01)


if __name__ == '__main__':
    main()
