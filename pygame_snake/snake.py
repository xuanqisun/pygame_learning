import sys, pygame, random
from pygame.math import Vector2
# 不用写全self.pos = pygame.math.Vector2() 二维向量

class SNAKE:

    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]  # 用向量表示的是第几格
        self.direction = Vector2(1, 0)  # 假设蛇头是向右移动的
        self.new_block = False

        # self.bgm_sound = pygame.mixer.Sound('sound/bgm.mp3')
        self.crunch_sound = pygame.mixer.Sound('sound/get_score.mp3')

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def draw_snake(self):
        for block in self.body:
            # create a rect, and draw the rect
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)  # 在列表0号位插入元素
            self.body = body_copy[:]  # 获取一个完整的切片，相当于复制
            self.new_block = False

        else:
            body_copy = self.body[:-1]  # 切片操作 从第一个元素，到倒数第二个元素
            body_copy.insert(0, body_copy[0] + self.direction)  # 在列表0号位插入元素
            self.body = body_copy[:]  # 获取一个完整的切片，相当于复制

    def add_block(self):
        self.new_block = True

    '''def reset(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)'''

class FRUIT:

    # create an x and y position
    # draw a square
    def __init__(self):
        self.randomize()

    def draw_fruit(self):  # 先生成矩形位置形状，再填色
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple,fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)  # 注意 cell_number-1 取得到，区分于range()
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:

    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):  # 碰撞时，重新放置水果
        if self.fruit.pos == self.snake.body[0]:  # 蛇头位置
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:  # 万一水果生成到蛇身上
            if block == self.fruit.pos:
                self.fruit.randomize()
    def check_fail(self):
        # 蛇碰壁  self.snake.body[0]是蛇头, 向量不能与数字比较
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        # 蛇碰自己的尾巴
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

    def draw_grass(self):
        grass_color = (167,209,61)
        for col_1 in range(cell_number):
            if col_1 % 2 == 0:
                for col_2 in range(cell_number):
                    if col_2 % 2 == 0:
                        grass_rect = pygame.Rect(col_2*cell_size, col_1*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen,grass_color, grass_rect)
            else:
                for col_2 in range(cell_number):
                    if col_2 % 2 == 1:
                        grass_rect = pygame.Rect(col_2*cell_size, col_1*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body)-3)  # 从0开始记分
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 80)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))

        screen.blit(score_surface, score_rect)
        screen.blit(apple,apple_rect)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()  # 引入时钟对象，统一帧数
apple = pygame.image.load('image/apple.png').convert_alpha()

game_font = pygame.font.Font(None, 25)

SCREEN_UPDATE = pygame.USEREVENT  # 自定义事件，用于驱动蛇的移动
pygame.time.set_timer(SCREEN_UPDATE, 150)  # 用于设置定时器

main_game = MAIN()
bgm = pygame.mixer.Sound('sound/bgm.mp3')
bgm.play()
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            main_game.game_over()

        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:  # main_game.snake.direction是蛇头的方向向量
                  main_game.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != 1:  # 不能一条线上自己吃自己
                    main_game.snake.direction = Vector2(1, 0)
            elif event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(-1, 0)
            elif event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)  # 帧数
