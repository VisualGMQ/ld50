import os.path

import pygame
import gvar
import ui
import game_scene
import log
import map


class WelcomeScene:
    def __init__(self):
        self.title_image: pygame.Surface = None

    def Init(self):
        self.title_image = gvar.ImageStorage['title']

        log.Log("map size is " + str(gvar.MaxTileNumX) + "," + str(gvar.MaxTileNumY))
        gvar.GameMap = map.LoadMapFromFile(os.path.join("assets", "gamemap.map"))

        self.background = pygame.Surface(gvar.GameWindowSize).convert_alpha()
        if self.background is None:
            log.Log("background image is one")
        gvar.GameMap.GetCurRooom().Render(self.background)

    def Quit(self):
        pass

    def Update(self):
        pass

    def Render(self):
        self.background.set_alpha(100)
        gvar.GameSurface.blit(self.background, (0, 0))
        self.__render_welcome()

    def __render_welcome(self):
        title_trans = pygame.transform.scale(self.title_image,
                                             (self.title_image.get_size()[0] * 4,
                                              self.title_image.get_size()[1] * 4))
        gvar.GameSurface.blit(title_trans,
                              ((gvar.GameWindowSize[0] - title_trans.get_width()) // 2,
                               100))

        text = "Leave"
        text_size = gvar.GameFont.size(text)
        if ui.Button(text,
                     (255, 255, 255),
                     (0, 255, 0),
                     ((gvar.GameWindowSize[0] - text_size[0]) // 2,
                       gvar.GameWindowSize[1] // 2 + 100),
                     pygame.Vector2(1, 1)) == ui.UIEvent.BtnDown:
            gvar.ExitGame()

        text = "Start Game"
        text_size = gvar.GameFont.size(text)
        if ui.Button(text,
                     (255, 255, 255),
                     (0, 255, 0),
                     ((gvar.GameWindowSize[0] - text_size[0]) // 2,
                       gvar.GameWindowSize[1] // 2),
                     pygame.Vector2(1, 1)) == ui.UIEvent.BtnDown:
            gvar.SetScence(game_scene.GameScene())

        text = "VisualGMQ made for LD50"
        img = gvar.GameFont.render(text, True, (255, 255, 255))
        img = pygame.transform.scale(img, (img.get_width() // 2, img.get_height() // 2))
        gvar.GameSurface.blit(img, (0, gvar.GameWindowSize[1] - img.get_height()))
