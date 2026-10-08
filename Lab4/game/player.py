import pygame


SPEED = 4


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(
            x,
            y,
            32,
            32
        )

        self.vel_y = 0
        self.on_ground = False

        self.color = (60, 160, 220)

    def update(self, keys, platforms, width):
        dx = 0

        # Move left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -SPEED

        # Move right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = SPEED

        # Normal jump
        if (
            keys[pygame.K_SPACE]
            or keys[pygame.K_w]
            or keys[pygame.K_UP]
        ) and self.on_ground:
            self.vel_y = -13
            self.on_ground = False

        # Gravity
        self.vel_y = min(
            self.vel_y + 0.55,
            12
        )

        # Horizontal movement
        self.rect.x = max(
            0,
            min(
                width - self.rect.width,
                self.rect.x + dx
            )
        )

        # Remember where the player's feet were
        # before vertical movement.
        previous_bottom = self.rect.bottom

        # Vertical movement
        self.rect.y += int(self.vel_y)

        # Assume player is in the air
        self.on_ground = False

        # Platform collision
        for p in platforms:

            # Ignore destroyed platforms
            if not p.active:
                continue

            # Only allow landing while falling
            # and crossing the TOP of the platform.
            if (
                self.rect.colliderect(p.rect)
                and self.vel_y > 0
                and previous_bottom <= p.rect.top
            ):
                # Place player exactly on platform
                self.rect.bottom = p.rect.top

                # Spring platform
                if p.spring:
                    # Strong upward launch
                    self.vel_y = -20

                    # Player is immediately airborne
                    self.on_ground = False

                # Normal platform
                else:
                    self.vel_y = 0
                    self.on_ground = True

                # Start crumble countdown if necessary
                p.start_crumbling()

    def draw(self, screen, cam_y):
        dr = self.rect.move(
            0,
            -int(cam_y)
        )

        # Player body
        pygame.draw.rect(
            screen,
            self.color,
            dr,
            border_radius=6
        )

        # Player head
        pygame.draw.circle(
            screen,
            (255, 220, 180),
            (
                dr.centerx,
                dr.top + 8
            ),
            7
        )
