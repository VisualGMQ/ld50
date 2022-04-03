import pygame
import gvar
import enum


class UIEvent(enum.IntEnum):
    NoEvent = 0,
    Hover = 1,
    BtnDown = 2,


def Button(text: str, color: pygame.Color, hover_color: pygame.Color, pos: pygame.Vector2, scale: pygame.Vector2 = pygame.Vector2(1, 1)) -> UIEvent:
    event = UIEvent.NoEvent
    c = color

    scale_size = (gvar.GameFont.size(text)[0] * scale.x,
                  gvar.GameFont.size(text)[1] * scale.y)

    if pygame.Rect(pos, scale_size).collidepoint(gvar.Mouse.GetPos()):
        if gvar.Mouse.IsPressed(1):
            event = UIEvent.BtnDown
        else:
            event = UIEvent.Hover
            c = hover_color

    surface = pygame.transform.scale(gvar.GameFont.render(text, True, c),
                                     scale_size)
    gvar.GameSurface.blit(surface, pos)
    return event


def ImgButton(img: pygame.Surface.subsurface, pos: pygame.Vector2):
    if img is None:
        return UIEvent.NoEvent

    drawRect = pygame.Rect(pos, (gvar.TileSize, gvar.TileSize))

    event = UIEvent.NoEvent
    if drawRect.collidepoint(gvar.Mouse.GetPos()):
        if gvar.Mouse.IsPressed(1):
            event = UIEvent.BtnDown
        else:
            event = UIEvent.Hover

    gvar.GameSurface.blit(img, (pos.x, pos.y))
    if event == UIEvent.Hover:
        pygame.draw.rect(gvar.GameSurface, (255, 0, 0), drawRect, 1)
    else:
        pygame.draw.rect(gvar.GameSurface, (0, 0, 0), drawRect, 1)
    return event
