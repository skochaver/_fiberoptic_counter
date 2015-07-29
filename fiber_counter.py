'''
All functions are copied almost verbatim from this stack overflow post: http://stackoverflow.com/questions/6136588/image-cropping-using-python/8696558
Big thanks to those guys.
When run this opens a box for you to navigate to an image, the opens it for a one-off cropping instance before running
the computer vision counting algorithms.
'''

import pygame, sys
pygame.init()
import os
from PIL import Image
import Tkinter
import tkFileDialog
from watershed_methods import watershed_counter

root = Tkinter.Tk()
root.withdraw()

filename = tkFileDialog.askopenfilename(parent=root, title='Open Fiber Optic Image File')

def displayImage(screen, px, topleft, prior):
    # ensure that the rect always has positive width, height
    x, y = topleft
    width =  pygame.mouse.get_pos()[0] - topleft[0]
    height = pygame.mouse.get_pos()[1] - topleft[1]
    if width < 0:
        x += width
        width = abs(width)
    if height < 0:
        y += height
        height = abs(height)

    # eliminate redundant drawing cycles (when mouse isn't moving)
    current = x, y, width, height
    if not (width and height):
        return current
    if current == prior:
        return current

    # draw transparent box and blit it onto canvas
    screen.blit(px, px.get_rect())
    im = pygame.Surface((width, height))
    im.fill((128, 128, 128))
    pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
    im.set_alpha(128)
    screen.blit(im, (x, y))
    pygame.display.flip()

    # return current box extents
    return (x, y, width, height)

def setup(path):
    px = pygame.image.load(path)
    rect = map(lambda x: x / 4, px.get_rect()[2:])
    screen = pygame.display.set_mode(rect)
    px = pygame.transform.scale(px, rect)
    screen.blit(px, px.get_rect())
    pygame.display.flip()
    return screen, px

def mainLoop(screen, px):
    topleft = bottomright = prior = None
    n=0
    while n!=1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if not topleft:
                    topleft = event.pos
                else:
                    bottomright = event.pos
                    n=1
                    
        if topleft:
            prior = displayImage(screen, px, topleft, prior)
            
    return ( topleft + bottomright )

if __name__ == "__main__":
    input_loc = filename
    output_loc = os.path.join(os.getcwd(), 'temp_crop.png')
    screen, px = setup(input_loc)
    left, upper, right, lower = mainLoop(screen, px)

    # ensure output rect always has positive width, height
    if right < left:
        left, right = right, left
    if lower < upper:
        lower, upper = upper, lower
    im = Image.open(input_loc)
    im = im.crop(map(lambda x: x * 4,( left, upper, right, lower)))
    pygame.display.quit()
    im.save(output_loc)
    watershed_counter(output_loc)

