class Matrix:
    def __init__(self, w, h):
        self.__w = w
        self.__h = h
        self.data = []

        for i in range(0, w * h):
            self.data.append(None)

    def GetWidth(self) -> int:
        return self.__w

    def GetHeight(self) -> int:
        return self.__h

    def Get(self, x, y):
        return self.data[x + y * self.__w]

    def Set(self, x, y, value):
        self.data[x + y * self.__w] = value


def Sign(value):
    if value > 0:
        return 1
    elif value ==0:
        return 0
    else:
        return -1