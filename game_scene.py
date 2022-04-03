import gvar
import creature
import pygame

import package
import ui

StoryText = [
    "Where are they come from?",
    "How did they get in here?",
    "My colleagues are all dead! On their hand!",
    "And my wireless communication equipment can't work either.",
    "I must find the console in the main room,",
    "and tell the people on Earth what's going on here.",
    "But THEY infect me too!",
    "I don't think I'll live long, but I must finish my mission.",
    "There's some medicine in the other room, they might buy me some time.",
    "And if I see THEM, I'll shoot them by my gnu!",
    "Use W, A, S, D to go to the main room.",
    "Use SPACE to wait a turn.",
    "E to open my baggage and click item to use,",
    "Right click on the monster to shoot them."
]


class GameScene:
    def Init(self):
        gvar.Mode = gvar.GameMode.BackgroundStory
        gvar.Player = creature.CreatePlayer()

        self.curStoryLineIdx = 0

        doors = gvar.GameMap.GetCurRooom().FindDoors()
        if len(doors) != 0:
            gvar.Player.Move(doors[0].GetPos().x, doors[0].GetPos().y)
            doors[0].Open()
        gvar.GameMap.GetCurRooom().AddCreature(gvar.Player)

        gvar.Controller.ChangeTarget(gvar.Player)

    def Update(self):
        if gvar.Mode == gvar.GameMode.Playing:
            if gvar.Controller is not None:
                gvar.Controller.Update()

        gvar.GameMap.GetCurRooom().Update()

        if gvar.Mode == gvar.GameMode.BackgroundStory:
            if gvar.Keyboard.IsKeyPressed(pygame.K_SPACE):
                self.curStoryLineIdx += 1
                if self.curStoryLineIdx >= len(StoryText):
                    gvar.Mode = gvar.GameMode.Playing

        if gvar.Player.hp <= 0:
            gvar.Mode = gvar.GameMode.MissionFailed

    def Render(self):
        gvar.GameMap.GetCurRooom().Render(gvar.GameSurface)
        self.__renderBloodImage()
        self.__renderInfection()

        self.__renderBattery()

        if gvar.ShowBaggage:
            self.__renderBaggage()

        if gvar.Mode == gvar.GameMode.BackgroundStory:
            textImg = gvar.GameFont.render(StoryText[self.curStoryLineIdx], True, (99, 155, 255))
            gvar.GameSurface.blit(pygame.transform.scale(textImg,
                                                         (textImg.get_width() // 1.5,
                                                          textImg.get_height() // 1.5)),
                                  (0, 50))
            hintImg = gvar.GameFont.render("[Press Enter to continue]", True, (200, 155, 255))
            gvar.GameSurface.blit(pygame.transform.scale(hintImg,
                                                         (hintImg.get_width() // 1.5,
                                                          hintImg.get_height() // 1.5)),
                                  (0, 60 + textImg.get_height()))

        if gvar.Mode == gvar.GameMode.MissionFailed:
            self.__renderMissionFailedText()
        if gvar.Mode == gvar.GameMode.MissionOK:
            self.__renderMissionOKText()

        self.__renderMsgText()

    def __renderMissionFailedText(self):
        font_surface = gvar.GameFont.render("Mission Failed", True, (255, 0, 0))
        gvar.GameSurface.blit(font_surface,
                              ((gvar.GameWindowSize[0] - font_surface.get_width()) // 2,
                               (gvar.GameWindowSize[1] - font_surface.get_height()) // 2))
        font_surface = gvar.GameFont.render("You failed to fight the infection and collapsed", True, (255, 0, 0))
        gvar.GameSurface.blit(font_surface,
                              ((gvar.GameWindowSize[0] - font_surface.get_width()) // 2,
                               (gvar.GameWindowSize[1] - font_surface.get_height()) // 2 + 50))

    def __renderMissionOKText(self):
        font_surface = gvar.GameFont.render("Mission Complete", True, (0, 255, 0))
        gvar.GameSurface.blit(font_surface,
                              ((gvar.GameWindowSize[0] - font_surface.get_width()) // 2,
                               (gvar.GameWindowSize[1] - font_surface.get_height()) // 2 - 50))
        font_surface = gvar.GameFont.render("Although You died on Mars, but you save the world",
                                            True,
                                            (0, 255, 0))
        gvar.GameSurface.blit(font_surface,
                              ((gvar.GameWindowSize[0] - font_surface.get_width()) // 2,
                               (gvar.GameWindowSize[1] - font_surface.get_height()) // 2))
        font_surface = gvar.GameFont.render("Thanks for playing",
                                            True,
                                            (255, 255, 255))
        gvar.GameSurface.blit(font_surface,
                              ((gvar.GameWindowSize[0] - font_surface.get_width()) // 2,
                               (gvar.GameWindowSize[1] - font_surface.get_height()) // 2 + 50))

    def __renderBaggage(self):
        drawRect = pygame.Rect((gvar.GameWindowSize[0] - 400) // 2, 32, 450, 300)
        pygame.draw.rect(gvar.GameSurface, (87, 98, 76), drawRect)
        padding = drawRect.w // (2 * gvar.TileSize)
        maxX = drawRect.w // (gvar.TileSize + padding)
        x = 0
        y = 0

        titleImg = gvar.GameFont.render("Baggage", True, (0, 255, 0))
        gvar.GameSurface.blit(titleImg, (drawRect.x, drawRect.y))

        for item in gvar.Player.GetItems():
            img = self.__getItemImg(item.type)
            evt = ui.ImgButton(img, pygame.Vector2(padding // 2 + x * (padding + gvar.TileSize) + drawRect.x,
                                                   padding // 2 + (y + 1) * (padding + gvar.TileSize) + drawRect.y))
            if evt == ui.UIEvent.Hover:
                fontImg = gvar.GameFont.render(package.ItemDescription[item.type], True, (255, 255, 255))
                gvar.GameSurface.blit(fontImg, (drawRect.x, drawRect.y + drawRect.h - gvar.TileSize))
            elif evt == ui.UIEvent.BtnDown:
                gvar.Player.UseItem(item)
                gvar.PlaySound("powerup")

            x += 1
            if x >= maxX:
                x = 0
                y += 1

    def __getItemImg(self, itemType: package.PackageContentType):
        if itemType == package.PackageContentType.Alcohol:
            return gvar.GetSubImage(gvar.ImageStorage['tiles'], 3, 0)
        elif itemType == package.PackageContentType.Penicillin:
            return gvar.GetSubImage(gvar.ImageStorage['tiles'], 3, 1)

    def __renderBloodImage(self):
        if gvar.BloodImageRemainTime > 0:
            blood = gvar.ImageStorage['blood']
            gvar.GameSurface.blit(blood, (0, 0))
            gvar.GameSurface.blit(pygame.transform.flip(blood, True, True),
                                  (gvar.GameWindowSize[0] - 64,
                                   gvar.GameWindowSize[1] - 64))
            gvar.BloodImageRemainTime -= 1

    def __renderInfection(self):
        hpWidth = gvar.TileSize
        hpHeight = (gvar.MaxTileNumY - 1) * gvar.TileSize * (1 - gvar.Player.hp / gvar.MaxHp)
        pygame.draw.rect(gvar.GameSurface,
                         (0, 255, 0),
                         pygame.Rect(gvar.GameWindowSize[0] - gvar.TileSize,
                                     gvar.GameWindowSize[1] - hpHeight - gvar.TileSize,
                                     hpWidth, hpHeight))
        infectionTile = gvar.GetSubImage(gvar.ImageStorage['tiles'], 4, 3)
        gvar.GameSurface.blit(infectionTile, (gvar.GameWindowSize[0] - 32, gvar.GameWindowSize[1] - 32))

    def __renderBattery(self):
        batteryImg = gvar.GetSubImage(gvar.ImageStorage['tiles'], 4, 1)
        gvar.GameSurface.blit(batteryImg, (0, 0))
        batteryNumImg = gvar.GameFont.render(str(gvar.Player.batteryNum), True, (255, 255, 255))
        gvar.GameSurface.blit(batteryNumImg, (gvar.TileSize, 0))

    def __renderMsgText(self):
        if gvar.TextRemainTime >= 0:
            if gvar.MsgText is not None:
                img = gvar.GameFont.render(gvar.MsgText, True, (255, 255, 255))
                gvar.GameSurface.blit(img, (0, gvar.GameWindowSize[1] - gvar.TileSize))
            gvar.TextRemainTime -= 1

    def Quit(self):
        pass
