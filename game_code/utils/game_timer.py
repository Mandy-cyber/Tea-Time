import pygame

class GameTimer:
    
    def __init__(self, duration, end_function = None):
        self.duration = duration
        self.start_time = 0 # in ms
        self.end_func = end_function
        self.active = False
    
    def activate(self):
        """start timer"""
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        """end timer"""
        self.active = False
        self.start_time = 0
    
    def update(self):
        """update timer until time to end"""
        if (pygame.time.get_ticks() - self.start_time) >= self.duration:
            if self.end_func != None and self.start_time != 0:
                self.end_func()
                
            self.deactivate()