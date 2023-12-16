import pygame
import random
from pygame import mixer

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 400
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TURGUETS")

som_tiro = pygame.mixer.Sound('jogo\\sons\\tiro.wav')
musica = pygame.mixer.Sound('jogo\\sons\\musica.mp3')
musica.set_volume(0.5)
bomba = pygame.mixer.Sound('jogo\\sons\\bomba.mp3')

logo_img = pygame.image.load('jogo\\imagens\\balas.ico')
pygame.display.set_icon(logo_img)

inimigos_img = pygame.image.load('jogo\\imagens\\inimigo.png')
balas_inimigos = pygame.image.load('jogo\\imagens\\balas_inimigo.png')
balas_img = pygame.image.load('jogo\\imagens\\balas.ico')
nave1_img = pygame.image.load('jogo\\imagens\\nivel1.png')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(nave1_img, (30, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 6
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_cooldown = 200
        musica.play()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_w]:
            tempo = pygame.time.get_ticks()
            if tempo - self.last_shot_time > self.shoot_cooldown:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                self.last_shot_time = tempo

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(balas_img, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        som_tiro.play()
        self.speed = 6

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Bullet_enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(balas_inimigos, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 4

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        tamanho = random.randint(15, 35)
        self.image = pygame.transform.scale(inimigos_img, (tamanho, tamanho))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed = random.randrange(1, 4)
        self.shoot_cooldown = random.randint(550, 800)
        self.last_shot_time = 0

    def update(self):
        self.rect.y += self.speed
        tempo = pygame.time.get_ticks()
        if  tempo - self.last_shot_time > self.shoot_cooldown :
            if player.rect.centery > self.rect.centery:
                bullet = Bullet_enemy(self.rect.centerx, self.rect.bottom)
                all_sprites.add(bullet)
                bullet_enemy.add(bullet)
                self.last_shot_time = tempo

        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed = random.randrange(1, 3)

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
bullet_enemy = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites.add(player)

enemies = pygame.sprite.Group()
for _ in range(4):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

pontos = 0
font = pygame.font.Font(None, 20)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # Verifica colisões entre balas e inimigos
    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    for _ in range(len(hits)):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        bomba.play()
        pontos += 1

    hits = pygame.sprite.spritecollide(player, bullet_enemy,True)
    for hit in hits:
        pontos -= 1
        hit.kill()
        if pontos == 0:
            player.kill()

    tela.fill(BLACK)
    all_sprites.draw(tela)

    pontos_texto = font.render(f'Pontos: {pontos}', True, WHITE)
    tela.blit(pontos_texto, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()