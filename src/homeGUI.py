import tkinter
import sys
import pygame
import random
from pygame.locals import KEYDOWN, K_q      # <--- was on the tutorial

#MY OWN CLASSES
from src.NodeObj import NodeObj
from src.LinkObj import LinkObj

# CONSTANTS:
WIDTH = 1000
HEIGHT = 800

WORKING_WIDTH = 940
WORKING_HEIGHT = 740

SCREENSIZE = (WIDTH, HEIGHT)
WORKING_SCREENSIZE = (WORKING_WIDTH, WORKING_HEIGHT)

PADTOPBOTTOM = 60
PADLEFTRIGHT = 60
PADDING = (PADTOPBOTTOM, PADLEFTRIGHT)


#COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (160, 160, 160)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

StaticCurrentDisplayedNodes = []

#--------------------------------
# GLOBAL VARS, Using a Dictionary. # No idea why I need this tbh
_VARS = {'surf': False}
#-------------------------------



# RECT = pygame.rect()


def main():
    pygame.init()  # Initial Setup
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)

    # Hard coded test nodes
    newNodeA = NodeObj(1, (80, 50), "A", (40, 40, 40), 1, 5)
    newNodeB = NodeObj(2, (140, 50), "A", (40, 40, 40), 1, 5)
    newNodeC = NodeObj(3, (240, 50), "A", (40, 40, 40), 1, 5)
    newNodeD = NodeObj(4, (380, 50), "A", (40, 40, 40), 1, 5)
    newNodeE = NodeObj(5, (550, 50), "A", (40, 40, 40), 1, 5)
    newNodeF = NodeObj(6, (550, 50), "A", (40, 40, 40), 1, 5)
    newNodeG = NodeObj(7, (550, 50), "A", (40, 40, 40), 1, 5)
    newNodeH = NodeObj(8, (550, 50), "A", (40, 40, 40), 1, 5)

    newLinkA = LinkObj(1, 2, 100, 0.3, 5)
    newLinkB = LinkObj(1, 3, 100, 0.3, 5)
    newLinkC = LinkObj(1, 5, 100, 0.3, 5)
    newLinkD = LinkObj(1, 8, 100, 0.3, 5)

    tempNodeList = [newNodeA, newNodeB, newNodeC, newNodeD, newNodeE, newNodeF, newNodeG, newNodeH]
    tempLinkList = [newLinkA, newLinkB, newLinkC, newLinkD]

    for node in tempNodeList:
        randoPosition = [random.randint(60, 940), random.randint(60, 740)]
        node.nodePosition = randoPosition

    # The loop proper, things inside this loop will
    # be called over and over until you exit the window

    nodesDrawn = True # Flipped False when all nodes are drawn
    linksDrawn = True

    while True:
        checkEvents()
        _VARS['surf'].fill(GREY)
        #drawLine()
        #drawRect()
        drawGrid(1)

        if nodesDrawn:
            for nodes in tempNodeList:
                drawNode(nodes)

        if linksDrawn:
            for link in tempLinkList:
                drawLink(link, tempNodeList)

        pygame.display.update()


def drawLink(link, tempNodeList):
    for node in tempNodeList:
        if node.nodeID == link.linkSrc:
            startingNode = node
        if node.nodeID == link.linkDest:
            endingNode = node

    pygame.draw.line(_VARS['surf'], BLACK, startingNode.nodePosition, endingNode.nodePosition)
    # pygame.draw.line(screen, Color_line, (60, 80), (130, 100))
    # pygame.display.flip()



def drawNode(node): # Parameter will be nodeObj
        if node.status == "A":
            nodeColor = GREEN
        else:
            nodeColor = RED

        pygame.draw.circle(_VARS['surf'], nodeColor, node.nodePosition, 20)
        # pygame.draw.rect(_VARS['surf'], WHITE, (node.nodePosition[0], node.nodePosition[1], 60, 10)) # <---WORKING

        font = pygame.font.SysFont('Arial', 24)
        txt_surface = font.render("Node: {}".format(node.nodeID), False, BLACK)
        rect = pygame.draw.rect(_VARS['surf'], WHITE, (node.nodePosition[0], node.nodePosition[1], 60, 20))
        _VARS['surf'].blit(txt_surface, (rect.x, rect.y))

        StaticCurrentDisplayedNodes.append(node)


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


def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    main()


