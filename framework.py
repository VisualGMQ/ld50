import pygame
import gvar
import log
import os


class Framework:
    def Init(self, s):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        gvar.GameSurface = pygame.display.set_mode(gvar.GameWindowSize)
        pygame.display.set_caption("Infection")

        for name in gvar.LoadImageNames:
            path = os.path.join("assets", name + ".png")
            img = pygame.image.load(path).convert_alpha()
            if img is None:
                log.Log(path + " can't load")
            gvar.ImageStorage[name] = img

        for name in gvar.LoadSoundNames:
            path = os.path.join("assets", name + ".wav")
            sound = pygame.mixer.Sound(path)
            if sound is None:
                log.Log(path + " can't load")
            gvar.SoundStorage[name] = sound

        gvar.GameFont = pygame.font.Font(gvar.GameFontName, 30)

        if gvar.GameFont is not None:
            log.Log("font" + gvar.GameFontName + " load OK")

        gvar.SetScence(s)

    def __eventHandle(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            gvar.ExitGame()
        if event.type == pygame.KEYDOWN:
            gvar.Keyboard.Update(True, event.__dict__['key'])
            if event.__dict__['key'] == pygame.K_l:
                pygame.display.toggle_fullscreen()
        if event.type == pygame.KEYUP:
            gvar.Keyboard.Update(False, event.__dict__['key'])
        if event.type == pygame.MOUSEBUTTONDOWN:
            gvar.Mouse.UpdateBtn(True, event.__dict__['button'])
        if event.type == pygame.MOUSEBUTTONUP:
            gvar.Mouse.UpdateBtn(False, event.__dict__['button'])
        if event.type == pygame.MOUSEMOTION:
            gvar.Mouse.UpdatePos(event.__dict__['pos'])

    def Run(self):
        fps_ticker = pygame.time.Clock()
        while not gvar.GameShouldClose:
            gvar.Keyboard.UpdateOldKey()
            gvar.Mouse.UpdateOldButton()
            for event in pygame.event.get():
                self.__eventHandle(event)
            gvar.GameSurface.fill((0, 0, 0))
            if gvar.Scene is not None:
                gvar.Scene.Update()
                gvar.Scene.Render()
            pygame.display.flip()
            fps_ticker.tick(60)

    def Shutdown(self):
        if gvar.Scene is not None:
            gvar.Scene.Quit()
        pygame.mixer.quit()
        pygame.font.quit()
        pygame.quit()
