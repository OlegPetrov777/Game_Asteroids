import random
import time
import pygame
from pygame.transform import scale

""" Параметры экрана """
WIDTH = 1000  # ширина игрового окна
HEIGHT = 655  # высота игрового окна
FPS = 60  # частота кадров в секунду
bg = pygame.image.load('static/bg.jpg')  # Картинка для фона

""" Создаем игру и окно """
pygame.init()  # запускает pygame
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("StarWars")  # название окна
clock = pygame.time.Clock()  # для ФПС


""" ПАРАМЕТРЫ """
class Cursor:
    def __init__(self):
        self.cord_x = 0
        self.cord_y = 0
        self.status = None

    def set_x(self, value):
        self.cord_x = value

    def set_y(self, value):
        self.cord_y = value


class Gamer:
    def __init__(self):
        self.sprite = pygame.image.load('static/UFO.png')
        self.height = 45
        self.width = 45
        self.speed = 5
        self.cord_x = WIDTH // 2 - 50
        self.cord_y = HEIGHT // 2 - 50
        self.status = True
        self.boost_status = False  # ускорние
        self.health = 3
        self.time = -1

    def move_left(self):
        self.cord_x -= self.speed

    def move_right(self):
        self.cord_x += self.speed

    def move_up(self):
        self.cord_y -= self.speed

    def move_down(self):
        self.cord_y += self.speed


class Bullets:
    def __init__(self):
        self.speed = 25
        self.long = 25
        self.width = 3
        self.color = "red"

        self.damage = 3

        self.start_cord_x = 0
        self.start_cord_y = 0

        self.end_cord_x = 0
        self.end_cord_y = 0

        self.create_x = 0
        self.create_y = 0

        self.status = False

    def fire_right(self):
        self.start_cord_x += self.speed
        self.end_cord_x += self.speed
        return pygame.draw.line(screen, "red",
                                (self.start_cord_x, self.create_y),
                                (self.end_cord_x, self.create_y),
                                self.width)

    def fire_left(self):
        self.start_cord_x -= self.speed
        self.end_cord_x -= self.speed
        return pygame.draw.line(screen, "red",
                                (self.start_cord_x, self.create_y),
                                (self.end_cord_x, self.create_y),
                                self.width)


class Asteroid:
    def __init__(self, x):
        size = random.randint(60, 180)  # Рандомный размер астероида
        self.sprite = scale(pygame.image.load("static/aster.png"), (size, size))
        self.speed = random.randint(1, 6)
        if 60 <= size <= 90:
            self.health = 15
        elif 90 <= size <= 140:
            self.health = 30
        else:
            self.health = 60
        self.death_step = 0
        self.cord_x = x  # random.randint(0, WIDTH - 62)
        self.cord_y = random.randint(0, 440)
        self.size = size
        self.boom_list = [
            pygame.image.load('static/boom_1.png'),
            pygame.image.load('static/boom_2.png'),
            pygame.image.load('static/boom_3.png'),
            pygame.image.load('static/boom_4.png'),
            pygame.image.load('static/boom_5.png'),
            pygame.image.load('static/boom_6.png'),
            pygame.image.load('static/boom_7.png'),
            pygame.image.load('static/boom_8.png'),
            pygame.image.load('static/boom_9.png')
        ]


cursor = Cursor()
gamer = Gamer()
bullets = Bullets()
asteroids_r = []  # для хранения объектов Астероид
asteroids_l = []


""" Цикл игры MAIN """
running = True
run = True
while running:
    times = int(time.time())
    clock.tick(FPS)  # держим цикл на правильной скорости

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # выходи из игры через крестик
            running = False

            """ Управление мышкой """
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # ЛКМ - выстрел
                cursor.status = True

            elif event.button == 2:
                running = False

            elif event.button == 3:
                gamer.health -= 1

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                cursor.status = False

        elif event.type == pygame.MOUSEMOTION:
            cursor.cord_x = event.pos[0]
            cursor.cord_y = event.pos[1]

    """ Бинды кнопок, перемещение игрока """
    keys = pygame.key.get_pressed()  # or distance <= gamer["width"] + asteroid["radius"]:
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and gamer.cord_x > 1:
        gamer.move_left()
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and gamer.cord_x < WIDTH - gamer.width - 1:
        gamer.move_right()
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and gamer.cord_y > -1:
        gamer.move_up()
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and gamer.cord_y < 465:  # 465 - нижняя граница
        gamer.move_down()
    if keys[pygame.K_ESCAPE]:
        time.sleep(0.2)
        if run:
            scr = pygame.Surface((WIDTH, HEIGHT))
            scr.set_alpha(80)
            pygame.draw.rect(scr, (255, 255, 255),
                             (0, 0, WIDTH, HEIGHT))
            screen.blit(scr, (0, 0))
            screen.blit(pygame.image.load('static/pause.png'), (WIDTH // 2 - 360 // 2, HEIGHT // 2 - 360 // 2))
            pygame.display.update()
            run = False
        else:
            run = True

    if keys[pygame.K_f]:
        time.sleep(0.2)
        if gamer.boost_status:
            gamer.boost_status = False
        else:
            gamer.boost_status = True


    if run:
        """ Рисование """
        screen.blit(bg, (0, -50))  # обновление фона
        screen.blit(pygame.image.load('static/panel.bmp'), (0, 555))  # нижняя панель - декор

        # СПАУН АСТРОИДОВ
        if random.randint(1, 1000) > 990:
            asteroid = Asteroid(WIDTH)
            asteroids_r.append(asteroid)

        if random.randint(1, 1000) > 990:
            asteroid = Asteroid(-100)
            asteroids_l.append(asteroid)

        # НЕУЯЗВИМОСТЬ
        if 0 <= times - gamer.time < 5:
            scr = pygame.Surface((WIDTH, HEIGHT))
            scr.set_alpha(80)
            pygame.draw.circle(scr, (153, 255, 153), (gamer.cord_x + 40, gamer.cord_y + 40), 50)
            screen.blit(scr, (0, 0))
            gamer.status = False
        elif times - gamer.time > 5:
            gamer.status = True
            gamer.time = -1

        # УСКОРЕНИЕ
        if gamer.boost_status:
            gamer.speed = 10
            scr = pygame.Surface((WIDTH, HEIGHT))
            scr.set_alpha(80)
            pygame.draw.circle(scr, (128, 212, 255), (gamer.cord_x + 40, gamer.cord_y + 40), 50)
            screen.blit(scr, (0, 0))
        else:
            gamer.speed = 5

        # СТРЕЛЬБА
        if cursor.status and bullets.status is False:
            bullets.create_x = bullets.end_cord_x = gamer.cord_x + 35
            bullets.create_y = bullets.end_cord_y = gamer.cord_y + 40
            bullets.start_cord_x = bullets.end_cord_x + bullets.long
            bullets.start_cord_y = bullets.end_cord_y + bullets.long
            bullets.status = True

        # НАПРАВЛЕИЕ стрельбы
        if bullets.status:
            if cursor.cord_x > gamer.cord_x and bullets.start_cord_x - bullets.create_x < 300:
                bullets.fire_right()
            elif cursor.cord_x < gamer.cord_x and bullets.create_x - bullets.start_cord_x < 300:
                bullets.fire_left()
            else:
                bullets.status = False

        # Сам игрок
        screen.blit(gamer.sprite, (gamer.cord_x, gamer.cord_y))

        """ АСТЕРОИДЫ и взаимодействия с нимим"""
        def damage_and_boom(asteroid, asteroids):
            global bullets
            # Если пуля попала, ...
            if asteroid.cord_x <= bullets.start_cord_x <= asteroid.cord_x + asteroid.size and \
                    asteroid.cord_y <= bullets.start_cord_y <= asteroid.cord_y + asteroid.size and \
                    bullets.status:
                asteroid.health -= bullets.damage
                bullets.status = False
            # Удаление, если нет хп
            if asteroid.health <= 0:
                asteroids.remove(asteroid)
                for boom in asteroid.boom_list:
                    screen.blit(boom, (asteroid.cord_x, asteroid.cord_y))
                    pygame.display.update()

        def gamer_get_damage(asteroid):
            global gamer
            n = 15
            if (asteroid.cord_x + n <= gamer.cord_x + gamer.width <= asteroid.cord_x + asteroid.size - n or
                asteroid.cord_x + n*2 <= gamer.cord_x <= asteroid.cord_x + asteroid.size - n*2) and \
                    (asteroid.cord_y + n <= gamer.cord_y + gamer.height <= asteroid.cord_y + asteroid.size - n or
                     asteroid.cord_y + n*2 <= gamer.cord_y <= asteroid.cord_y + asteroid.size - n*2) and gamer.status:
                gamer.health -= 1
                gamer.status = False
                gamer.time = time.time()

        # ПРАВЫЕ
        if len(asteroids_r) != 0:
            for asteroid in asteroids_r:
                screen.blit(asteroid.sprite, (asteroid.cord_x, asteroid.cord_y))
                asteroid.cord_x -= asteroid.speed
                damage_and_boom(asteroid, asteroids_r)
                gamer_get_damage(asteroid)
        # ЛЕВЫЕ
        if len(asteroids_l) != 0:
            for asteroid in asteroids_l:
                screen.blit(asteroid.sprite, (asteroid.cord_x, asteroid.cord_y))
                asteroid.cord_x += asteroid.speed
                damage_and_boom(asteroid, asteroids_l)
                gamer_get_damage(asteroid)

        # ХП ИГРОКА
        if gamer.health == 3:
            screen.blit(pygame.image.load('static/hp.png'), (WIDTH - 70, 583))
            screen.blit(pygame.image.load('static/hp.png'), (WIDTH - 120, 583))
            screen.blit(pygame.image.load('static/hp.png'), (WIDTH - 170, 583))
        elif gamer.health == 2:
            screen.blit(pygame.image.load('static/hp.png'), (WIDTH - 120, 583))
            screen.blit(pygame.image.load('static/hp.png'), (WIDTH - 170, 583))
        elif gamer.health == 1:
            screen.blit(pygame.image.load('static/hp.png'), (WIDTH - 170, 583))
        else:
            scr = pygame.Surface((WIDTH, HEIGHT))
            scr.set_alpha(80)
            pygame.draw.rect(scr, "red", (0, 0, 1000, 560))
            screen.blit(scr, (0, 0))
            screen.blit(pygame.image.load("static/the_end.png"), (WIDTH//2-421//2, HEIGHT//2-168))
            run = False  # GAME OVER
        pygame.display.update()  # обновление экрана
pygame.quit()
