import creature
import gvar
import pygame
import tile


class Controller:
    def __init__(self, c: creature.Creature):
        self.ChangeTarget(c)

    def ChangeTarget(self, c: creature.Creature):
        self.target = c

    def Update(self):
        if self.target is None:
            return None
        pos = self.target.GetPos()
        dst = pos.copy()

        if gvar.Keyboard.IsKeyPressed(pygame.K_a):
            dst.x -= 1
        elif gvar.Keyboard.IsKeyPressed(pygame.K_d):
            dst.x += 1
        elif gvar.Keyboard.IsKeyPressed(pygame.K_w):
            dst.y -= 1
        elif gvar.Keyboard.IsKeyPressed(pygame.K_s):
            dst.y += 1
        elif gvar.Keyboard.IsKeyPressed(pygame.K_SPACE):
            gvar.ShouldUpdateMonster = True

        if gvar.Mouse.IsPressed(3) and self.target.batteryNum > 0:
            pos = gvar.Mouse.GetPos()
            monster = gvar.GameMap.GetCurRooom().GetCreature(pos.x // gvar.TileSize, pos.y // gvar.TileSize)
            if monster is not None and monster != self.target:
                gvar.PlaySound("shoot")
                monster.hp -= 1
                self.target.batteryNum -= 1
                if monster.hp == 0:
                    gvar.GameMap.GetCurRooom().RemoveCreature(monster)

        if self.target.MoveWithCollision(dst):
            gvar.PlaySound("walk")

        if gvar.Keyboard.IsKeyPressed(pygame.K_e):
            gvar.ShowBaggage = not gvar.ShowBaggage