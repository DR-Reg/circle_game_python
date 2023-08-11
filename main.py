from classes import *
from constants import *
from functions import *
from graph import Graph
import time


def main():
    # global clicked, drawing_line, last_line, last_click, lines, last_gui_upda
    drawing_line = False
    clicked = False
    last_line = Line(0,0,0,0,0)
    last_click = 0
    last_gui_upd = 0
    lines = []
    graph = Graph()
    intsects = []
    should_exit = False
    new_line = False
    last_del = []
    last_add = []
    # g1 = gui_windows()
    #!!!!!!! WIN MUST BE DEFINED AFTTER GUI WINDOWS
    WIN = pygame.display.set_mode(SCREEN_SIZE) 
    pygame.font.init()
    while not should_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                should_exit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # .4 sec cooldown between clicks
                if time.time() - last_click > 0.4:
                    clicked = True
                    last_click = time.time()

        draw_background(WIN)
        #### NEW LINE ADDED #### 
        if new_line:
            intsects = []
            iline = update_intsects(lines, intsects)
            names, last_del, last_add = update_graph(intsects, iline, graph, lines[-1])
            if detect_pentagon(WIN, graph, names, lines):
                print("PENTAGON")
                break
            new_line = False

        #### GRAPHICS + INPUT #####
        prev_d = drawing_line
        drawing_line, clicked, last_line = \
                mouse_ops(WIN, drawing_line, clicked, last_line, lines)
        new_line = prev_d and not drawing_line
        draw_lines(WIN, lines)
        draw_intsects(WIN, intsects)
        # draw_graph(WIN, graph)
        draw_edges(WIN, graph, last_del, RED)
        # draw_edges(WIN, graph, last_add, GREEN)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
