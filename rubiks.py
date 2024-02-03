import numpy as np
import pygame

# A LOT OF DICTIONARIES ????
right = {
    18: 2,
    19: 5,
    20: 8,
    53: 18,
    52: 19,
    51: 20,
    44: 53,
    43: 52,
    42: 51,
    2: 44,
    5: 43,
    8: 42
}

left = {
    0: 24,
    3: 25,
    6: 26,
    24: 47,
    25: 46,
    26: 45,
    47: 38,
    46: 37,
    45: 36,
    38: 0,
    37: 3,
    36: 6
}

up = {
    9: 0,
    10: 1,
    11: 2,
    51: 9,
    48: 10,
    45: 11,
    35: 51,
    34: 48,
    33: 45,
    0: 35,
    1: 34,
    2: 33
}

down = {
    27: 8,
    28: 7,
    29: 6,
    47: 27,
    50: 28,
    53: 29,
    17: 47,
    16: 50,
    15: 53,
    8: 17,
    7: 16,
    6: 15
}

front = {
    9: 18,
    12: 21,
    15: 24,
    18: 27,
    21: 30,
    24: 33,
    27: 36,
    30: 39,
    33: 42,
    36: 9,
    39: 12,
    42: 15
}

back = {
    11: 38,
    14: 41, 
    17: 44,
    20: 11,
    23: 14,
    26: 17,
    29: 20,
    32: 23,
    35: 26,
    38: 29,
    41: 32,
    44: 35
}

all_move_dict = {
    'L': (left, 3),
    'R': (right, 1),
    'U': (up, 4),
    'D': (down, 2),
    'F': (front, 0),
    'B': (back, 5)
}

# define dict for cw and ccw face rotations
cw_rotations = {
    0: 2,
    1: 5,
    2: 8,
    5: 7,
    8: 6,
    7: 3,
    6: 0,
    3: 1
}

# dict to go from (0-5) colors to RGB for display
color_dict = {
    0: (255, 255, 0),   # YELLOW
    1: (255, 0, 0),     # RED
    2: (0, 0, 255),     # BLUE
    3: (255, 102, 0),   # ORANGE
    4: (0, 255, 0),     # GREEN
    5: (255, 255, 255)  # WHITE
}

# COLORS THAT ARE COOL
LILAC = (160, 158, 214)
PURPLE = (111, 84, 149)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 102, 0)

# SCREEN BUSINESS
RESOLUTION = (1920, 1080)
CENTER_3D = np.array([RESOLUTION[0]/2, RESOLUTION[1]/2, 1000])

def rotation_x(alpha):
    return np.array([
    [1, 0, 0],
    [0, np.cos(alpha), -np.sin(alpha)],
    [0, np.sin(alpha), np.cos(alpha)]
])

def rotation_y(beta):
    return np.array([
    [np.cos(beta), 0, np.sin(beta)],
    [0, 1, 0],
    [-np.sin(beta), 0, np.cos(beta)]
])

def rotation_z(gamma): 
    return np.array([
    [np.cos(gamma), -np.sin(gamma), 0],
    [np.sin(gamma), np.cos(gamma), 0],
    [0, 0, 1]
])

FACES = [
    (0, 1, 2, 3),   # YELLOW
    (1, 5, 6, 2),   # RED
    (2, 6, 7, 3),   # BLUE
    (3, 7, 4, 0),   # ORANGE
    (0, 4, 5, 1),   # GREEN
    (4, 7, 6, 5)    # WHITE
    ]

class Rubiks:
    def __init__(self, center=np.array([0, 0, 0]), length=1, size=3, alpha=0, beta=0, gamma=0):

        # initialize piece array
        piece_count = 6 * size ** 2
        self.piece_arr = np.zeros(piece_count, dtype=int)
        for i in range(6):
            for j in range(9):
                idx = i*9 + j
                self.piece_arr[idx] = i

        default_vertices = np.array([
            [-1, 1, -1],    #0
            [1, 1, -1],     #1
            [1, -1, -1],    #2
            [-1, -1, -1],   #3
            [-1, 1, 1],     #4 
            [1, 1, 1],      #5
            [1, -1, 1],     #6
            [-1, -1, 1]     #7
        ])
        self.length = length
        self.center = center
        self.vertices = length * default_vertices / 2 + center
        self.set_alpha(alpha)
        self.set_beta(beta)
        self.set_gamma(gamma)        

    def get_2d_projection(self):
        projected_vertices = []
        for vertex in self.vertices:
            projected_vertex = vertex.copy()
            projected_vertex[:2] -= CENTER_3D[:2]
            projected_vertex = 1000 * projected_vertex / vertex[2]
            projected_vertex[:2] += CENTER_3D[:2]
            projected_vertices.append(projected_vertex)
        return projected_vertices

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.vertices -= CENTER_3D
        self.vertices = np.transpose(np.matmul(rotation_x(self.alpha), np.transpose(self.vertices)))
        self.vertices += CENTER_3D

    def set_beta(self, beta):
        self.beta = beta
        self.vertices -= CENTER_3D
        self.vertices = np.transpose(np.matmul(rotation_y(self.beta), np.transpose(self.vertices)))
        self.vertices += CENTER_3D

    def set_gamma(self, gamma):
        self.gamma = gamma
        self.vertices -= CENTER_3D
        self.vertices = np.transpose(np.matmul(rotation_z(self.gamma), np.transpose(self.vertices)))
        self.vertices += CENTER_3D

    def cw_face_rot(self, face_num):
        piece_dup = self.piece_arr.copy()
        for i in cw_rotations:
            start = face_num * 9 + i
            end = face_num * 9 + cw_rotations[i]
            piece_dup[end] = self.piece_arr[start]
        self.piece_arr = piece_dup

    def ccw_face_rot(self, face_num):
        piece_dup = self.piece_arr.copy()
        for i in cw_rotations:
            start = face_num * 9 + cw_rotations[i]
            end = face_num * 9 + i
            piece_dup[end] = self.piece_arr[start]
        self.piece_arr = piece_dup

    def make_move(self, move):
        move_dict, face = all_move_dict[move[0]]
        piece_dup = self.piece_arr.copy()

        if "'" in move:
            self.ccw_face_rot(face_num=face)
            for i in move_dict:
                piece_dup[i] = self.piece_arr[move_dict[i]]
        else:
            self.cw_face_rot(face_num=face)
            for i in move_dict:
                piece_dup[move_dict[i]] = self.piece_arr[i]

        self.piece_arr = piece_dup

    def reset(self):
        for i in range(6):
            for j in range(9):
                idx = i*9 + j
                self.piece_arr[idx] = i

    def print(self):
        print(self.piece_arr)

    def face_draw(self, starting_coord, color_arr, side_len, edges_on):
        for i in range(3):
            y_offset = i * side_len
            for j in range(3):
                color_idx = i * 3 + j
                color = color_dict[color_arr[color_idx]]
                x_offest = j * side_len
                coord_1 = (starting_coord[0] + x_offest, starting_coord[1] + y_offset)
                coord_2 = (coord_1[0] + side_len, coord_1[1])
                coord_3 = (coord_1[0] + side_len, coord_1[1] + side_len)
                coord_4 = (coord_1[0], coord_1[1] + side_len)
                pygame.draw.polygon(screen, color, (coord_1, coord_2, coord_3, coord_4))
                if edges_on:
                    pygame.draw.polygon(screen, BLACK, (coord_1, coord_2, coord_3, coord_4), 4)

    def draw_2d(self, edges_on, center):
        side_len = 50
        starting_x = center[0] - 4.5 * side_len
        starting_y = center[1] - 6 * side_len

        # SIDE 0
        color_arr = self.piece_arr[0:9]
        self.face_draw((starting_x, starting_y), color_arr, side_len, edges_on)

        # SIDE 1
        color_arr = self.piece_arr[9:18]
        starting_x += side_len * 3
        self.face_draw((starting_x, starting_y), color_arr, side_len, edges_on)

        # SIDE 2
        color_arr = self.piece_arr[18:27]
        starting_y += side_len * 3
        self.face_draw((starting_x, starting_y), color_arr, side_len, edges_on)

        # SIDE 3
        color_arr = self.piece_arr[27:36]
        starting_y += side_len * 3
        self.face_draw((starting_x, starting_y), color_arr, side_len, edges_on)

        # SIDE 4
        color_arr = self.piece_arr[36:45]
        starting_y += side_len * 3
        self.face_draw((starting_x, starting_y), color_arr, side_len, edges_on)

        # SIDE 5
        color_arr = self.piece_arr[45:54]
        starting_x += side_len * 3
        self.face_draw((starting_x, starting_y), color_arr, side_len, edges_on)        

    def draw_3d(self, edges_on=False):
        points = self.get_2d_projection()
        front_vertex_index = np.argmin(self.vertices[:, 2])

        faces_to_render = []
        for i, face in enumerate(FACES):
            if front_vertex_index in face:
                verts = []
                for j in face:
                    verts.append(self.vertices[j])
                verts = np.array(verts)
                idx = np.argmax(verts[:, 2])
                val = verts[idx][2]
                faces_to_render.append((i, val))


        sorted_faces_by_z = sorted(faces_to_render, key=lambda x: x[1], reverse=True)
        sorted_faces = [idx for idx, _ in sorted_faces_by_z]

        for i in sorted_faces:
            face = FACES[i]
            for j in range(2):
                for k in range(2):
                    pygame.draw.polygon(screen, color_dict[i], (points[face[0]][:2], points[face[1]][:2], points[face[2]][:2], points[face[3]][:2]))
                    if edges_on:
                        pygame.draw.polygon(screen, BLACK, (points[face[0]][:2], points[face[1]][:2], points[face[2]][:2], points[face[3]][:2]), 4)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("poopy cube 2.0")

    # auto rotate (ar) factors
    ar_alpha, ar_beta, ar_gamma = -0.01, -0.02, 0
    length = 200
    fps = 60
    cube_color = RED
    pause = False
    auto_rotate = False
    done = False
    edges_on = True
    background_color = LILAC
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(RESOLUTION)
    cube_center = CENTER_3D
    flat = True
    dragging = False
    start_pos = (0, 0)
    debug = False

    cube = Rubiks(length=length, center=cube_center, size=3)

    # main loop
    while not done:
        clock.tick(fps)
        screen.fill(background_color)

        if flat:
            cube.draw_2d(edges_on=edges_on, center=cube_center)
        else:
            cube.draw_3d(edges_on=edges_on)

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_SPACE:
                    if pause:
                        pause = False
                    else:
                        pause = True
                if event.key == pygame.K_l:
                    cube.make_move('L')
                if event.key == pygame.K_r:
                    cube.make_move('R')
                if event.key == pygame.K_f:
                    cube.make_move('F')
                if event.key == pygame.K_b:
                    cube.make_move('B')
                if event.key == pygame.K_u:
                    cube.make_move('U')
                if event.key == pygame.K_d:
                    cube.make_move('D')
                if event.key == pygame.K_p:
                    cube.reset()
                if event.key == pygame.K_2:
                    flat = True
                if event.key == pygame.K_3:
                    flat = False
                if event.key == pygame.K_a:
                    if auto_rotate:
                        auto_rotate = False
                    else:
                        auto_rotate = True
                if event.key == pygame.K_m:
                    if debug:
                        debug = False
                    else:
                        debug = True
        
        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_buttons[0]:
            if not dragging:
                dragging = True
                start_pos = pygame.mouse.get_pos()
            else:
                end_pos = pygame.mouse.get_pos()
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                # adjust cube angle based on mouse movement
                cube.set_alpha(dy/100)
                cube.set_beta(-dx/100)
               # update mouse position
                start_pos = end_pos
                if debug:
                    print(f'Mouse moved by: {dx}, {dy}')
        else:
            dragging = False

        # pause action on screen
        if auto_rotate:
            cube.set_alpha(ar_alpha)
            cube.set_beta(ar_beta)
            cube.set_gamma(ar_gamma)

        pygame.display.flip()
    pygame.quit()