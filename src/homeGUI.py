import tkinter
import sys
import pygame
import random
from pygame.locals import KEYDOWN, K_q  # <--- was on the tutorial

# ToDo need to fix the overall layout and cleanliness of this script bc its a mess...

# MY OWN CLASSES
import main as m
from src.NodeObj import NodeObj
from src.LinkObj import LinkObj

# CONSTANTS:
WIDTH = 1200
HEIGHT = 850

WORKING_WIDTH = 1000
WORKING_HEIGHT = 800

SCREENSIZE = (WIDTH, HEIGHT)
WORKING_SCREENSIZE = (WORKING_WIDTH, WORKING_HEIGHT)

PADTOPBOTTOM = 60
PADLEFTRIGHT = 60
PADDING = (PADTOPBOTTOM, PADLEFTRIGHT)

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (160, 160, 160)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

StaticCurrentDisplayedNodes = []

# --------------------------------
# GLOBAL VARS, Using a Dictionary. # No idea why I need this tbh
_VARS = {'surf': False}
# -------------------------------

def startGUI():
    pygame.init()  # Initial Setup
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)

    # The loop proper, things inside this loop will
    # be called over and over until you exit the window

    nodesDrawn = True  # Flipped False when all nodes are drawn
    linksDrawn = True

    while True:
        checkEvents()
        _VARS['surf'].fill(GREY)
        drawGrid(1)

        if nodesDrawn:
            for nodes in NodeObj.StaticNodeList:    # Currently draws all available nodes
                drawNode(nodes)

        if linksDrawn:
            for link in NodeObj.StaticLinkList:     # Currently draws all available links
                drawLink(link, NodeObj.StaticNodeList)

        pygame.display.update()

# def drawRequestBox():
#     for request in StaticRequestList:
#           requestBox.display(request)
#   # Needs to then get retrieve the node object from the StaticNodes List.
#      request.findPath()
#

#   Draws a link between nodes
def drawLink(link, tempNodeList):
    for node in tempNodeList:
        if node.nodeID == link.linkSrc:
            startingNode = node
        if node.nodeID == link.linkDest:
            endingNode = node

    startingNodePosition = (int(startingNode.nodePosition[0]), int(startingNode.nodePosition[1]))
    endingNodePosition = (int(endingNode.nodePosition[0]), int(endingNode.nodePosition[1]))

    pygame.draw.line(_VARS['surf'], BLACK, startingNodePosition, endingNodePosition)
    # pygame.draw.line(screen, Color_line, (60, 80), (130, 100))
    # pygame.display.flip()


def drawNode(node):  # Parameter will be nodeObj

    if node.status == "I":
        nodeColor = YELLOW

    elif node.status == "R":
        nodeColor = BLUE

    elif node.status == "O":
        nodeColor = RED

    elif node.status == "A":
        nodeColor = GREEN

    pygame.draw.circle(_VARS['surf'], nodeColor, (int(node.nodePosition[0]), int(node.nodePosition[1])), 20)

    font = pygame.font.SysFont('Arial', 24)
    txt_surface = font.render("Node: {}".format(node.nodeID), False, BLACK)
    rect = pygame.draw.rect(_VARS['surf'], WHITE, (int(node.nodePosition[0]), int(node.nodePosition[1]), 60, 20))
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
    horizontal_cellsize = (WIDTH - (PADLEFTRIGHT * 2)) / divisions
    vertical_cellsize = (HEIGHT - (PADTOPBOTTOM * 2)) / divisions

    # VERTICAL DIVISIONS: (0,1,2) for grid(3) for example
    for x in range(divisions):
        pygame.draw.line(
            _VARS['surf'], BLACK,
            (0 + PADLEFTRIGHT + (horizontal_cellsize * x), 0 + PADTOPBOTTOM),
            (0 + PADLEFTRIGHT + horizontal_cellsize * x, HEIGHT - PADTOPBOTTOM), 2)
        # HORITZONTAL DIVISION
        pygame.draw.line(
            _VARS['surf'], BLACK,
            (0 + PADLEFTRIGHT, 0 + PADTOPBOTTOM + (vertical_cellsize * x)),
            (WIDTH - PADLEFTRIGHT, 0 + PADTOPBOTTOM + (vertical_cellsize * x)), 2)


def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    m.processData()
    startGUI()
