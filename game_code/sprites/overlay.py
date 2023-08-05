import pygame
from game_code.constants import *

class Overlay:

    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # importing graphics for herbs and tools
        overlay_path = 'assets/images/overlays/'
        self.tools_surf = {tool: pygame.transform.scale(pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha(), (64, 64)) for tool in player.tools}
        self.herbs_surf = {herb: pygame.transform.scale(pygame.image.load(f'{overlay_path}{herb}.png').convert_alpha(), OVERLAY_IMG_SIZE) for herb in player.herbs}
        self.items_surf = {item: pygame.transform.scale(pygame.image.load(f'{overlay_path}{item}.png').convert_alpha(), OVERLAY_IMG_SIZE) for item in player.items}
        

    def display(self):
        # show tools
        tool_surf = self.tools_surf[self.player.current_tool]
        tool_rect = tool_surf.get_rect(midbottom = OVERLAYS['tool'])
        self.display_surface.blit(tool_surf, tool_rect)

        # show herbs
        herb_surf = self.herbs_surf[self.player.current_herb]
        herb_rect = herb_surf.get_rect(midbottom = OVERLAYS['herb'])
        self.display_surface.blit(herb_surf, herb_rect)

        # show items
        item_surf = self.items_surf[self.player.current_item]
        item_rect = item_surf.get_rect(midbottom = OVERLAYS['item'])
        self.display_surface.blit(item_surf, item_rect)
