import engine, sys
import pygame

def CheckPygame():
    try:
        check_if_it_is_pygame_ce = pygame.rect.FRect(1,1,1,1)
    except:
        raise ImportError("import pygame isn't recognised as pygame-ce make sure you have uninstalled pyagme and installed pygame-ce")

if __name__ == "__main__":
    CheckPygame()


    kraszak_banger = engine.Game()
    kraszak_banger.GameLooping()