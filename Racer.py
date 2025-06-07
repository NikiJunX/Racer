from pygame import *
from random import randint


font.init()
mixer.init()

# Окно меню
win_menu = display.set_mode((800, 500))
display.set_caption('Гонки по прямой - Меню')


fon = transform.scale(image.load('fon.png'), (800, 500))  
but_play = transform.scale(image.load('but_play.png'), (820, 500))



# Классы спрайтов
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

    def fire(self):
        bullet = Bullet(10, 'bullet.png', self.rect.centerx, self.rect.top)
        bullets.add(bullet)
        fire_s.play()

class V_Car(GameSprite):
    def __init__(self, player_speed, player_image, player_x, player_y, is_ammo = False):
        super().__init__(player_speed, player_image, player_x, player_y)
        self.image = transform.scale(image.load(player_image), (70, 80))
        self.rect.inflate_ip(-20, -25)
        self.original_speed = player_speed  # Сохраняем исходную скорость
        self.is_ammo = is_ammo
        if is_ammo:
            self.image = transform.scale(image.load(player_image), (50, 50))

    def update(self):
        self.rect.y += self.speed
        global score
        if self.rect.y > 700:
            self.reset_car()
            score += 1
    
    def reset_car(self):
        self.rect.y = randint(-300, -100)
        self.rect.x = randint(80, 400)
        self.speed = randint(5, 7)  

class Bullet(GameSprite):
    def __init__(self, player_speed, player_image, player_x, player_y):
        super().__init__(player_speed, player_image, player_x, player_y)
        self.image = transform.scale(image.load(player_image), (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def update(self):
        self.rect.y -= 5
        if self.rect.y == 0:
            self.kill()


def draw_road(bg_surface, scroll_y):
    height = bg_surface.get_height()
    width = bg_surface.get_width()
    window.blit(bg_surface, (0, scroll_y % height - height))
    window.blit(bg_surface, (0, scroll_y % height))

def create_enemies():
    vstrechka.empty()
    cars = [
        V_Car(randint(4,6), 'porshe.png', randint(100, 200), randint(10, 15)),
        V_Car(randint(4,6), 'ferrari.png', randint(100, 200), randint(10, 15)),
        V_Car(randint(4,6), 'cls.png', randint(100, 200), randint(10, 15)),
        V_Car(randint(4,6), 'gtr.png', randint(100, 200), randint(10, 15)),
        V_Car(randint(4,6), 'buggati.png', randint(100, 200), randint(10, 15))
    ]
    vstrechka.add(*cars)
    return vstrechka


clock = time.Clock()
fps = 90
score = 0
game_over = False
in_menu = True

boom = mixer.Sound('boom.wav')
fire_s = mixer.Sound('fire.ogg')
sel = mixer.Sound('select.wav')

bullets = sprite.Group()

kill = 0
pat = 0

#Кнопка меню
but_x = 290
but_y = 190
but_w = 185
but_h = 100

last_ammo_score = 0

running = True
while running:
    #Меню
    if in_menu:
        win_menu.blit(fon, (0, 0))
        win_menu.blit(but_play, (0, 0))
        
        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                mouse_pos = mouse.get_pos()
                if but_x <= mouse_pos[0] <= but_x + but_w and but_y <= mouse_pos[1] <= but_y + but_h:
                    in_menu = False
                    window = display.set_mode((500, 700))
                    display.set_caption('Гонки по прямой')
                    
                    # Загрузка игровых ресурсов
                    background = transform.scale(image.load('track.png'), (500, 800))
                    black_screen = Surface((500, 700))
                    black_screen.fill((0, 0, 0))
                    
                    # Создание машин
                    vstrechka = sprite.Group()
                    car = Car(0, 'my_car.png', 250, 550)
                    cars = [
                        V_Car(randint(4,6), 'porshe.png', randint(100, 200), randint(10, 15)),
                        V_Car(randint(4,6), 'ferrari.png', randint(100, 200), randint(10, 15)),
                        V_Car(randint(4,6), 'cls.png', randint(100, 200), randint(10, 15)),
                        V_Car(randint(4,6), 'gtr.png', randint(100, 200), randint(10, 15)),
                        V_Car(randint(4,6), 'buggati.png', randint(100, 200), randint(10, 15))
                    ]
                    vstrechka.add(*cars)

                    scroll_y = 0
                    speed_factor = 4
                    
                    # Шрифты
                    score_font = font.Font(None, 36)
                    game_over_font = font.Font(None, 72)
                    patr = font.Font(None, 36)
    
    # Игра
    else:
        if score - last_ammo_score >= 15:
            if not any(car.is_ammo for car in vstrechka):
                ammo = V_Car(3, 'ammo_box.png', randint(100, 300), -100, is_ammo=True)
                vstrechka.add(ammo)
                last_ammo_score = score

        for car_obj in list(vstrechka):  # Используем list для безопасного удаления
            if car_obj.is_ammo:
                if sprite.collide_rect(car, car_obj):
                    pat += randint(3, 7)
                    sel.play()
                    sel.set_volume(1)
                    car_obj.kill()
            else:
                if sprite.collide_rect(car, car_obj):
                    game_over = True
                    boom.play()

        hits = sprite.groupcollide(bullets, vstrechka, True, False)
        for bullet, hit_cars in hits.items():
            for car_obj in hit_cars:
                car_obj.reset_car()
                kill += 1
        
        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE and pat > 0:  # Выстрел только если есть патроны
                    car.fire()
                    pat -= 1
                if game_over and e.key == K_r:
                    bullets.empty()
                    boom.stop()
                    game_over = False
                    car.rect.x = 250
                    create_enemies()  # Создаём новых врагов
                    score = 0
                    scroll_y = 0
                    pat = 0
                    last_ammo_score = -15
        
        if not game_over:
            # Обновление и отрисовка
            draw_road(background, scroll_y)
            car.update()
            vstrechka.update()
            bullets.update()
            
            car.reset()
            vstrechka.draw(window)
            bullets.draw(window)
            
            scroll_y += speed_factor
        
        # Отрисовка интерфейса
        score_txt = score_font.render(f'Очки: {score}', True, (255, 255, 255))
        pat_txt = patr.render(f'Патроны: {pat}', True, (255, 255, 255))
        window.blit(score_txt, (20, 20))
        window.blit(pat_txt, (20, 50))
        
        if game_over:
            game_over_text = game_over_font.render('GAME OVER', True, (255, 0, 0))
            restart_text = score_font.render('Нажмите R для рестарта', True, (255, 255, 255))
            g_score_text = score_font.render(f'Ваши очки: {score}', True, (255, 255, 255))
            window.blit(game_over_text, (100, 300))
            window.blit(restart_text, (100, 380))
            window.blit(g_score_text, (100, 460))
    
    display.update()
    clock.tick(fps)
