import pygame
import sys
import random

# 초기화
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, hp, name):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height
        self.hp = hp
        self.max_hp = hp
        self.name = name
        self.alive = True

    def draw(self, surface):
        if self.alive:  # 타워가 살아있을 때만 그립니다.
            pygame.draw.rect(surface, (255, 0, 0), self.rect)  # 타워의 히트박스를 빨간색으로 그립니다.

    def deal(self, damage):
        if self.hp != 0:
            self.hp -= damage
            if self.hp <= 0:
                print(f"{self.name} destroyed!")
                self.hp = 0
                #self.alive = False  # 타워의 생존 여부를 False로 설정합니다.
    
    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)

    def get_hitbox(self):
        return self.rect

# 타워 객체를 생성합니다.
Towers = [
    Tower(700, 452, 50, 100, 200, "1"),
    Tower(200, 452, 50, 100, 300, "2"),
    Tower(600, 452, 50, 100, 100, "3"),
    Tower(500, 452, 50, 100, 500, "4"),
    Tower(300, 452, 50, 100, 600, "5")
 ]

def SetTarget():
    while True:
        target = random.randint(0, len(Towers) - 1)
        if Towers[target].hp > 0:
            return target

target = SetTarget() 

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # 사용자가 스페이스 키를 눌렀을 때
                print("스페이스 키가 눌렸습니다.", target, Towers[target].hp, Towers[target].name)
                Towers[target].deal(20)

    # 화면 업데이트
    screen.fill((5, 255, 255))  # 화면을 흰색으로 채웁니다.
    for Tower in Towers:
        if Tower.hp <= 0 and Tower.alive == True:
            
            Tower.alive = False
            target = SetTarget()
            Tower.remove[Tower]
        else:
            Tower.draw(screen)


    # mouse_x, mouse_y = pygame.mouse.get_pos()
    # print("마우스 위치:", mouse_x, mouse_y)
    

    pygame.display.flip()  # 화면을 업데이트합니다.
    clock.tick(60)  # FPS를 60으로 설정합니다.

pygame.quit()
sys.exit()