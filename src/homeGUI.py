import tkinter
import sys
import pygame
from pygame.locals import KEYDOWN, K_q      # <--- was on the tutorial

#MY OWN CLASSES
from src.NodeObj import NodeObj
from src.LinkObj import LinkObj

# CONSTANTS:
WIDTH = 1000
HEIGHT = 800
SCREENSIZE = (WIDTH, HEIGHT)
PADTOPBOTTOM = 60
PADLEFTRIGHT = 60
PADDING = (PADTOPBOTTOM, PADLEFTRIGHT)

#COLORS
BLACK = (0, 0, 0)
GREY = (160, 160, 160)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#--------------------------------
# GLOBAL VARS, Using a Dictionary. # No idea why I need this tbh
_VARS = {'surf': False}
#-------------------------------

def main():
    pygame.init()  # Initial Setup
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)

    # Hard coded test nodes
    newNodeA = NodeObj(1, (80, 50), "A", (40, 40, 40), 1, 5)
    newNodeB = NodeObj(2, (140, 50), "A", (40, 40, 40), 1, 5)
    newNodeC = NodeObj(3, (240, 50), "A", (40, 40, 40), 1, 5)
    newNodeD = NodeObj(5, (380, 50), "A", (40, 40, 40), 1, 5)
    newNodeE = NodeObj(8, (550, 50), "A", (40, 40, 40), 1, 5)

    newLinkA = LinkObj(1, 2, 100, 0.3, 5)
    newLinkB = LinkObj(1, 3, 100, 0.3, 5)
    newLinkC = LinkObj(1, 5, 100, 0.3, 5)
    newLinkD = LinkObj(1, 8, 100, 0.3, 5)

    tempNodeList = [newNodeA, newNodeB, newNodeC, newNodeD, newNodeE]
    tempLinkList = [newLinkA, newLinkB, newLinkC, newLinkD]

    # The loop proper, things inside this loop will
    # be called over and over until you exit the window
    while True:
        checkEvents()
        _VARS['surf'].fill(GREY)
        #drawLine()
        #drawRect()
        drawGrid(1)
        drawNodes(tempNodeList)
#        drawLinks(tempLinkList)
        pygame.display.update()



# def drawLinks(links):
#     for link in links:
#
#         startingNode = link.linkSrc
#         endingNode = link.linkDest
#
#         startingPos = 0
#         endingPos = 0
#
#         for node in NodeObj.StaticNodeList:
#             if node.nodeID == startingNode:
#                 startingPos = node.nodePosition[0]
#             if node.nodeID == endingNode:
#                 endingPos = node.nodePosition[1]
#
#         pygame.draw.line(_VARS['surf'], BLACK, startingPos, endingPos)



def drawNodes(nodes): # Parameter will be nodeObj
    for node in nodes:
        if node.status == "A":
            nodeColor = GREEN
        else:
            nodeColor = RED

        position = node.nodePosition
        pygame.draw.circle(_VARS['surf'], nodeColor, position, 20)



def drawGrid(divisions):
    # DRAW Rectangle
    # TOP lEFT TO RIGHT
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (0 + PADLEFTRIGHT, 0 + PADTOPBOTTOM),
      (WIDTH - PADLEFTRIGHT, 0 + PADTOPBOTTOM), 2)
    # BOTTOM lEFT TO RIGHT
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (0 + PADLEFTRIGHT, HEIGHT - PADTOPBOTTOM),
      (WIDTH - PADLEFTRIGHT, HEIGHT - PADTOPBOTTOM), 2)
    # LEFT TOP TO BOTTOM
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (0 + PADLEFTRIGHT, 0 + PADTOPBOTTOM),
      (0 + PADLEFTRIGHT, HEIGHT - PADTOPBOTTOM), 2)
    # RIGHT TOP TO BOTTOM
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (WIDTH - PADLEFTRIGHT, 0 + PADTOPBOTTOM),
      (WIDTH - PADLEFTRIGHT, HEIGHT - PADTOPBOTTOM), 2)

    # Get cell size
    horizontal_cellsize = (WIDTH - (PADLEFTRIGHT*2))/divisions
    vertical_cellsize = (HEIGHT - (PADTOPBOTTOM*2))/divisions

    # VERTICAL DIVISIONS: (0,1,2) for grid(3) for example
    for x in range(divisions):
        pygame.draw.line(
           _VARS['surf'], BLACK,
           (0 + PADLEFTRIGHT+(horizontal_cellsize*x), 0 + PADTOPBOTTOM),
           (0 + PADLEFTRIGHT+horizontal_cellsize*x, HEIGHT - PADTOPBOTTOM), 2)
    # HORITZONTAL DIVISION
        pygame.draw.line(
          _VARS['surf'], BLACK,
          (0 + PADLEFTRIGHT, 0 + PADTOPBOTTOM + (vertical_cellsize*x)),
          (WIDTH - PADLEFTRIGHT, 0 + PADTOPBOTTOM + (vertical_cellsize*x)), 2)


# def drawRect():
#     # There's a native way to draw a rectangle in pygame,
#     # this is just to explain how lines can be drawn.
#     # TOP lEFT TO RIGHT
#     pygame.draw.line(
#       _VARS['surf'], BLACK,
#       (0 + PADLEFTRIGHT, 0 + PADTOPBOTTOM),
#       (WIDTH - PADLEFTRIGHT, 0 + PADTOPBOTTOM), 2)
#     # BOTTOM lEFT TO RIGHT
#     pygame.draw.line(
#       _VARS['surf'], BLACK,
#       (0 + PADLEFTRIGHT, HEIGHT - PADTOPBOTTOM),
#       (WIDTH - PADLEFTRIGHT, HEIGHT - PADTOPBOTTOM), 2)
#     # LEFT TOP TO BOTTOM
#     pygame.draw.line(
#       _VARS['surf'], BLACK,
#       (0 + PADLEFTRIGHT, 0 + PADTOPBOTTOM),
#       (0 + PADLEFTRIGHT, HEIGHT - PADTOPBOTTOM), 2)
#     # RIGHT TOP TO BOTTOM
#     pygame.draw.line(
#       _VARS['surf'], BLACK,
#       (WIDTH - PADLEFTRIGHT, 0 + PADTOPBOTTOM),
#       (WIDTH - PADLEFTRIGHT, HEIGHT - PADTOPBOTTOM), 2)



# def drawLine():
#     # draw a diagonal line from top left coordinates 0,0
#     # to bottom right with coordinates 600 (Width), 400 (Height)
#     pygame.draw.line(_VARS['surf'], BLACK, (0, 0), (WIDTH, HEIGHT), 2)


def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    main()


