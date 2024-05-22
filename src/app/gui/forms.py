
import pygame as pg
from models.enums import GameMode
from gui.elements import Icon, AbstractGUIElement, Label
from scores import ScoreBoard
from space import PlayerSpace
from utils import load_and_transform_image
from settings import LABEL_COLOR, TEXT_SIZE_REL, BUTTON_COLOR


class GameModeSelectionBox(AbstractGUIElement):
    text_size_rel = 0.03
    alpha = 200
    def __init__(self, screen, id_, rect, available_game_mode_names: list[str]):
        AbstractGUIElement.__init__(self, screen=screen, id_=id_, rect=rect)
        self.available_game_mode_names = available_game_mode_names
        self.image = load_and_transform_image("selection_box_background.png", space_width=rect[2], size_factor=1)
        self.label = Label(
            screen, 
            id_="GameModeSelectionBoxLabel", 
            rect=self.rect, 
            text="GameMode selection"
        )
        self.label.rect[0] += self.label.text_size*8

        size_factor = 0.15
        icon_position = [
            (rect[0] + rect[2]/3 - rect[2]/6, rect[1] + rect[3]/2 - rect[3]/4 + self.text_size, 0, 0),
            (rect[0] + rect[2]/3 - rect[2]/6, rect[1] + rect[3]/2 + rect[3]/4 + self.text_size, 0, 0),
            (rect[0] + rect[2]/1.5 - rect[2]/6, rect[1] + rect[3]/2 + rect[3]/4 + self.text_size, 0, 0),
            (rect[0] + rect[2]/1.5 - rect[2]/6, rect[1] + rect[3]/2 - rect[3]/4 + self.text_size, 0, 0), 
            (rect[0] + rect[2]/1.5 + rect[2]/6, rect[1] + rect[3]/2 - rect[3]/4 + self.text_size, 0, 0),
            (rect[0] + rect[2]/1.5 + rect[2]/6, rect[1] + rect[3]/2 + rect[3]/4 + self.text_size, 0, 0),
            ]
        self.group = [
            Icon(screen=screen, 
                 id_=f"{GameMode.Clubs.name}Icon",
                 rect=icon_position[0],
                 image=load_and_transform_image("icons", f"{GameMode.Clubs.name.lower()}.png", space_width=rect[2], size_factor=size_factor),
                 game_mode=GameMode.Clubs
            ),
            Icon(screen=screen,
                 id_=f"{GameMode.Spades.name}Icon",
                 rect=icon_position[1],
                 image=load_and_transform_image("icons", f"{GameMode.Spades.name.lower()}.png", space_width=rect[2], size_factor=size_factor),
                 game_mode=GameMode.Spades
            ),
            Icon(screen=screen,
                 id_=f"{GameMode.Diamonds.name}Icon",
                 rect=icon_position[2],
                 image=load_and_transform_image("icons", f"{GameMode.Diamonds.name.lower()}.png", space_width=rect[2], size_factor=size_factor),
                 game_mode=GameMode.Diamonds
            ),
            Icon(screen=screen,
                 id_=f"{GameMode.Hearts.name}Icon",
                 rect=icon_position[3],
                 image=load_and_transform_image("icons", f"{GameMode.Hearts.name.lower()}.png", space_width=rect[2], size_factor=size_factor),
                 game_mode=GameMode.Hearts
            ),
            Icon(screen=screen,
                 id_=f"{GameMode.NoTricks.name}Icon",
                 rect=icon_position[4],
                 image=load_and_transform_image("icons", f"{GameMode.NoTricks.name.lower()}.png", space_width=rect[2], size_factor=size_factor),
                 game_mode=GameMode.NoTricks
            ),
            Icon(screen=screen,
                 id_=f"{GameMode.NoTrump.name}Icon",
                 rect=icon_position[5],
                 image=load_and_transform_image("icons", f"{GameMode.NoTrump.name.lower()}.png", space_width=rect[2], size_factor=size_factor),
                 game_mode=GameMode.NoTrump
            )
        ]
        self.icon_selected = None
        self.expired = False

    def simulate_selecting_icon(self, game_mode: GameMode):
        icon_selected = [i for i in self.group if i.game_mode.name == game_mode.name][0]
        icon_selected.clicked = True
        self.icon_selected = icon_selected

    def expire(self):
        self.expired = True

    def update(self):
        pass

    def render(self):
        self.image.set_alpha(self.alpha)
        self.screen.blit(self.image, (self.rect.topleft))
        for icon in self.group: 
            if icon.game_mode.name not in self.available_game_mode_names:
                icon.image.set_alpha(10)
                self.screen.blit(icon.image, icon.rect)
            else:
                icon.render()
        self.label.render()
    
    def check_mouse(self, pos, down):
        for icon in self.group:
            icon.check_mouse(pos, down)
            if not self.icon_selected and icon.clicked:
                self.icon_selected = icon


class ScoreBoardBox(AbstractGUIElement):
    text_size_rel = 0.1
    def __init__(self, screen, id_, rect, score_board: ScoreBoard):
        AbstractGUIElement.__init__(self, screen=screen, id_=id_, rect=rect)
        self.text_size = int(rect[2]*self.text_size_rel)
        self.score_board = score_board
        self.font = pg.font.SysFont('arial', self.text_size, bold=1)
        self.image = load_and_transform_image("score_board.png", space_width=rect[2], size_factor=1)
        self.player_name_position = [
            (rect[0] + rect[2]/10, rect[1] + rect[3]/3 - rect[3]/6),
            (rect[0] + rect[2]/10, rect[1] + rect[3]/3 + rect[3]/6),
            (rect[0] + rect[2]/10, rect[1] + rect[3]/1.5 + rect[3]/6),
            ]
        self.icon_rendered = None

    def update_game_mode_icon(self):
        if self.score_board.game_mode and not self.icon_rendered:
            image = None
            size_factor = 0.35
            if self.score_board.game_mode == GameMode.Clubs:
                image = load_and_transform_image("icons", f"{GameMode.Clubs.name.lower()}.png", space_width=self.rect[2], size_factor=size_factor)
            elif self.score_board.game_mode == GameMode.Spades:
                image = load_and_transform_image("icons", f"{GameMode.Spades.name.lower()}.png", space_width=self.rect[2], size_factor=size_factor)
            elif self.score_board.game_mode == GameMode.Diamonds:
                image = load_and_transform_image("icons", f"{GameMode.Diamonds.name.lower()}.png", space_width=self.rect[2], size_factor=size_factor)
            elif self.score_board.game_mode == GameMode.Hearts:
                image = load_and_transform_image("icons", f"{GameMode.Hearts.name.lower()}.png", space_width=self.rect[2], size_factor=size_factor)
            elif self.score_board.game_mode == GameMode.NoTricks:
                image = load_and_transform_image("icons", f"{GameMode.NoTricks.name.lower()}.png", space_width=self.rect[2], size_factor=size_factor)
            elif self.score_board.game_mode == GameMode.NoTrump:
                image = load_and_transform_image("icons", f"{GameMode.NoTrump.name.lower()}.png", space_width=self.rect[2], size_factor=size_factor)

            if image:
                icon = Icon(
                    screen=self.screen,
                    rect=(self.rect[0]+self.rect[2]/1.3, (self.rect[1]+self.rect[3]/1.7), 0, 0),
                    image=image, 
                    game_mode=self.score_board.game_mode,
                    id_="GameModeSelectedIcon"
                )
                self.icon_rendered = icon

        elif not self.score_board.game_mode:
            self.icon_rendered = None

    def update(self):
        self.update_game_mode_icon()

    def render_player_score(self, player: PlayerSpace, pos):
        txt = f"{player.name}: {player.player_info.total_score}"
        text_surface = self.font.render(txt, True, self.color)
        self.screen.blit(text_surface, pos)

    def render(self):
        self.screen.blit(self.image, (self.rect.topleft))
        self.render_player_score(self.score_board.first_player, self.player_name_position[0])
        self.render_player_score(self.score_board.second_player, self.player_name_position[1])
        self.render_player_score(self.score_board.third_player, self.player_name_position[2])
        if self.icon_rendered:
            self.icon_rendered.render()

    def check_mouse(self, pos, down):
        if self.icon_rendered:
            self.icon_rendered.check_mouse(pos, down)