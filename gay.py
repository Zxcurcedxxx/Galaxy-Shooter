import random
import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_SPACE, K_q, K_e

from objects import Rocket, Asteroid, Bullet, Explosion
#from power_ups import PowerUp

SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500

pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Asteroids')

gunshot_sound = pygame.mixer.Sound("music/laser.wav")
explosion_sound = pygame.mixer.Sound("music/explosion.mp3")

font = pygame.font.Font('freesansbold.ttf', 32)
# text = font.render('', True, green, blue)


ADDAST1 = pygame.USEREVENT + 1
ADDAST2 = pygame.USEREVENT + 2
ADDAST3 = pygame.USEREVENT + 3
ADDAST4 = pygame.USEREVENT + 4
ADDAST5 = pygame.USEREVENT + 5
#ADDPOWERUP = pygame.USEREVENT + 6
pygame.time.set_timer(ADDAST1, 2000)
pygame.time.set_timer(ADDAST2, 6000)
pygame.time.set_timer(ADDAST3, 10000)
pygame.time.set_timer(ADDAST4, 15000)
pygame.time.set_timer(ADDAST5, 20000)
#pygame.time.set_timer(ADDPOWERUP, 10000)  # Spawn a power-up every 10 seconds

rocket = Rocket(SIZE)

asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()
#power_ups = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(rocket)
#all_sprites.add(power_ups)

backgrounds = [f'assets/background/bg{i}s.png' for i in range(1,5)]
bg = pygame.image.load(random.choice(backgrounds))

startbg = pygame.image.load('assets/start.jpg')

try:
    with open('highscore.txt', 'r') as f:
        high_score = int(f.read())
except FileNotFoundError:
    high_score = 0

if __name__ == '__main__':
  score = 0
  lives = 3  # Убедитесь, что это значение всегда 3 в начале игры
  level = 1
  score_for_next_level = 10
  
  running = True
  gameStarted = False
  musicStarted = False
  paused = False
  while running:
    if lives < 0:
      lives = 3
    if not gameStarted:
      if not musicStarted:
        pygame.mixer.music.load('music/Apoxode_-_Electric_1.mp3')
        pygame.mixer.music.play(loops=-1)
        musicStarted = True
      for event in pygame.event.get():
        if event.type == QUIT:
          running = False

        if event.type == KEYDOWN:
          if event.key == K_SPACE:
            gameStarted = True
            musicStarted = False

        win.blit(startbg, (0,0))
    else:
      if not musicStarted:
        pygame.mixer.music.load('music/rpg_ambience_-_exploration.ogg')
        pygame.mixer.music.play(loops=-1)
        musicStarted = True
      for event in pygame.event.get():
        if event.type == QUIT:
          running = False

        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            paused = not paused
          if event.key == K_SPACE:
            if rocket.double_shot:
                pos = rocket.rect[:2]
                bullet1 = Bullet(pos, rocket.dir, SIZE, offset=-10)
                bullet2 = Bullet(pos, rocket.dir, SIZE, offset=10)
                bullets.add(bullet1, bullet2)
                all_sprites.add(bullet1, bullet2)
                gunshot_sound.play()
            else:
                pos = rocket.rect[:2]
                bullet = Bullet(pos, rocket.dir, SIZE)
                bullets.add(bullet)
                all_sprites.add(bullet)
                gunshot_sound.play()
          if event.key == K_q:
            rocket.rotate_left()
          if event.key == K_e:
            rocket.rotate_right()
        elif event.type == KEYDOWN and event.key == pygame.K_d:
            rocket.toggle_double_shot()

        elif event.type == ADDAST1:
          ast = Asteroid(1, SIZE)
          asteroids.add(ast)
          all_sprites.add(ast)
        elif event.type == ADDAST2:
          ast = Asteroid(2, SIZE)
          asteroids.add(ast)
          all_sprites.add(ast)
        elif event.type == ADDAST3:
          ast = Asteroid(3, SIZE)
          asteroids.add(ast)
          all_sprites.add(ast)
        elif event.type == ADDAST4:
          ast = Asteroid(4, SIZE)
          asteroids.add(ast)
          all_sprites.add(ast)
        elif event.type == ADDAST5:
          ast = Asteroid(5, SIZE)
          asteroids.add(ast)
          all_sprites.add(ast)
        #elif event.type == ADDPOWERUP:
        #    power_up = PowerUp(SIZE)
        #    power_ups.add(power_up)
        #    all_sprites.add(power_up)


      pressed_keys = pygame.key.get_pressed()
      if not paused:
        rocket.update(pressed_keys)

        asteroids.update()
        bullets.update()
        explosions.update()
        #power_ups.update()

        win.blit(bg, (0,0))
        explosions.draw(win)
        #power_ups.draw(win)

        for sprite in all_sprites:
          win.blit(sprite.surf, sprite.rect)
        win.blit(rocket.surf, rocket.rect)

        if pygame.sprite.spritecollideany(rocket, asteroids):
          lives -= 1
          rocket.kill()
          if lives <= 0:  # Изменено с == 0 на <= 0
            score = 0
            lives = 3  # Сбрасываем жизни на 3
            for sprite in all_sprites:
              sprite.kill()
            all_sprites.empty()
            rocket = Rocket(SIZE)
            all_sprites.add(rocket)
            gameStarted = False
            musicStarted = False
          else:
            rocket = Rocket(SIZE)
            all_sprites.add(rocket)

        for bullet in bullets:
          collision = pygame.sprite.spritecollide(bullet, asteroids, True)
          if collision:
            pos = bullet.rect[:2]
            explosion = Explosion(pos)
            explosions.add(explosion)
            score += 1
            explosion_sound.play()

            bullet.kill()
            bullets.remove(bullet)

        #power_up_collision = pygame.sprite.spritecollide(rocket, power_ups, True)
        #for power_up in power_up_collision:
        #    if power_up.type == 'shield':
        #        rocket.shield = True
        #    elif power_up.type == 'double_shot':
        #        rocket.double_shot = True
        #    elif power_up.type == 'speed_boost':
        #        rocket.speed *= 1.5

        text = font.render('Score : ' + str(score), 1, (200,255,0))
        win.blit(text, (340, 10))

        text = font.render(str(lives), 1, (200,255,0))
        win.blit(text, (10, 10))

        high_score_text = font.render('High Score: ' + str(high_score), 1, (200,255,0))
        win.blit(high_score_text, (10, 50))

        if score >= score_for_next_level:
            level += 1
            score_for_next_level += 10 * level
            # Increase difficulty
            pygame.time.set_timer(ADDAST1, max(500, 2000 - level * 100))


    pygame.display.flip()
    clock.tick(30)

  if score > high_score:
    high_score = score
    with open('highscore.txt', 'w') as f:
        f.write(str(high_score))

  pygame.quit()

