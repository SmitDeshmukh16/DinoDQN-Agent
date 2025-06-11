import pygame
import os
import random
import numpy as np
pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.recently_jumped = False
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, action):
        # Actions: 0 = Run, 1 = Jump, 2 = Duck
        if action == 1 and not self.dino_jump:  # Jump
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
            self.recently_jumped = True
        elif action == 2 and not self.dino_jump:  # Duck
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
            self.recently_jumped = False
        elif not self.dino_jump and action == 0:  # Run
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
            self.recently_jumped = False

        if self.dino_duck:
            self.duck()
        elif self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        self.dino_rect.y -= self.jump_vel * 4
        self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.recently_jumped = False  # Reset when landing
            self.jump_vel = self.JUMP_VEL

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self, game_speed):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type_):
        self.image = image
        self.type = type_
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
        self.passed = False

    def update(self, game_speed):
        self.rect.x -= game_speed

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        type_ = 1
        super().__init__(image, type_)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        type_ = 1
        super().__init__(image, type_)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image):
        type_ = 0
        super().__init__(image, type_)
        self.rect.y = 250
        self.index = 0

    def draw(self, screen):
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index // 5], self.rect)
        self.index += 1

class DinoGame:
    def __init__(self):
        self.screen = SCREEN
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.reset()

    def reset(self):
        self.player = Dinosaur()
        self.cloud = Cloud()
        self.obstacles = []
        self.upcoming_obstacle = None
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.points = 0
        self.done = False
        return self.get_observation()

    def step(self, action):
        reward = 1  # Survival reward
      

        # Spawn & update obstacles
        self.spawn_obstacle()
        for obstacle in list(self.obstacles):
            obstacle.update(self.game_speed)

        self.identify_upcoming_obstacle()

        # Update player action
        self.player.update(action)

        # Reward and collision logic
        for obstacle in list(self.obstacles):
            if obstacle.rect.x < -obstacle.rect.width:
                self.obstacles.remove(obstacle)

            if self.player.dino_rect.colliderect(obstacle.rect):
                self.done = True
                reward = -100
                # Log collision details
                distance = obstacle.rect.x - self.player.dino_rect.x
                print(f"Collision with {type(obstacle).__name__}, distance: {distance}, dino_y: {self.player.dino_rect.y},action: {action},points: {self.points}")
                return self.get_observation(), reward, self.done

            if not obstacle.passed and obstacle.rect.x < self.player.dino_rect.x:
                obstacle.passed = True
                reward = 10
                if isinstance(obstacle, (SmallCactus, LargeCactus)) and self.player.recently_jumped:
                    reward = 30  # Increased bonus for jumping cacti
                elif isinstance(obstacle, Bird) and action == 2:
                    reward = 20

        # Timing-based rewards for jumping cacti
        if self.upcoming_obstacle and isinstance(self.upcoming_obstacle, (SmallCactus, LargeCactus)):
            distance = self.upcoming_obstacle.rect.x - self.player.dino_rect.x 
            if action == 1:  # Jump action
                if 20 <= distance <= 100:  # Optimal jump range
                    reward += 5
                

        self.cloud.update(self.game_speed)
        self.x_pos_bg -= self.game_speed
        self.points += 1

        return self.get_observation(), reward, self.done

    def identify_upcoming_obstacle(self):
        self.upcoming_obstacle = None
        for obstacle in self.obstacles:
            if obstacle.rect.x > self.player.dino_rect.x:
                if self.upcoming_obstacle is None or obstacle.rect.x < self.upcoming_obstacle.rect.x:
                    self.upcoming_obstacle = obstacle

    def render(self):
        self.screen.fill((255, 255, 255))
        self.player.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        self.cloud.draw(self.screen)
        self.background()
        self.score()
        pygame.display.update()
        self.clock.tick(30)

    def background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.x_pos_bg = 0

    def score(self):
        text = self.font.render("Points: " + str(self.points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        self.screen.blit(text, textRect)

    def spawn_obstacle(self):
        if len(self.obstacles) == 0:  # Minimum gap
            r = random.randint(0, 2)
            if r == 0:
                self.obstacles.append(SmallCactus(SMALL_CACTUS))
            elif r == 1:
                self.obstacles.append(LargeCactus(LARGE_CACTUS))
            else:
                self.obstacles.append(Bird(BIRD))

    def get_observation(self):
        max_speed = 50  # Adjust based on max game speed
        if self.upcoming_obstacle:
            obstacle = self.upcoming_obstacle
            distance = obstacle.rect.x - self.player.dino_rect.x 

            if isinstance(obstacle, SmallCactus):
                obs_type = 0
            elif isinstance(obstacle, LargeCactus):
                obs_type = 1
            elif isinstance(obstacle, Bird):
                obs_type = 2
            else:
                obs_type = -1

            jump_vel = self.player.jump_vel / self.player.JUMP_VEL if self.player.dino_jump else 0.0

            obs = np.array([
                distance / SCREEN_WIDTH,
                obstacle.rect.height / SCREEN_HEIGHT,
                obstacle.rect.width / SCREEN_WIDTH,
                obstacle.rect.y / SCREEN_HEIGHT,
                obs_type,
                self.player.dino_rect.y / SCREEN_HEIGHT,
                self.game_speed / max_speed,
                jump_vel
            ], dtype=np.float32)
        else:
            obs = np.array([
                1.0, 0.0, 0.0, 0.0, -1,
                self.player.dino_rect.y / SCREEN_HEIGHT,
                self.game_speed / max_speed,
                0.0
            ], dtype=np.float32)

        return obs