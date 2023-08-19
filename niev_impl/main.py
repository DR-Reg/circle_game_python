import pygame
import math
import numpy as np
from colorama import Fore
import os

window = pygame.display.set_mode((500, 500))
active = True
pygame.init()

# Initialize variables
center = (250,250)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
radius = 200
score = 0


all_lines = [[]]
all_lines_nodes = []


def orderNodes():
    from operator import itemgetter
    result = []
    # print("order nodes called")
    for line in all_lines_nodes:
        if line[0][0] < line[-1][0]:
            res = sorted(line, key=itemgetter(0))
            result.append(res)
        elif line[0][0] > line[-1][0]:
            res = sorted(line, key=itemgetter(0), reverse=True)
            result.append(res)

    # print(result)
    return result

def findIntersection(line1, line2):

    slope1 = (line1[1][1]-line1[0][1])/(line1[1][0]-line1[0][0])
    slope2 = (line2[1][1]-line2[0][1])/(line2[1][0]-line2[0][0])

    bias1 = line1[0][1] - (slope1 * line1[0][0])
    bias2 = line2[0][1] - (slope2 * line2[0][0])

    a = np.array([[slope1, -1], [slope2, -1]])
    b = np.array([-bias1, -bias2])


    return list(np.linalg.solve(a, b))

def lineIntersections(all_lines):
    line = all_lines[-1]
    x0 = line[0][0]
    y0 = line[0][1]
    x1 = line[1][0]
    y1 = line[1][1]

    list_of_nodes = []
    list_of_nodes.append((x0, y0))

    temp_list_x = [x0, x1]
    temp_list_y = [y0, y1]
    nodes_temp_list = (x1, y1)
    temp_list_x.sort(key=int)
    temp_list_y.sort(key=int)

    x0, x1 = temp_list_x
    y0, y1 = temp_list_y

    intersections = []
    tempAllLinesNodes = []
    # counter = 0
    for i in all_lines[:-1]:
        inter = findIntersection(line, i)
        intersections.append(inter)
        # print(f"ALL LINES NODES: {all_lines_nodes}")
        for j in all_lines_nodes:
            if i[0] == j[0] and i[1] == j[-1]:
                # print("APPENDING RN")
                if (inter[0], inter[1]) not in all_lines_nodes[all_lines_nodes.index(j)]:
                    # print(orderNodes())
                    x_green_flag = False
                    y_green_flag = False
                    if line[0][0] < line[1][0]:  # x0 < x1
                        if line[0][0] < inter[0] < line[1][0]:  # ix > x0 and ix < x1
                            x_green_flag = True
                    if line[1][0] < line[0][0]:  # x1 < x0
                        if line[1][0] < inter[0] < line[0][0]:  # ix > x1 and ix < x0
                            x_green_flag = True
                    if line[0][1] < line[1][1]:  # y0 < y1
                        if line[0][1] < inter[1] < line[1][1]:  # iy > y0 and iy < y1
                            y_green_flag = True
                    if line[1][1] < line[0][1]:  # y1 < y0
                        if line[1][1] < inter[1] < line[0][1]:  # iy > y1 and iy < y0
                            y_green_flag = True
                    if x_green_flag and y_green_flag:  # both flags are green
                        all_lines_nodes[all_lines_nodes.index(j)].append((inter[0], inter[1]))

                tempAllLinesNodes = orderNodes()
                # print(orderNodes())
    # all_lines_nodes = tempAllLinesNodes

    ints = intersections.copy()
    for i in intersections:
        if i[0] < x0 or i[0] > x1:
            ints.remove(i)
        elif i[1] < y0 or i[1] > y1:
            ints.remove(i)

    for i in ints:
        list_of_nodes.append((i[0],i[1]))

    list_of_nodes.append(nodes_temp_list)
    # print(Fore.CYAN + f"{list_of_nodes}" + Fore.RESET)
    # print(f"TEMP ALL LINES NODES {tempAllLinesNodes}")

    return {
        "intersections": ints,
        "nodes": list_of_nodes,
        "allNodes": tempAllLinesNodes
    }

def find_adjacent_nodes(node):
    from itertools import chain
    final = []
    for g in all_lines_nodes:
        try:
            idx = g.index(node)
            if g[idx] == g[0]:
                final.append([(g[idx + 1][0], g[idx + 1][1])])
            elif g[idx] == g[-1]:
                final.append([(g[idx - 1][0], g[idx - 1][1])])
            else:
                final.append([g[idx - 1], g[idx + 1]])
        except ValueError:
            ...
    return list(chain.from_iterable(final))

def node_dictionary():
    unique_nodes = list(set([item for sublist in all_lines_nodes for item in sublist]))
    # print(unique_nodes)
    # exit(0)
    node_guide = {}
    for n in unique_nodes:
        node_guide[n] = find_adjacent_nodes(n)
    return node_guide

def colinearity_check(shape):
    # in all_line_nodes list
    # check if there exists a line
    # that contains three of the points in the shape
    for line in all_lines_nodes:
        counter = 0
        for point in shape:
            if point in line:
                counter += 1
        if counter > 2:
            # 3 points are on the same line (colinearity overload)
            return True
    return False

def check_pentagon(origin, parent, depth, shape, myself):
    # Exit conditions
    if depth > 5:
        return [False, shape]
    if myself == origin:
        if depth == 5:
            global solution
            solution = shape.copy()
            # print(solution)
            return [True, shape]
        else:
            return [False, shape]
    if myself is None:
        return [False, shape]
    if myself == parent:
        return [False, shape]
    if colinearity_check(shape):
        return [False, shape]
    # if found:
    #     return [True, shape]

    immediate_neighbors = get_immediate_neighbors(myself)
    for neighbor in immediate_neighbors:
        # print(Fore.GREEN + "Starting recur neighbor:" + str(neighbor) + Fore.RESET)
        my_shape = shape[:]
        if neighbor not in my_shape or (neighbor == origin and depth > 1):
            my_shape.append(neighbor)
            # print(Fore.RED + f"origin={origin}, parent={myself}, depth={depth + 1}, myself={neighbor}, checking shape={my_shape}" + Fore.RESET)
            check_pentagon(origin=origin, parent=myself, depth=depth+1, myself=neighbor, shape=my_shape)
        # Leaf Node Detection
        if len(immediate_neighbors) == 1 and parent == neighbor:
            neighbor = None
            check_pentagon(origin=origin, parent=myself, depth=depth + 1, myself=neighbor, shape=my_shape)

def computeClick():

    # Get all nodes
    all_nodes = list(node_dictionary().keys())
    solution = []
    found = 0

    # os.system('cls' if os.name == 'nt' else 'clear')
    #
    # # print(all_lines)
    # # print(all_lines_nodes)
    #
    # print(f"There are {len(all_nodes)} nodes.")
    # counter = 1

    # Check pentagon
    for current_node in all_nodes:
        # print(Fore.GREEN + "Starting new origin:" + str(current_node) + Fore.RESET)
        shape = []
        shape.append(current_node)
        if found:
            # print("pentagon")
            pentagonFound = True
            break

        immediate_neighbors = get_immediate_neighbors(current_node)
        for neighbor in immediate_neighbors:
            # print(Fore.GREEN + "Starting new neighbor:" + str(neighbor) + Fore.RESET)
            my_shape = shape[:]
            my_shape.append(neighbor)
            # try:
            depth = 0
            origin = current_node
            myself = current_node
            # print(Fore.RED + f"origin={origin}, parent={myself}, depth={depth + 1}, myself={neighbor}, checking shape={my_shape}" + Fore.RESET)
            # check_pentagon(origin=origin, parent=myself, depth=depth + 1, myself=neighbor, shape=my_shape)
            check_pentagon(origin=origin, parent=myself, depth=depth + 1, myself=neighbor, shape=my_shape)

    return list(set(solution))

### Main
scaffold = False
pentagonFound = False
pentagonFormationPoints = []
isCheckingPentagon = True
printColorama = lambda content, color: print(color + f"{content}" + Fore.RESET)
get_immediate_neighbors = lambda n: node_dictionary()[n]

# Holds the solution points
solution = []

while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False

        # printColorama(all_lines, Fore.YELLOW)
        # printColorama(all_lines_nodes, Fore.YELLOW)

        # Calculate angle based on mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x_component = mouse_x - center[0]
        y_component = mouse_y - center[1]
        angle = math.atan2(y_component, x_component)

        # Calculate endpoint on circumference
        end_x = int(center[0] + radius * math.cos(angle))
        end_y = int(center[1] + radius * math.sin(angle))

        # Draw circles and cursor line
        window.fill((0,0,0))
        pygame.draw.circle(window, white, center, radius, 2)
        pygame.draw.circle(window, red, center, 3)
        pygame.draw.line(window, red, center, (end_x,end_y), width=3)
        pygame.draw.circle(window, red, (end_x,end_y),5)


        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                if len(all_lines[-1]) == 0:
                    all_lines[-1].append((end_x, end_y))
                    # all_lines_nodes.append([])
                    scaffold = True
                elif len(all_lines[-1]) == 1:
                    all_lines[-1].append((end_x,end_y))
                    all_lines.append([])
                    lintersections = lineIntersections(all_lines[:-1])
                    all_lines_nodes.append(lintersections["nodes"])
                    all_lines_nodes = orderNodes()
                    scaffold = False
                    score += (len(lintersections["intersections"]) + 2)

                    computeClick()
                    if len(solution) > 0:
                        pentagonFound = True
                        print(solution)


        if scaffold:
            pygame.draw.line(window, blue, all_lines[-1][0], (end_x, end_y), 2)

        # print(Fore.LIGHTMAGENTA_EX + f"{pentagonFormationPoints}")

        f = pygame.font.Font(None, 36)
        text = f.render(str(score), True, white)
        window.blit(text, (30, 30))

        pt = "Pentagon" if pentagonFound else ""
        m = pygame.font.Font(None, 20)
        pentatext = m.render(str(pt), True, white)
        window.blit(pentatext, (225, 465))


        for l in all_lines:
            try:
                pygame.draw.line(window,white,l[0],l[1],2)
                intersections = lineIntersections(all_lines[:-1])["intersections"]
                for i in intersections:
                    if not pentagonFound:
                        pygame.draw.circle(window, red, i, 5)
            except IndexError:
                pass

        if pentagonFound:
            # print(Fore.CYAN + f"{pentagonFormationPoints}")
            for p in solution:
                pygame.draw.circle(window, green, p, 5)
        else:
            for n in node_dictionary().keys():
                pygame.draw.circle(window, blue, n, 5)



    pygame.display.flip()

pygame.quit()
