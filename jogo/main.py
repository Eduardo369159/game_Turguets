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
bala_inimigo = pygame.image.load('jogo\\imagens\\balas_inimigo.png')
balas_img = pygame.image.load('jogo\\imagens\\balas.ico')
balas_super_img = pygame.image.load('jogo\\imagens\\bala4.png')
nivel_super_img = pygame.image.load('jogo\\imagens\\nivel5.png')
nave1_img = pygame.image.load('jogo\\imagens\\nivel1.png')
drop_img = pygame.image.load('jogo\\imagens\\drop.png')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(nave1_img, (30, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 6
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_cooldown = 200
        self.health = 100
        self.score = 0
        self.max_shots = 1
        self.shot_delay = 150 
        self.shot_timer = 0
        musica.play()

    def update(self):
        self.shot_timer += 1
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
                start_positions = [-15, 0, 15]
                for i in range(self.max_shots):
                    delay = i * self.shot_delay 
                    bullet = Bullet(self.rect.centerx, self.rect.top, self.speed, delay)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                self.last_shot_time = tempo
                som_tiro.play()
                self.shot_timer = 0
        self.shot_timer += self.speed

        # Verifica colisões entre balas inimigas e o jogador
        hits = pygame.sprite.spritecollide(self, enemy_bullets, True)
        for hit in hits:
            self.health -= 1

        # Verifica se o jogador está sem vida
        if self.health <= 0:
            game_over()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, delay):
        super().__init__()
        self.image = pygame.transform.scale(balas_img, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.delay = delay

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class PowerDrop(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(drop_img, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        tamanho = random.randint(15, 35)
        self.image = pygame.transform.scale(inimigos_img, (tamanho, tamanho))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed = random.randrange(1, 4)
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_cooldown = random.randint(1000, 3000)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed = random.randrange(1, 5)

        tempo = pygame.time.get_ticks()
        if tempo - self.last_shot_time > self.shoot_cooldown:
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)
            self.last_shot_time = tempo

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(bala_inimigo, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 4

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

def game_over():
    pygame.quit()
    quit()

all_sprites = pygame.sprite.Group()
power_drops = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
player = Player()
enemies = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(power_drops)

for _ in range(4):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

pontos = 0
pontos_price = 10
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

        if random.randint(1, 10) == 1: 
            power_drop = PowerDrop(enemy.rect.centerx, enemy.rect.centery)
            all_sprites.add(power_drop)
            power_drops.add(power_drop)

    # Verifica colisões entre balas inimigas e o jogador
    hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
    for hit in hits:
        player.health -= 1

    # Verifica se o jogador ganhou pontos suficientes para recuperar vida
    if pontos == pontos_price and player.health < 100:
        player.health += 2
        pontos_price+=10
    
    power_hits = pygame.sprite.spritecollide(player, power_drops, True)
    for power_hit in power_hits:
        valor = random.randint(1,4)
        if valor == 1:
            player.speed = 6
            player.shoot_cooldown = 150
        elif valor == 2:
            player.health+=20
        elif valor == 3:
            player.speed = 8
            player.shoot_cooldown = 200
        elif valor == 4:
            player.max_shots = 3
            player.shoot_cooldown = 180
            player.speed = 6


    tela.fill(BLACK)
    all_sprites.draw(tela)
    
    power_drops.update()
    power_drops.draw(tela)

    pontos_texto = font.render(f'Pontos: {pontos}    Vida: {player.health}', True, WHITE)
    tela.blit(pontos_texto, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()