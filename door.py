import tile
import pygame


class Door(tile.Tile):
    def __init__(self, open_img: pygame.Surface.subsurface, close_img: pygame.Surface.subsurface):
        tile.Tile.__init__(self, close_img, tile.TileColliType.Door)
        self.open_img = open_img
        self.close_img = close_img
        self.is_closing = True

    def IsClosing(self) -> bool:
        return self.is_closing

    def ToggleClose(self):
        if self.is_closing:
            self.Open()
        else:
            self.Close()

    def Open(self):
        self.is_closing = False
        self.image = self.open_img

    def Close(self):
        self.is_closing = True
        self.image = self.close_img
