import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
#from serv1 import *
import threading
#import client1
import time
from Serv1 import *
from Client1 import *

serv=Serv1()
client=Client1()

th2= threading.Thread(target=serv.startServ)
th3= threading.Thread(target=client.runClient)    

def create_sphere_sky_ground(radius, slices, stacks):
    """
    Draw a sphere of the given radius centered at (0,0,0).
    The top hemisphere (y>0) is sky-blue,
    the bottom hemisphere (y<0) is brown (ground).
    """
    lat_step = math.pi / stacks
    lon_step = 2.0 * math.pi / slices

    for i in range(stacks):
        lat0 = -math.pi/2 + i * lat_step
        lat1 = lat0 + lat_step
        s0, c0 = math.sin(lat0), math.cos(lat0)
        s1, c1 = math.sin(lat1), math.cos(lat1)
        
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(slices + 1):
            lon = j * lon_step
            slon, clon = math.sin(lon), math.cos(lon)
            
            # Vertex at lat0
            x0 = radius * c0 * clon
            y0 = radius * s0
            z0 = radius * c0 * slon
            if y0 >= 0.0:
                glColor3f(0.55, 0.75, 1.0)  # sky
            else:
                glColor3f(0.5, 0.25, 0.0)   # ground
            glVertex3f(x0, y0, z0)
            
            # Vertex at lat1
            x1 = radius * c1 * clon
            y1 = radius * s1
            z1 = radius * c1 * slon
            if y1 >= 0.0:
                glColor3f(0.55, 0.75, 1.0)
            else:
                glColor3f(0.5, 0.25, 0.0)
            glVertex3f(x1, y1, z1)
        glEnd()

def draw_text_2d(x, y, text, font, color=(255,255,255,255)):
    surface = font.render(text, True, color)
    text_data = pygame.image.tostring(surface, "RGBA", True)
    w, h = surface.get_size()
    
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glBegin(GL_QUADS)
    glTexCoord2f(0,0); glVertex2f(x,   y)
    glTexCoord2f(1,0); glVertex2f(x+w, y)
    glTexCoord2f(1,1); glVertex2f(x+w, y+h)
    glTexCoord2f(0,1); glVertex2f(x,   y+h)
    glEnd()
    
    glDisable(GL_TEXTURE_2D)
    glDeleteTextures([tex_id])


def mainRun():
    pygame.init()
    
    display = (1000, 700)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Sphere Environment – Control Compensation Only")
    #serv1.start()


    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, display[0]/display[1], 0.1, 1000.0)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    glEnable(GL_DEPTH_TEST)
    
    # Orientation angles in degrees.
    pitch = 0.0  # Nose up/down
    yaw   = 0.0  # Turn left/right (heading)
    # We'll use a separate variable for roll that is updated with compensation.
    virtual_roll = 0.0  # This represents the pilot's intended roll.
    
    # Speeds
    pitch_speed = 1.5
    yaw_speed   = 1.5
    roll_speed  = 1.5

    pygame.font.init()
    font = pygame.font.SysFont("Arial", 20, bold=True)

    clock = pygame.time.Clock()
    running = True
    
    while running:
        dt = clock.tick(60) / 1000.0
        virtual_roll=int(serv.msg1["roll"])
        pitch=int(serv.msg1["pitch"])
        yaw=int(serv.msg1["yaw"])
        """for event in pygame.event.get():
            if event.type == QUIT:
                running = False"""
        """keys = serv.msg1###################################################################serv1.get_msg()####pygame.key.get_pressed()
        # Update pitch and yaw normally:
        if keys[K_UP]:
            pitch -= pitch_speed   # Up arrow: nose down
        if keys[K_DOWN]:
            pitch += pitch_speed   # Down arrow: nose up
        if keys[K_q]:
            yaw -= yaw_speed
        if keys[K_e]:
            yaw += yaw_speed"""

        # Update virtual_roll with compensation.
        # In normal flight (|pitch| ≤ 90), left arrow increases virtual_roll.
        # In inverted flight (|pitch| > 90), reverse the control.
        """if abs(pitch) <= 90:
            if keys[K_LEFT]:
                virtual_roll += roll_speed
            if keys[K_RIGHT]:
                virtual_roll -= roll_speed
        else:
            if keys[K_LEFT]:
                virtual_roll -= roll_speed
            if keys[K_RIGHT]:
                virtual_roll += roll_speed
        """
        # Use virtual_roll as the roll angle.
        roll = virtual_roll

        # Normalize angles to [-180, 180]
        pitch = (pitch + 180) % 360 - 180
        yaw   = (yaw   + 180) % 360 - 180
        roll  = (roll  + 180) % 360 - 180
        virtual_roll = roll  # keep virtual_roll in sync

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # The environment is rotated by the negative of the actual angles.
        glRotatef(-pitch, 1, 0, 0)
        glRotatef(-yaw,   0, 1, 0)
        glRotatef(-roll,  0, 0, 1)

        create_sphere_sky_ground(radius=50, slices=64, stacks=32)

        # Draw 2D HUD text
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, display[0], 0, display[1])
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Heading (yaw) in [0,360)
        heading_display = yaw % 360
        if heading_display < 0:
            heading_display += 360
        
        draw_text_2d(20, 20, f"Heading: {heading_display:.1f}°", font, (0,255,0,255))
        draw_text_2d(20, 50, f"Pitch: {pitch:.1f}°   Roll: {roll:.1f}°", font, (0,255,0,255))
        draw_text_2d(20, 80, "Arrow Keys => Pitch & Roll; Q/E => Yaw", font, (255,255,255,255))
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        pygame.display.flip()

    pygame.quit()


def main():
    th2.start()
    th3.start()
    th1= threading.Thread(target=mainRun)
    th1.start()
    #time.sleep(1)
    

         


    
if __name__ == "__main__":
    main()
