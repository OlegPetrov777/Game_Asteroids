import pygame
import random

""" Параметры экрана """
WIDTH = 800  # ширина игрового окна
HEIGHT = 500  # высота игрового окна
FPS = 70  # частота кадров в секунду
bg = pygame.image.load('static/bg_2.jpg')  # Картинка для фона

""" Параметры игрока """
gamer = {"height": 70,
         "width": 70,
         "speed": 5,
         "cord_x": 100,
         "cord_y": 100,
         "sprite": pygame.image.load('static/UFO.png')
         }


rocket = {
    "speed": 25,
    "long": 25,
    "width": 3,
    "color": "red",
    "start": None,
    "start_cord_x": None,
    "start_cord_y": None,
    "end_cord_x": None,
    "end_cord_y": None,
    "status": False,
}


""" Создаем игру и окно """
pygame.init()  # запускает pygame
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("StarWars")  # название окна
clock = pygame.time.Clock()  # для ФПС


def bind_buttons(gamer, rocket):
    """ Бинды кнопок """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and gamer["cord_x"] > 10:
        gamer["cord_x"] -= gamer["speed"]
    if keys[pygame.K_RIGHT] and gamer["cord_x"] < WIDTH - gamer["width"] - 10:
        gamer["cord_x"] += gamer["speed"]
    if keys[pygame.K_UP] and gamer["cord_y"] > 10:
        gamer["cord_y"] -= gamer["speed"]
    if keys[pygame.K_DOWN] and gamer["cord_y"] < HEIGHT - gamer["height"] - 10:
        gamer["cord_y"] += gamer["speed"]

    if keys[pygame.K_SPACE] and rocket["status"] is False:
        rocket["status"] = True
        rocket["start_cord_x"] = gamer["cord_x"] + gamer["width"] + rocket["long"]
        rocket["start"] = rocket["start_cord_x"]
        rocket["end_cord_x"] = gamer["cord_x"] + gamer["width"]
        rocket["start_cord_y"] = gamer["cord_y"] + gamer["height"] // 2
        rocket["end_cord_y"] = gamer["cord_y"] + gamer["height"] // 2
        pygame.draw.line(screen, "red",
                         (rocket["start_cord_x"],
                          rocket["start_cord_y"]),
                         (rocket["end_cord_x"],
                          rocket["end_cord_y"]),
                         rocket["width"]
                         )


def draw(gamer, rocket, screen):
    global bg
    screen.blit(bg, (0, 0))
    screen.blit(gamer["sprite"], (gamer["cord_x"], gamer["cord_y"]))

    if rocket["status"] and rocket["start_cord_x"] - rocket["start"] < 300:  # 100 - путь которы живет ракета
        rocket["start_cord_x"] += rocket["speed"]
        rocket["end_cord_x"] += rocket["speed"]
        pygame.draw.line(screen, "red",
                         (rocket["start_cord_x"],
                          rocket["start_cord_y"]),
                         (rocket["end_cord_x"],
                          rocket["end_cord_y"]),
                         rocket["width"]
                         )
    else:
        rocket["status"] = False

    pygame.display.update()


""" Цикл игры MAIN """
running = True
while running:
    clock.tick(FPS)  # держим цикл на правильной скорости

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # выходи из игры через крестик
            running = False

    bind_buttons(gamer, rocket)  # Бинды кнопок
    draw(gamer, rocket, screen)  # Рисование объектов и обновление экрана

pygame.quit()
