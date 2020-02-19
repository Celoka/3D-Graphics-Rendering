import os, sys
import pygame
import builtins

from cam import Cam
from cube import Cube
from helper import pacman_points, rotate2d

# Initialize pygame object
pygame.init()

# Create a global varible for pygame object
builtins.pygame = pygame

# size of screen
w = 800
h = 600
fov = min(w,h)
cx, cy = w//2, h//2
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.set_caption('3D Graphics')
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

# grab pygame internal methods
pygame.event.get()
pygame.mouse.get_rel()
pygame.mouse.set_visible(0)
pygame.event.set_grab(1)

# Instantiate classes
cubes = [Cube((x,0,z)) for x,z in pacman_points]
cam = Cam((0,0,-5))

run = True

while run:
    face_list = []
    face_color = []
    depth = []
    dt = clock.tick()/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
              run = False  
        cam.events(event)

    screen.fill((0,0,0))

    for obj in cubes:
        vert_list = []
        screen_coords = []
        for x,y,z in obj.verts:
            x-=cam.pos[0]
            y-=cam.pos[1]
            z-=cam.pos[2]
            x,z = rotate2d((x,z), cam.rot[1])
            x,z = rotate2d((x,z), cam.rot[0])
            vert_list+=[(x,y,z)]

            f = fov/z
            x,y = x*f,y*f
            screen_coords +=[(cx+int(x), cy+int(y))]
        
        for f in range(len(obj.faces)):
            face = obj.faces[f]

            on_screen = False
            for i in face:
                x,y = screen_coords[i]
                if vert_list[i][2]>0 and x>0 and x<w and y>0 and y<h:
                    on_screen = True
                    break;
            if on_screen:
                coords = [screen_coords[i] for i in face]
                face_list += [coords]
                face_color += [obj.colors[f]]
                depth += [sum(sum(vert_list[j][i] for j in face)**2 for i in range(3))]
    
    order = sorted(range(len(face_list)), key=lambda i: depth[i], reverse=1)
    for i in order:
        try:
            pygame.draw.polygon(screen, face_color[i], face_list[i])
        except:
            pass



    pygame.display.flip()
    
    key = pygame.key.get_pressed()
    cam.update(dt,key)

pygame.quit()
