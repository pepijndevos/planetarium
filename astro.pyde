import math
from nomy import planets, planet_position

jd = 2448392.79167
speed = 0
center = 3
xview = 0
yview = 0
zoom = 15

symbols = {
           "Sun": u"\u2609",
           "Moon": u"\u263D",
           "Mercury": u"\u263F",
           "Venus": u"\u2640",
           "Earth": u"\u2641",
           "Mars": u"\u2642",
           "Jupiter": u"\u2643",
           "Saturn": u"\u2644",
           "Uranus": u"\u2645",
           "Neptune": u"\u2646",
           "Pluto": u"\u2647",
}

def setup():
    global sun, bgimg
    size(800, 800, P3D)
    #shapeMode(CENTER)
    freesans = createFont("FreeSans", 32);
    textFont(freesans);
    
    bgimg = loadImage("Signs.png")

def draw():
    global jd
    background(255)
    with pushMatrix():
        translate(width/2, height/2)
        rotateX(xview)
        rotateZ(yview)
        fill(0)
        ellipse(100, 100, 0, 0)
    
        #pointLight(255, 230, 200, 0, 0, 0);
        #ambientLight(50,50,50);
        points = [(symbols['Sun'], width/2, height/2)]
        for p in planets:
            eqx, eqy, eqz = planet_position(p, jd)
                            
            x = screenX(eqx*zoom, eqy*zoom, eqz*zoom)
            y = screenY(eqx*zoom, eqy*zoom, eqz*zoom)
            points.append((symbols[p.name], x, y))

    with pushMatrix():
        #translate(width/2, height/2)
        #translate(-points[center][1], -points[center][2])
        for p in points:
            text(p[0], p[1], p[2])
            
    with pushMatrix():
        sphereDetail(30)
        translate(width/2, height/2, -400)
        backdrop = createShape(SPHERE, 2000)
        backdrop.setTexture(bgimg)
        rotateX(xview+(math.pi/2))
        rotateY(yview)

        #noStroke()
        shape(backdrop)
        #sphere(200)
    
    fill(0);
    jd += speed

def mouseDragged(event):
    global xview, yview
    yview -= (pmouseX - mouseX) / 100.
    xview -= (pmouseY - mouseY) / 100.

def mouseWheel(event):
    global zoom
    zoom += event.count
    
def keyPressed(event):
    global center, speed
    if keyCode == LEFT:
        center -= 1
    if keyCode == RIGHT:
        center += 1
    if keyCode == UP:
        speed *= 2
    if keyCode == DOWN:
        speed /= 2
    if key == " ":
        speed = int(not bool(speed))
        
