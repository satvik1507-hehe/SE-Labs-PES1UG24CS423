import pygame
from game.player import Player
from game.world import generate_platforms, draw_lava


WIDTH, HEIGHT = 500, 640
FPS = 60

BG = (20, 15, 30)

GROUND_Y = HEIGHT + 200


class GameEngine:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption(
            "Lava Escape"
        )

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(
            "monospace",
            24,
            bold=True
        )

        self.small_font = pygame.font.SysFont(
            "monospace",
            18,
            bold=True
        )

        self.big_font = pygame.font.SysFont(
            "monospace",
            42,
            bold=True
        )

        self.reset()

    def reset(self):
        self.platforms = generate_platforms(
            WIDTH,
            GROUND_Y
        )

        self.player = Player(
            WIDTH // 2 - 16,
            GROUND_Y - 50
        )

        self.cam_y = 0

        # Lava
        self.lava_y = GROUND_Y + 60

        # Normal lava rise speed
        self.lava_rise = 0.4

        # Current temporary surge speed
        self.lava_surge_speed = 0

        # Frames remaining in current surge
        self.surge_timer = 0

        # Frames until the next possible surge
        self.next_surge = 600

        self.score = 0

        self.game_over = False
        self.won = False

        self.top_y = self.platforms[-1].rect.y

        self.frame = 0

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_r
            ):
                self.reset()

        return True

    def update(self):
        if self.game_over or self.won:
            return

        keys = pygame.key.get_pressed()

        self.player.update(
            keys,
            self.platforms,
            WIDTH
        )

        # Update platforms
        for p in self.platforms:
            p.update()

        # Camera follows player upward
        target = (
            self.player.rect.centery
            - HEIGHT // 2
        )

        if target < self.cam_y:
            self.cam_y = target

        # ---------------------------------
        # LAVA SURGE SYSTEM
        # ---------------------------------

        # Count down to the next surge
        self.next_surge -= 1

        if (
            self.next_surge <= 0
            and self.surge_timer <= 0
        ):
            # Start a lava burst
            self.surge_timer = 120

            # Temporary additional rise speed
            self.lava_surge_speed = 2.0

            # Next surge occurs later
            self.next_surge = 600

        # If a surge is active
        if self.surge_timer > 0:
            self.surge_timer -= 1

            # Slowly reduce the burst strength
            progress = self.surge_timer / 120

            self.lava_surge_speed = 2.0 * progress

        else:
            self.lava_surge_speed = 0

        # Normal lava acceleration
        self.lava_rise = min(
            1.2,
            self.lava_rise + 0.0003
        )

        # Total lava movement
        total_lava_speed = (
            self.lava_rise
            + self.lava_surge_speed
        )

        self.lava_y -= total_lava_speed

        # ---------------------------------
        # SCORE
        # ---------------------------------

        self.score = max(
            0,
            (GROUND_Y - self.player.rect.y) // 10
        )

        self.frame += 1

        # ---------------------------------
        # GAME OVER
        # ---------------------------------

        if self.player.rect.bottom >= self.lava_y:
            self.game_over = True

        # ---------------------------------
        # WIN
        # ---------------------------------

        if self.player.rect.top <= self.top_y - 20:
            self.won = True

    def get_danger_percentage(self):
        """
        Returns how close the lava is to the player.

        0%   = lava is far below
        100% = lava has reached the player
        """

        distance = (
            self.player.rect.bottom
            - self.lava_y
        )

        # Distance at which we consider the player
        # to be in serious danger.
        danger_distance = 300

        danger = (
            1
            - distance / danger_distance
        )

        danger = max(
            0,
            min(1, danger)
        )

        return danger * 100

    def draw(self):
        self.screen.fill(BG)

        # ---------------------------------
        # PLATFORMS
        # ---------------------------------

        for p in self.platforms:
            p.draw(
                self.screen,
                self.cam_y
            )

        # ---------------------------------
        # PLAYER
        # ---------------------------------

        self.player.draw(
            self.screen,
            self.cam_y
        )

        # ---------------------------------
        # LAVA
        # ---------------------------------

        draw_lava(
            self.screen,
            self.lava_y,
            self.cam_y,
            WIDTH,
            HEIGHT,
            self.frame
        )

        # ---------------------------------
        # HUD
        # ---------------------------------

        score_text = self.font.render(
            f"Height: {self.score}m",
            True,
            (220, 200, 180)
        )

        self.screen.blit(
            score_text,
            (8, 10)
        )

        # Danger percentage
        danger = self.get_danger_percentage()

        danger_text = self.small_font.render(
            f"LAVA DANGER: {int(danger)}%",
            True,
            (240, 220, 200)
        )

        self.screen.blit(
            danger_text,
            (8, 42)
        )

        # Danger bar
        bar_x = 8
        bar_y = 68
        bar_width = 220
        bar_height = 18

        pygame.draw.rect(
            self.screen,
            (60, 60, 60),
            (
                bar_x,
                bar_y,
                bar_width,
                bar_height
            ),
            border_radius=5
        )

        filled_width = int(
            bar_width * danger / 100
        )

        if danger < 40:
            danger_color = (80, 200, 100)

        elif danger < 70:
            danger_color = (230, 190, 60)

        else:
            danger_color = (230, 70, 50)

        pygame.draw.rect(
            self.screen,
            danger_color,
            (
                bar_x,
                bar_y,
                filled_width,
                bar_height
            ),
            border_radius=5
        )

        # ---------------------------------
        # SURGE WARNING
        # ---------------------------------

        if self.surge_timer > 0:

            surge_text = self.font.render(
                "LAVA SURGE!",
                True,
                (255, 100, 40)
            )

            self.screen.blit(
                surge_text,
                (
                    WIDTH
                    - surge_text.get_width()
                    - 10,
                    10
                )
            )

        # ---------------------------------
        # GAME OVER / WIN
        # ---------------------------------

        if self.game_over:
            self._msg(
                "LAVA GOT YOU!",
                (220, 80, 40)
            )

        if self.won:
            self._msg(
                "ESCAPED!",
                (80, 220, 100)
            )

        pygame.display.flip()

    def _msg(self, text, color):
        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 150)
        )

        self.screen.blit(
            overlay,
            (0, 0)
        )

        message = self.big_font.render(
            text,
            True,
            color
        )

        restart = self.font.render(
            "Press R to Play Again",
            True,
            (200, 200, 200)
        )

        self.screen.blit(
            message,
            (
                WIDTH // 2
                - message.get_width() // 2,
                HEIGHT // 2 - 40
            )
        )

        self.screen.blit(
            restart,
            (
                WIDTH // 2
                - restart.get_width() // 2,
                HEIGHT // 2 + 20
            )
        )

    def run(self):
        running = True

        while running:
            running = self.handle_events()

            self.update()
            self.draw()

            self.clock.tick(FPS)

        pygame.quit()
