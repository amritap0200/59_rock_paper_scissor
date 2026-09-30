import math
import random
import pygame
from game.button import ChoiceButton

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.choices = ["ROCK", "PAPER", "SCISSORS"]
        btn_w, btn_h = 130, 50
        gap = 20
        total_w = 3 * btn_w + 2 * gap
        start_x = (width - total_w) // 2
        btn_y = height - 85

        self.buttons = [
            ChoiceButton("ROCK", pygame.Rect(start_x, btn_y, btn_w, btn_h), (160, 50, 50), (200, 70, 70)),
            ChoiceButton("PAPER", pygame.Rect(start_x + btn_w + gap, btn_y, btn_w, btn_h), (40, 100, 170), (60, 130, 210)),
            ChoiceButton("SCISSORS", pygame.Rect(start_x + 2 * (btn_w + gap), btn_y, btn_w, btn_h), (180, 140, 30), (220, 180, 50)),
        ]

        self.player_choice = None
        self.cpu_choice = None
        self.result_text = "Make your move!"
        self.result_color = (220, 225, 235)

        self.player_score = 0
        self.cpu_score = 0
        self.target_score = 5
        self.game_state = "PLAYING"
        self.player_history = []
        self.history_window = 10
        self.adaptive_threshold = 0.5
        self.counter_bias = 0.7

        self.round_resolved_time = 0
        self.reveal_started_time = 0
        self.reveal_duration = 500
        self.display_duration = 1800
        self.showing_result = False
        self.result_revealed = False

        self.font_title = pygame.font.SysFont(None, 36)
        self.font_hud = pygame.font.SysFont(None, 26)
        self.font_arena = pygame.font.SysFont(None, 32)

    def determine_winner(self, player, cpu):
        if player == cpu:
            return "TIE"
        
        rules = {
            ("ROCK", "SCISSORS"): "PLAYER",
            ("SCISSORS", "PAPER"): "PLAYER",
            ("PAPER", "ROCK"): "PLAYER",
            ("SCISSORS", "ROCK"): "CPU",
            ("PAPER", "SCISSORS"): "CPU",
            ("ROCK", "PAPER"): "CPU",
        }
        return rules.get((player, cpu), "TIE")

    def draw_hidden_icon(self, screen, center, offset=(0, 0)):
        center_x, center_y = center
        center_x += offset[0]
        center_y += offset[1]
        pygame.draw.circle(screen, (38, 45, 57), (center_x, center_y), 40)
        pygame.draw.circle(screen, (105, 118, 138), (center_x, center_y), 40, 2)
        question = self.font_title.render("?", True, (195, 202, 214))
        screen.blit(question, (center_x - question.get_width() // 2, center_y - question.get_height() // 2))

    def draw_move_icon(self, screen, choice, center):
        center_x, center_y = center
        pygame.draw.circle(screen, (38, 45, 57), center, 40)

        if choice == "ROCK":
            points = [
                (center_x - 27, center_y + 11),
                (center_x - 24, center_y - 8),
                (center_x - 11, center_y - 25),
                (center_x + 9, center_y - 29),
                (center_x + 26, center_y - 11),
                (center_x + 24, center_y + 14),
                (center_x + 8, center_y + 25),
                (center_x - 17, center_y + 23),
            ]
            pygame.draw.polygon(screen, (125, 139, 157), points)
            pygame.draw.polygon(screen, (215, 222, 232), points, 3)
            pygame.draw.line(screen, (83, 97, 116), (center_x - 10, center_y - 19), (center_x - 3, center_y + 1), 2)
            pygame.draw.line(screen, (83, 97, 116), (center_x + 11, center_y - 18), (center_x + 5, center_y - 4), 2)
        elif choice == "PAPER":
            sheet = [
                (center_x - 21, center_y - 29),
                (center_x + 8, center_y - 29),
                (center_x + 22, center_y - 15),
                (center_x + 22, center_y + 29),
                (center_x - 21, center_y + 29),
            ]
            pygame.draw.polygon(screen, (220, 231, 238), sheet)
            pygame.draw.polygon(screen, (245, 248, 250), sheet, 3)
            pygame.draw.lines(
                screen,
                (91, 143, 166),
                False,
                [(center_x + 8, center_y - 29), (center_x + 8, center_y - 15), (center_x + 22, center_y - 15)],
                2,
            )
            pygame.draw.line(screen, (91, 143, 166), (center_x - 12, center_y - 2), (center_x + 12, center_y - 2), 2)
            pygame.draw.line(screen, (91, 143, 166), (center_x - 12, center_y + 8), (center_x + 12, center_y + 8), 2)
        elif choice == "SCISSORS":
            blade_color = (238, 191, 92)
            handle_color = (230, 111, 72)
            pygame.draw.line(screen, blade_color, (center_x - 3, center_y + 3), (center_x + 25, center_y - 27), 5)
            pygame.draw.line(screen, blade_color, (center_x + 3, center_y + 3), (center_x - 25, center_y - 27), 5)
            pygame.draw.circle(screen, handle_color, (center_x - 12, center_y + 19), 9, 4)
            pygame.draw.circle(screen, handle_color, (center_x + 12, center_y + 19), 9, 4)
            pygame.draw.circle(screen, (245, 225, 185), center, 4)

    def choose_cpu_choice(self):
        if len(self.player_history) < 3:
            return random.choice(self.choices)

        counts = {choice: self.player_history.count(choice) for choice in self.choices}
        favored_choice = max(self.choices, key=lambda choice: counts[choice])
        frequency = counts[favored_choice] / len(self.player_history)
        if frequency < self.adaptive_threshold:
            return random.choice(self.choices)

        counters = {
            "ROCK": "PAPER",
            "PAPER": "SCISSORS",
            "SCISSORS": "ROCK",
        }
        counter_choice = counters[favored_choice]
        if random.random() < self.counter_bias:
            return counter_choice

        alternatives = [choice for choice in self.choices if choice != counter_choice]
        return random.choice(alternatives)

    def play_round(self, choice):
        if self.game_state == "GAME_OVER":
            return

        self.player_choice = choice
        self.player_history.append(choice)
        self.player_history = self.player_history[-self.history_window:]
        self.cpu_choice = self.choose_cpu_choice()

        outcome = self.determine_winner(self.player_choice, self.cpu_choice)
        if outcome == "PLAYER":
            self.player_score += 1
            self.result_text = f"You Win! {self.player_choice} beats {self.cpu_choice}."
            self.result_color = (80, 230, 120)
        elif outcome == "CPU":
            self.cpu_score += 1
            self.result_text = f"You Lose! {self.cpu_choice} beats {self.player_choice}."
            self.result_color = (240, 80, 80)
        else:
            self.result_text = f"It's a Draw! Both picked {self.player_choice}."
            self.result_color = (240, 210, 80)

        if self.player_score >= self.target_score or self.cpu_score >= self.target_score:
            self.game_state = "GAME_OVER"

        self.showing_result = True
        self.reveal_started_time = pygame.time.get_ticks()
        self.result_revealed = False
        self.round_resolved_time = 0

    def handle_event(self, event):
        if self.game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_match()
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.buttons:
                if btn.contains(event.pos):
                    self.play_round(btn.choice_name)
                    break

    def reset_match(self):
        self.player_score = 0
        self.cpu_score = 0
        self.player_history.clear()
        self.player_choice = None
        self.cpu_choice = None
        self.result_text = "Make your move!"
        self.result_color = (220, 225, 235)
        self.showing_result = False
        self.result_revealed = False
        self.reveal_started_time = 0
        self.round_resolved_time = 0
        self.game_state = "PLAYING"

    def update(self):
        if self.game_state == "GAME_OVER" and not self.showing_result:
            return

        now = pygame.time.get_ticks()
        if self.showing_result:
            if not self.result_revealed and now - self.reveal_started_time >= self.reveal_duration:
                self.result_revealed = True
                self.round_resolved_time = now
            elif self.result_revealed and now - self.round_resolved_time >= self.display_duration:
                self.player_choice = None
                self.cpu_choice = None
                self.result_text = "Make your move!"
                self.result_color = (190, 195, 205)
                self.showing_result = False
                self.result_revealed = False

    def render(self, screen):
        screen.fill((24, 28, 36))

        if self.game_state == "GAME_OVER" and not self.showing_result:
            champion = "Player" if self.player_score >= self.target_score else "CPU"
            champion_surf = self.font_title.render(f"{champion} Wins the Match!", True, (245, 245, 245))
            score_surf = self.font_arena.render(
                f"Final Score: {self.player_score} - {self.cpu_score}", True, (220, 225, 235)
            )
            reset_surf = self.font_hud.render("Press R to play again", True, (190, 195, 205))
            screen.blit(champion_surf, (self.width // 2 - champion_surf.get_width() // 2, 105))
            screen.blit(score_surf, (self.width // 2 - score_surf.get_width() // 2, 160))
            screen.blit(reset_surf, (self.width // 2 - reset_surf.get_width() // 2, 215))
            return

        title_surf = self.font_title.render("Rock Paper Scissors", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 14))

        p_surf = self.font_hud.render(f"Player Score: {self.player_score}", True, (100, 180, 255))
        c_surf = self.font_hud.render(f"CPU Score: {self.cpu_score}", True, (255, 120, 120))
        screen.blit(p_surf, (35, 52))
        screen.blit(c_surf, (self.width - c_surf.get_width() - 35, 52))

        pygame.draw.line(screen, (45, 52, 66), (25, 82), (self.width - 25, 82), 2)

        player_center = (self.width // 2 - 105, 158)
        cpu_center = (self.width // 2 + 105, 158)
        player_label = self.font_hud.render("YOUR PICK", True, (225, 225, 230))
        cpu_label = self.font_hud.render("CPU PICK", True, (225, 225, 230))
        screen.blit(player_label, (player_center[0] - player_label.get_width() // 2, 101))
        screen.blit(cpu_label, (cpu_center[0] - cpu_label.get_width() // 2, 101))

        is_shaking = self.showing_result and not self.result_revealed
        if is_shaking:
            elapsed = max(0, pygame.time.get_ticks() - self.reveal_started_time)
            progress = min(1, elapsed / self.reveal_duration)
            shake_x = round(math.sin(elapsed * 0.08) * 9 * (1 - progress))
            shake_y = round(math.cos(elapsed * 0.11) * 3 * (1 - progress))
            self.draw_hidden_icon(screen, player_center, (shake_x, shake_y))
            self.draw_hidden_icon(screen, cpu_center, (-shake_x, -shake_y))
            visible_result = "Revealing..."
            visible_color = (190, 195, 205)
        else:
            if self.player_choice:
                self.draw_move_icon(screen, self.player_choice, player_center)
            else:
                self.draw_hidden_icon(screen, player_center)
            if self.cpu_choice:
                self.draw_move_icon(screen, self.cpu_choice, cpu_center)
            else:
                self.draw_hidden_icon(screen, cpu_center)
            visible_result = self.result_text
            visible_color = self.result_color

        res_surf = self.font_arena.render(visible_result, True, visible_color)
        screen.blit(res_surf, (self.width // 2 - res_surf.get_width() // 2, 218))

        for btn in self.buttons:
            btn.render(screen)