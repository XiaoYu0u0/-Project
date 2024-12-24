import pygame
import random
import math
import sys

# 初始化 Pygame
pygame.init()

# 畫布設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 顏色
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

# 字型設定
FONT = pygame.font.SysFont('arial', 40)

# 加載101大樓背景圖片
background_image = pygame.image.load('taipei101.png')  # 確保有這個圖片

# 粒子類
class Particle:
    def __init__(self, x, y, color, dx, dy, lifetime=100, text=None):
        self.x = x
        self.y = y
        self.color = color
        self.dx = dx
        self.dy = dy
        self.lifetime = lifetime
        self.text = text  # 用來儲存文字

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1

    def draw(self):
        if self.text:  # 如果是文字粒子，顯示文字
            text_surface = FONT.render(self.text, True, self.color)
            screen.blit(text_surface, (self.x, self.y))
        elif self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)

# 火箭類
class Rocket:
    def __init__(self, x, y, color, speed):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.exploded = False

    def update(self):
        if not self.exploded:
            self.y -= self.speed
            if self.y < random.randint(100, 300):
                self.exploded = True

    def draw(self):
        if not self.exploded:
            pygame.draw.rect(screen, self.color, (self.x - 2, self.y, 4, 10))

# 爆炸形狀
def generate_particles(x, y, color, shape):
    particles = []
    num_particles = 100

    if shape == "circle":
        for i in range(num_particles):
            angle = 2 * math.pi * i / num_particles
            r = 50
            dx = r * math.cos(angle) * 0.1
            dy = r * math.sin(angle) * 0.1
            particles.append(Particle(x, y, color, dx, dy))

    elif shape == "heart":
        for i in range(num_particles):
            t = 2 * math.pi * i / num_particles
            dx = 16 * math.sin(t)**3 * 0.2
            dy = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) * 0.2
            particles.append(Particle(x, y, color, dx, dy))

    elif shape == "star":
        for i in range(num_particles):
            t = 2 * math.pi * i / num_particles
            r = 5 * (1 + 0.2 * math.sin(5 * t))
            dx = r * math.cos(t) * 0.2
            dy = r * math.sin(t) * 0.2
            particles.append(Particle(x, y, color, dx, dy))

    elif shape == "scatter":
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 4)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            particles.append(Particle(x, y, color, dx, dy))

    elif shape == "text1":
        # 當煙火為文字形狀時，顯示"I LOVE STLIN"
        text = "I LOVE STLIN"
        text_width = FONT.size(text)[0]
        total_text_width = FONT.size(text)[0]
        x_pos = x - total_text_width -150/ 2  # 讓文字顯示在爆炸中心
        y_pos = y
        letter_spacing = 5  # 控制字母之間的間距

        for i, letter in enumerate(text):
            # 讓每個字母按照間距排列
            particles.append(Particle(x_pos + i * (FONT.size(letter)[1] + letter_spacing), y_pos, color, 0, 0, text=letter))

    elif shape == "text2":
        # 當煙火為文字形狀時，顯示"I LOVE STLIN"
        text = "HAPPY NEW YEAR"
        text_width = FONT.size(text)[0]
        total_text_width = FONT.size(text)[0]
        x_pos = x - total_text_width -100/ 2  # 讓文字顯示在爆炸中心
        y_pos = y
        letter_spacing = 5  # 控制字母之間的間距

        for i, letter in enumerate(text):
            # 讓每個字母按照間距排列
            particles.append(Particle(x_pos + i * (FONT.size(letter)[1] + letter_spacing), y_pos, color, 0, 0, text=letter))


    # 添加隨機粒子效果
    for _ in range(50):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 4)
        dx = math.cos(angle) * speed
        dy = math.sin(angle) * speed
        particles.append(Particle(x, y, random.choice(COLORS), dx, dy))

    return particles

# 主程式邏輯
def main():
    particles = []
    rockets = []
    explosion_done = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 填充背景
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))  # 畫背景圖片

        if explosion_done:
            rockets = []
            shape = random.choice(["text2"])
            if shape == "text1":
                # 當選擇文字形狀時，從畫面底部中間發射
                x = WIDTH / 2
                y = HEIGHT - 50  # 火箭從底部中間發射
                rocket = Rocket(x, y, random.choice(COLORS), speed=random.randint(5, 8))  # 一定的速度
                rockets.append((rocket, shape))
            elif shape == "text2":
                # 當選擇文字形狀時，從畫面底部中間發射
                x = WIDTH / 2
                y = HEIGHT - 50  # 火箭從底部中間發射
                rocket = Rocket(x, y, random.choice(COLORS), speed=random.randint(5, 8))  # 一定的速度
                rockets.append((rocket, shape))
            else:
                # 其他形狀從底部發射
                for _ in range(3):
                    x = random.randint(100, 700)
                    color = random.choice(COLORS)
                    rocket = Rocket(x, HEIGHT, color, speed=random.randint(5, 8))
                    rockets.append((rocket, shape))
            explosion_done = False

        new_particles = []
        for rocket, shape in rockets[:]:
            rocket.update()
            rocket.draw()

            if rocket.exploded:
                new_particles.extend(generate_particles(rocket.x, rocket.y, rocket.color, shape))
                rockets.remove((rocket, shape))

        if new_particles:
            particles.extend(new_particles)

        for particle in particles[:]:
            particle.update()
            particle.draw()
            if particle.lifetime <= 0:
                particles.remove(particle)

        if not rockets and not particles:
            explosion_done = True

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
