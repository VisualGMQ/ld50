import pygame
import copy


class Mouse:
    def __init__(self):
        self.__button = [False, False, False]
        self.__oldbutton = [False, False, False]
        self.__pos = pygame.Vector2(0, 0)

    def UpdateOldButton(self):
        self.__oldbutton = copy.deepcopy(self.__button)

    def UpdateBtn(self, ispressed: bool, button: int):
        if button - 1 >= 0 and button - 1 < 3:
            self.__button[button - 1] = ispressed

    def IsPressed(self, btn: int):
        return not self.__oldbutton[btn - 1] and self.__button[btn - 1]

    def GetPos(self) -> pygame.Vector2:
        return self.__pos

    def UpdatePos(self, pos: tuple):
        self.__pos.x = pos[0]
        self.__pos.y = pos[1]
