import pygame
from sys import exit
from random import randint, choice
import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate("firebase/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_surface1 = pygame.image.load("player_ani/playerA.png").convert_alpha()
        player_surface2 = pygame.image.load("player_ani/playerB.png").convert_alpha()
        self.player_walk = [player_surface1, player_surface2]
        self.player_index = 0
        self.player_jump = pygame.image.load("player_ani/playerC.png").convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(50, 325))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound("pop_sound.mp3")
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 325:
            self.gravity = -20
            self.jump_sound.play()
        if keys[pygame.MOUSEBUTTONDOWN] and self.rect.bottom >= 325:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 325:
            self.rect.bottom = 325

    def animation_state(self):
        if self.rect.bottom < 325:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "fly":
            flypoo1 = pygame.image.load("poop/flypoop/flypoo1.png").convert_alpha()
            flypoo2 = pygame.image.load("poop/flypoop/flypoo2.png").convert_alpha()
            self.frames = [flypoo1, flypoo2]
            y_pos = 170
        else:
            poop_move1 = pygame.image.load(
                "poop/dung original/dung1.png"
            ).convert_alpha()
            poop_move2 = pygame.image.load(
                "poop/dung original/dung2.png"
            ).convert_alpha()
            poop_move3 = pygame.image.load(
                "poop/dung original/dung3.png"
            ).convert_alpha()
            self.frames = [poop_move1, poop_move2, poop_move3]
            y_pos = 322

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f"SCORE : {current_time}", False, (20, 20, 20))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        collide_Sound.play()
        obstacle_group.empty()
        return False
    else:
        return True


def data_to_firebase(user_text, score):
    # screen.blit(input_surf, input_text)
    doc_ref = db.collection("leaderboard").document()
    data = {
        "user_name": user_text,
        "score": score,
        "timestamp": firestore.SERVER_TIMESTAMP,
    }

    doc_ref.set(data)
    print("data added to firestore successfully")

def show_leaderboard():
     # Query Firestore for the top 5 scores, ordered by score in descending order
    leaderboard_ref = db.collection("leaderboard").order_by("score", direction=firestore.Query.DESCENDING).limit(5)
    leaderboard_data = leaderboard_ref.get()

    # Display the leaderboard data on the screen
    y_offset = 100
    for idx, doc in enumerate(leaderboard_data):
        user_name = doc.to_dict()["user_name"]
        score = doc.to_dict()["score"]
        timestamp = doc.to_dict()["timestamp"]

        timestamp_str = str(timestamp)
        date_str = timestamp_str[:10]

        text_surf = test_font.render(f"{idx+1}.  {user_name}:   {score}---({date_str})", True, (0, 0, 0))
        text_rect = text_surf.get_rect(midleft=(50, y_offset))
        screen.blit(text_surf, text_rect)

        y_offset += 35


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Poopilicious")
clock = pygame.time.Clock()
game_active = False
inputname = False
leaderboard = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound("bg_sound.mp3")
bg_music.set_volume(0.3)
bg_music.play(loops=-1)


collide_Sound = pygame.mixer.Sound("collision sound.mp3")

# GROUPS
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# importing assets
test_font = pygame.font.Font("poopfont1.otf", 30)
score_font = pygame.font.Font("poopfont2.ttf", 30)

background_surface = pygame.image.load("bg3.png").convert_alpha()

text_surf = test_font.render("POOPilicious", False, "white").convert_alpha()
text_rect = text_surf.get_rect(topleft=(0, 0))


add_button_surf = pygame.image.load("addyourscore.png").convert_alpha()
skip_button_surf = pygame.image.load("playagain.png").convert_alpha()
leaderboard_surf = pygame.image.load("leaderboard.png").convert_alpha()
add_button_rect = add_button_surf.get_rect(center=(275, 350))
skip_button_rect = skip_button_surf.get_rect(center=(520, 350))
leaderboard_rect = leaderboard_surf.get_rect(center=(400,50))
playagain_rect = skip_button_surf.get_rect(center=(400,350))


user_text = ""
# input_surf = pygame.image.load("input_box.png").convert_alpha()
# input_rect = input_surf.get_rect(center=(400, 80))
input_rect = pygame.Rect(100, 100, 100, 20)
# color_active = pygame.Color("lightskyblue3")
# color_passive = pygame.Color("chartreuse4")
# color = color_passive
# select = False


# intro screen
# player_stand = pygame.image.load('poop/poop_idel/idelpoo1.png').convert_alpha()
# player_stand = pygame.transform.scale2x(player_stand)
# player_stand_rect = player_stand.get_rect(center=(400, 200))
p_sprite = [
    pygame.image.load("poop/poop_idel/idelpoo1.png").convert_alpha(),
    pygame.image.load("poop/poop_idel/idelpoo2.png").convert_alpha(),
    pygame.image.load("poop/poop_idel/idelpoo3.png").convert_alpha(),
    pygame.image.load("poop/poop_idel/idelpoo4.png").convert_alpha(),
    pygame.image.load("poop/poop_idel/idelpoo5.png").convert_alpha(),
    pygame.image.load("poop/poop_idel/idelpoo6.png").convert_alpha(),
    pygame.image.load("poop/poop_idel/idelpoo7.png").convert_alpha(),
]

pindex = 0
# if pindex >= len(p_sprite):
#     pindex = 0
p_surf = p_sprite[pindex]
p_rect = p_surf.get_rect(center=(400, 200))
screen.fill((94, 129, 162))
# screen.blit(p_surf, p_rect)
# pindex += 1


# intro screen text
game_name = test_font.render("POOPilicious", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render("press space to run", False, (20, 20, 20))
game_message_rect = game_message.get_rect(center=(400, 275))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["fly", "poop", "poop", "poop"])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and inputname == False :
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if p_rect.collidepoint(event.pos):
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if skip_button_rect.collidepoint(event.pos):
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)
                    score = 0
                    obstacle_group.empty()

                if add_button_rect.collidepoint(event.pos):
                    inputname = True
                    print("hoi hoi")
                
                if playagain_rect.collidepoint(event.pos):
                    game_active=True
                    leaderboard=False
                    inputname=False
                    start_time = int(pygame.time.get_ticks()/1000)
                    score = 0
                    obstacle_group.empty()

            if inputname and event.type == pygame.KEYDOWN:
                key = event.key

                if key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]

                elif key == pygame.K_RETURN:
                    print(user_text)
                    data_to_firebase(user_text, score)
                    inputname = False
                    leaderboard = True
                else:
                    user_text += event.unicode


    if game_active:
        screen.blit(background_surface, (0, 0))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        if inputname:
            screen.blit(background_surface, (0, 0))
            lb_heading = test_font.render("LEADERBOARD", False, "black").convert_alpha()
            lb_rect = lb_heading.get_rect(center=(400, 80))
            screen.blit(lb_heading, lb_rect)

            screen.blit(
                test_font.render("Enter you Text:", True, (0, 0, 0)), (100, 100)
            )
            input_surf = test_font.render(user_text, True, (255, 255, 255))
            screen.blit(input_surf, (100, 150))

        elif leaderboard:
            screen.blit(background_surface, (0, 0))

            # lb_heading = test_font.render(
            #     "LEADERBOARD", False, "black"
            # ).convert_alpha()
            # lb_rect = lb_heading.get_rect(center=(400, 50))
            # screen.blit(lb_heading, lb_rect)
            screen.blit(leaderboard_surf,leaderboard_rect)
            show_leaderboard()
            screen.blit(skip_button_surf,playagain_rect)


        else:
            screen.fill((1, 169, 155))
            screen.blit(p_surf, p_rect)
            title_surf = pygame.image.load("heading.png").convert_alpha()
            game_name_rect = title_surf.get_rect(center=(400, 80))
            score_message = test_font.render(
                f"Your score : {score}", False, (20, 20, 20)
            )
            score_message_rect = score_message.get_rect(center=(400, 275))
            screen.blit(title_surf, game_name_rect)

            if score == 0:
                screen.blit(game_message, game_message_rect)
            else:
                screen.blit(score_message, score_message_rect)
                screen.blit(add_button_surf, add_button_rect)
                screen.blit(skip_button_surf, skip_button_rect)
                # input_surf = base_font.render(user_text, True, (255, 255, 255))

    pygame.display.update()
    clock.tick(60)
