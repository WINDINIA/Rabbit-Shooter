#1. Import Library 
import pygame
from pygame.locals import *
import math
from random import randint

#2. Initialize the Game 
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height)) # setting screen size
pygame.display.set_caption("Rabbit Shooter!!") # setting caption window
clock = pygame.time.Clock() 
FPS = 120 #fps

#9. Key mapping
keys = {"top": False, "bottom": False}

running = True
playerpos = [150, 150] # initial position for player

#14. Exit code for game over and win codition
exitcode = 0
EXIT_CODE_GAME_OVER = 0
EXIT_CODE_WIN = 1


#13. Score
score = 0 
health_point = 194 # default health point for carrot
countdown_timer = 61000 # 61 detik
arrows = [] # list of arrows

enemy_timer = 100 # waktu kemunculan
enemies = [[width, 100]] # list yang menampung koordinat musuh

#3 Load Game Assets 
#3.1 Load Images
player = pygame.image.load("resources/images/rabbit.png")
grass = pygame.image.load("resources/images/grass.png")
carrot = pygame.image.load("resources/images/carrot.png")
arrow = pygame.image.load("resources/images/bullet.png")
enemy_img = pygame.image.load("resources/images/mouse.png")
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

#3.2 Load audio
pygame.mixer.init()
hit_sound = pygame.mixer.Sound("resources/audio/explode.wav")
enemy_hit_sound = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot_sound = pygame.mixer.Sound("resources/audio/shoot.wav")
hit_sound.set_volume(0.05)
enemy_hit_sound.set_volume(0.05)
shoot_sound.set_volume(0.05)

#3.2.1 background music
pygame.mixer.music.load("resources/audio/backsound.wav")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)


#4. The Game Loop 
while(running):
    
    # 5 - Clear the screen 
    screen.fill(0)
    
    #6. Draw the game object 
    #6.1 Draw the grass
    for x in range(int(width/grass.get_width()+1)):
        for y in range(int(height/grass.get_height()+1)):
            screen.blit(grass, (x*100, y*100))
	
	#6.2 Draw the carrot
    screen.blit(carrot, (0, 30))
    screen.blit(carrot, (0, 135))
    screen.blit(carrot, (0, 240))
    screen.blit(carrot, (0, 345))

    #6.3 Draw the player
    mouse_position = pygame.mouse.get_pos()
    angle = math.atan2(mouse_position[1] - (playerpos[1]+32), mouse_position[0] - (playerpos[0]+26))
    player_rotation = pygame.transform.rotate(player, 360 - angle * 57.29)
    new_playerpos = (playerpos[0] - player_rotation.get_rect().width / 2, playerpos[1] - player_rotation.get_rect().height / 2)
    screen.blit(player_rotation, new_playerpos) 

    # 6.4 Draw arrows
    for bullet in arrows:
        arrow_index = 0
        velx=math.cos(bullet[0])*10
        vely=math.sin(bullet[0])*10
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1] < -64 or bullet[1] > width or bullet[2] < -64 or bullet[2] > height:
            arrows.pop(arrow_index)
        arrow_index += 1
        # draw the arrow
        for projectile in arrows:
            new_arrow = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(new_arrow, (projectile[1], projectile[2]))

    #6.5 - Draw Enemy
    #6.5.1 Waktu musuh akan muncul
    enemy_timer -= 1
    if enemy_timer == 0:
        #6.5.2 Buat musuh baru
        enemies.append([width, randint(50, height-32)])
        #6.5.3 Reset enemy timer to random time
        enemy_timer = randint(1, 150)

    index = 0
    for enemy in enemies:
        #6.5.4 Musuh bergerak dengan kecepatan 0.5 pixel ke kiri
        enemy[0] -= 0.5
        #6.5.5 Hapus musuh saat mencapai batas layar sebelah kiri
        if enemy[0] < -64:
            enemies.pop(index)

        #6.5.6 Collision between enemies and carrot 
        enemy_rect = pygame.Rect(enemy_img.get_rect())
        enemy_rect.top = enemy[1] # ambil titik y 
        enemy_rect.left = enemy[0] # ambil titik x
        #6.5.7 Benturan musuh dengan markas kelinci
        if enemy_rect.left < 64:
            enemies.pop(index)
            health_point -= randint (5, 20)
            hit_sound.play()
            print("Oh tidak, Markas diserang!!")
        
        #6.5.8 Check for collisions between enemies and arrows
        index_arrow = 0
        for bullet in arrows:
            bullet_rect = pygame.Rect(arrow.get_rect())
            bullet_rect.left = bullet[1]
            bullet_rect.top = bullet[2]
            #6.5.9 Benturan anak panah dengan musuh
            if enemy_rect.colliderect(bullet_rect):
                score += 1
                enemies.pop(index)
                arrows.pop(index_arrow)    
                enemy_hit_sound.play()
                print("Musnah kau!")
                print("Score: {}".format(score))
            index_arrow += 1
        index += 1

    #6.5.10 gambar musuh ke layar
    for enemy in enemies:
        screen.blit(enemy_img, enemy)

    #6.6 Draw Health bar
    screen.blit(healthbar, (5,5))
    for hp in range(health_point):
        screen.blit(health, (hp+8, 8))

    #6.7 Draw clock
    font = pygame.font.Font(None, 30)
    minutes = int((countdown_timer-pygame.time.get_ticks())/60000) # 60000 itu sama dengan 60 detik
    seconds = int((countdown_timer-pygame.time.get_ticks())/1000%60)
    time_text = "{:02}:{:02}".format(minutes, seconds)
    clock = font.render(time_text, True, (255,255,255))
    textRect = clock.get_rect()
    textRect.topright = [635, 5]
    screen.blit(clock, textRect)

    
    #6.9 gambar musuh ke layar
    for enemy in enemies:
        screen.blit(enemy_img, enemy)

    #7 Update the screen 
    pygame.display.flip()

    #8 Event Loop 
    for event in pygame.event.get():
        #8.1 Event saat tombol exit diklik
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        
        #8.2 Fire!!
        if event.type == pygame.MOUSEBUTTONDOWN:
            arrows.append([angle, new_playerpos[0]+32, new_playerpos[1]+32])
            shoot_sound.play()

        #9.1 Check the keydown and keyup
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                keys["top"] = True
            if event.key == K_DOWN:
                keys["bottom"] = True
            
        if event.type == pygame.KEYUP:
            if event.key == K_UP:
                keys["top"] = False
            if event.key == K_DOWN:
                keys["bottom"] = False
            
    # End of event loop 

    #10. Move the player 
    if keys["top"]:
        playerpos[1] -= 5 # kurangi nilai y
    if keys["bottom"]:
        playerpos[1] += 5 # tambah nilai y 
    

    #11. Win/Lose check 
    if pygame.time.get_ticks() > countdown_timer:
        running = False
        exitcode = EXIT_CODE_WIN
    if health_point <= 0:
        running = False
        exitcode = EXIT_CODE_GAME_OVER

# End of Game Loop 

#12. Win/lose display 
if exitcode == EXIT_CODE_GAME_OVER:
    screen.blit(gameover, (0, 0))
else:
    screen.blit(youwin, (0, 0))


#15. Tampilkan score
text = font.render("Score: {}".format(score), True, (255, 255, 255))
textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery + 24
screen.blit(text, textRect)

#16. Event Quit
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()


