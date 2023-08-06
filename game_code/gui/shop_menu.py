import pygame
from game_code.constants import *
from game_code.utils.game_timer import GameTimer


class Shop:
    def __init__(self, player, toggle_menu):
        # general setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('assets/fonts/LycheeSoda.ttf', 30)

        # misc
        self.width = 400
        self.space = 10
        self.padding = 8

        # menu options
        self.options = list(self.player.herb_inventory.keys()) + list(self.player.item_inventory.keys())
        self.sell_border = len(self.player.herb_inventory) - 1
        self.setup()

        # movement
        self.selected_index = 0
        self.timer = GameTimer(200)

        # buy/sell text surfaces
        self.buy_text = self.font.render('buy', False, 'Black')
        self.sell_text = self.font.render('sell', False, 'Black')


    def setup(self):
        # text surfaces and icons
        self.text_surfs = []
        self.icon_surfs = []
        self.total_height = 0

        for item in self.options:
            text_surf = self.font.render(item, False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)

            if item == 'glass_bottle' or item == 'journal':
                icon = pygame.transform.scale(pygame.image.load(f'assets/images/shop/{item}.PNG'), (48, 48))
                
            else:
                icon = pygame.transform.scale(pygame.image.load(f'assets/images/herbs/{item}/drop.PNG'), (48, 48))

            self.icon_surfs.append(icon)

        self.total_height += (len(self.text_surfs) - 1) * self.space
        self.menu_top = (SCREEN_HEIGHT / 2) - (self.total_height / 2)
        self.menu_left = (SCREEN_WIDTH / 2) - (self.width / 2)
        self.main_rect = pygame.Rect(self.menu_left, self.menu_top, self.width, self.total_height)


    def display_hearts(self):
        text_surf = self.font.render(f'${self.player.hearts}', False, 'Black')
        text_rect = text_surf.get_rect(midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20))

        pygame.draw.rect(self.display_surface, 'White', text_rect.inflate(10,10), 0, 6)
        self.display_surface.blit(text_surf, text_rect)


    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()
        num_options = len(self.options) - 1

        # show menu
        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

        if not self.timer.active:
            # navigate items in menu
            if keys[pygame.K_UP]:
                self.selected_index -= 1
                if self.selected_index < 0:
                    self.selected_index = num_options
                self.timer.activate()

            elif keys[pygame.K_DOWN]:
                self.selected_index += 1
                if self.selected_index > num_options:
                    self.selected_index = 0
                self.timer.activate()

            # buying and selling
            if keys[pygame.K_SPACE]:
                self.timer.activate()
                current_item = self.options[self.selected_index]
                
                # sell
                if self.selected_index <= self.sell_border:
                    if self.player.herb_inventory[current_item] > 0:
                        self.player.herb_inventory[current_item] -= 1
                        self.player.hearts += HERB_PRICES[current_item]
                # buy
                else:
                    price = SHOP_PRICES[current_item]
                    if self.player.hearts >= price:
                        if current_item == 'glass_bottle' or current_item == 'journal':
                            self.player.item_inventory[current_item] += 1
                        else:
                            self.player.herb_inventory[current_item] += 1
                        self.player.hearts -= price

    
    def show_entry(self, icon_surf, text_surf, amount, top, selected):
        # background
        bg_rect = pygame.Rect(self.main_rect.left, top, self.width, text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 4)

        # image icon
        icon_rect = icon_surf.get_rect(midleft = (self.main_rect.left + 10, bg_rect.centery))
        self.display_surface.blit(icon_surf, icon_rect)

        # text
        text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 300, bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)

        # amount
        amount_surf = self.font.render(str(amount), False, 'Black')
        amount_rect = amount_surf.get_rect(midright = (self.main_rect.right -20, bg_rect.centery))
        self.display_surface.blit(amount_surf, amount_rect)

        if selected:
            pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)
            # sell
            if self.selected_index <= self.sell_border:
                pos_rect = self.sell_text.get_rect(midleft = (self.main_rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.sell_text, pos_rect)
            # buy    
            else:
                pos_rect = self.buy_text.get_rect(midleft = (self.main_rect.left + 190, bg_rect.centery))
                self.display_surface.blit(self.buy_text, pos_rect)



    def update(self):
        self.input()
        self.display_hearts()
        for idx, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + idx * (text_surf.get_height() + (self.padding * 2) + self.space)
            amount_list = list(self.player.herb_inventory.values()) + list(self.player.item_inventory.values())
            amount = amount_list[idx]
            icon_surf = self.icon_surfs[idx]
            self.show_entry(text_surf, icon_surf, amount, top, self.selected_index == idx)