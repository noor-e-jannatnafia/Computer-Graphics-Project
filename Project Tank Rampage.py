from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

score=0
m_x=0
m_y=0
temp=0
dx=0
dy=0
arr=[] # points of the tank stored after converting to previous zone (after all the operations)
arr2=[] # points of the enemies/circles stored after converting to previous zone (after all the operations)
arr3=[] # points of the bullet stored after converting to previous zone (after all the operations)
d=0
bx=0 # x_coordinate of the bullet
by=0 # y_coordinate of the bullet
bullet=[]
bullet_dir=[]
incE=0
incNE=0
c_x1=0
c_x2=0
c_y1=0
c_y2=0
c_x=0
c_y=0
rad=0 # random radius of the enemy/circle
rx=0
ry=0
pause=False
limit=False
game_over=False
outside=False # bullet leaves the window
hit=False
draw_bullet=False
speed=0.01 # rate at which radius of enemies/circles increase
x_move=5 # length of bullet
rotate="left" # direction of the tank
tank=[[200,250],[300,250],[200,220],[300,220],[300,230],[300,240],[320,230],[320,240]] # coordinates of the tank
zone=0
# 4 enemies/circles at a time
radius=[3, 3, 3, 3] # radius of the enemies
center=[[50,400], [400,50], [50,50], [400,400]] # centre of the enemies

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
    glutPostRedisplay()

def line_algo(x_1, y_1, x_2, y_2): # of the tank
    
    global dx, dy, d, incE, incNE, c_x1, c_x2, c_y1, c_y2, zone, arr
    
    arr=[]
    dx = x_2-x_1
    dy = y_2-y_1
    if abs(dx)>abs(dy):
        if dx>0 and dy>0:
            # convert to zone 0
            c_x1=x_1
            c_y1=y_1
            c_x2=x_2
            c_y2=y_2
            zone=0
        elif dx<0 and dy>0:
            c_x1=-x_1
            c_y1=y_1
            c_x2=-x_2
            c_y2=y_2
            zone=3
        elif dx<0 and dy<0:
            c_x1=-x_1
            c_y1=-y_1
            c_x2=-x_2
            c_y2=-y_2
            zone=4
        elif dx>0 and dy<0:
            c_x1=x_1
            c_y1=-y_1
            c_x2=x_2
            c_y2=-y_2
            zone=7
        if dx>0 and dy==0: # horizontal line (left to right)
            c_x1=x_1
            c_y1=y_1
            c_x2=x_2
            c_y2=y_2
            zone=0
        elif dx<0 and dy==0: # hotrizontal line (right to left)
            c_x1=-x_1
            c_y1=y_1
            c_x2=-x_2
            c_y2=y_2
            zone=3
    else:
        if dx>0 and dy>0:
            c_x1=y_1
            c_y1=x_1
            c_x2=y_2
            c_y2=x_2
            zone=1
        elif dx<0 and dy>0:
            c_x1=y_1
            c_y1=-x_1
            c_x2=y_2
            c_y2=-x_2
            zone=2
        elif dx<0 and dy<0:
            c_x1=-y_1
            c_y1=-x_1
            c_x2=-y_2
            c_y2=-x_2
            zone=5
        elif dx>0 and dy<0:
            c_x1=-y_1
            c_y1=x_1
            c_x2=-y_2
            c_y2=x_2
            zone=6
        elif dx==0 and dy>0: # vertical line (down to up)
            c_x1=y_1
            c_y1=x_1
            c_x2=y_2
            c_y2=x_2
            zone=1
        elif dx==0 and dy<0: # vertical line (up to down)
            c_x1=-y_1
            c_y1=x_1
            c_x2=-y_2
            c_y2=x_2
            zone=6
     # midpoint line drawing algorithm         
    dy=c_y2-c_y1
    dx=c_x2-c_x1
    d=2*dy-dx
    incE=2*dy
    incNE=2*(dy - dx)
    
    while c_x1<c_x2:
        if d>0:
            d+=incNE
            c_x1+=1
            c_y1+=1
        else:
            d+=incE
            c_x1+=1 
            
        if zone==0:
            arr.append((c_x1,c_y1)) # convert to provious zone
        elif zone==1:
            arr.append((c_y1,c_x1))
        elif zone==2:
            arr.append((-c_y1,c_x1))
        elif zone==3:
            arr.append((-c_x1,c_y1))
        elif zone==4:
            arr.append((-c_x1,-c_y1))
        elif zone==5:
            arr.append((-c_y1,-c_x1))
        elif zone==6:
            arr.append((c_y1,-c_x1))
        elif zone==7:
            arr.append((c_x1,-c_y1))
    for x,y in arr:
        glPointSize(1) 
        glBegin(GL_POINTS)
        glVertex2f(x,y)
        glEnd()
        
def line_algo2(x_1,y_1,x_2,y_2): # of the bullet
    global dx,dy,d,incE,incNE,c_x1, c_x2, c_y1, c_y2,zone, arr3
    arr3=[]
    dy=y_2-y_1
    dx=x_2-x_1
    if abs(dx)>abs(dy):
        if dx>0 and dy>0:
            c_x1=x_1
            c_y1=y_1
            c_x2=x_2
            c_y2=y_2
            zone=0
        elif dx<0 and dy>0:
            c_x1=-x_1
            c_y1=y_1
            c_x2=-x_2
            c_y2=y_2
            zone=3
        elif dx<0 and dy<0:
            c_x1=-x_1
            c_y1=-y_1
            c_x2=-x_2
            c_y2=-y_2
            zone=4
        elif dx>0 and dy<0:
            c_x1=x_1
            c_y1=-y_1
            c_x2=x_2
            c_y2=-y_2
            zone=7
        if dx>0 and dy==0:
            c_x1=x_1
            c_y1=y_1
            c_x2=x_2
            c_y2=y_2
            zone=0
        elif dx<0 and dy==0:
            c_x1=-x_1
            c_y1=y_1
            c_x2=-x_2
            c_y2=y_2
            zone=3
    else:
        if dx>0 and dy>0:
            c_x1=y_1
            c_y1=x_1
            c_x2=y_2
            c_y2=x_2
            zone=1
        elif dx<0 and dy>0:
            c_x1=y_1
            c_y1=-x_1
            c_x2=y_2
            c_y2=-x_2
            zone=2
        elif dx<0 and dy<0:
            c_x1=-y_1
            c_y1=-x_1
            c_x2=-y_2
            c_y2=-x_2
            zone=5
        elif dx>0 and dy<0:
            c_x1=-y_1
            c_y1=x_1
            c_x2=-y_2
            c_y2=x_2
            zone=6
        elif dx==0 and dy>0:
            c_x1=y_1
            c_y1=x_1
            c_x2=y_2
            c_y2=x_2
            zone=1
        elif dx==0 and dy<0:
            c_x1=-y_1
            c_y1=x_1
            c_x2=-y_2
            c_y2=x_2
            zone=6
    dy=c_y2-c_y1
    dx=c_x2-c_x1
    d=2*dy-dx
    incE=2*dy
    incNE=2*dy-2*dx
    while c_x1<c_x2:
        if d>0:
            d+=incNE
            c_x1+=1
            c_y1+=1
        else:
            d+=incE
            c_x1+=1 
        if zone==0:
            arr3.append((c_x1,c_y1))
        elif zone==1:
            arr3.append((c_y1,c_x1))
        elif zone==2:
            arr3.append((-c_y1,c_x1))
        elif zone==3:
            arr3.append((-c_x1,c_y1))
        elif zone==4:
            arr3.append((-c_x1,-c_y1))
        elif zone==5:
            arr3.append((-c_y1,-c_x1))
        elif zone==6:
            arr3.append((c_y1,-c_x1))
        elif zone==7:
            arr3.append((c_x1,-c_y1))
    for x,y in arr3:

        glPointSize(5) 
        glBegin(GL_POINTS)
        glVertex2f(x,y)
        glEnd()
        
def tank_position():
    global tank
    # generates shape of the tank
    line_algo(tank[0][0],tank[0][1],tank[1][0],tank[1][1])
    line_algo(tank[2][0],tank[2][1],tank[3][0],tank[3][1])
    line_algo(tank[0][0],tank[0][1],tank[2][0],tank[2][1])
    line_algo(tank[1][0],tank[1][1],tank[3][0],tank[3][1])
    line_algo(tank[4][0],tank[4][1],tank[6][0],tank[6][1])
    line_algo(tank[5][0],tank[5][1],tank[7][0],tank[7][1])
    line_algo(tank[6][0],tank[6][1],tank[7][0],tank[7][1])

def draw(): # the enemies
    global d, c_y, c_x, limit, arr3, hit, pause, score, game_over, speed
    arr2=[]
    for i in range(len(radius)):
        # midpoint circle drawing algorithm
        d=1-c_y
        c_x=0
        c_y=radius[i]
        while c_x<c_y:
            if d<0:
                d+=(2*c_x)+3
                c_x+=1
            else:
                d+=(2*c_x)-(2*c_y)+5
                c_x+=1
                c_y-=1

            if c_x+center[i][0]>500 or c_y+center[i][1]>500 or c_y+center[i][1]<0 or c_x+center[i][0]<0: # zone 1
                limit=True
                game_over=True
            if c_x+center[i][0]>500 or -c_y+center[i][1]>500 or -c_y+center[i][1]<0 or c_x+center[i][0]<0: # zone 6
                limit=True
                game_over=True
            if -c_x+center[i][0]>500 or -c_y+center[i][1]>500 or -c_y+center[i][1]<0 or -c_x+center[i][0]<0: # zone 5
                limit=True
                game_over=True
            if -c_x+center[i][0]>500 or c_y+center[i][1]>500 or c_y+center[i][1]<0 or -c_x+center[i][0]<0: # zone 2
                limit=True
                game_over=True
            if c_y+center[i][0]>500 or c_x+center[i][1]>500 or c_x+center[i][1]<0 or c_y+center[i][0]<0: # zone 0
                limit=True
                game_over=True
            if -c_y+center[i][0]>500 or c_x+center[i][1]>500 or c_x+center[i][1]<0 or -c_y+center[i][0]<0: # zone 3
                limit=True
                game_over=True
            if -c_y+center[i][0]>500 or -c_x+center[i][1]>500 or -c_x+center[i][1]<0 or -c_y+center[i][0]<0: # zone 4
                limit=True
                game_over=True
            if c_y+center[i][0]>500 or -c_x+center[i][1]>500 or -c_x+center[i][1]<0 or c_y+center[i][0]<0: # zone 7
                limit=True
                game_over=True
  
            if radius[i]>40: # game over condition: max radius = 40
                limit=True
                game_over=True
    
            for j in range(len(arr2)): # list of coordinates of enemies/cicles
                for k in range(len(arr3)): # list of coordinates of bullet
                    if int(arr2[j][1]) == int(arr3[k][1]) and int(arr2[j][0]) == int(arr3[k][0]): # collision
                        hit=True
                        limit=True
                        score+=5
                        speed+=0.01
                        print("Score:",score)
                        break # breaks drawing the circle

            if limit==False:
                arr2.append((c_x+center[i][0],c_y+center[i][1])) # zone 1
                arr2.append((c_x+center[i][0],-c_y+center[i][1])) # zone 6
                arr2.append((-c_x+center[i][0],-c_y+center[i][1])) # zone 5
                arr2.append((-c_x+center[i][0],c_y+center[i][1]))  #zone 2
                arr2.append((c_y+center[i][0],c_x+center[i][1])) # zone 0
                arr2.append((-c_y+center[i][0],c_x+center[i][1])) # zone 3
                arr2.append((-c_y+center[i][0],-c_x+center[i][1])) # zone 4
                arr2.append((c_y+center[i][0],-c_x+center[i][1])) # zone 7

            else:
                radius.pop(i)
                center.pop(i)
                break # omits the enemy/circle
 
        if limit==False and game_over==False:
            for x,y in arr2:
                if radius[i]>=35:
                     # red enemies/circles
                    glColor3f(1, 0, 0)
                    glPointSize(1) 
                    glBegin(GL_POINTS)
                    glVertex2f(x,y)
                    glEnd()
                
                else:
                    # green enemies/circles
                    glColor3f(0, 1, 0)
                    glPointSize(1) 
                    glBegin(GL_POINTS)
                    glVertex2f(x,y)
                    glEnd()
            if pause==False and game_over==False:
                # increases difficulty level by increasing the rate of increase of enemies/circles
                radius[i]+=speed
        
        else:
            limit=False
            break
 
def bullet_shot():
    global bullet,bullet_dir,x_move, hit, temp, outside, pause, game_over
    if len(bullet)==0:
        pass
    elif game_over==False:
        for i in range(len(bullet)): # draws the bullet
            if bullet_dir[i]=="left":
                line_algo2(bullet[i][0],bullet[i][1],bullet[i][0]+x_move,bullet[i][1])
                if hit==True:
                    temp=i
                if bullet[i][0]>500:
                    outside=True
                    temp=i
                if pause==False:
                    bullet[i][0]+=x_move

            if bullet_dir[i]=="right":
                line_algo2(bullet[i][0],bullet[i][1],bullet[i][0]-x_move,bullet[i][1])
                if hit==True:
                    temp=i
                if bullet[i][0]<0:
                    outside=True
                    temp=i
                if pause==False:
                    bullet[i][0]-=x_move
        if hit==True:
            bullet.pop(temp)
            bullet_dir.pop(temp)
            hit=False
        if outside==True:
            bullet.pop(temp)
            bullet_dir.pop(temp)
            outside=False

def circle_generate(): # generate enemy/circle
    global rad, rx, ry
    if len(radius)<4: # add another enemy/circle
        rad=random.randint(3, 9)
        radius.append(rad)
        rx=random.randint(100, 400)
        ry=random.randint(100, 400)
        center.append([rx, ry])
        draw()

def art_icons():
    global pause
    # restart button
    glColor3f(1, 0, 0)        
    line_algo(20,460,80,460)
    line_algo(20,460,55,490)
    line_algo(20,460,55,430)

    if pause==True:
        # triangle button
        glColor3f(0, 1, 0)
        line_algo(230,490,230,430) 
        line_algo(230,430,280,460)
        line_algo(230,490,280,460)
    else:
        # equal button
        glColor3f(0, 1, 0)
        line_algo(240,490,240,430) 
        line_algo(270,490,270,430)
    #cross button
    glColor3f(1, 1, 0)
    line_algo(445,490,495,430) 
    line_algo(495,490,445,430)
    glColor3f(1, 1, 1) # color of the tank
    
def mouseListener(button, state, x, y):	
    global m_x, m_y, pause, game_over, score, center, radius, speed, bullet, bullet_dir, tank, rotate
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        m_x=x
        m_y=500-y
        if m_x>=445 and m_x<=495 and m_y>=430 and m_y<=490: # cross button
            print("Goodbye")
            glutLeaveMainLoop()

        if pause==False and m_x>=240 and m_x<=270 and m_y>=430 and m_y<=490: # pause button
            pause=True
        elif pause==True and m_x>=230 and m_x<=280 and m_y>=430 and m_y<=490: # unpause button
            pause=False
            
        if m_x>=20 and m_x<=80 and m_y>=460 and m_y<=490: # restart button
            game_over=False
            pause=False
            score=0
            speed=0.01
            radius=[3,3,3,3]
            center=[[50,400], [400,50], [50,50], [400,400]]
            tank=[[200,250],[300,250],[200,220],[300,220],[300,230],[300,240],[320,230],[320,240]]
            bullet=[]
            bullet_dir=[]
            rotate="left"
            print("Starting Over!")

def specialKeyListener(key, x, y):
    
    global game_over, tank, pause

    if pause==False and game_over==False:
        if key==GLUT_KEY_RIGHT:
            if tank[7][0]<=500 and tank[0][0]<=500: # condition to keep tank inside window on right side
                for i in range(8): # move every x-coordinate to right
                    tank[i][0]+=2
        if key==GLUT_KEY_LEFT:
            if tank[0][0]>=0 and tank[7][0]>=0: # condition to keep tank inside window on left side
                for i in range(8): # move every x-coordinate to left
                    tank[i][0]-=2
        if key==GLUT_KEY_UP:
            if tank[0][1]<=500: # condition to keep tank inside window on top side
                for i in range(8): # move every y-coordinate to up
                    tank[i][1]+=2
        if key==GLUT_KEY_DOWN:
            if tank[3][1]>=0: # condition to keep tank inside window on bottom side
                for i in range(8): # move every y-coordinate to down
                    tank[i][1]-=2
    glutPostRedisplay()

def keyboardListener(key, x, y):

    global tank, rotate, bx, by, bullet, bullet_dir, pause, game_over
    
    if pause==False and game_over==False:
        if key==b' ' and rotate=="left":
            bx=tank[1][0]
            by=(tank[1][1]+tank[3][1])/2
            bullet.append([bx,by])
            bullet_dir.append("left")
        if key==b' ' and rotate=="right":
            bx=tank[1][0] # = tank[3][0]
            by=(tank[1][1]+tank[3][1])/2
            bullet.append([bx,by])
            bullet_dir.append("right")
        if key==b's':
            if rotate=="left":
                tank[0],tank[1]=tank[1],tank[0]
                tank[2],tank[3]=tank[3],tank[2]
                tank[4][0]-=100
                tank[5][0]-=100
                tank[6][0]-=140
                tank[7][0]-=140
                rotate="right"
            elif rotate=="right": 
                tank[0],tank[1]=tank[1],tank[0]
                tank[2],tank[3]=tank[3],tank[2]
                tank[4][0]+=100
                tank[5][0]+=100
                tank[6][0]+=140
                tank[7][0]+=140
                rotate="left"

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0)
    glLoadIdentity()
    iterate()
    art_icons()
    tank_position()
    circle_generate()
    draw()
    bullet_shot()
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500) 
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Tank Rampage") 
glutDisplayFunc(showScreen)
glutSpecialFunc(specialKeyListener)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()