import pygame
import random

# pygame setup
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=2048)
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
db = False

pygame.mixer.music.load("assets/sounds/techno.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

pygame.display.set_caption("Collect The Cake")
pygame.display.set_icon(pygame.image.load("icon.ico"))
font = pygame.font.Font("freesansbold.ttf", 32)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
random_pos = [random.randint(0, screen.get_width()), random.randint(0, screen.get_height())]

score = 0
score_text = font.render(str(score), True, (0,255,0), (255,0,0))
scoreRect = score_text.get_rect()
scoreRect.center = (400 // 2, 400 // 2)

highscore_file = open("highscore.txt", "r")

highscore_text = font.render(str(("highscore:"+highscore_file.read())), True, (0,255,0), (255,0,0))
highscoreRect = highscore_text.get_rect()
highscoreRect.center = (300 // 2, 300 // 2)
highscore_file.close()

collect_sound = pygame.mixer.Sound("assets/sounds/collect.mp3")

normalSprite = pygame.image.load("assets/images/player.png")
collectSprite = pygame.image.load("assets/images/playercollect.png")
currentSprite = normalSprite

background = pygame.image.load("assets/images/background.png")
background = pygame.transform.smoothscale(background, screen.get_size())

class Player(pygame.sprite.Sprite):
    def __init__(self, size, pos=(0, 0)):
        super().__init__()

        self.image = currentSprite

        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.radius = size // 2

class Cake(pygame.sprite.Sprite):
    def __init__(self, size, pos=(0, 0)):
        super().__init__()
        self.image = pygame.image.load("assets/images/cake.png")

        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.radius = size // 2

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.unload()
            highscore_file.close()
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    collectible = Cake(size=50, pos=(random_pos))

    screen.blit(collectible.image, collectible.rect)

    player = Player(size=100, pos=(player_pos))

    screen.blit(player.image, player.rect)
    screen.blit(background, (0, 0))

    things = pygame.sprite.Group()
    things.add(player)
    things.add(collectible)
    things.draw(screen)
    screen.blit(score_text, scoreRect)
    screen.blit(highscore_text, highscoreRect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 500 * dt
    if keys[pygame.K_s]:
        player_pos.y += 500 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 500 * dt
    if keys[pygame.K_d]:
        player_pos.x += 500 * dt

    if pygame.sprite.collide_circle(player, collectible):
        currentSprite = collectSprite
        screen.blit(player.image, player.rect)
        score += 1
        collect_sound.play(0)
        score_text = font.render(str(score), True, (0,255,0), (255,0,0))
        random_pos = [random.randint(0, screen.get_width()), random.randint(0, screen.get_height())]
    else:
        currentSprite = normalSprite

    highscore_file = open("highscore.txt", "r")
    if score > int(highscore_file.readline()):
        highscore_file.close()
        highscore_file = open("highscore.txt", "w")
        highscore_file.write(str(score))
        highscore_text = font.render(str(("highscore:"+str(score))), True, (0,255,0), (255,0,0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()