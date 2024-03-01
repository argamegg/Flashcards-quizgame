import pygame
import sys
import random
import time
import os

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Fonts
font_dir = os.path.join(os.path.dirname(__file__), "fonts")
question_font = pygame.font.Font(os.path.join(font_dir, "OpenSans-Bold.ttf"), 36)
menu_font = pygame.font.Font(os.path.join(font_dir, "OpenSans-Bold.ttf"), 32)

# Load background music
try:
    pygame.mixer.music.load("1.mp3")
except pygame.error as e:
    print("Error loading background music:", e)
else:
    pygame.mixer.music.set_volume(0.5)  # Initial volume
    pygame.mixer.music.play(-1)  # Looping playback

# Variables for sound volume and mute status
sound_volume = 0.5  # Initial volume
mute = False  # Initially unmuted

# Define a list of flashcards (questions and answers) for each level
# Define a list of flashcards (questions and answers) for each level
flashcards = {
    "easy": [
        {"question": "What is 2 + 2?", "answer": "4"},
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "What color is the sky?", "answer": "Blue"},
        {"question": "What color is the grass?", "answer": "Green"}
    ],
    "medium": [
        {"question": "What is the chemical symbol for water?", "answer": "H2O"},
        {"question": "What is the largest mammal?", "answer": "Blue whale"},
        {"question": "How many continents are there?", "answer": "7"}
    ],
    "hard": [
        {"question": "What is the square root of 144?", "answer": "12"},
        {"question": "What year did World War II end?", "answer": "1945"},
        {"question": "What is the capital of Australia?", "answer": "Canberra"}
    ]
}

# Shuffle and select only 3 questions for the easy level
easy_flashcards = [
    {"question": "What is 2 + 2?", "answer": "4"},
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What color is the sky?", "answer": "Blue"},
    {"question": "What color is the grass?", "answer": "Green"}
]
random.shuffle(easy_flashcards)
flashcards["easy"] = easy_flashcards[:3]

# Function to draw buttons with text
def draw_button(text, x, y, width, height, font, action):
    button_rect = pygame.Rect(x, y, width, height)
    is_hovered = button_rect.collidepoint(pygame.mouse.get_pos())

    # Button color based on hover state
    button_color = (144, 238, 144)  # Light green
    if is_hovered:
        button_color = (173, 255, 47)  # Lighter green when hovered

    # Draw button background
    pygame.draw.rect(screen, button_color, button_rect, border_radius=5)

    # Draw button border
    pygame.draw.rect(screen, BLACK, button_rect, width=2, border_radius=5)

    # Render button text
    button_text = font.render(text, True, BLACK if is_hovered else WHITE)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

    # Check if button is clicked
    if is_hovered and pygame.mouse.get_pressed()[0]:
        action()

# Function to display settings
def display_settings():
    global sound_volume, mute

    while True:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the volume slider or mute button is clicked
                if 200 <= event.pos[0] <= 600 and 300 <= event.pos[1] <= 350:
                    sound_volume = (event.pos[0] - 200) / 400  # Adjust volume based on slider position
                    pygame.mixer.music.set_volume(sound_volume)
                elif 200 <= event.pos[0] <= 300 and 400 <= event.pos[1] <= 450:
                    mute = not mute
                    if mute:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif 20 <= event.pos[0] <= 120 and 20 <= event.pos[1] <= 70:
                    return  # Return to the main menu

        # Draw volume slider background
        pygame.draw.rect(screen, GRAY, (200, 325, 400, 5))
        pygame.draw.rect(screen, BLACK, (200 + int(sound_volume * 400), 315, 10, 25))

        # Draw mute button
        mute_button_text = "Mute" if not mute else "Unmute"
        pygame.draw.rect(screen, (144, 238, 144), (200, 400, 100, 50))
        mute_button_surface = menu_font.render(mute_button_text, True, BLACK)
        mute_button_rect = mute_button_surface.get_rect(center=(250, 425))
        screen.blit(mute_button_surface, mute_button_rect)

        # Draw back button
        draw_button("Back", 20, 20, 100, 50, menu_font, return_to_menu)

        pygame.display.flip()
        clock.tick(30)

# Function to exit the game
def exit_game():
    print("Exiting the game...")
    pygame.quit()
    sys.exit()

def check_answer(user_input, correct_answer):
    return user_input.lower() == correct_answer.lower()

# Function to start the game
def start_game():
    nickname = get_nickname()
    level = "easy"  # Start with easy level
    score = 0
    timer = 60  # 60 seconds per level

    running = True
    while running:
        current_flashcard = 0
        flashcards_list = flashcards[level]
        random.shuffle(flashcards_list)

        start_time = time.time()

        # Display a message indicating the level change
        if level != "easy":
            screen.fill((173, 216, 230))  # Light blue background color
            level_message_surface = question_font.render(level.capitalize() + " level will start next!", True, BLACK)
            level_message_rect = level_message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(level_message_surface, level_message_rect)
            score_message_surface = question_font.render("Current score: " + str(score), True, BLACK)
            score_message_rect = score_message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            screen.blit(score_message_surface, score_message_rect)
            pygame.display.flip()
            time.sleep(2)  # Display the message for 2 seconds

        while current_flashcard < len(flashcards_list):
            display_flashcard(level, current_flashcard)

            # Countdown timer
            remaining_time = int(timer - (time.time() - start_time))
            if remaining_time <= 0:
                break
            timer_text = question_font.render("Time: " + str(remaining_time), True, BLACK)
            screen.blit(timer_text, (10, 10))

            # Get user input
            user_input = get_user_input()

            # Check user input against correct answer
            correct_answer = flashcards_list[current_flashcard]["answer"].lower()
            if user_input.lower() == correct_answer:
                display_answer_and_wait(correct_answer, correct=True)
                score += 1
                current_flashcard += 1
            else:
                display_answer_and_wait(correct_answer, correct=False)
                current_flashcard += 1  # Move to the next question without changing the score

            pygame.display.flip()
            clock.tick(60)

        # Display score and move to the next level
        screen.fill((173, 216, 230))  # Light blue background color
        score_text = question_font.render("Score: " + str(score), True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
        pygame.display.flip()

        save_score(nickname, score)  # Save score to leaderboard
        time.sleep(2)  # Wait for 2 seconds before moving to the next level

        if level == "easy":
            level = "medium"
        elif level == "medium":
            level = "hard"
        else:
            # Game over
            screen.fill((173, 216, 230))  # Light blue background color
            game_over_text = question_font.render("Game Over!", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
            score_text = question_font.render("Final Score: " + str(score), True, BLACK)
            screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20))
            pygame.display.flip()
            time.sleep(3)  # Wait for 3 seconds before quitting
            running = False

# Function to display a flashcard with animation
def display_flashcard(level, index):
    flashcard = flashcards[level][index]
    question_surface = question_font.render(flashcard["question"], True, BLACK)
    question_rect = question_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    screen.fill((173, 216, 230))  # Light blue background color
    screen.blit(question_surface, question_rect)  # Render the question
    pygame.display.flip()  # Update the display once

    # Animation: slide flashcard from top
    for i in range(1, 101):
        screen.fill((173, 216, 230))  # Light blue background color
        screen.blit(question_surface, (
            SCREEN_WIDTH // 2 - question_rect.width // 2, SCREEN_HEIGHT // 2 - question_rect.height // 2 - i * 5))
        pygame.display.flip()
        clock.tick(30)


# Function to display answer and wait for a certain amount of time
def display_answer_and_wait(answer, correct):
    if correct:
        flashcard_surface = question_font.render("Correct! Answer: " + answer, True, BLACK)
    else:
        flashcard_surface = question_font.render("Incorrect! Answer: " + answer, True, BLACK)
    flashcard_rect = flashcard_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.fill((173, 216, 230))  # Light blue background color
    screen.blit(flashcard_surface, flashcard_rect)
    pygame.display.flip()
    time.sleep(2)  # Wait for 2 seconds

def get_user_input():
    input_box = pygame.Rect(200, 400, 400, 50)
    user_text = ''
    font = pygame.font.Font(None, 32)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('gray15')
    color = color_passive
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    color = color_active
                else:
                    color = color_passive
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return user_text
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
        screen.fill((173, 216, 230))  # Light blue background color
        txt_surface = font.render(user_text, True, color)
        width = max(400, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        clock.tick(120)

# Function to get user's nickname
def get_nickname():
    nickname = ''
    font = pygame.font.Font(None, 32)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('gray15')
    color = color_passive
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return nickname
                elif event.key == pygame.K_BACKSPACE:
                    nickname = nickname[:-1]
                else:
                    nickname += event.unicode
        screen.fill((173, 216, 230))  # Light blue background color
        txt_surface = font.render("Enter your nickname: " + nickname, True, color)
        width = max(400, txt_surface.get_width() + 10)
        pygame.draw.rect(screen, color, (200, 200, width, 50), 2)
        screen.blit(txt_surface, (205, 205))
        pygame.display.flip()
        clock.tick(120)

# Function to save scores
def save_score(nickname, score):
    leaderboard = []
    # Read existing leaderboard data
    with open('leaderboard.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) >= 2:
                nickname = parts[0]
                total_score = int(parts[1])
                leaderboard.append((nickname, total_score))

    # Add the new score
    leaderboard.append((nickname, score))

    # Sort the leaderboard by score
    leaderboard.sort(key=lambda x: x[1], reverse=True)

    # Write the sorted leaderboard to the file
    with open('leaderboard.txt', 'w') as file:
        for entry in leaderboard:
            file.write(f"{entry[0]}: {entry[1]}\n")

# Function to display leaderboard
def display_leaderboard():
        leaderboard = []
        with open('leaderboard.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(':')
                if len(parts) >= 2:  # Adjusted condition to handle lines with less than 2 parts
                    nickname = parts[0]
                    total_score = int(parts[1])  # Only consider the final score
                    leaderboard.append((nickname, total_score))
        leaderboard.sort(key=lambda x: x[1], reverse=True)

        screen.fill((173, 216, 230))  # Light blue background color
        leaderboard_text = question_font.render("Leaderboard", True, BLACK)
        screen.blit(leaderboard_text, (SCREEN_WIDTH // 2 - 100, 50))
        y_offset = 100
        for i, (nickname, total_score) in enumerate(leaderboard[:10], start=1):
            entry_text = menu_font.render(f"{i}. {nickname}: {total_score}", True, BLACK)
            screen.blit(entry_text, (SCREEN_WIDTH // 2 - 100, y_offset))
            y_offset += 40

        # Draw back button
        draw_button("Back", 20, 20, 100, 50, menu_font, return_to_menu)

        pygame.display.flip()  # Update the display once

        # Wait for the back button to be clicked
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 20 <= event.pos[0] <= 120 and 20 <= event.pos[1] <= 70:
                        return  # Return to the main menu

# Function to return to the main menu
def return_to_menu():
    main_menu()

# Main menu loop
def main_menu():
    logo = pygame.image.load("logo.png")
    logo = pygame.transform.scale(logo, (200, 150))
    while True:
        screen.fill((173, 216, 230))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
        logo_rect = logo.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(logo, logo_rect)

        draw_button("Play Quiz", 300, 200, 200, 50, menu_font, start_game)
        draw_button("Settings", 300, 300, 200, 50, menu_font, display_settings)
        draw_button("Leaderboard", 300, 400, 200, 50, menu_font, display_leaderboard)
        draw_button("Exit", 300, 500, 200, 50, menu_font, exit_game)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main_menu()
