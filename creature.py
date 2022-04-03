import gvar
import mathf
import tile
import pygame
import enum
import package
import collifunc


class CreatureState(enum.IntEnum):
    Stand = 1,
    Attack = 2,
    Run = 3,


class Creature(tile.Tile):
    def __init__(self, stand_img: pygame.Surface.subsurface, run_img: pygame.Surface.subsurface, attack_img: pygame.Surface.subsurface):
        tile.Tile.__init__(self, stand_img, tile.TileColliType.Block)

        self.stand_img = stand_img
        self.run_img = run_img
        self.attack_img = attack_img
        self.Stand()

        self.hp = 1
        self.attack = 1
        self.direction = -1
        self.collifuncs = collifunc.MonsterCollideFunc

    def SetColliFuncs(self, funcs):
        self.collifuncs = funcs

    def Move(self, x, y):
        if self.GetPos().x - x > 0:
            self.direction = 1
        elif self.GetPos().x - x < 0:
            self.direction = -1
        tile.Tile.Move(self, x, y)

    def Stand(self):
        self.image = self.stand_img

    def Run(self):
        self.image = self.run_img

    def Render(self, surface: pygame.Surface):
        if self.direction < 0:
            surface.blit(pygame.transform.flip(self.image, True, False),
                         (self.rect.x, self.rect.y))
        else:
            surface.blit(self.image,
                         (self.rect.x, self.rect.y))

    def Update(self):
        pass

    def MoveWithCollision(self, dst: pygame.Vector2):
        moved = False
        if dst != self.GetPos() and self.__CanMove(dst):
            self.Move(dst.x, dst.y)
            gvar.ShouldUpdateMonster = True
            moved = True

        obj = gvar.GameMap.GetCurRooom().GetObject(dst.x, dst.y)
        if moved and obj is not None and obj.GetColliType() == tile.TileColliType.Door:
            room = self.__findTheNearbyRoom(dst)
            if room is not None:
                if dst.x == gvar.MaxTileNumX - 1:
                    dst.x = 0
                elif dst.x == 0:
                    dst.x = gvar.MaxTileNumX - 1
                if dst.y == gvar.MaxTileNumY - 1:
                    dst.y = 0
                elif dst.y == 0:
                    dst.y = gvar.MaxTileNumY - 1
                gvar.GameMap.GetCurRooom().RemoveCreature(self)
                self.Move(dst.x, dst.y)
                room.AddCreature(self)
                room.GetObject(dst.x, dst.y).Open()
                gvar.GameMap.ChangeRoom(room)
        return moved

    def __CanMove(self, target: pygame.Vector2) -> bool:
        if target.x < 0 or target.y < 0 or target.x >= gvar.MaxTileNumX or target.y >= gvar.MaxTileNumY:
            return False
        c = gvar.GameMap.GetCurRooom().GetCreature(target.x, target.y)
        if c != self and c is not None:
            return False
        obj = gvar.GameMap.GetCurRooom().GetObject(target.x, target.y)
        if obj is None:
            return True
        else:
            return self.collifuncs[obj.GetColliType()](self, target, obj)

    def __findTheNearbyRoom(self, pos: pygame.Vector2):
        rooms = gvar.GameMap.FindNearbyRooms(gvar.GameMap.GetCurRooom())
        if pos.x == 0:
            return rooms.left
        if pos.x == gvar.MaxTileNumX - 1:
            return rooms.right
        if pos.y == 0:
            return rooms.top
        if pos.y == gvar.MaxTileNumY - 1:
            return rooms.bottom
        return None


class Player(Creature):
    def __init__(self, stand_img: pygame.Surface.subsurface, run_img: pygame.Surface.subsurface, attack_img: pygame.Surface.subsurface):
        Creature.__init__(self, stand_img, run_img, attack_img)
        self.baggage = []
        self.batteryNum = 3

    def AddItem(self, item: package.Item):
        gvar.TextRemainTime = gvar.TextMaxTime
        gvar.PlaySound("pickup")
        if item.type == package.PackageContentType.GnuBattery:
            self.batteryNum += 1
            gvar.MsgText = "Got a bullet"
        else:
            self.baggage.append(item)
            if item.type == package.PackageContentType.Alcohol:
                gvar.MsgText = "Got an alcohol"
            if item.type == package.PackageContentType.Penicillin:
                gvar.MsgText = "Got an penicillin"

    def UseItem(self, item: package.Item):
        self.hp += item.heal
        if self.hp >= gvar.MaxHp - 10:
            self.hp = gvar.MaxHp - 10
        self.baggage.remove(item)

    def GetItems(self) -> list:
        return self.baggage


class Monster(Creature):
    def __init__(self, stand_img: pygame.Surface.subsurface, run_img: pygame.Surface.subsurface, attack_img: pygame.Surface.subsurface):
        Creature.__init__(self, stand_img, run_img, attack_img)

    def Update(self):
        dir = gvar.Player.GetPos() - self.GetPos()
        if dir.x == 0 and abs(dir.y) == 1 or abs(dir.x) == 1 and dir.y == 0:
            self.Attack(self.GetPos() + dir)
        if dir.x == 0:
            self.MoveWithCollision(self.GetPos() + pygame.Vector2(0, mathf.Sign(dir.y)))
        elif dir.y == 0:
            self.MoveWithCollision(self.GetPos() + pygame.Vector2(mathf.Sign(dir.x), 0))
        elif abs(dir.x) > abs(dir.y):
            self.MoveWithCollision(self.GetPos() + pygame.Vector2(mathf.Sign(dir.x), 0))
        elif abs(dir.x) < abs(dir.y):
            self.MoveWithCollision(self.GetPos() + pygame.Vector2(0, mathf.Sign(dir.y)))
        elif abs(dir.x) == abs(dir.y):
            self.MoveWithCollision(self.GetPos() + pygame.Vector2(0, mathf.Sign(dir.y)))

    def Attack(self, dst: pygame.Vector2):
        target = gvar.GameMap.GetCurRooom().GetCreature(dst.x, dst.y)
        if target is not None and target != self:
            target.hp -= self.attack
            gvar.PlaySound("hurt")
            gvar.TextRemainTime = gvar.TextMaxTime
            gvar.MsgText = "AHHHHHHH"
            if target == gvar.Player:
                gvar.BloodImageRemainTime = gvar.BloodImageMaxTime
            if target.hp == 0:
                gvar.GameMap.GetCurRooom().RemoveCreature(target)


def CreatePlayer():
    tilesheet = gvar.ImageStorage['tiles']
    player = Player(gvar.GetSubImage(tilesheet, 0, 0),
                    gvar.GetSubImage(tilesheet, 1, 0),
                    gvar.GetSubImage(tilesheet, 2, 0))
    player.hp = 50
    player.SetColliFuncs(collifunc.PlayerCollideFunc)
    return player


def CreateMonster():
    tiles = gvar.ImageStorage['tiles']
    monster = Monster(gvar.GetSubImage(tiles, 0, 1),
                      gvar.GetSubImage(tiles, 1, 1),
                      gvar.GetSubImage(tiles, 2, 1))
    monster.SetColliFuncs(collifunc.MonsterCollideFunc)
    monster.hp = 1
    monster.attack = 20
    return monster
