# 실험결과
# 100: [5,7,2,2,3,6,2,10,2,3]
# 500: [18,12,10,4,10,9,11,12,12,11]

import matplotlib.pyplot as plt
import pygame
import random
import time
import colorsys

pygame.init()

# 기본 설정
myfont = pygame.font.SysFont(None, 30)
width = 1000
height = 700
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()  
pygame.display.set_caption("진화 시뮬레이터")

# 생물 기본 파라미터
red_size = 35
red_speed = 20 
red_activity = 0.1
interval = 1 # 세대간의 간격
fake = 0.7 #변이율(************************핵심************************)
sonp = 0.5 #자식 비율

# 최소값 
min_size=1
min_speed=5
min_activity=0.1
# 각 개체의 초기값
red_num = 5
black_num = 20 
max_num = 300


class character(pygame.sprite.Sprite):
    def __init__(self, color, w_size,h_size, speed,activity,mom_x,dad_y):
            super().__init__()
            self.image = pygame.Surface((w_size,h_size))
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.x = mom_x
            self.rect.y = dad_y
            self.speed = speed
            self.activity = activity
            self.color = color
            self.pos = pygame.Vector2(random.uniform(-1,1),random.uniform(-1,1)).normalize()
            self.change_time = time.time()+random.uniform(1,5)*(1-activity)

    def update(self):
        # 활동량
        now=time.time()
        if now >= self.change_time:
            self.pos = pygame.Vector2(random.uniform(-1,1),random.uniform(-1,1)).normalize()
            self.change_time = time.time()+random.uniform(1,5)*(1-self.activity)

        # 지정한 각도로 이동
        self.rect.x += self.pos.x * self.speed
        self.rect.y += self.pos.y * self.speed

        # 벽 튕기기
        if self.rect.left<=0 or self.rect.right>=width:
            self.pos.x *= -1
        if self.rect.top<=0 or self.rect.bottom>=height:
            self.pos.y *= -1    

        # 안전 구역 튕기기
        if self.color == (0,0,0):
            if self.rect.colliderect(safe_rect):
                self.pos *= -1

                if self.rect.centerx < safe_rect.left:
                    self.rect.right = safe_rect.left
                elif self.rect.centerx > safe_rect.right:
                    self.rect.left = safe_rect.right
                
                if self.rect.centery < safe_rect.top:
                    self.rect.bottom = safe_rect.top
                elif self.rect.centery > safe_rect.bottom:
                    self.rect.top = safe_rect.bottom

        # 화면 글램핑
        self.rect.x = max(0, min(width-self.rect.width, self.rect.x))  
        self.rect.y = max(0, min(height-self.rect.height, self.rect.y))    

# 룰렛휠
def ruleret(gene):
    p=[x[2]/g_sum for x in gene]
    pick=random.uniform(0,1)
    num=0
    for j,g in zip(p,gene):
        num+=j
        if num>pick:
            return [g[1][:],g[0]]

# 색상 섞기 함수
def mix_color(mom_color, dad_color, mask):
    # mask의 1 비율만큼 dad, 0 비율만큼 mom 색상 섞기
    dad_ratio = mask.count(1) / len(mask)
    mom_ratio = 1 - dad_ratio
    return tuple(
        int(mom_color[i] * mom_ratio + dad_color[i] * dad_ratio)
        for i in range(3)
    )

# 초기 생물 설정
black_creatures = pygame.sprite.Group()
black_genes = [] # [생물정보(0), 유전자[가로 길이, 세로 길이, 속도, 활동성](1), 지속세대(2)]
monsters = pygame.sprite.Group()
all_creatures = pygame.sprite.Group()

# 안전 구역 설정
safe_size= 150
safe_x = width//2-safe_size//2
safe_y = height//2-safe_size//2
safe_rect = pygame.Rect(safe_x, safe_y, safe_size, safe_size)

for i in range(red_num):
    while 1:
        monster_x = random.randint(0, width - red_size)
        monster_y = random.randint(0, height - red_size)
        if not pygame.Rect(monster_x, monster_y, red_size, red_size).colliderect(safe_rect):
            break
    monster=character((0,0,0),red_size,red_size,red_speed,red_activity,monster_x, monster_y)
    monsters.add(monster)
    all_creatures.add(monster)

for i in range(black_num): 
    black_w_size = [31, 37, 49, 31, 29, 49, 36, 44, 50, 31, 27, 43, 23, 38, 25, 35, 32, 25, 44, 25][i]
    black_h_size = [44, 43, 20, 30, 20, 20, 38, 38, 43, 42, 40, 26, 31, 41, 20, 44, 21, 47, 33, 20][i]
    black_speed = [11, 9, 11, 8, 13, 14, 12, 15, 15, 14, 11, 5, 6, 7, 7, 7, 5, 14, 9, 5][i]
    black_activity = [0.7972862444415537, 0.9030724604270954, 0.9773630284508631, 0.9233527840265423, 0.8370232986568447, 0.5604918352656703, 0.6559027366422281, 0.59024325131856, 0.8242641231989087, 0.7403674244950744, 0.5049394206837068, 0.6006591093737974, 0.8911900430796866, 0.7715139526505119, 0.9445191828061481, 0.608285989516135, 0.5259107189115546, 0.8853002091124119, 0.5604588703251933, 0.5018800414962189][i]
    h = i / black_num
    rgb = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(h, 0.7, 0.8))
    black_creatur=character(rgb,black_w_size,black_h_size,black_speed,black_activity,random.randint(0, width - black_w_size), random.randint(0, height - black_h_size))
    black_genes.append([black_creatur,[black_w_size,black_h_size,black_speed,black_activity],0])
    black_creatures.add(black_creatur)
    all_creatures.add(black_creatur)

# 진화 시작
run=1
end = time.time()
g=0
t=0 # 그래프 y축
f=1
fa=1

while run:
    # 100세대 반환
    if g==100 and f:
        print(sum([x[2] for x in black_genes])//len(black_genes))
        f=0
    if g==500 and fa:
        print(sum([x[2] for x in black_genes])//len(black_genes))
        fa=0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:run=0
    # 분열 시작
    start=time.time()
    if start-end > interval:

        end = start
        g+=1
        for i in black_genes:i[2]+=1
        if len(all_creatures)<max_num:
            for _ in range(int(len(black_genes)*sonp)):
                # 교차
                g_sum=sum([x[2] for x in black_genes])
                mom=ruleret(black_genes)
                dad=ruleret(black_genes)
                mom_color = mom[1].color
                dad_color = dad[1].color
                mask = [random.choice([0,1]) for _ in range(4)] # 0은 엄마 1은 아빠
                son = [dad[0][i] if mask[i] else mom[0][i] for i in range(4)] #아들 유전자 (균등 교차)
                son_color = mix_color(mom_color, dad_color, mask)

                #돌연변이
                for i in range(4):
                    if random.uniform(0,1)<=fake:   
                        if i<2: #크기
                            son[i] = max(min_size, son[i]+random.randint(-3,3))
                        if i==2: #속도
                            son[i] = max(min_speed, son[i]+random.randint(-2,2))
                        if i==3: #활동성
                            son[i] = max(min_activity, son[i]+random.uniform(-0.05,0.05))

                new_cre = character(son_color,son[0],son[1],son[2],son[3],mom[1].rect.x,dad[1].rect.y)
                black_genes.append([new_cre, son, 0])
                black_creatures.add(new_cre)
                all_creatures.add(new_cre)

    all_creatures.update()

    # 충돌 처리
    a=[] # 충돌 유전자 목록
    for red in monsters:
        collided = pygame.sprite.spritecollide(red,black_creatures,True)
        if collided:
            for creatur in list(collided):
                a.append(creatur)
                all_creatures.remove(creatur)

    black_genes = [empty for empty in black_genes if empty[0] not in a] # 충돌한 생물 유전자 목록에서 삭제

    # 화면 그리기
    screen.fill((255,255,255))
    pygame.draw.rect(screen,(184,232,157),safe_rect)
    all_creatures.draw(screen)
    red_text = myfont.render(f"RED: {len(monsters)}", True, (0,0,0))
    screen.blit(red_text, (10, 10))
    black_text = myfont.render(f"BLACK: {len(black_creatures)}", True, (0,0,0))
    screen.blit(black_text, (10, 40))
    black_text = myfont.render(f"Generation: {g}", True, (0,0,0))
    screen.blit(black_text, (10, 70))

    pygame.display.flip()

    clock.tick(30)

pygame.quit()