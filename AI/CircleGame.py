from Vector import V2
import numpy as np
import pygame

class CircleGame:
    def __init__(self, agents, radius = 1):
        self.agents = agents
        # index keeping the index of the next agent's move
        self.move = 0
        self.points = [0,0]
        # Game data
        self.radius = radius
        self.all_lines = [[]]
        self.all_lines_nodes = []
        self.scaffold = False
        self.pentagonFound = False
        self.pentagonFormationPoints = []
        self.isCheckingPentagon = True
        self.printColorama = lambda content, color: print(color + f"{content}" + Fore.RESET)
        self.get_immediate_neighbors = lambda n: self.node_dictionary()[n]
        self.solution = []

    def node_dictionary(self):
        unique_nodes = list(set([item for sublist in self.all_lines_nodes for item in sublist]))
        # print(unique_nodes)
        # exit(0)
        node_guide = {}
        for n in unique_nodes:
            node_guide[n] = self.find_adjacent_nodes(n)
        return node_guide

    def find_adjacent_nodes(self,node):
        from itertools import chain
        final = []
        for g in self.all_lines_nodes:
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



    def make_move(self):
        # each agent should eventually call add_line func
        self.agents[self.move].make_move(self)
        self.add_points()
        if self.check_win():
            return True, self.move
        self.move = not self.move
        return False, self.move

    def orderNodes(self):
        from operator import itemgetter
        result = []
        # print("order nodes called")
        for line in self.all_lines_nodes:
            if line[0][0] < line[-1][0]:
                res = sorted(line, key=itemgetter(0))
                result.append(res)
            elif line[0][0] > line[-1][0]:
                res = sorted(line, key=itemgetter(0), reverse=True)
                result.append(res)

        # print(result)
        return result


    def findIntersection(self,line1, line2):
        slope1 = (line1[1][1]-line1[0][1])/(line1[1][0]-line1[0][0])
        slope2 = (line2[1][1]-line2[0][1])/(line2[1][0]-line2[0][0])

        bias1 = line1[0][1] - (slope1 * line1[0][0])
        bias2 = line2[0][1] - (slope2 * line2[0][0])

        a = np.array([[slope1, -1], [slope2, -1]])
        b = np.array([-bias1, -bias2])


        return list(np.linalg.solve(a, b))
    
    def lineIntersections(self,all_lines):
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
            inter = self.findIntersection(line, i)
            intersections.append(inter)
            # print(f"ALL LINES NODES: {all_lines_nodes}")
            for j in self.all_lines_nodes:
                if i[0] == j[0] and i[1] == j[-1]:
                    # print("APPENDING RN")
                    if (inter[0], inter[1]) not in self.all_lines_nodes[self.all_lines_nodes.index(j)]:
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
                            self.all_lines_nodes[self.all_lines_nodes.index(j)].append((inter[0], inter[1]))

                    tempAllLinesNodes = self.orderNodes()
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


    def check_pentagon(self,origin, parent, depth, shape, myself):
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
        if self.colinearity_check(shape):
            return [False, shape]
        # if found:
        #     return [True, shape]

        # FIXME: why no return down here?

        immediate_neighbors = self.get_immediate_neighbors(myself)
        for neighbor in immediate_neighbors:
            # print(Fore.GREEN + "Starting recur neighbor:" + str(neighbor) + Fore.RESET)
            my_shape = shape[:]
            if neighbor not in my_shape or (neighbor == origin and depth > 1):
                my_shape.append(neighbor)
                # print(Fore.RED + f"origin={origin}, parent={myself}, depth={depth + 1}, myself={neighbor}, checking shape={my_shape}" + Fore.RESET)
                self.check_pentagon(origin=origin, parent=myself, depth=depth+1, myself=neighbor, shape=my_shape)
            # Leaf Node Detection
            if len(immediate_neighbors) == 1 and parent == neighbor:
                neighbor = None
                self.check_pentagon(origin=origin, parent=myself, depth=depth + 1, myself=neighbor, shape=my_shape)

    def colinearity_check(self,shape):
        # in all_line_nodes list
        # check if there exists a line
        # that contains three of the points in the shape
        for line in self.all_lines_nodes:
            counter = 0
            for point in shape:
                if point in line:
                    counter += 1
            if counter > 2:
                # 3 points are on the same line (colinearity overload)
                return True
        return False

    def add_line(self,x,y):
        dir = V2(x,y)
        dir.normalise()
        dir = dir * self.radius
        if len(self.all_lines[-1]) == 0:
            self.all_lines[-1].append(dir.tuple)
            # all_lines_nodes.append([])
            self.scaffold = True
            return False # no new line
        elif len(self.all_lines[-1]) == 1:
            self.all_lines[-1].append(dir.tuple)
            self.all_lines.append([])
            lintersections = self.lineIntersections(self.all_lines[:-1])
            self.all_lines_nodes.append(lintersections["nodes"])
            self.all_lines_nodes = self.orderNodes()
            self.scaffold = False
            # score += (len(lintersections["intersections"]) + 2)

            self.computeClick()
            if len(self.solution) > 0:
                self.pentagonFound = True
                print(self.solution)
            
            return True # new line


    def computeClick(self):
        # Get all nodes
        all_nodes = list(self.node_dictionary().keys())
        solution = []
        found = 0

        # Check pentagon
        for current_node in all_nodes:
            # print(Fore.GREEN + "Starting new origin:" + str(current_node) + Fore.RESET)
            shape = []
            shape.append(current_node)
            if found:
                # print("pentagon")
                self.pentagonFound = True
                break

            immediate_neighbors = self.get_immediate_neighbors(current_node)
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
                self.check_pentagon(origin=origin, parent=myself, depth=depth + 1, myself=neighbor, shape=my_shape)

        return list(set(solution))


    # blits only the circle and lines in no debug
    # else everything
    def blit(self,surf,debug=False):
        w,h = surf.get_size()
        center = (w/2,h/2)
        surf.fill((255,255,255))
        drad = min(w/2,h/2)
        pygame.draw.circle(surf, (0,0,0), center, drad, 2)
        for l in self.all_lines:
            try:
                start = drad * (V2(*l[0]) / self.radius)
                end = drad * (V2(*l[1]) / self.radius)
                pygame.draw.line(surf,(0,0,0),start.tuple,end.tuple,2)
                if debug:
                    intersections = self.lineIntersections(self.all_lines[:-1])["intersections"]
                    for i in intersections:
                        if not self.pentagonFound:
                            pygame.draw.circle(surf, (255,0,0), i, 5)
            except IndexError:
                pass
        
        if debug and self.pentagonFound:
            for p in self.solution:
                pygame.draw.circle(surf, (0,255,0), p, 5)
        elif debug:
            for n in self.node_dictionary().keys():
                pygame.draw.circle(surf, (0,0,255), n, 5)

    def add_points(self):
        # self.points[self.move] += lineInts
        pass
        # raise NotImplementedError
    def check_win(self):
        # pentagon check etc expected to have been called with the make move func
        return self.pentagonFound
        # raise NotImplementedError 
