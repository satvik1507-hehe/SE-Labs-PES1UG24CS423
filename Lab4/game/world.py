import pygame
import random

PLATFORM_COLOR = (100, 80, 50)
LAVA_COLOR = (220, 60, 20)


class Platform:
    def __init__(self, x, y, width, height, crumbling=False, spring=False):
        self.rect = pygame.Rect(x, y, width, height)

        # Platform types
        self.crumbling = crumbling
        self.spring = spring

        # Crumbling state
        self.crumble_started = False
        self.crumble_timer = 0

        # Whether the platform still exists
        self.active = True

    def start_crumbling(self):
        if self.crumbling and not self.crumble_started:
            self.crumble_started = True
            self.crumble_timer = 60

    def update(self):
        if self.crumble_started:
            self.crumble_timer -= 1

            if self.crumble_timer <= 0:
                self.active = False

    def draw(self, screen, cam_y):
        if not self.active:
            return

        dr = self.rect.move(
            0,
            -int(cam_y)
        )

        # Spring platforms are green
        if self.spring:
            color = (80, 200, 120)
        else:
            color = PLATFORM_COLOR

        # Crumbling platforms shake
        if self.crumble_started:
            offset = random.choice(
                [-3, -2, -1, 1, 2, 3]
            )
            dr.x += offset

        pygame.draw.rect(
            screen,
            color,
            dr,
            border_radius=4
        )


def generate_platforms(width, base_y, count=30):
    # Starting ground platform
    plats = [
        Platform(
            0,
            base_y,
            width,
            20
        )
    ]

    y = base_y - 110

    for i in range(count):
        w = random.randint(80, 200)
        x = random.randint(0, width - w)

        # Some platforms crumble
        crumbling = (i % 4 == 2)

        # Some platforms are springs
        spring = (i % 5 == 3)

        # A platform cannot be both
        if crumbling:
            spring = False

        plats.append(
            Platform(
                x,
                y,
                w,
                16,
                crumbling=crumbling,
                spring=spring
            )
        )

        y -= random.randint(80, 130)

    return plats


def draw_lava(screen, lava_y, cam_y, width, height, frame):
    import math

    ly = int(lava_y - cam_y)

    if ly < height:
        pts = [(0, ly)]

        for x in range(0, width + 20, 20):
            pts.append(
                (
                    x,
                    ly + int(
                        math.sin(
                            x * 0.08 + frame * 0.1
                        ) * 8
                    )
                )
            )

        pts.append((width, height))
        pts.append((0, height))

        pygame.draw.polygon(
            screen,
            LAVA_COLOR,
            pts
        )

        s = pygame.Surface(
            (width, 30),
            pygame.SRCALPHA
        )

        for i in range(15):
            pygame.draw.line(
                s,
                (
                    255,
                    100,
                    0,
                    max(0, 60 - i * 4)
                ),
                (0, i),
                (width, i),
                1
            )

        screen.blit(
            s,
            (0, ly - 15)
        )
