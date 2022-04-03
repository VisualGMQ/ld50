import gvar
import package
import tile

def SimpleNoColliFunc(monster, dst, obj):
    return True

def SimplePushColliFunc(monster, dst, obj):
    pushDstPos = dst + dst - monster.GetPos()
    curMap = gvar.GameMap.GetCurRooom()
    if curMap.GetCreature(pushDstPos.x, pushDstPos.y) is None and \
            curMap.GetObject(pushDstPos.x, pushDstPos.y) is None:
        curMap.SetObject(obj.GetPos().x, obj.GetPos().y, None)
        obj.Move(pushDstPos.x, pushDstPos.y)
        curMap.SetObject(obj.GetPos().x, obj.GetPos().y, obj)
        return True
    else:
        return False

def SimpleDoorColliFunc(monster, dst, obj):
    obj.Open()
    return True

def SimplePackageColliFunc(monster, dst, obj):
    return False

def SimpleBlockColliFunc(monster, dst, obj):
    return False

def SimpleSignalProjColliFunc(monster, dst, obj):
    return False


MonsterCollideFunc = {
    tile.TileColliType.NoColli: SimpleNoColliFunc,
    tile.TileColliType.Block: SimpleBlockColliFunc,
    tile.TileColliType.Door: SimpleDoorColliFunc,
    tile.TileColliType.SignalProjector: SimpleSignalProjColliFunc,
    tile.TileColliType.Package: SimplePackageColliFunc,
    tile.TileColliType.CanPush: SimplePushColliFunc,
}


def PlayerSignalProjColliFunc(player, dst, obj: package.Package):
    gvar.Mode = gvar.GameMode.MissionOK
    return False

def PlayerPackageColliFunc(player, dst, obj):
    if obj.IsClosing():
        obj.Open()
        if obj.content is not None:
            player.AddItem(obj.content)
        obj.content = None
    return False


PlayerCollideFunc = {
    tile.TileColliType.NoColli: SimpleNoColliFunc,
    tile.TileColliType.Block: SimpleBlockColliFunc,
    tile.TileColliType.Door: SimpleDoorColliFunc,
    tile.TileColliType.SignalProjector: PlayerSignalProjColliFunc,
    tile.TileColliType.Package: PlayerPackageColliFunc,
    tile.TileColliType.CanPush: SimplePushColliFunc,
}