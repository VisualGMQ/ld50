import creature
import gvar
import pygame
import enum
import tile_factory
import mathf
import log
import door
import package


class TileType(enum.IntEnum):
    Floor = 0,
    Object = 1,

    TileTypeNum = 3


EntryMark = '0'
FloorMark = '1'
ChairMark = '2'
TableMark = '3'
DoorMark = '4'
WallMark = '5'
MonsterMark = '6'
SignalProjectorMark = '7'
NothingMark = 'N'
AlcoholPackage = '8'
PenicPackage = '9'
BatteryPackage = 'A'

ObjectMarkNum = 8


class Room:
    def __init__(self, text_map: str, pos: pygame.Vector2):
        self.pos = pos

        self.groups = []
        self.creatures = []
        self.entry = None
        for i in range(0, TileType.TileTypeNum):
            self.groups.append(mathf.Matrix(gvar.MaxTileNumX, gvar.MaxTileNumY))

        for i in range(0, len(text_map)):
            x = i % gvar.MaxTileNumX
            y = i // gvar.MaxTileNumX

            if self.__isTypeValid(text_map[i]) and text_map[i] != 'N':
                sprite = tile_factory.CreateFloor()
                sprite.Move(x, y)
                self.groups[TileType.Floor].Set(x, y, sprite)

            if text_map[i] == ChairMark:
                sprite = tile_factory.CreateChair()
                sprite.Move(x, y)
                self.groups[TileType.Object].Set(x, y, sprite)
            elif text_map[i] == TableMark:
                sprite = tile_factory.CreateTable()
                sprite.Move(x, y)
                self.groups[TileType.Object].Set(x, y, sprite)
            elif text_map[i] == WallMark:
                sprite = tile_factory.CreateWall()
                sprite.Move(x, y)
                self.groups[TileType.Object].Set(x, y, sprite)
            elif text_map[i] == DoorMark:
                sprite = tile_factory.CreateDoor()
                sprite.Move(x, y)
                self.groups[TileType.Object].Set(x, y, sprite)
            elif text_map[i] == EntryMark:
                sprite = tile_factory.CreateDoor()
                sprite.Move(x, y)
                self.groups[TileType.Object].Set(x, y, sprite)
                self.entry = (x, y)
            elif text_map[i] == MonsterMark:
                sprite = creature.CreateMonster()
                sprite.Move(x, y)
                self.AddCreature(sprite)
            elif text_map[i] == SignalProjectorMark:
                sprite = tile_factory.CreateSignalProjector()
                sprite.Move(x, y)
                self.groups[TileType.Object].Set(x, y, sprite)
            elif text_map[i] == AlcoholPackage:
                sprite = tile_factory.CreatePackage(package.PackageContentType.Alcohol)
                sprite.Move(x, y)
                self.groups[TileType.Object].Set(x, y, sprite)
            elif text_map[i] == PenicPackage:
                sprite = tile_factory.CreatePackage(package.PackageContentType.Penicillin)
                sprite.Move(x, y)
                self.groups[TileType.Object].Set(x, y, sprite)
            elif text_map[i] == BatteryPackage:
                sprite = tile_factory.CreatePackage(package.PackageContentType.GnuBattery)
                sprite.Move(x, y)
                self.groups[TileType.Object].Set(x, y, sprite)


    def GetEntry(self) -> tuple:
        return self.entry

    def GetPos(self) -> pygame.Vector2:
        return self.pos.copy()

    def __isTypeValid(self, t) -> bool:
        return t[0] >= '0' and t[0] <= '9' or t[0] >= 'A' and t[0] <= 'Z'

    def GetFloor(self, x, y):
        return self.groups[TileType.Floor].Get(int(x), int(y))

    def GetObject(self, x, y):
        if self.__isInMap(x, y):
            return self.groups[TileType.Object].Get(int(x), int(y))
        else:
            return None

    def SetFloor(self, x, y, floor):
        return self.groups[TileType.Floor].Set(int(x), int(y), floor)

    def SetObject(self, x, y, floor):
        return self.groups[TileType.Object].Set(int(x), int(y), floor)

    def GetCreatures(self):
        return self.creatures

    def RemoveCreature(self, c: creature.Creature):
        self.creatures.remove(c)

    def __isInMap(self, x, y) -> bool:
        return x >= 0 and x < gvar.MaxTileNumX and y >= 0 and y < gvar.MaxTileNumY

    def AddCreature(self, c):
        if gvar.DebugMode:
            for creature in self.creatures:
                if creature.GetPos() == c.GetPos():
                    log.Log("You put two or more creature at one place!!!")
        return self.creatures.append(c)

    def FindDoors(self):
        doors = []
        for elem in self.groups[TileType.Object].data:
            if type(elem) == door.Door:
                doors.append(elem)
        return doors

    def GetCreature(self, x, y) -> bool:
        for c in self.creatures:
            if c.GetPos() == pygame.Vector2(int(x), int(y)):
                return c
        return None

    def Render(self, surface):
        for group in self.groups:
            for elem in group.data:
                if elem is not None:
                    surface.blit(elem.image, (elem.rect.x, elem.rect.y))
        for creature in self.creatures:
            if creature is not None:
                creature.Render(surface)

    def Update(self):
        for group in self.groups:
            for elem in group.data:
                if elem is not None:
                    elem.update()
        if gvar.ShouldUpdateMonster:
            for creature in self.creatures:
                if creature is not None:
                    creature.Update()
            gvar.Player.hp -= gvar.HpDownPerTurn
            gvar.ShouldUpdateMonster = False
        doors = self.FindDoors()
        for d in doors:
            canClose = True
            if not d.IsClosing():
                for c in self.GetCreatures():
                    if d.GetPos() == c.GetPos():
                        canClose = False
                if canClose:
                    d.Close()


def LoadRoomDataFromFile(file) -> tuple:
    map_data = ""
    line = file.readline().strip()
    if line is None or line == "":
        return map_data, None
    (x, y) = line.split(',')
    x = int(x)
    y = int(y)
    line = file.readline().strip()
    while line != "NewRoom" and line is not None and line != "":
        map_data += line
        line = file.readline().strip()
    return map_data, (x, y)


def CreateRoomFromFile(file) -> Room:
    roomInfo = LoadRoomDataFromFile(file)
    if roomInfo[0] != "":
        return Room(roomInfo[0], pygame.Vector2(roomInfo[1][0], roomInfo[1][1]))
    return None


class NearbyRoomInfo:
    def __init__(self):
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None


class GameMap:
    def __init__(self, rooms: list):
        self.rooms = rooms
        self.curRoom = None
        self.entryPos = None
        for room in rooms:
            if room.GetEntry() is not None:
                self.curRoom = room
                self.entryPos = room.GetEntry()

    def PutPlayerOnMap(self, player):
        player.Move(self.entryPos[0], self.entryPos[1])
        self.curRoom.AddCreature(player)

    def GetCurRooom(self) -> Room:
        return self.curRoom

    def ChangeRoom(self, room) -> Room:
        self.curRoom = room

    def FindNearbyRooms(self, room) -> NearbyRoomInfo:
        nearbyRooms: NearbyRoomInfo = NearbyRoomInfo()
        for r in self.rooms:
            rpos = r.GetPos()
            pos = room.GetPos()
            if not r == room:
                if pos.x == rpos.x and abs(pos.y - rpos.y) == 1:
                    if pos.y < rpos.y:
                        nearbyRooms.bottom = r
                    elif pos.y > rpos.y:
                        nearbyRooms.top = r
                elif pos.y == rpos.y and abs(pos.x - rpos.x) == 1:
                    if pos.x < rpos.x:
                        nearbyRooms.right = r
                    elif pos.x > rpos.x:
                        nearbyRooms.left = r
        return nearbyRooms


def LoadMapFromFile(filename: str) -> GameMap:
    rooms = []
    file = open(filename)
    file.readline()
    room = CreateRoomFromFile(file)
    while room is not None:
        rooms.append(room)
        room = CreateRoomFromFile(file)
    file.close()
    return GameMap(rooms)
