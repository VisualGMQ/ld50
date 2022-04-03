import pygame
import key
import mouse
import map
import creature
import controller

GameSurface: pygame.Surface = None
GameWindowSize = (832, 640)
GameShouldClose: bool = False
GameFontName: str = "assets/GridGazer.ttf"
GameFont: pygame.font.Font = None
DebugMode = False
ImageStorage = {}
SoundStorage = {}

LoadImageNames = ["title", "tiles", "blood"]
LoadSoundNames = ["shoot", "pickup", "walk", "hurt", "powerup"]

BloodImageRemainTime = 0
BloodImageMaxTime = 50

TextRemainTime = 0
TextMaxTime = 100
MsgText = None

MaxHp = 140


class GameMode:
    BackgroundStory = 0,
    MissionFailed = 1,
    MissionOK = 2,
    Playing = 3,


Mode: GameMode = GameMode.Playing

HpDownPerTurn = 1

TileSize = 32
MaxTileNumX = 25
MaxTileNumY = 20

Keyboard = key.Keyboard()
Mouse = mouse.Mouse()
Scene = None

ShouldUpdateMonster: bool = False

GameMap: map.GameMap = None


def SetScence(scene):
    global Scene
    if Scene is not None:
        Scene.Quit()
    Scene = scene

    if Scene is not None:
        Scene.Init()


def ExitGame():
    global GameShouldClose
    GameShouldClose = True


def GetSubImage(surface: pygame.Surface, x: int, y: int) -> pygame.Surface.subsurface:
    return surface.subsurface(pygame.Rect(x * TileSize, y * TileSize,
                                          TileSize, TileSize))


def PlaySound(name: str):
    SoundStorage[name].play()

Player: creature.Player = None
Controller: controller.Controller = controller.Controller(None)

ShowBaggage: bool = False