import pygame
import gvar
import enum


class TileColliType(enum.IntEnum):
    NoColli = 0,
    Block = 1,
    CanPush = 2,
    Door = 3,
    SignalProjector = 4,
    Package = 5,


class Tile(pygame.sprite.Sprite):
    def __init__(self, img: pygame.Surface.subsurface, t: TileColliType):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.__pos = pygame.Vector2(0, 0)
        self.__oldPos = self.__pos
        self.__collitype = t

    def GetColliType(self) -> bool:
        return self.__collitype

    def RecalcRect(self):
        self.rect.x = self.__pos.x * gvar.TileSize
        self.rect.y = self.__pos.y * gvar.TileSize

    def Move(self, x, y):
        self.__oldPos = self.__pos
        self.__pos.x = x
        self.__pos.y = y
        self.RecalcRect()

    def GetPos(self) -> pygame.Vector2:
        return self.__pos.copy()

    def Back2OldPos(self):
        self.__pos = self.__oldPos
