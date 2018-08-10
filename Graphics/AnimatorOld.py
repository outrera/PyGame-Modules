"""
Created on Oct 23, 2016
Updated on Jul 19, 2018

@author: rmainer
"""

import pygame
from Shared.GameConstants import GameConstants


class Animator:

    def __init__(self):
        self.__is_animating = False
        self.__animation_dict = {}  # a dictionary that holds all sprites lists per key (where key is animation name)
        self.__animation_key = ""   # animation key (name)
        self.__sprite_index = 0     # index of current sprite in animation list of sprites

    def prepare_animations(self, spritesheet_file, atlas_file):
        """
        load sprite sheet image and convert_alpha
        load the atlas file (created by: https://www.leshylabs.com/apps/sstool/)

        dictionary: ['action_name']['sprite_number'] = image
        """

        sprite_sheet = pygame.image.load(spritesheet_file).convert_alpha()

        with open(atlas_file, "r") as f:
            lines = f.readlines()  # read entire file

        actions_dict = {}  # actions dictionary
        actions_list = []

        for line in lines:
            name = line.split(" ")[0].lower()
            if name not in actions_list:
                actions_list.append(name)
                # for each dictionary define an empty array size MAX_SPRITES_IN_ANIMATION,
                # to store sprites without knowing how many there will be
                actions_dict[name] = [None] * GameConstants.MAX_SPRITES_IN_ANIMATION

        for line in lines:
            action_name = line.split(" ")[0].lower()
            sprite_number = line.split("(")[1].split(")")[0]
            x = int(line.split(",")[1])
            y = int(line.split(",")[2])
            w = int(line.split(",")[3])
            h = int(line.split(",")[4])
            r = pygame.Rect(x, y, w, h)
            sprite = sprite_sheet.subsurface(r)
            # sprite = pygame.transform.smoothscale(sprite, (int(r.width / 5.87), int(r.height / 5.87)))
            actions_dict[action_name][int(sprite_number)] = sprite

        # filter all None in list
        for key in actions_dict.keys():
            sprites_list = actions_dict[key]
            actions_dict[key] = [x for x in sprites_list if x is not None]

        self.__animation_dict = actions_dict

    def flip_sprites(self):
        """
        Flips the x axis of the sprites in the animation dict
        """
        for action_key, sprites_list in self.__animation_dict.items():
            for i in range(0, len(sprites_list)):
                sprite = sprites_list[i]
                self.__animation_dict[action_key][i] = pygame.transform.flip(sprite, True, False)
        return self.__animation_dict

    # def animate(self, character, animation_array_name, seconds, interval=0.02, single_cycle=False):
    #     # animate just changes the image to create the animation effect
    #     # animation method doesn't draw!!!
    #     # interval = how long one single image should be displayed in seconds
    #
    #     self.__cycle_time += seconds
    #
    #     if self.__cycle_time > interval:
    #         # each animation starts at image number 0
    #         character.image = character.animation_dictionary[animation_array_name][self.__number_of_images]
    #         print
    #         "{0} : {1} animation, image number: {2}".format(character.name, animation_array_name,
    #                                                         self.__number_of_images)
    #         # create rect for new image with previous center
    #         rect = character.image.get_rect()
    #         rect.centerx = character.rect.centerx
    #         rect.centery = character.rect.centery
    #         character.rect = rect
    #
    #         #             character.image_number += 1 # increment image number
    #         #             if character.image_number > len(character.animation_dictionary[animation_array_name])-1:
    #         #                 character.image_number = 0
    #         self.__number_of_images += 1  # increment image number
    #         if self.__number_of_images > len(character.animation_dictionary[animation_array_name]) - 1:
    #             self.__number_of_images = 0
    #             if single_cycle:  # single cycle animation (ex. death)
    #                 return True  # return done
    #         # else continue animating in loop
    #         self.__cycle_time = 0
    #     return False

    def play_animation(self, animation_key):
        if animation_key != self.__animation_key:
            # if changed to new animation, update key and reset sprite index
            self.__animation_key = animation_key
            self.__sprite_index = 0
        else:
            # increment the sprite index and reset to zero when overflow
            self.__sprite_index += 1
            if self.__sprite_index == len(self.__animation_dict[self.__animation_key]):
                self.__sprite_index = 0

        # load the new sprite
        sprite = self.__animation_dict[self.__animation_key][self.__sprite_index]

        return sprite

    def stop_animation(self):
        self.__is_animating = False
        return

    def reset_animation(self):
        self.__sprite_index = 0

    def is_animating(self):
        return self.__is_animating
