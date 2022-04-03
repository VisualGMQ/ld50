import tile
import pygame
import enum


class PackageContentType(enum.IntEnum):
    Alcohol = 1,
    Penicillin = 2,
    GnuBattery = 3,


ItemDescription = {
    PackageContentType.Alcohol: "Alcohol, heal some infection",
    PackageContentType.Penicillin: "Penicillin, heal much infection",
}

class Item:
    def __init__(self, type: PackageContentType, heal: int):
        self.type = type
        self.heal = heal


class Package(tile.Tile):
    def __init__(self, img: pygame.Surface.subsurface, opened_img: pygame.Surface.subsurface, item: Item):
        tile.Tile.__init__(self, img, tile.TileColliType.Package)
        self.opened_img = opened_img
        self.content = item
        self.isClosing = True

    def Open(self):
        self.image = self.opened_img
        self.isClosing = False

    def IsClosing(self):
        return self.isClosing

    def GetContent(self) -> PackageContentType:
        return self.content
