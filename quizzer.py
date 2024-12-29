import pygame
import json
import random
import sys

# Initialize Pygame
pygame.init()

# dimensions (screen size)
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Fonts
FONT = pygame.font.Font("freesansbold.ttf", 22)
BIG_FONT = pygame.font.Font("freesansbold.ttf", 32)

# function to load the questions
def load_questions(filename):
    with open(filename, "r") as file:
        return json.load(file)

# Draw text on screen
def draw_text(surface, text, color, x, y, font):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Main game function
def main():
    pygame.display.set_caption("Quizzer")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    score = 0
    player_name = ""

    # Load questions
    questions = load_questions("questions.json")
    categories = list(questions.keys())

    # Load background image
    background_image = pygame.image.load("4.jpg")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # Game states
    STATE_INTRO = "intro"
    STATE_CATEGORY = "category"
    STATE_QUIZ = "quiz"
    STATE_GAMEOVER = "gameover"
    game_state = STATE_INTRO

    selected_category = None
    category_questions = []
    current_question_index = 0

    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 40)
    user_text = ""

    while True:
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state == STATE_INTRO:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and user_text.strip():
                        player_name = user_text.strip()
                        user_text = ""
                        game_state = STATE_CATEGORY
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

            elif game_state == STATE_CATEGORY:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    for i, category in enumerate(categories):
                        if pygame.Rect(WIDTH // 2 - 150, 200 + i * 60, 300, 50).collidepoint(mouse_x, mouse_y):
                            selected_category = category
                            category_questions = questions[selected_category]
                            random.shuffle(category_questions)
                            game_state = STATE_QUIZ
                            current_question_index = 0

            elif game_state == STATE_QUIZ:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and user_text.strip():
                        answer = user_text.strip().lower()
                        if answer == category_questions[current_question_index]["answer"].lower():
                            score += 1
                        user_text = ""
                        current_question_index += 1
                        if current_question_index >= len(category_questions):
                            game_state = STATE_GAMEOVER
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

        if game_state == STATE_INTRO:
            draw_text(screen, "Welcome to Quizzer!", BLACK, WIDTH // 2, HEIGHT // 2 - 40, BIG_FONT)
            draw_text(screen, "Enter your name and press Enter to start", BLACK, WIDTH // 2, HEIGHT // 2 + 70, FONT)
            pygame.draw.rect(screen, BLACK, input_box, 2)
            draw_text(screen, user_text, BLACK, input_box.centerx, input_box.centery, FONT)

        elif game_state == STATE_CATEGORY:
            draw_text(screen, "Select a category:", BLACK, WIDTH // 2, 100, BIG_FONT)
            for i, category in enumerate(categories):
                pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 150, 200 + i * 60, 300, 50))
                draw_text(screen, category, WHITE, WIDTH // 2, 225 + i * 60, FONT)

        elif game_state == STATE_QUIZ:
            question = category_questions[current_question_index]["question"]
            draw_text(screen, f"Question {current_question_index + 1}:", BLACK, WIDTH // 2, 100, BIG_FONT)
            draw_text(screen, question, BLACK, WIDTH // 2, 250, FONT)
            pygame.draw.rect(screen, BLACK, input_box, 2)
            draw_text(screen, user_text, BLACK, input_box.centerx, input_box.centery, FONT)

        elif game_state == STATE_GAMEOVER:
            draw_text(screen, f"Game Over, {player_name}!", BLACK, WIDTH // 2, HEIGHT // 2 - 50, BIG_FONT)
            draw_text(screen, f"Your final score is {score}/{len(category_questions)}", BLACK, WIDTH // 2, HEIGHT // 2 + 50, FONT)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
