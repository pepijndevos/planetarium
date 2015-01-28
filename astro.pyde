import math
from nomy import planets, planet_position, planet_ellipse

jd = 2448392.79167
speed = 0
center = 2
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
    size(800, 800, P3D)
    freesans = createFont("FreeSans", 32);
    textFont(freesans);
    

def draw():
    global jd
    background(255)
    with pushMatrix():
        translate(width/2, height/2)
        rotateX(xview)
        rotateZ(yview)
        ox, oy, oz = planet_position(planets[center], jd)
        x = screenX(ox*zoom, -oy*zoom, -oz*zoom)
        y = screenY(ox*zoom, -oy*zoom, -oz*zoom)
        points = [(symbols['Sun'], x, y)]
        for p in planets:
            with pushMatrix():
                eqx, eqy, eqz = planet_position(p, jd)
                h, w, c = planet_ellipse(p, jd)
    
                #noFill()
                #stroke(0)
                #ellipse(c*zoom, 0, h*zoom, w*zoom)
    
                x = screenX(-(eqx-ox)*zoom, (eqy-oy)*zoom, (eqz-oz)*zoom)
                y = screenY(-(eqx-ox)*zoom, (eqy-oy)*zoom, (eqz-oz)*zoom)
                points.append((symbols[p.name], x, y))
            
    with pushMatrix():
        translate(width/2, height/2)
        rotateX(xview)
        rotateZ(yview)    
        noFill()
        stroke(0)
        rotateY(math.pi/2)
        rotateX(math.radians(23.4))
        for i in range(6):
            ellipse(0, 0, 2000, 2000)
            rotateX(math.pi/6)
    
    with pushMatrix():
        textAlign(CENTER, CENTER)
        fill(0)
        for p in points:
            text(p[0], p[1], p[2])

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
        
