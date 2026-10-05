from kivy.app import App from kivy.uix.widget import 
Widget from kivy.uix.label import Label from 
kivy.uix.boxlayout import BoxLayout from kivy.graphics 
import Color, Rectangle from kivy.core.window import 
Window from kivy.clock import Clock import random
# Размер карты
MAP_W, MAP_H = 20, 20 TILE = 30 # размер клетки в 
пикселях
# Символы карты
WALL = '#' FLOOR = '.' GOLD = '$' POTION = '!' MONSTER = 
'M' PLAYER = '@' class GameMap:
    def __init__(self): self.grid = [[WALL for _ in 
        range(MAP_W)] for _ in range(MAP_H)] 
        self.player_x, self.player_y = 1, 1 self.hp = 20 
        self.max_hp = 20 self.gold = 0 self.monsters = 
        [] self.generate()
    def generate(self):
        # Простая генерация комнат
        for _ in range(6): x = random.randint(1, MAP_W - 
            5) y = random.randint(1, MAP_H - 5) w = 
            random.randint(3, 5) h = random.randint(3, 
            5) for i in range(x, min(x + w, MAP_W - 1)):
                for j in range(y, min(y + h, MAP_H - 
                1)):
                    self.grid[j][i] = FLOOR
        # Соединяем комнаты коридорами
        for _ in range(4): x1 = random.randint(1, MAP_W 
            - 2) y1 = random.randint(1, MAP_H - 2) x2 = 
            random.randint(1, MAP_W - 2) y2 = 
            random.randint(1, MAP_H - 2) for i in 
            range(min(x1, x2), max(x1, x2) + 1):
                self.grid[y1][i] = FLOOR for j in 
            range(min(y1, y2), max(y1, y2) + 1):
                self.grid[j][x2] = FLOOR
        # Расставляем золото и зелья
        for _ in range(15): x, y = random.randint(1, 
            MAP_W - 2), random.randint(1, MAP_H - 2) if 
            self.grid[y][x] == FLOOR:
                self.grid[y][x] = GOLD for _ in 
        range(5):
            x, y = random.randint(1, MAP_W - 2), 
            random.randint(1, MAP_H - 2) if 
            self.grid[y][x] == FLOOR:
                self.grid[y][x] = POTION
        # Расставляем монстров
        for _ in range(8): x, y = random.randint(1, 
            MAP_W - 2), random.randint(1, MAP_H - 2) if 
            self.grid[y][x] == FLOOR:
                self.monsters.append([x, y, 
                random.randint(3, 6)])
        # Ставим игрока на свободную клетку
        while True: px, py = random.randint(1, MAP_W - 
            2), random.randint(1, MAP_H - 2) if 
            self.grid[py][px] == FLOOR:
                self.player_x, self.player_y = px, py 
                break
    def move_player(self, dx, dy): nx, ny = 
        self.player_x + dx, self.player_y + dy if 0 <= 
        nx < MAP_W and 0 <= ny < MAP_H:
            if self.grid[ny][nx] != WALL:
                # Проверка на монстра
                for m in self.monsters: if m[0] == nx 
                    and m[1] == ny:
                        # Атакуем монстра
                        m[2] -= random.randint(2, 5) if 
                        m[2] <= 0:
                            self.monsters.remove(m) 
                            self.gold += 5
                        else:
                            # Монстр бьёт в ответ
                            self.hp -= random.randint(1, 
                            3)
                        return self.player_x, 
                self.player_y = nx, ny
                # Подбираем предметы
                if self.grid[ny][nx] == GOLD: self.gold 
                    += 10 self.grid[ny][nx] = FLOOR
                elif self.grid[ny][nx] == POTION: 
                    self.hp = min(self.max_hp, self.hp + 
                    8) self.grid[ny][nx] = FLOOR
    def move_monsters(self): for m in self.monsters: dx 
            = random.choice([-1, 0, 1]) dy = 
            random.choice([-1, 0, 1]) nx, ny = m[0] + 
            dx, m[1] + dy if 0 <= nx < MAP_W and 0 <= ny 
            < MAP_H and self.grid[ny][nx] != WALL:
                m[0], m[1] = nx, ny
            # Если монстр рядом с игроком — атакует
            if abs(m[0] - self.player_x) <= 1 and 
            abs(m[1] - self.player_y) <= 1:
                self.hp -= random.randint(1, 2) class 
GameWidget(Widget):
    def __init__(self, **kwargs): 
        super().__init__(**kwargs) self.game = GameMap() 
        self.status = Label(text='', font_size='16sp', 
        color=(1, 1, 1, 1)) self.status.pos = (10, 
        Window.height - 40) self.add_widget(self.status) 
        self.bind(size=self.redraw, pos=self.redraw) 
        Clock.schedule_interval(self.tick, 0.5) # ход 
        монстров каждые 0.5 сек
    def tick(self, dt): self.game.move_monsters() if 
        self.game.hp <= 0:
            self.status.text = 'ТЫ ПОГИБ! Игра окончена. 
            Нажми R для рестарта.' 
            Clock.unschedule(self.tick) return
        self.redraw() def redraw(self, *args): 
        self.canvas.clear() with self.canvas:
            Color(0.1, 0.1, 0.1) Rectangle(pos=(0, 0), 
            size=(Window.width, Window.height))
            # Смещение для центрирования карты
            offset_x = (Window.width - MAP_W 
