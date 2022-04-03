import tile
import gvar
import door
import package


def CreateFloor():
    return tile.Tile(gvar.GetSubImage(gvar.ImageStorage['tiles'], 2, 2),
                     tile.TileColliType.NoColli)


def CreateChair():
    return tile.Tile(gvar.GetSubImage(gvar.ImageStorage['tiles'], 3, 2),
                     tile.TileColliType.CanPush)


def CreateTable():
    return tile.Tile(gvar.GetSubImage(gvar.ImageStorage['tiles'], 0, 3),
                     tile.TileColliType.Block)


def CreateWall():
    return tile.Tile(gvar.GetSubImage(gvar.ImageStorage['tiles'], 1, 3),
                     tile.TileColliType.Block)


def CreateDoor():
    return door.Door(gvar.GetSubImage(gvar.ImageStorage['tiles'], 2, 3),
                     gvar.GetSubImage(gvar.ImageStorage['tiles'], 1, 2))


def CreateSignalProjector():
    return tile.Tile(gvar.GetSubImage(gvar.ImageStorage['tiles'], 3, 3),
                     tile.TileColliType.SignalProjector)


PackageContentInfo = {
    package.PackageContentType.Alcohol: 10,
    package.PackageContentType.Penicillin: 20,
    package.PackageContentType.GnuBattery: 0,
}


def CreatePackage(content: package.PackageContentType):
    return package.Package(gvar.GetSubImage(gvar.ImageStorage['tiles'], 0, 2),
                           gvar.GetSubImage(gvar.ImageStorage['tiles'], 4, 2),
                           package.Item(content, PackageContentInfo[content]))
