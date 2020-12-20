import random
import time
import pygame
from pygame.transform import scale

""" Параметры экрана """
WIDTH = 1000  # ширина игрового окна
HEIGHT = 655  # высота игрового окна
FPS = 60  # частота кадров в секунду
bg = pygame.image.load('static/photos/bg.jpg')  # Картинка для фона

""" Создаем игру и окно """
pygame.init()  # запускает pygame
pygame.mixer.init()  # для звуков
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ASTEROIDS")  # название окна
clock = pygame.time.Clock()  # для ФПС




""" ОБЪЕКТЫ игры """
class Cursor:
    def __init__(self):
        self.cord_x = 0
        self.cord_y = 0
        self.status = None
        self.pause = False
        self.game_over = False
        self.start = False

    def set_x(self, value):
        self.cord_x = value

    def set_y(self, value):
        self.cord_y = value


class Gamer:
    def __init__(self):
        self.height = 45
        self.width = 45
        self.speed = 5
        self.health = 3
        self.score = 0
        self.time = -1  # Время щита при дамаге
        self.sprite = pygame.image.load('static/photos/UFO.png')
        self.sound_damage = pygame.mixer.Sound('static/music/damage.mp3')
        self.sound_die = pygame.mixer.Sound('static/music/game_over.mp3')

        self.cord_x = WIDTH // 2 - 50
        self.cord_y = HEIGHT // 2 - 50

        self.status = True
        self.boost_status = False  # ускорние

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
        # Характеристики
        self.speed = 25
        self.long = 25
        self.width = 3
        self.damage = 3
        self.color = "red"
        self.status = False

        # Звук
        self.sound = pygame.mixer.Sound('static/music/piu.mp3')

        # Координаты
        self.start_cord_x = 0
        self.start_cord_y = 0

        self.end_cord_x = 0
        self.end_cord_y = 0

        self.create_x = 0
        self.create_y = 0

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
        self.speed = random.randint(1, 6)
        size = random.randint(60, 180)  # Рандомный размер астероида
        self.size = size
        if 60 <= size <= 90:
            self.health = 15
            self.coin = 10
        elif 90 <= size <= 140:
            self.health = 30
            self.coin = 25
        else:
            self.health = 60
            self.coin = 50


        self.sprite = scale(pygame.image.load("static/photos/aster.png"), (size, size))
        self.sound_die = pygame.mixer.Sound('static/music/4_aster.mp3')

        self.cord_x = x  # random.randint(0, WIDTH - 62)
        self.cord_y = random.randint(0, 555 - 180)

        self.death_step = 0
        self.boom_list = [
            pygame.image.load('static/photos/boom_1.png'),
            pygame.image.load('static/photos/boom_2.png'),
            pygame.image.load('static/photos/boom_3.png'),
            pygame.image.load('static/photos/boom_4.png'),
            pygame.image.load('static/photos/boom_5.png'),
            pygame.image.load('static/photos/boom_6.png'),
            pygame.image.load('static/photos/boom_7.png'),
            pygame.image.load('static/photos/boom_8.png'),
            pygame.image.load('static/photos/boom_9.png')
        ]


def game():
    global Cursor
    global Gamer
    global Bullets
    global Asteroid

    cursor = Cursor()
    gamer = Gamer()
    bullets = Bullets()
    asteroids_r = []  # для хранения объектов Астероид
    asteroids_l = []

    """ Цикл игры MAIN """
    pygame.mixer.music.load('static/music/in_game.mp3')  # фоновая музыка
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

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
                if event.button == 1 and cursor.start and cursor.pause is False:  # ЛКМ
                    cursor.status = True

                if event.button == 1 and cursor.pause:  # курсор в паузее
                    # continue
                    if 343 <= event.pos[0] <= 659 and 233 <= event.pos[1] <= 292:
                        cursor.pause = False
                        run = True
                    # restart
                    elif 370 <= event.pos[0] <= 637 and 323 <= event.pos[1] <= 380:
                        cursor.pause = False
                        game()
                    # exit
                    elif 433 <= event.pos[0] <= 577 and 408 <= event.pos[1] <= 462:
                        running = False
                        pygame.quit()

                if event.button == 1 and cursor.start is False:  # курсор на сартовом экране
                    cursor.start = True

                if event.button == 1 and cursor.game_over:  # курсор на экране GAME OVER
                    # restart
                    if 383 <= event.pos[0] <= 623 and 367 <= event.pos[1] <= 403:
                        cursor.pause = False
                        game()
                    # exit
                    elif 440 <= event.pos[0] <= 567 and 423 <= event.pos[1] <= 461:
                        running = False
                        pygame.quit()

            elif event.type == pygame.MOUSEBUTTONUP:  # для зажима стрельбы
                if event.button == 1:
                    cursor.status = False

            elif event.type == pygame.MOUSEMOTION:  # передвижение мыши
                cursor.cord_x = event.pos[0]
                cursor.cord_y = event.pos[1]

        """ Бинды кнопок, перемещение игрока """
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and gamer.cord_x > 1:
            gamer.move_left()
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and gamer.cord_x < WIDTH - gamer.width - 1:
            gamer.move_right()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and gamer.cord_y > -1:
            gamer.move_up()
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and gamer.cord_y < 465:  # 465 - нижняя граница
            gamer.move_down()
        if keys[pygame.K_ESCAPE]:  # Меню
            time.sleep(0.2)
            if run:
                screen.blit(pygame.image.load('static/photos/pause.png'), (0, 0))
                pygame.display.update()
                cursor.pause = True
                run = False
            else:
                run = True
                cursor.pause = False
        if keys[pygame.K_f]:  # Ускорение
            time.sleep(0.2)
            if gamer.boost_status:
                gamer.boost_status = False
            else:
                gamer.boost_status = True

        """ Рисование """
        if cursor.start is False:
            # Окно старта
            screen.blit(bg, (0, -50))
            screen.blit(pygame.image.load('static/photos/start.png'), (300, 250))

        # игра началась
        if run and cursor.start:
            screen.blit(bg, (0, -50))  # обновление фона
            screen.blit(pygame.image.load('static/photos/panel.bmp'), (0, 555))  # нижняя панель - декор

            # СПАУН АСТРОИДОВ
            if random.randint(1, 1000) > 990:
                asteroid = Asteroid(WIDTH)
                asteroids_r.append(asteroid)

            if random.randint(1, 1000) > 990:
                asteroid = Asteroid(-100)
                asteroids_l.append(asteroid)

            # НЕУЯЗВИМОСТЬ
            def invulnerability(color):
                gamer.status = False
                scr = pygame.Surface((WIDTH, HEIGHT))
                scr.set_alpha(80)
                pygame.draw.circle(scr, color, (gamer.cord_x + 40, gamer.cord_y + 40), 50)
                screen.blit(scr, (0, 0))

            if 0 <= times - gamer.time < 1:
                invulnerability((153, 255, 153))
            elif 1 <= times - gamer.time < 2:
                invulnerability((255, 230, 128))
            elif 2 <= times - gamer.time < 3:
                invulnerability((255, 102, 102))
            elif times - gamer.time > 3:
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
                # движение пули
                bullets.create_x = bullets.end_cord_x = gamer.cord_x + 35
                bullets.create_y = bullets.end_cord_y = gamer.cord_y + 40
                bullets.start_cord_x = bullets.end_cord_x + bullets.long
                bullets.start_cord_y = bullets.end_cord_y + bullets.long
                bullets.status = True
                # звук пули
                pygame.mixer.Sound.play(bullets.sound)
                pygame.mixer.Sound.set_volume(bullets.sound, 0.1)

            # НАПРАВЛЕИЕ стрельбы
            if bullets.status:
                if cursor.cord_x > gamer.cord_x and bullets.start_cord_x - bullets.create_x < 300:
                    bullets.fire_right()
                elif cursor.cord_x < gamer.cord_x and bullets.create_x - bullets.start_cord_x < 300:
                    bullets.fire_left()
                else:
                    bullets.status = False

            # САМ ИГРОК
            screen.blit(gamer.sprite, (gamer.cord_x, gamer.cord_y))

            # СЧЕТ ИГРОКА
            font = pygame.font.SysFont('Showcard gothic', 40)
            text = font.render(str(gamer.score), True, (0, 0, 0))
            screen.blit(text, [70, 595])

            """ АСТЕРОИДЫ и взаимодействия с нимим"""

            def damage_and_boom(asteroid, asteroids, bullets):
                # Если пуля попала, ...
                if asteroid.cord_x <= bullets.start_cord_x <= asteroid.cord_x + asteroid.size and \
                        asteroid.cord_y <= bullets.start_cord_y <= asteroid.cord_y + asteroid.size and \
                        bullets.status:
                    asteroid.health -= bullets.damage
                    bullets.status = False
                # Удаление астероида, если у него нет хп
                if asteroid.health <= 0:
                    asteroids.remove(asteroid)
                    gamer.score += asteroid.coin
                    for boom in asteroid.boom_list:
                        screen.blit(boom, (asteroid.cord_x, asteroid.cord_y))
                        pygame.display.update()
                        # Звук как и у игрока
                        pygame.mixer.Sound.play(asteroid.sound_die)
                        pygame.mixer.Sound.set_volume(asteroid.sound_die, 0.1)


            def gamer_get_damage(asteroid, gamer):
                n = 15
                if (asteroid.cord_x + n <= gamer.cord_x + gamer.width <= asteroid.cord_x + asteroid.size - n or
                    asteroid.cord_x + n * 2 <= gamer.cord_x <= asteroid.cord_x + asteroid.size - n * 2) and \
                        (asteroid.cord_y + n <= gamer.cord_y + gamer.height <= asteroid.cord_y + asteroid.size - n or
                         asteroid.cord_y + n * 2 <= gamer.cord_y <= asteroid.cord_y + asteroid.size - n * 2) and \
                        gamer.status:
                    # Звук ранения
                    if gamer.health > 1:
                        pygame.mixer.Sound.play(gamer.sound_damage)
                        pygame.mixer.Sound.set_volume(gamer.sound_damage, 0.5)
                    elif gamer.health == 1:
                        pygame.mixer.Sound.play(gamer.sound_die)
                        pygame.mixer.Sound.set_volume(gamer.sound_die, 0.5)

                    gamer.health -= 1
                    gamer.status = False
                    gamer.time = time.time()

            # ПРАВЫЕ
            if len(asteroids_r) != 0:
                for asteroid in asteroids_r:
                    screen.blit(asteroid.sprite, (asteroid.cord_x, asteroid.cord_y))
                    asteroid.cord_x -= asteroid.speed
                    damage_and_boom(asteroid, asteroids_r, bullets)
                    gamer_get_damage(asteroid, gamer)
            # ЛЕВЫЕ
            if len(asteroids_l) != 0:
                for asteroid in asteroids_l:
                    screen.blit(asteroid.sprite, (asteroid.cord_x, asteroid.cord_y))
                    asteroid.cord_x += asteroid.speed
                    damage_and_boom(asteroid, asteroids_l, bullets)
                    gamer_get_damage(asteroid, gamer)

            # ХП ИГРОКА
            if gamer.health == 3:
                screen.blit(pygame.image.load('static/photos/hp.png'), (WIDTH - 70, 583))
                screen.blit(pygame.image.load('static/photos/hp.png'), (WIDTH - 120, 583))
                screen.blit(pygame.image.load('static/photos/hp.png'), (WIDTH - 170, 583))
            elif gamer.health == 2:
                screen.blit(pygame.image.load('static/photos/hp.png'), (WIDTH - 120, 583))
                screen.blit(pygame.image.load('static/photos/hp.png'), (WIDTH - 170, 583))
            elif gamer.health == 1:
                screen.blit(pygame.image.load('static/photos/hp.png'), (WIDTH - 170, 583))
            else:
                # Красный фон после смерти
                scr = pygame.Surface((WIDTH, HEIGHT))
                scr.set_alpha(160)
                pygame.draw.rect(scr, (204, 0, 0), (0, 0, 1000, 560))
                screen.blit(scr, (0, 0))
                # К
                screen.blit(pygame.image.load("static/photos/TheEnd.png"),
                            (WIDTH // 2 - 421 // 2 + 5, HEIGHT // 2 - 210))

                # СЧЕТ ИГРОКА НА ФИНАЛЬНОМ ЭКРАНЕ
                font = pygame.font.SysFont('Showcard gothic', 80)
                text = font.render(str(gamer.score), True, (250, 250, 250))
                screen.blit(text, [450, 285])

                # Меню после смерти
                scr = pygame.Surface((WIDTH, 555))
                scr.set_alpha(65)
                pygame.draw.rect(scr, (255, 153, 153), (0, 0, 1000, 560))
                screen.blit(scr, (0, 0))
                cursor.game_over = True
                run = False  # GAME OVER

            # обновление экрана
            pygame.display.update()
        pygame.display.update()
    pygame.quit()


game()
