import pygame
import sys
import os
import math

os.environ['SDL_VIDEODRIVER'] = 'x11'
# 초기화
#test
pygame.init()

# 화면 크기 설정
screen = pygame.display.set_mode((800, 600))

# 객체 생성
object_rect = pygame.Rect(100, 100, 50, 50)
object_color = (255, 0, 0)

# 드래그 중인지 여부를 나타내는 변수
dragging = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if object_rect.collidepoint(event.pos):
                dragging = True
                offset_x = event.pos[0] - object_rect.x
                offset_y = event.pos[1] - object_rect.y
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                object_rect.x = event.pos[0] - offset_x
                object_rect.y = event.pos[1] - offset_y

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, object_color, object_rect)

    pygame.display.flip()