from classes import *
from constants import *
from gui import *
import pygame
import random
from threading import Thread
import time

def update_intsects(lines, intsects):
    isect_line = []
    line = lines[-1]
    intsects.append(line.p1)
    isect_line.append(None)
    for oline in lines[:-1]:
        intsect = line.get_intsect(oline)
        if intsect.magnitude < RADIUS:
            intsects.append(intsect)
            isect_line.append(oline)
    intsects.append(line.p2)
    isect_line.append(None)
    return isect_line

def update_graph(intsects, iline, graph, parent_line):
    # V2 mutable => referential?
    # sort our intsects
    pivot = intsects[0]
    siline = sorted(
            zip(intsects, iline),
            key = lambda e:
            (pivot.x - e[0].x)**2 + (pivot.y-e[0].y)**2
            )
    # update intsect array for drawing
    intsects = [i for i,_ in siline]
    intsect_names = []
    last_added_edges = []
    last_deleted_edges = []

    # TODO: include first and last nodes too.
    # TODO: store my nodes in line class so no graph shenaningas
    i = 0
    line_idx_1 = parent_line.idx
    graph.add_node(f"{line_idx_1};start", siline[0][0].copy())
    graph.add_node(f"{line_idx_1};end", siline[-1][0].copy())
    for intsect, iline in siline[1:]:
        # we name our nodes in the following manner:
        # "line_idx_1;line_idx_2"
        # we store the x and y in the intsect object,
        # which we copy so its not referential
        ## FIXME: in the future, if we need other information
        ## to create edges, we must change the name to do so
        prv_li = siline[i-1][1]
        if prv_li == None:
            prv_lidx = "start"
        else:
            prv_lidx = prv_li.idx
        if iline == None:
            line_idx_2 = "end"
        else:
            line_idx_2 = iline.idx
        ## TODO: CHECK: i don't need to add an edge with the previous
        # one. but maybe i do.
        # prev_lidx = siline[i-1][1].idx
        my_name = f"{line_idx_1};{line_idx_2}"
        intsect_names.append(my_name)
        graph.add_node(my_name, intsect.copy())
        prev_name = f"{line_idx_1};{prv_lidx}"
        graph.add_edge(my_name,prev_name)
        graph.add_edge(prev_name, my_name)
        last_added_edges.append((prev_name,my_name))
        
        # if we are at circ, no nodes on other line
        if iline == None:
            break


        # now, lets find the nodes neighboring this one on  the other line
        # first extract the nodes:
        nodes_on_other_line = []
        for j in range(0, parent_line.idx):
            name = f"{line_idx_2};{j}"
            n = graph.node(name)
            if n!= None:
                nodes_on_other_line.append((n,name))
        for j in range(0, parent_line.idx):
            name = f"{j};{line_idx_2}"
            n = graph.node(name)
            if n!= None:
                nodes_on_other_line.append((n,name))
        # print(my_name,"has",len(nodes_on_other_line),":",nodes_on_other_line)
        pivot = iline.p1
        vdist = lambda v: (pivot.x-v.x)**2 + (pivot.y-v.y)**2
        edist = lambda e: (pivot.x-e[0].x)**2 + (pivot.y-e[0].y)**2
        distances = list(map(edist, nodes_on_other_line))
        nodes_on_other_line.sort(key=edist)
        distances.sort()
        my_dist = vdist(intsect)
        added = False
        for j, dist in enumerate(distances):
            if dist > my_dist:
                front_name = nodes_on_other_line[j - 1][1]
                back_name = nodes_on_other_line[j][1]
                graph.del_edge(front_name, back_name)
                graph.del_edge(back_name, front_name)
                last_deleted_edges.append((front_name,back_name))

                graph.add_edge(front_name, my_name)
                graph.add_edge(back_name, my_name)
                graph.add_edge(my_name, front_name)
                graph.add_edge(my_name, back_name)
                last_added_edges.append((front_name,my_name))
                last_added_edges.append((back_name,my_name))
                added = True
                break
        # with last one
        # NOTE: could be that adding these to distances etc is better
        if not added and len(nodes_on_other_line) > 0:
            front_name = nodes_on_other_line[-1][1]
            back_name = f"{line_idx_2};end"
            if graph.node(back_name) == None:
                print("CODE SHOULD NOT BE REACHED !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! "\
                        "WHY IS END THE FIRST ARGUMENT?")
            graph.del_edge(front_name, back_name)
            graph.del_edge(back_name, front_name)
            last_deleted_edges.append((front_name,back_name))

            graph.add_edge(front_name, my_name)
            graph.add_edge(back_name, my_name)
            graph.add_edge(my_name, front_name)
            graph.add_edge(my_name, back_name)
            last_added_edges.append((front_name,my_name))
            last_added_edges.append((back_name,my_name))
                
        i += 1
    return intsect_names, last_deleted_edges, last_added_edges

def detect_pentagon(WIN, graph, intsect_names,lines):
    # go from each neighbor, to some other neighbor
    # without going through the intsect
    for i in intsect_names: 
        neighs = graph.nodes(from_node = i) + graph.nodes(to_node = i)
        print(i)
        for n in neighs:
            for k in neighs:
                if n != k:
                    sdist = graph.shortest_path(k, n, avoids=set(i))
                    print(f"\t{n} -> {k} :\t\t{sdist}")
                    # draw_background(WIN)
                    # draw_lines(WIN,lines)
                    # for j in range(len(sdist[1])-1):
                    #     nd = graph.node(sdist[1][j])
                    #     nnd = graph.node(sdist[1][j+1])
                    #     pygame.draw.circle(WIN, GREEN, (VCENT+nd).tuple, 6)
                    #     pygame.draw.line(WIN, BLUE, (VCENT+nd).tuple, (VCENT+nnd).tuple)

                    # nd = graph.node(sdist[1][-1])
                    # nnd = graph.node(sdist[1][0])
                    # pygame.draw.circle(WIN, GREEN, (VCENT+nd).tuple, 6)
                    # # pygame.draw.line(WIN, BLUE, (VCENT+nd).tuple, (VCENT+nnd).tuple)
                    # pygame.display.update()
                    # time.sleep(5)

                    if sdist[0] == 4:
                        for n in sdist[1]:
                            nd = graph.node(n)
                            pygame.draw.circle(WIN, GREEN, (VCENT+nd).tuple, 6)
                            pygame.display.update()
                            time.sleep(5)

def draw_graph(WIN, graph):
    # print(len(graph.nodes()))
    for n in graph.nodes():
        n = graph.node(n)
        pygame.draw.circle(WIN, RED, (n+VCENT).tuple, 6)
    for e in graph.edges():
        p1 = graph.node(e[0]) + VCENT
        p2 = graph.node(e[1]) + VCENT
        pygame.draw.line(WIN, RED, p1.tuple, p2.tuple)

def draw_edges(WIN, graph, edges, col):
    # print(len(graph.nodes()))
    for e in edges:
        p1 = graph.node(e[0]) + VCENT
        p2 = graph.node(e[1]) + VCENT
        pygame.draw.line(WIN, col, p1.tuple, p2.tuple)




def draw_intsects(WIN, intsects):
    fnt = pygame.font.SysFont('Comic Sans MS', 30)
    for i, intsect in enumerate(intsects):
        pygame.draw.circle(WIN, BLUE, (VCENT + intsect).tuple, 4)
        # text = fnt.render(f"{i}", False, BLUE)
        # WIN.blit(text, (VCENT+intsect).tuple)
        

def mouse_ops(WIN, dline:bool, clicked:bool, last_line:Line, lines:list):
    ## LINE FROM CENTER TO CINC
    mpos = V2(*pygame.mouse.get_pos())
    vec = mpos - VCENT
    vec.normalize()
    vec = vec * RADIUS
    pygame.draw.line(WIN, GREEN, CENT, (VCENT + vec).tuple)
    if clicked and not dline:
        dline = True
        last_line.p1 = vec
    elif clicked:
        dline = False
        last_line.p2 = vec
        lines.append(last_line)
        # only place where i append lines
        last_line = Line(0,0,0,0,len(lines))
    if dline:
        pygame.draw.line(WIN, RED, (last_line.p1 + VCENT).tuple, (vec + VCENT).tuple)
    return dline, False, last_line

def draw_background(WIN):
    WIN.fill((255,255,255))
    pygame.draw.circle(WIN, (0,0,0), CENT, RADIUS, width=2)

def sample_vid():
    surf = pygame.Surface((200,200))
    pygame.draw.circle(surf, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), (100,100),100)
    return surf

def gwin(g1):
    g1.init_tk()
    g1.add_video(sample_vid)
    g1.run()
# to be called outside of main loop thanks to threading:
def gui_windows():
    g1 = GUIWindow(200,200,"TEST")
    g1.add_video(sample_vid)
    return g1
    # g1.run()
    # t1 = Thread(target=gwin, args=(g1,))
    # t1.daemon = True
    # t1.start()
    # while not g1.running:
    #     print("WAITING FOR TK INIT")

def update_gui(g1):
    g1.run()

def draw_lines(WIN, lines):
    fnt = pygame.font.SysFont('Comic Sans MS', 15)
    for line in lines:
        line.draw(WIN, BLACK, VCENT)
        text = fnt.render(f"{line.idx}", False, BLACK)
        WIN.blit(text, (VCENT+line.p1).tuple)
