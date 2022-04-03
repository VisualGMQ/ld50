import copy


class Keyboard:
    def __init__(self):
        self.__key = {}
        self.__oldkey = {}

    def UpdateOldKey(self):
        self.__oldkey = copy.deepcopy(self.__key)

    def Update(self, pressed: bool, keycode: int):
        self.__key[keycode] = pressed

    def IsKeyPressed(self, keycode: int) -> bool:
        if keycode in self.__key and keycode not in self.__oldkey:
            return self.__key[keycode]
        elif keycode in self.__key and keycode in self.__oldkey:
            return self.__key[keycode] and not self.__oldkey[keycode]
        else:
            return False
