#Alright let's make shapes
import pygame, sys
from pygame.locals import *
from random import randrange
import time
from math import ceil,sin,cos,tan,atan,asin,pi,acos
#Constants
FPS=30
Width=600
Height=600
#colors
RED=[255 , 0, 0]
Blue=[0 ,0 , 255]
GREEN=[0,255,0]
YELLOW=[255,255,0]
WHITE=[230,230,230]
ORANGE=[255,170,200]
BLACK=[0,0,0]

class point:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
    def uppos(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
    def move(self,dx,dy,dz):
        self.x+=dx
        self.y+=dy
        self.z+=dz
class rotate:
    def __init__(self,rx,ry,rz):
        self.rx=rx
        self.ry=ry
        self.rz=rz
        self.store=[0,0,0]
        self.axis=[[1,0,0],[0,1,0],[0,0,1]]
    def update(self,rx,ry,rz):
        self.rx=rx
        self.ry=ry
        self.rz=rz
    def rotate(self,rx,ry,rz):
        self.rx+=rx
        self.ry+=ry
        self.rz+=rz
    def get_ra(self,a):
        ret=[]
        c_a=a
        #get the necxt two axis
        for i in range(2):
            c_a+=1
            if c_a>2:
                c_a-=3
            #print(c_a)
            ret.append(c_a)
        
        return ret
    def add_sq(self,List):
        #find the hypothesus
        A=0
        for l in List:
            A+=l**2
        A=(A**0.5)
        return A
  
    def get_axis(self):
        axis=self.axis.copy()
        #rotate X
        axis=self.about_a(0,axis,self.rx)
        #rotate Y
        axis=self.about_a(1,axis,self.ry)
        #rotate Z
        axis=self.about_a(2,axis,self.rz)
        return axis
        
    def cal_coords(self,vec,List):
        ans=0
        nos=0
        for l in List:
            ans+=l*vec[nos]
            nos+=1
        return ans
            
        
                
        
    
        
        
            
        

class camera:
    def __init__(self,rot):
        self.pos=point(Width/2,Height/2,0)
        self.rot=rot
        self.Look=False
        self.surfaces=[]
        self.depths=[]
        self.colors=[RED,YELLOW]
    def uppos(self,x,y,z):
        pos.uppos(self,x,y,z)
    def move(self,dx,dy,dz):
        self.pos.move(dx,dy,dz)
    def rotate(self,rx,ry,rz):
        self.rot.rotate(rx,ry,rz)


    def rot_X(self,List):
        x=List[0]
        y=List[1]
        z=List[2]
        #rotate about x
        nx=x
        ny=(y*cos(self.rot.rx))+(z*sin(self.rot.rx))
        nz=(z*cos(self.rot.rx))-(y*sin(self.rot.rx))
        return [nx,ny,nz].copy()
        
    def rot_Y(self,List):
        x=List[0]
        y=List[1]
        z=List[2]
        #rotate about x
        nx=(x*cos(self.rot.ry))+(z*sin(self.rot.ry))
        ny=y
        nz=(z*cos(self.rot.ry))-(x*sin(self.rot.ry))
        return [nx,ny,nz].copy()
        
    def rot_Z(self,List):
        x=List[0]
        y=List[1]
        z=List[2]
        #rotate about x
        nx=(x*cos(self.rot.rz))+(y*sin(-self.rot.rz))
        ny=(y*cos(self.rot.rz))-(x*sin(-self.rot.rz))
        nz=z
        return [nx,ny,nz].copy()
    def LookAt(self,p):
        X=p[0]-self.pos.x
        Y=p[1]-self.pos.y
        Z=p[2]-self.pos.z
        #set rotation angle
        if abs(Z)<0.001:
            if Z>0:
                Z=0.001
            else:
                Z=-0.001
            
        
        rx=-atan(Y/Z)
        ry=-atan(X/Z)
        
        if Z<0:
            rx=(pi)-atan(Y/-Z)
            ry=(pi)-atan(X/-Z)
        self.rot.update(rx,ry,0)
        self.Look=True
    def transform(self,List):
        NL=List.copy()
        #rotate x first
        NL=self.rot_X(NL)
        #rotate y
        NL=self.rot_Y(NL)
        #rotate z
        NL=self.rot_Z(NL)
        return NL.copy()
    def interpolate(self,P1,P2):
        inter=False
        draw=True
        normal=True
        start=0
        stop=0
        indraw=[]
        if P1[2]<0 and P2[2]>0:
            start=P1
            stop=P2
            inter=True
        if P1[2]>0 and P2[2]<0:
            start=P2
            stop=P1
            inter=True
            normal=False
        if P1[2]<0 and P2[2]<0:
            draw=False
        #interpolate point for new depth
        if inter:
            length=start[2]-stop[2]
            tl=abs(stop[2])
            ratio=tl/length
            #do for x first
            nX=(ratio*(start[0]-stop[0]))+stop[0]
            nY=(ratio*(start[1]-stop[1]))+stop[1]
            #append
            indraw.append(nX)
            indraw.append(nY)
            indraw.append(0)
        p1=P1.copy()
        p2=P2.copy()
        if normal and inter:
            p1=indraw.copy()
            p2=stop.copy()
        elif inter:
            p2=indraw.copy()
            p1=stop.copy()
        if draw==False:
            p1=False
            p2=False
            nos=0
        return p1,p2
    def getcoords(self,List):
        x=(List[0]-self.pos.x)
        y=(List[1]-self.pos.y)
        z=(List[2]-self.pos.z)
   
        #rotate coordinate about the angle
        CL=[x,y,z]
        #print("CL before ", CL)
       
        CL=self.transform(CL)
        
        #print("CL after ", CL)
        r_a=pi/5
        #get coordinate
        X=CL[0]
        Y=CL[1]
        Z=CL[2]

        
        
        if abs(Z)<0.000001:
            Z=0.000001
        
        #add in a perspective view
        di=tan(r_a)
        if di==0:
            di=0.0000000001
        scale=Z/(di)
        #print(X)
        if abs(scale)<0.001:
            scale=0.001

        ax=((X/scale)*(Width/2))+Width/2
        ay=((Y/scale)*(Height/2))+Height/2
        
        
        #you can see things at your back
        #Todo: try not to draw objects behind you
        #print([ax,ay])
        #return [(X+Width/2),(Y+Height/2)]
        return ([ax,ay,Z])
    
    def drawL(self,p1,p2):
        #drawing a line based on the actual scale
        #get coords
        d1=self.getcoords(p1)
        d2=self.getcoords(p2)
        #interpolate
        P1,P2=self.interpolate(d1,d2)

        #now draw it
        if P1!=False:
            P1.remove(P1[2])
            P2.remove(P2[2])
            pygame.draw.lines(WIN,BLACK,True,[P1,P2],2)
    def add(self,s,c=YELLOW):
        self.surfaces.append(s)
        self.colors.append(c)
    def bodyadd(self,B,c=RED):
        for b in B:
            self.add(b)
    def clear(self):
        self.surfaces=[]
        self.depth=[]
        self.colors=[]
        
    def arrange(self):
        Sur=self.surfaces.copy()
        sur=[]
        dep=[]
        for a in Sur:
            b,c=self.convS(a)
            if b!=False:
                sur.append(b)
                dep.append(c)
        ans=[]
        ansdep=[]
        dnos=0
        for s in sur:
            true=0
            nos=0
            while(true==0):
                if nos<len(ans):
                    if dep[dnos]>=ansdep[nos]:
                        ans.insert((nos),s)
                        ansdep.insert(nos,dep[dnos])
                        true=1
                else:
                    ans.append(s)
                    ansdep.append(dep[dnos])
                    true=1
                nos+=1
            dnos+=1
        return ans      
    def convS(self,S):
        y=0
        ynos=0
        ret=[]
        d=True
        for s in S:
            a=self.getcoords(s)
            y+=a[2]
            ynos+=1
            ret.append(a)
            if a[2]<0:
                d=False
        Zave=y/ynos #get the average depth of the surface
        if d:
            return ret,Zave
        else:
            return False,Zave
        
    def sdraw(self,s,c=YELLOW):
        if s!=False:
            #remove z
            for lit in s:
                if len(s)>=2:
                    lit.remove(lit[2])
            #Fill up shape and draw line
            pygame.draw.polygon(WIN,c,s)
            pygame.draw.lines(WIN,BLACK,True,s,2)
    def draw(self):
        sur=self.arrange()
        nos=0
        for s in sur:
            if len(s)>2:
                if nos<len(self.colors):
                    self.sdraw(s.copy(),self.colors[nos])
                else:
                    self.sdraw(s.copy())
            nos+=1
                
cam=camera(rotate(0,0,0))
#cam.move(0,0,150)
#cam.LookAt([100,100,20])
cam.add([[100,100,20],[200,100,20],[200,200,30],[100,200,30]])
cam.add([[100,100,100],[200,100,100],[200,200,100],[100,200,100]])
#cam.add([[150,150,50],[50,150,50],[80,100,50]])
cam.add([[100,100,50],[200,100,50],[200,200,50],[100,200,50]])
entities=[]
class body:
    def __init__(self,pos,sur):
        self.rot=[0,0,0]
        self.pos=pos
        self.surfaces=sur
        self.color=None
    def rot_X(self,List):
        x=List[0]
        y=List[1]
        z=List[2]
        #rotate about x
        nx=x
        ny=(y*cos(self.rot[0]))+(z*sin(self.rot[0]))
        nz=(z*cos(self.rot[0]))-(y*sin(self.rot[0]))
        return [nx,ny,nz].copy()
        
    def rot_Y(self,List):
        x=List[0]
        y=List[1]
        z=List[2]
        #rotate about x
        nx=(x*cos(self.rot[1]))+(z*sin(self.rot[1]))
        ny=y
        nz=(z*cos(self.rot[1]))-(x*sin(self.rot[1]))
        return [nx,ny,nz].copy()
        
    def rot_Z(self,List):
        x=List[0]
        y=List[1]
        z=List[2]
        #rotate about x
        nx=(x*cos(self.rot[2]))+(y*sin(-self.rot[2]))
        ny=(y*cos(self.rot[2]))-(x*sin(-self.rot[2]))
        nz=z
        return [nx,ny,nz].copy()
    def position(self,sur):
        ans=[]
        for s in sur:
            l=[]
            for p in s:
                l.append([(p[0]+self.pos[0]),(p[1]+self.pos[1]),(p[2]+self.pos[2])])
            ans.append(l)
        return ans.copy()
    def transform(self,List):
        ans=[]
        for l in List:
            NL=l.copy()
            aL=[]
            for p in NL:
                p=self.rot_X(p)
                p=self.rot_Y(p)
                p=self.rot_Z(p)
                aL.append(p)
            ans.append(aL)
        return ans
    def drawget(self):
        na=self.transform(self.surfaces)
        a=self.position(na)
        return a
class cube:
    def __init__(self,pos,size):
        self.pos=pos
        self.size=size
        self.body=[]
        self.initialize()
    def initialize(self):
        sur=[]
        size=self.size
        p1=[-size/2,-size/2,-size/4]
        p2=[size/2,-size/2,-size/4]
        p3=[size/2,size/2,-size/4]
        p4=[-size/2,size/2,-size/4]
        p5=[-size/2,-size/2,size/4]
        p6=[size/2,-size/2,size/4]
        p7=[size/2,size/2,size/4]
        p8=[-size/2,size/2,size/4]
        sur.append([p1,p2,p3,p4])
        sur.append([p1,p2,p6,p5])
        sur.append([p1,p4,p8,p5])
        sur.append([p4,p3,p7,p8])
        sur.append([p2,p3,p7,p6])
        sur.append([p5,p6,p7,p8])
        self.body=body(self.pos,sur)
    def rotate(self,a):
        self.body.rot[0]+=a[0]
        self.body.rot[1]+=a[1]
        self.body.rot[2]+=a[2]
    def move(self,m):
        self.body.pos[0]+=m[0]
        self.body.pos[1]+=m[1]
        self.body.pos[2]+=m[2]
    def drawget(self):
        return self.body.drawget()

entity=[]
entity.append(cube([0,0,500],50))
entity.append(cube([500,0,600],100))
    
def main():
    global WIN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    WIN = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption('3d Rendering')
    fpsClock = pygame.time.Clock()
    pygame.key.set_repeat(50,50)
    while True:
        #clear everything
        WIN.fill(WHITE)
        cam.clear()
        cam.rotate(0,0,0)
        speed=8
        for event in pygame.event.get():            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN:
                keys=pygame.key.get_pressed()
                if keys[K_RIGHT]:
                    cam.move(speed,0,0)
                elif keys[K_LEFT]:
                    cam.move(-speed,0,0)
                if keys[K_UP]:
                    cam.move(0,0,speed)
                elif keys[K_DOWN]:
                    cam.move(0,0,-speed)
                if keys[K_w]:
                    cam.move(0,-speed,0)
                elif keys[K_s]:
                    cam.move(0,speed,0)
                if keys[K_z]:
                    cam.rotate(0,0.05,0)
                if keys[K_x]:
                    cam.rotate(0,-0.05,0)
                if keys[K_SPACE]:
                    no=1
        e=entity
        m1=[-(e[1].pos[0]-e[0].pos[0])/505,-(e[1].pos[1]-e[0].pos[1])/505,-(e[1].pos[2]-e[0].pos[2])/505]
        m2=[(e[0].pos[0]-e[1].pos[0])/505,(e[0].pos[1]-e[1].pos[1])/505,(e[0].pos[2]-e[1].pos[2])/505]
        e[0].move(m1)
        e[1].move(m2)
        #add surfaces
        for e in entity:
            e.rotate([0,0,0.25])
            cam.bodyadd(e.drawget())
        cam.draw()
        pygame.display.update()
        fpsClock.tick(FPS)   

main()                

