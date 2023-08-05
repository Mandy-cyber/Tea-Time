from os import walk
import pygame
from game_code.constants import *

class Utils:

    def __init__(self):
        pass

    @staticmethod
    def folder_to_surf_list(filepath):
        """
        import images from the given filepath, convert them into surfaces,
        and return them as a list of surfaces
        """
        image_surfs = []

        for _, __, image_files in walk(filepath):
            for image in image_files:
                image_path = f"{filepath}/{image}"
                image_surf = pygame.image.load(image_path).convert_alpha()
                image_surfs.append(image_surf)

        return image_surfs
    

    @staticmethod
    def folder_to_surf_dict(filepath):
        """
        import images from the given filepath, convert them into surfaces,
        and return them as a dictionary
        """
        image_dict = {}

        for _, __, image_files in walk(filepath):
            for image in image_files:
                image_path = f"{filepath}/{image}"
                image_surf = pygame.image.load(image_path).convert_alpha()
                image_name = image.split('0')[0]
                image_dict[image_name] = image_surf

        return image_dict