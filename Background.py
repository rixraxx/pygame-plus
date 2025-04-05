import pygame
from math import ceil

class Scrolling_Background:
    def __init__(self, image_path: str, screen: pygame.Surface, scroll_speed: float = 7.5) -> None:
        self.image = pygame.image.load(image_path).convert_alpha()
        self.screen = screen

        # Get image and screen dimensions
        self.img_width, self.img_height = self.image.get_width(), self.image.get_height()
        self.screen_width, self.screen_height = self.screen.get_width(), self.screen.get_height()

        # Scale the image to fit screen height while maintaining aspect ratio
        scale_factor = self.screen_height / self.img_height
        new_width = int(self.img_width * scale_factor)
        new_height = int(self.img_height * scale_factor)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.img_width = new_width  # Update width after scaling

        # Scrolling properties
        self.scroll_speed = scroll_speed
        self.scroll: float = 0
        self.tiles = ceil(self.screen_width / self.img_width) + 1  # Ensure full coverage

    def draw(self):
        for i in range(self.tiles):
            self.screen.blit(self.image, (i * self.img_width + self.scroll, 0))

    def update(self):
        self.scroll -= self.scroll_speed
        if self.scroll <= -self.img_width:
            self.scroll += self.img_width  
        self.draw()

class FixedBackground:
    def __init__(self, image_src: str, display_surface: pygame.Surface):
        self.image = pygame.image.load(image_src).convert_alpha()
        self.screen = display_surface

        # Get dimensions
        self.img_width, self.img_height = self.image.get_width(), self.image.get_height()
        self.screen_width, self.screen_height = self.screen.get_width(), self.screen.get_height()

        # Scale the image to fit screen height while maintaining aspect ratio
        scale_factor = self.screen_height / self.img_height
        new_width = int(self.img_width * scale_factor)
        new_height = int(self.img_height * scale_factor)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.img_width = new_width  # Update width after scaling

    def update(self):
        """Draw the background at the top-left corner."""
        self.screen.blit(self.image, (0, 0))

class ScrollingTiledBackground:
    def __init__(self, screen: pygame.Surface, tilePath: str, scrollSpeed: float, directionX=0, directionY=0):
        self.screen = screen    
        self.tile = pygame.image.load(tilePath).convert_alpha()
        self.scrollDirectionX, self.scrollDirectionY = directionX, directionY
        self.scrollSpeedX = scrollSpeed * directionX
        self.scrollSpeedY = scrollSpeed * directionY
        self.isscrolledX, self.isscrolledY = 0, 0

        self.tileWidth, self.tileHeight = self.tile.get_size()
        screenWidth, screenHeight = screen.get_size()

        # Ensure the background is large enough to tile seamlessly
        self.bgWidth = (ceil(screenWidth / self.tileWidth) + 1) * self.tileWidth
        self.bgHeight = (ceil(screenHeight / self.tileHeight) + 1) * self.tileHeight
        self.image = pygame.Surface((self.bgWidth, self.bgHeight))

        # Determine range for both X and Y directions
        self.startX, self.endX = (-1, 1) if directionX == 1 else (0, 2)
        self.startY, self.endY = (-1, 1) if directionY == 1 else (0, 2)

        self.createBackground()
    
    def createBackground(self):
        rows = ceil(self.bgWidth / self.tileWidth)
        cols = ceil(self.bgHeight / self.tileHeight)
        for row in range(rows):
            for col in range(cols):
                self.image.blit(self.tile, (row * self.tileWidth, col * self.tileHeight))

    def update(self):
        for i in range(self.startX, self.endX):
            for j in range(self.startY, self.endY):
                x = i * self.bgWidth + self.isscrolledX if self.scrollDirectionX else 0
                y = j * self.bgHeight + self.isscrolledY if self.scrollDirectionY else 0
                self.screen.blit(self.image, (x, y))

        self.isscrolledX += self.scrollSpeedX
        self.isscrolledY += self.scrollSpeedY

        # Reset scrolling when the entire tile set moves out of view
        if abs(self.isscrolledX) >= self.bgWidth:
            self.isscrolledX = 0
        
        if abs(self.isscrolledY) >= self.bgHeight:
            self.isscrolledY = 0

class FixedTiledBackground:
    def __init__(self, screen: pygame.Surface, tilePath: str):
        self.screen = screen    
        self.tile = pygame.image.load(tilePath).convert_alpha()
        self.image = screen.copy()

        self.tileWidth, self.tileHeight = self.tile.get_size()
        self.screenWidth, self.screenHeight = screen.get_size()

        self.createBackground()
    
    def createBackground(self):
        cols = ceil(self.screenWidth / self.tileWidth)
        rows = ceil(self.screenHeight / self.tileHeight)
        for row in range(rows):
            for col in range(cols):
                self.image.blit(self.tile, (col * self.tileWidth, row * self.tileHeight))

    def update(self):
        self.screen.blit(self.image, (0, 0))

class ParallaxBackground:
    def __init__(self, image_paths: list[str], ground_path: str, screen: pygame.Surface, speeds: list[float]) -> None:
        """
        Initialize the parallax background.

        :param image_paths: List of image file paths for each layer.
        :param ground_path: File path for the ground layer.
        :param screen: The pygame screen surface.
        :param speeds: List of scroll speeds corresponding to each layer.
        """
        self.screen = screen
        self.layers = [Scrolling_Background(path, screen, speed) for path, speed in zip(image_paths, speeds)]
        self.ground = pygame.image.load(ground_path).convert_alpha()

    def update(self):
        """
        Update and draw all layers in the parallax background.
        """
        for layer in self.layers:
            layer.update()

        # Draw the ground layer at the bottom
        self.screen.blit(self.ground, (0, self.screen.get_height() - self.ground.get_height()))
