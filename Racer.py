from pygame import *
from random import randint

font.init()
mixer.init()

window = display.set_mode((500, 700))
display.set_caption('Гонки по прямой')
background = transform.scale(image.load('track.png'), (500, 700))

black_screen = Surface((500, 700))
black_screen.fill((0, 0, 0))

win = display.set_mode((800, 500))
fon = transform.scale(image.load('fon.png'), (800, 500)) 
but_play = transform.scale(image.load('but_play.png'),(820, 500))


class GameSprite(sprite.Sprite):
    def __init__(self, player_speed, player_image, player_x, player_y):
        super().__init__()
        self.speed = player_speed
        self.image = transform.scale(image.load(player_image), (75, 90))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.rect.inflate_ip(-20, -25)
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Car(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= 12
        if keys_pressed[K_d] and self.rect.x < 400:
            self.rect.x += 12

score = 0
lost = 0
class V_Car(GameSprite):
    def __init__(self, player_speed, player_image, player_x, player_y):
        super().__init__(player_speed, player_image, player_x, player_y)
        self.image = transform.scale(image.load(player_image), (70, 80))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.rect.inflate_ip(-20, -25)

    def update(self):
        self.rect.y += self.speed
        global score
        if self.rect.y > 700:
            self.rect.y = 0
            self.rect.x = randint(80, 400)
            score += 1

clock = time.Clock()
fps = 60

but_x = 290
but_y = 190
but_w = 185
but_h = 100

game_status = True
 
while game_status:
    win.blit(fon, (0, 0))
    win.blit(but_play, (0, 0))


    for e in event.get():
        if e.type == QUIT:
            game_status = False

        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                game_status = False
                mouse_pos = mouse.get_pos()

                if but_x <= mouse_pos[0] <= but_x + but_w and but_y <= mouse_pos[1] <= but_y + but_h:
                    print('Хорошей игры!')

    #draw.rect(window, (255,0,0), (but_x, but_y, but_w, but_h))


    clock.tick(fps)

    display.update()



boom = mixer.Sound('boom.mp3')

vstrechka = sprite.Group()

car = Car(0, 'my_car.png', 250, 550)

porshe = V_Car(randint(3,6), 'porshe.png', randint(100, 400), randint(10, 15))
ferrari = V_Car(randint(4,6), 'ferrari.png', randint(100, 400), randint(10, 15))
clss = V_Car(randint(3,6), 'cls.png', randint(100, 400), randint(10, 15))
gtr = V_Car(randint(3,6), 'gtr.png', randint(100, 400), randint(10, 15))

vstrechka.add(porshe, ferrari, clss, gtr)

score_font = font.Font(None, 36)
game_over_font = font.Font(None, 72)
g_score_font = font.Font(None, 36)

game_over = False

while game_status == False:
    if game_over:
        window.blit(black_screen, (0, 0)) 
    else:
        window.blit(background, (0, 0))  

    for e in event.get():
        if e.type == QUIT:
            game_status = True
        if game_over and e.type == KEYDOWN and e.key == K_r:
            game_over = False
            car.rect.x = 250
            for car_obj in vstrechka:
                car_obj.rect.y = randint(-300, 0)
            score = 0
            boom.stop()

    if not game_over:
        car.update()
        vstrechka.update()
        car.reset()
        vstrechka.draw(window)
        if sprite.spritecollide(car, vstrechka, False):
            game_over = True
    
    score_txt = score_font.render('Очки:'+ str(score), True, (255, 255, 255))
    window.blit(score_txt, (20, 20))
    
    if game_over:
        game_over_text = game_over_font.render('GAME OVER', True, (255, 0, 0))
        restart_text = score_font.render('Нажмите R для рестарта', True, (255, 255, 255))
        g_score_text = g_score_font.render('Ваши очки:' + str(score), True, (255, 255, 255))
        window.blit(game_over_text, (100, 300))
        window.blit(restart_text, (100, 380))
        window.blit(g_score_text, (100, 460))
        boom.play()

    display.update()
    clock.tick(fps)
