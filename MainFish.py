import pygame, sys
from button import Button
from pygame.locals import *
import random
import time

pygame.init()

SCREEN = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Giddy's Plunge (Main Menu)")

BG = pygame.image.load("bckgrnd.png")
BG1 = pygame.image.load("stry.png")
font = pygame.font.Font("font.ttf", 10)

# this is so that i can use multilines

def render_multiline(font, text, antialias, color, background=None):
    y_offset = 0
    text_lines = text.split("\n")
    line_sizes = tuple(font.size(string) for string in text_lines)
    output_size = [max(line_sizes, key=lambda s: s[0])[0], sum(size[1] for size in line_sizes)]
    output_surf = pygame.Surface(output_size, flags=pygame.SRCALPHA)

    for i, string in enumerate(text_lines):
        output_surf.blit(font.render(string, antialias, color, background), (0, y_offset))
        y_offset += line_sizes[i][1]

    return output_surf

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font.ttf", size)

def get_titlefont(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("title.ttf", size)

def play():
    while True:

        def main():
            # * * * * * * * * * * * * *
            # * * * INITIALIZING  * * *
            # * * * * * * * * * * * * *

            # Constants
            width = 600
            height = 600
            blue_color = (97, 159, 182)
            starting_width = int(width / 2)
            starting_height = int(height - 58)

            # Variables
            level = 0
            level_reset = 1  # Toggles starting level
            max_lives = 5  # To toggle max lives
            algae_reset = 12  # To toggle algae required
            game_length = 31  # Toggles time (seconds) per level. Add 1 to desired number.
            player_victory = False
            repeat_game = True
            show_title_screen = True
            fade_title_screen = False
            clock_tick_playing = False
            title_fade_index = 255

            next_algae_time = 0.0
            next_can_time = 0.0
            next_speed_boost = 0.0
            next_oil_time = 0.0
            next_bottle_time = 0.0
            next_extra_lives_time = 0.0
            next_shrimp = 0.0

            # Setting up the screen and clock
            pygame.init()
            screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption("Giddy's Plunge")
            clock = pygame.time.Clock()

            # Initialize Music

            # Initialize Sounds

            # Initializing Text
            font = pygame.font.Font("font.ttf", 10)
            large_font = pygame.font.Font(None, 70)
            med_font = pygame.font.Font(None, 50)
            victory_message = font.render('Level Won! Press ENTER to continue', True, (255, 255, 255))
            victory_rect = victory_message.get_rect(center=(int(width / 2), int(height / 2)))
            loss_message = font.render('You lost! To play again, press ENTER', True, (255, 255, 255))
            loss_rect = loss_message.get_rect(center=(int(width / 2), int(height / 2)))
            game_won_message = font.render('You Won! To play again, press ENTER', True, (255, 255, 255))
            game_won_rect = game_won_message.get_rect(center=(int(width / 2), int(height / 2) + 10))
            congrats_message = large_font.render('Congratulations!', True, (255, 255, 255))
            congrats_rect = congrats_message.get_rect(midbottom=(int(width / 2), game_won_rect.top - 10))
            easy_message = med_font.render('EASY', True, (255, 255, 255)).convert_alpha()
            easy_rect = easy_message.get_rect(center=(250, 473))

            # Victory / Loss Overlay
            overlay_surf = pygame.Surface((width, height))
            overlay_surf.fill((0, 0, 0))
            overlay_surf.set_alpha(70)
            overlay_surf = overlay_surf.convert_alpha()
            overlay_rect = overlay_surf.get_rect()

            # Create All Sprite Groups
            all_catchables = pygame.sprite.Group()
            all_avoidables = pygame.sprite.Group()
            all_falling = pygame.sprite.Group()
            all_sprites = pygame.sprite.Group()

            # Load Health Images
            red_health_img = pygame.image.load('redheart.png')
            red_health_img = pygame.transform.scale(red_health_img, (25, 25)).convert_alpha()
            gray_health_img = pygame.image.load('grayheart.png')
            gray_health_img = pygame.transform.scale(gray_health_img, (25, 25)).convert_alpha()

            # Load Background Image
            bg_image = pygame.image.load('backgrnd.png')
            bg_image = pygame.transform.scale(bg_image, (600, 600)).convert()
            title_image = pygame.image.load('backgrnd.png')
            title_image = pygame.transform.scale(title_image, (600, 600)).convert()

            # Load Class Images
            player_img = pygame.image.load('fishleft.gif')
            algae_img = pygame.image.load('algae.gif')
            shrimp_img = pygame.image.load('shrimp.png')
            can_img = pygame.image.load('can.png')
            bottle_img = pygame.image.load('BOTTLE.gif')
            speed_img = pygame.image.load('bolt.png')
            red_heart_img = pygame.image.load('redheart.png')
            slow_img = pygame.image.load('oil.png')

            # * * * * * * * * * * * * *
            # * * *    CLASSES    * * *
            # * * * * * * * * * * * * *

            class Player(pygame.sprite.Sprite):
                # Initialize
                def __init__(self):
                    super(Player, self).__init__()
                    self.surf = pygame.transform.scale(player_img, (100, 100)).convert_alpha()
                    # self.surf.fill((255, 255, 255))
                    self.rect = self.surf.get_rect(center=(starting_width, starting_height))
                    self.speed = 5
                    all_sprites.add(self)

                # Update - Once per frame
                def update(self, pressed_keys, has_speed_boost):
                    # Movement
                    if pressed_keys[K_LEFT] or pressed_keys[K_a]:  # West
                        self.rect.move_ip(-self.speed, 0)
                    elif pressed_keys[K_RIGHT] or pressed_keys[K_d]:  # East
                        self.rect.move_ip(self.speed, 0)
                        # Movement Boundaries
                    if self.rect.right > width - 15:
                        self.rect.right = width - 15
                    elif self.rect.left < 15:
                        self.rect.left = 15

                    # Oil / Speed Boost
                    if has_oil:
                        self.speed = 3
                    elif has_speed_boost:
                        self.speed = 9
                    else:
                        self.speed = 5

            class Falling_Object(pygame.sprite.Sprite):
                # Super class for falling objects
                def __init__(self):
                    super(Falling_Object, self).__init__()

                    self.starting_x = self.calculate_x()
                    all_sprites.add(self)
                    all_falling.add(self)

                    # Default speed
                    self.speed = random.randint(1, 3)

                # Every Frame, Update Position
                def update(self):
                    self.rect.move_ip(0, self.speed)

                    # Remove When Off Screen
                    if self.rect.top > height + 50:
                        self.kill()

                # Calculates a random starting X value
                def calculate_x(self):
                    return random.randint(50, width - 50)

            class Algae(Falling_Object):
                # NOTE: Perhaps add level as an argument and use that to adjust variables
                def __init__(self):
                    super(Algae, self).__init__()

                    # Object Surface Properties

                    self.surf = pygame.transform.scale(algae_img, (70, 70)).convert_alpha()

                    # self.surf.fill((255, 255, 255))
                    self.rect = self.surf.get_rect(center=(self.starting_x, -50))

                    # Add to Group
                    all_catchables.add(self)

            class Shrimp(Falling_Object):
                def __init__(self):
                    super(Shrimp, self).__init__()

                    # Object surface properties
                    self.surf = pygame.transform.scale(shrimp_img, (80, 80)).convert_alpha()
                    # self.surf.fill((212, 175, 55))
                    self.rect = self.surf.get_rect(center=(self.starting_x, -50))

                    # Add to Group
                    all_catchables.add(self)

            class Can(Falling_Object):
                # Costs the player one life
                def __init__(self, level):
                    super(Can, self).__init__()

                    # Object Surface Properties
                    self.surf = pygame.transform.scale(can_img, (40, 40)).convert_alpha()
                    # self.surf.fill((0, 0, 0))
                    self.rect = self.surf.get_rect(center=(self.starting_x, -50))

                    # Variables
                    self.level = level
                    self.speed = int((random.random() * 2 + 1) * (1 + self.level / 5))

                    # Add to Group
                    all_avoidables.add(self)

            class Bottle(Falling_Object):
                # An instant game over
                def __init__(self, level):
                    super(Bottle, self).__init__()

                    # Object Surface Properties
                    self.surf = pygame.transform.scale(bottle_img, (30, 30)).convert_alpha()
                    # self.surf.fill((148, 178, 28))
                    self.rect = self.surf.get_rect(center=(self.starting_x, -50))

                    # Variables
                    self.level = level
                    self.speed = int((random.random() * 2 + 1) * (1 + self.level / 5))

                    # Add to Group
                    all_avoidables.add(self)

            class Speed_Boost(Falling_Object):
                # Gives an X second boost to walking speed
                def __init__(self):
                    super(Speed_Boost, self).__init__()

                    # Object Surface Properties
                    self.surf = pygame.transform.scale(speed_img, (100, 100)).convert_alpha()
                    # self.surf.fill((175, 55, 212))
                    self.rect = self.surf.get_rect(center=(self.starting_x, -50))

                    # Variables
                    self.speed = random.randint(1, 3)

                    # Add to Groups
                    all_catchables.add(self)

            class Extra_Lives(Falling_Object):
                def __init__(self):
                    super(Extra_Lives, self).__init__()

                    self.surf = pygame.transform.scale(red_heart_img, (30, 30)).convert_alpha()
                    # self.surf.fill((240, 180, 240))
                    self.rect = self.surf.get_rect(center=(self.starting_x, -50))

                    all_catchables.add(self)

            class Oil(Falling_Object):
                # Slows the player for X seconds
                def __init__(self, level):
                    super(Oil, self).__init__()

                    # Object Surface Properties
                    self.surf = pygame.transform.scale(slow_img, (50, 50)).convert_alpha()
                    # self.surf.fill((240, 94, 35))
                    self.rect = self.surf.get_rect(center=(self.starting_x, -50))

                    # Variables
                    self.level = level
                    self.speed = int((random.random() * 2 + 1) * (1 + self.level / 5))

                    # Add to Group
                    all_avoidables.add(self)

            class Booster(Falling_Object):
                # --- Insert Code ---
                # Should booster item types be a sub class, or just have different functions within this class?
                #  -  Extra Life
                #  -  Speed Boost
                #  -  Reduced Cans
                #  -  Increased Algae / Algae Speed
                #  -  Invincibility
                #  -  Increased catch width
                #  -  Slow down time
                #  -  Bigger and Immune
                pass

            # * * * * * * * * * * * * * *
            # * * *    FUNCTIONS    * * *
            # * * * * * * * * * * * * * *

            # Next Falling Object Functions
            def calc_next_algae_time():
                next_algae_time = time.time() + random.randint(0, 3)
                return next_algae_time

            def calc_next_can_time():
                next_can_time = time.time() + random.random() * (max_can_time - min_can_time) + min_can_time
                return next_can_time

            def calc_next_speed_boost():
                next_speed_boost = time.time() + random.randint(1, 20)
                return next_speed_boost

            def calc_next_oil_time():
                next_oil_time = time.time() + random.randint(1, 15)
                return next_oil_time

            def calc_next_bottle_time():
                next_bottle_time = time.time() + random.random() * (max_bottle_time - min_bottle_time) + min_bottle_time
                return next_bottle_time

            def calc_next_extra_lives_time():
                next_extra_lives_time = time.time() + random.randint(1, 90)
                return next_extra_lives_time

            def calc_next_shrimp():
                next_shrimp = time.time() + random.randint(1, 90)
                return next_shrimp


                # Displays the underlying background image and the title overay
                screen.blit(bg_image, (0, 0))
                screen.blit(title_image, (0, 0))

                pygame.display.update()
                clock.tick(60)

            # On Hard, Speeds Up Music

            # * * * * * * * * * * * * * *
            # * * * OUTER GAME LOOP * * *
            # * * * * * * * * * * * * * *

            # OUTER LOOP - New Levels & New Games

            while repeat_game:

                # Level Increment (6 for now since 10 is kinda long)
                if player_victory and level < 6:
                    level += 1
                else:  # New Game
                    level = level_reset
                    lives_remaining = max_lives

                # Variable Resets
                stop_game = False
                player_victory = False
                player_loss = False
                has_speed_boost = False
                has_oil = False
                game_over_music_unplayed = True
                victory_music_unplayed = True
                level_up_music_unplayed = True
                end_time = time.time() + game_length
                algae_caught = 0
                algae_needed = algae_reset

                # # Resets Booster Clock Tick
                if clock_tick_playing:
                    tick_channel.stop()
                    clock_tick_playing = False

                # Resets Time Counters
                speed_boost_ending_time = 0
                oil_ending_time = 0

                # Can Time - Toggles based on level
                min_can_time = 2.25 - level * 0.2
                max_can_time = 5.0 - level * 0.4
                min_bottle_time = 12 - level * 1  # (Level 10: 2) (Level 4: 8)
                max_bottle_time = 30 - level * 2.5  # (Level 10: 5) (Level 4: 20)

                # Generate Time Variables
                next_algae_time = time.time()  # Start every level with an algae
                next_can_time = time.time() + 2  # Start every level with a can after 2 seconds
                calc_next_speed_boost()
                calc_next_oil_time()
                calc_next_bottle_time()
                calc_next_extra_lives_time()
                calc_next_shrimp()

                # Create Our Player
                player = Player()

                # * * * * * * * * * * * * * *
                # * * * INNER GAME LOOP * * *
                # * * * * * * * * * * * * * *

                # INNER LOOP - Current Game
                while not stop_game:

                    # Event Handling
                    for event in pygame.event.get():
                        # Player Closed Pygame
                        if event.type == pygame.QUIT:
                            stop_game = True
                            repeat_game = False
                        elif event.type == KEYDOWN:
                            # Player Hit ESC to Quit
                            if event.key == K_ESCAPE:
                                stop_game = True
                                repeat_game = False
                            # Player Hit ENTER to Continue / Restart
                            if (player_victory == True or player_loss == True) and event.key == K_RETURN:
                                for entity in all_sprites:
                                    entity.kill()
                                    stop_game = True

                    # Create Falling Objects
                    #   Algae - Level 1
                    if time.time() > next_algae_time:
                        Algae()
                        next_algae_time = calc_next_algae_time()
                    #   Can - Level 1
                    if time.time() > next_can_time:
                        Can(level)
                        next_can_time = calc_next_can_time()
                    if level >= 2:
                        #   SPEED BOOST - Level 2
                        if time.time() > next_speed_boost:
                            Speed_Boost()
                            next_speed_boost = calc_next_speed_boost()
                        #   OIL - Level 2
                        if time.time() > next_oil_time:
                            Oil(level)
                            next_oil_time = calc_next_oil_time()

                    if level >= 3:
                        #   BOTTLE - Level 3
                        if time.time() > next_bottle_time:
                            Bottle(level)
                            next_bottle_time = calc_next_bottle_time()
                    if level >= 4:
                        #   EXTRA LIVES - Level 4
                        if time.time() > next_extra_lives_time:
                            Extra_Lives()
                            next_extra_lives_time = calc_next_extra_lives_time()
                        #   SHRIMP - Level 4
                        if time.time() > next_shrimp:
                            Shrimp()
                            next_shrimp = calc_next_shrimp()

                    # Checks and removes status effects
                    if has_speed_boost:
                        if time.time() > speed_boost_ending_time:
                            has_speed_boost = False
                    if has_oil:
                        if time.time() > oil_ending_time:
                            has_oil = False

                    # Update All Objects
                    player.update(pygame.key.get_pressed(), has_speed_boost)
                    for entity in all_falling:
                        entity.update()

                    # Check for Collisions
                    if player_loss == False and player_victory == False:
                        # For the GOOD items
                        for catchable in all_catchables:
                            if pygame.sprite.collide_rect_ratio(0.6)(player, catchable):
                                catchable.kill()
                                catchable.rect.top = height + 100
                                if type(catchable) == Algae:

                                    algae_caught += 1
                                elif type(catchable) == Shrimp:

                                    algae_caught += 5
                                elif type(catchable) == Speed_Boost:

                                    has_speed_boost = True
                                    has_oil = False
                                    speed_boost_ending_time = time.time() + 10
                                elif type(catchable) == Extra_Lives:

                                    lives_remaining += 1
                                    lives_remaining = min(lives_remaining, max_lives)
                        # For the BAD items
                        for avoidable in all_avoidables:
                            if pygame.sprite.collide_rect_ratio(0.6)(player, avoidable):
                                avoidable.kill()
                                avoidable.rect.top = height + 100
                                if type(avoidable) == Can:

                                    lives_remaining -= 1
                                elif type(avoidable) == Bottle:
                                    lives_remaining = 0
                                    player_loss = True
                                elif type(avoidable) == Oil:

                                    has_oil = True
                                    has_speed_boost = False
                                    oil_ending_time = time.time() + 10

                    # TIME UP: Win or Lose
                    if algae_caught >= algae_needed:
                        player_victory = True
                    elif time.time() > end_time:
                        player_loss = True
                        if game_over_music_unplayed:
                            game_over_music_unplayed = False

                    # LIVES: Win or Lose
                    if lives_remaining <= 0:
                        player_loss = True
                        if game_over_music_unplayed:
                            game_over_music_unplayed = False

                    # * * * * * * * * * * * * * * * *
                    # * * * DRAW OBJECTS / TEXT * * *
                    # * * * * * * * * * * * * * * * *

                    # Draw Background
                    screen.fill(blue_color)
                    screen.blit(bg_image, (0, 0))

                    # Draw All Objects
                    for entity in all_falling:
                        screen.blit(entity.surf, entity.rect)
                    screen.blit(player.surf, player.rect)

                    # Gray Overlay on Victory / Loss
                    if player_victory or player_loss:
                        screen.blit(overlay_surf, overlay_rect)

                    # Draw Victory/Loss Message
                    if player_victory and level == 6:
                        screen.blit(game_won_message, game_won_rect)
                        screen.blit(congrats_message, congrats_rect)
                        if victory_music_unplayed:
                            victory_music_unplayed = False
                    elif player_victory:
                        screen.blit(victory_message, victory_rect)
                        if level_up_music_unplayed:
                            level_up_music_unplayed = False
                    elif player_loss:
                        screen.blit(loss_message, loss_rect)

                    # Calculate & Print Time Remaining
                    if not player_victory and not player_loss:
                        time_remaining = max(int(end_time - time.time()), 0)
                    time_message = font.render('Time Remaining: {}'.format(time_remaining), True, (0, 0, 0))
                    time_rect = time_message.get_rect(topright=(width - 20, 20))
                    screen.blit(time_message, time_rect)

                    # Print Algae Caught
                    apple_message = font.render('Food Eaten: {} / {}'.format(algae_caught, algae_needed), True, (0, 0, 0))
                    apple_rect = apple_message.get_rect(topright=(time_rect.right, time_rect.bottom + 5))
                    screen.blit(apple_message, apple_rect)

                    # Draw Red Hearts for Lives Remaining
                    if lives_remaining >= 1:
                        health_rect = red_health_img.get_rect(topright=(apple_rect.right, apple_rect.bottom + 5))
                        screen.blit(red_health_img, health_rect)
                    i = 2
                    while i <= lives_remaining:
                        health_rect = red_health_img.get_rect(topright=(health_rect.left - 5, health_rect.top))
                        screen.blit(red_health_img, health_rect)
                        i += 1

                    # Draw Gray Hearts for Lives Lost
                    lives_lost = max_lives - lives_remaining
                    if lives_lost == max_lives:
                        gray_health_rect = gray_health_img.get_rect(topright=(apple_rect.right, apple_rect.bottom + 5))
                        screen.blit(gray_health_img, gray_health_rect)
                    if lives_lost > 0 and lives_lost < max_lives:
                        gray_health_rect = gray_health_img.get_rect(topright=(health_rect.left - 5, health_rect.top))
                        screen.blit(gray_health_img, gray_health_rect)
                    i = 2
                    while i <= lives_lost:
                        gray_health_rect = red_health_img.get_rect(
                            topright=(gray_health_rect.left - 5, gray_health_rect.top))
                        screen.blit(gray_health_img, gray_health_rect)
                        i += 1

                    # TOP LEFT MESSAGES
                    top_left_messages = []

                    # Creates the Current Level Message
                    level_message = font.render('Level {}'.format(level), True, (0, 0, 0))
                    level_rect = level_message.get_rect(topleft=(20, 20))
                    top_left_messages.append([level_message, level_rect])

                    # Creates the Boost Messages

                    if has_speed_boost:
                        speed_boost_message = font.render(
                            'Speed Boost: {}'.format(int(speed_boost_ending_time - time.time())),
                            True, (0, 0, 0))
                        speed_boost_rect = speed_boost_message.get_rect(topleft=(20, 20))
                        top_left_messages.append([speed_boost_message, speed_boost_rect])
                    if has_oil:
                        oil_message = font.render('Slow-mo: {}'.format(int(oil_ending_time - time.time())), True,
                                                     (0, 0, 0))
                        oil_rect = oil_message.get_rect(topleft=(20, 20))
                        top_left_messages.append([oil_message, oil_rect])

                    # Prints All Messages in Top Left Corner
                    for i in range(len(top_left_messages)):
                        if i != 0:
                            top_left_messages[i][1] = top_left_messages[i][0].get_rect(
                                topleft=(top_left_messages[i - 1][1].left, top_left_messages[i - 1][1].bottom + 5))
                        screen.blit(top_left_messages[i][0], top_left_messages[i][1])

                    # Ticks if we've got Boost Messages

                    # Refresh Game Display
                    pygame.display.update()
                    clock.tick(60)

            pygame.quit()

        if __name__ == '__main__':
            main()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

                main_menu()

        pygame.display.update()


def story():
    while True:
        SCREEN.blit(BG1, (0, 0))

        STORY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(render_multiline(font, """
         One day, Giddy the fish was swimming along his
        
        usual route in search of something to eat. While
        
        on his way there, a thought came to mind: he 
        
        hasn't seen much of his buddies around anymore.
        
        
         In fact, he realized that he sees less and less
        
        fish by the day. Giddy didn't need to wonder why
        
        though. It was because it was getting harder to
        
        live in their part of the ocean as more time 
        
        went on. All he knew was that humans made life 
        
        more difficult and dangerous for fish such as him.
        
        
         It gets harder to breathe, find food, and settle
        
        for a shelter to rest in. That's when it hit 
        
        Giddy: it was finally time to move elsewhere.
        
        
         He knew that staying here would only lead to 
        
        worse things. It made him sad that he had to 
        
        leave behind the place he grew up in ever 
        
        since he was just a fry. Finding a better
        
        place wouldn't be easy though. Giddy has to go
        
        through human populated waters if he wants to
        
        go in this journey. It was dangerous, but a 
        
        risk that Giddy was willing to plunge into 
        
        for a better life.
            """, True, pygame.Color("yellow")), (-20,20))
        STORY_BACK = Button(image=None, pos=(300, 550),
                            text_input="BACK", font=get_font(35), base_color="Black", hovering_color="Green")

        STORY_BACK.changeColor(STORY_MOUSE_POS)
        STORY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if STORY_BACK.checkForInput(STORY_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=pygame.image.load("buttonn.png"), pos=(300, 360),
                             text_input="PLAY", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        STORY_BUTTON = Button(image=pygame.image.load("buttonn.png"), pos=(300, 460),
                              text_input="STORY", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("buttonn.png"), pos=(300, 560),
                             text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(render_multiline(get_titlefont(105), """ Giddy's
 Plunge
               
                   """, True, pygame.Color("#F9C70C")), (15, 65))
        STORY_BACK = Button(image=None, pos=(300, 550),
                            text_input="BACK", font=get_font(35), base_color="Black", hovering_color="Green")
        for button in [PLAY_BUTTON, STORY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if STORY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    story()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
