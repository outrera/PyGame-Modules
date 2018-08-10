import pygame

from Shared.GameConstants import GameConstants
from Shared.MiniGameEngine import MiniGameEngine
from Shared.UIConstants import UIConstants
from UI.MenuPointer import MenuPointer
from UI.Text import Text
from UI.UIObject import UIObject
from typing import Tuple


class Menu(UIObject):

    def __init__(self, image: pygame.Surface,
                 size: Tuple,
                 menu_options=[],
                 position=(0, 0)):

        self.__padx = 15  # padding between menu left side and item left side
        self.__pady = 15  # padding between menu items

        self.image = pygame.transform.scale(image, size)
        super(Menu, self).__init__(image, position)

        self.__menu_items_list = []
        self.add_menu_items(menu_options)

        self.__pointer = MenuPointer(self)  # a pointer sprite to select menu items
        self.__menu_item_selected = None  # the selected menu item
        self.__focused = True  # active menu True/False

    def update(self):
        # TODO: should remove it from here and from the game engine, events handling should be done only by the Scene
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_UP:
                    self.move_pointer_up()
                if event.key == pygame.K_DOWN:
                    self.move_pointer_down()

    def move_pointer_up(self):
        self.__pointer.move_up()

    def move_pointer_down(self):
        self.__pointer.move_down()

    def add_text_to_menu(self, string):

        # calc item position
        if any(self.__menu_items_list):
            # if list is not empty
            last_item = self.__menu_items_list[-1]  # get the last item in the list
            position = (last_item.get_position()[0], last_item.get_position()[1] + last_item.get_size()[1] + self.__pady)
        else:
            # if there are no items in the list (this is the new item added)
            position = (self.get_position()[0] + self.__padx, self.get_position()[1] + self.__pady)

        menu_item = Text(string, position, GameConstants.WHITE, None, 48)

        self.__menu_items_list.append(menu_item)

    def add_menu_items(self, menu_items):
        for item in menu_items:
            self.add_text_to_menu(item)

    def get_menu_items_count(self):
        return len(self.__menu_items_list)

    def get_item_from_menu(self, index):
        return self.__menu_items_list[index]

    def remove_item_from_menu(self, index):
        item = self.__menu_items_list[index]
        self.__menu_items_list.remove(item)

    def get_pointer(self):
        return self.__pointer

    def is_focused(self):
        return self.__focused

    def set_focused(self):
        self.__focused = True

    def unset_focused(self):
        self.__focused = False


if __name__ == "__main__":

    SCREEN_SIZE = (480, 320)
    FPS = 60
    BLACK = (0, 0, 0)
    INTERVAL = .10  # how long one single sprite should be displayed in seconds

    menu_image = pygame.image.load(UIConstants.SPRITE_BLUE_MENU)
    menu_size = (120, 120)
    menu_options = ["Attack", "Magic", "Defend", "Item"]
    menu_position = (SCREEN_SIZE[0]/4-menu_size[0]/2, SCREEN_SIZE[1]/4-menu_size[1]/2)

    mini_game_engine = MiniGameEngine()

    menu = Menu(menu_image, menu_size, menu_options, menu_position)

    mini_game_engine.add_sprite(menu)  # add menu to engine
    for i in range(menu.get_menu_items_count()):
        mini_game_engine.add_sprite(menu.get_item_from_menu(i))

    mini_game_engine.add_sprite(menu.get_pointer())

    mini_game_engine.start()